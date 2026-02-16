use bollard::Docker;
use bollard::container::{Config, CreateContainerOptions, RemoveContainerOptions, StartContainerOptions, WaitContainerOptions};
use bollard::models::{HostConfig, RestartPolicy, RestartPolicyNameEnum};
use bollard::exec::{CreateExecOptions, StartExecResults};
use anyhow::{Result, anyhow};
use std::collections::HashMap;
use tokio::time::{timeout, Duration};
use futures_util::stream::StreamExt;

use crate::limits::ResourceLimits;

pub struct ContainerResult {
    pub stdout: String,
    pub stderr: String,
    pub exit_code: i64,
    pub memory_used: u64,
    pub cpu_time: f64,
}

pub struct ContainerManager {
    docker: Docker,
}

impl ContainerManager {
    pub async fn new() -> Result<Self> {
        let docker = Docker::connect_with_socket_defaults()
            .map_err(|e| anyhow!("Failed to connect to Docker: {}", e))?;
        
        Ok(Self { docker })
    }

    pub async fn execute(
        &self,
        code: &str,
        language: &str,
        limits: &ResourceLimits,
    ) -> Result<ContainerResult> {
        let image = self.get_image(language)?;
        let command = self.build_command(code, language)?;

        let host_config = Some(HostConfig {
            memory: Some(limits.memory_bytes as i64),
            nano_cpus: Some((limits.cpu_quota * 1_000_000_000.0) as i64),
            network_mode: Some("none".to_string()),
            read_only_root_fs: Some(true),
            tmpfs: Some({
                let mut map = HashMap::new();
                map.insert("/tmp".to_string(), "size=100m".to_string());
                map
            }),
            cap_drop: Some(vec!["ALL".to_string()]),
            restart_policy: Some(RestartPolicy {
                name: Some(RestartPolicyNameEnum::NO),
                ..Default::default()
            }),
            ..Default::default()
        });

        let config = Config {
            image: Some(image.clone()),
            cmd: Some(command),
            working_dir: Some("/workspace".to_string()),
            user: Some("1000:1000".to_string()),
            host_config,
            attach_stdout: Some(true),
            attach_stderr: Some(true),
            tty: Some(false),
            ..Default::default()
        };

        let container_name = format!("yuubox-{}", uuid::Uuid::new_v4());
        
        let container = self.docker
            .create_container(
                Some(CreateContainerOptions {
                    name: &container_name,
                    ..Default::default()
                }),
                config,
            )
            .await?;

        let container_id = container.id.clone();

        let exec_result = timeout(
            Duration::from_secs(limits.timeout_seconds),
            self.run_container(&container_id)
        ).await;

        let result = match exec_result {
            Ok(Ok(res)) => res,
            Ok(Err(e)) => {
                self.cleanup_container(&container_id).await?;
                return Err(e);
            }
            Err(_) => {
                self.docker.kill_container::<String>(&container_id, None).await.ok();
                self.cleanup_container(&container_id).await?;
                return Err(anyhow!("Execution timeout after {} seconds", limits.timeout_seconds));
            }
        };

        self.cleanup_container(&container_id).await?;

        Ok(result)
    }

    async fn run_container(&self, container_id: &str) -> Result<ContainerResult> {
        self.docker.start_container::<String>(container_id, None).await?;

        let mut wait_stream = self.docker.wait_container(
            container_id,
            Some(WaitContainerOptions {
                condition: "not-running",
            })
        );

        let mut exit_code = 0i64;
        while let Some(wait_result) = wait_stream.next().await {
            if let Ok(status) = wait_result {
                exit_code = status.status_code;
            }
        }

        let logs = self.docker.logs::<String>(
            container_id,
            Some(bollard::container::LogsOptions {
                stdout: true,
                stderr: true,
                ..Default::default()
            })
        );

        let mut stdout = String::new();
        let mut stderr = String::new();

        let log_output = logs.collect::<Vec<_>>().await;
        for log in log_output {
            if let Ok(log_line) = log {
                match log_line {
                    bollard::container::LogOutput::StdOut { message } => {
                        stdout.push_str(&String::from_utf8_lossy(&message));
                    }
                    bollard::container::LogOutput::StdErr { message } => {
                        stderr.push_str(&String::from_utf8_lossy(&message));
                    }
                    _ => {}
                }
            }
        }

        Ok(ContainerResult {
            stdout,
            stderr,
            exit_code,
            memory_used: 0,
            cpu_time: 0.0,
        })
    }

    async fn cleanup_container(&self, container_id: &str) -> Result<()> {
        self.docker.remove_container(
            container_id,
            Some(RemoveContainerOptions {
                force: true,
                ..Default::default()
            })
        ).await?;
        
        Ok(())
    }

    pub async fn cleanup(&self) -> Result<()> {
        Ok(())
    }

    fn get_image(&self, language: &str) -> Result<String> {
        let image = match language.to_lowercase().as_str() {
            "python" => "python:3.11-slim",
            "javascript" | "js" | "node" => "node:20-slim",
            "rust" => "rust:1.75-slim",
            "go" => "golang:1.21-alpine",
            "java" => "openjdk:17-slim",
            _ => return Err(anyhow!("Unsupported language: {}", language)),
        };
        
        Ok(image.to_string())
    }

    fn build_command(&self, code: &str, language: &str) -> Result<Vec<String>> {
        let command = match language.to_lowercase().as_str() {
            "python" => vec![
                "python".to_string(),
                "-c".to_string(),
                code.to_string(),
            ],
            "javascript" | "js" | "node" => vec![
                "node".to_string(),
                "-e".to_string(),
                code.to_string(),
            ],
            "rust" => vec![
                "sh".to_string(),
                "-c".to_string(),
                format!("echo '{}' > /tmp/main.rs && rustc /tmp/main.rs -o /tmp/main && /tmp/main", code),
            ],
            "go" => vec![
                "sh".to_string(),
                "-c".to_string(),
                format!("echo '{}' > /tmp/main.go && go run /tmp/main.go", code),
            ],
            "java" => vec![
                "sh".to_string(),
                "-c".to_string(),
                format!("echo '{}' > /tmp/Main.java && javac /tmp/Main.java && java -cp /tmp Main", code),
            ],
            _ => return Err(anyhow!("Unsupported language: {}", language)),
        };
        
        Ok(command)
    }
}
