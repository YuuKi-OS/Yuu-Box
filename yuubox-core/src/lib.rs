use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use tokio::runtime::Runtime;
use std::time::Instant;

mod container;
mod limits;
mod monitor;

use container::ContainerManager;
use limits::ResourceLimits;

#[pyclass]
#[derive(Clone)]
pub struct ExecutionResult {
    #[pyo3(get)]
    pub stdout: String,
    #[pyo3(get)]
    pub stderr: String,
    #[pyo3(get)]
    pub exit_code: i64,
    #[pyo3(get)]
    pub execution_time: f64,
    #[pyo3(get)]
    pub memory_used: u64,
    #[pyo3(get)]
    pub cpu_time: f64,
}

#[pyclass]
pub struct ContainerExecutor {
    runtime: Runtime,
    manager: ContainerManager,
}

#[pymethods]
impl ContainerExecutor {
    #[new]
    pub fn new() -> PyResult<Self> {
        let runtime = Runtime::new()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to create runtime: {}", e)))?;
        
        let manager = runtime.block_on(async {
            ContainerManager::new().await
        }).map_err(|e| PyRuntimeError::new_err(format!("Failed to create manager: {}", e)))?;

        Ok(Self { runtime, manager })
    }

    pub fn execute(
        &self,
        code: String,
        language: String,
        memory_mb: Option<u64>,
        cpu_quota: Option<f64>,
        timeout_seconds: Option<u64>,
    ) -> PyResult<ExecutionResult> {
        let limits = ResourceLimits {
            memory_bytes: memory_mb.unwrap_or(256) * 1024 * 1024,
            cpu_quota: cpu_quota.unwrap_or(1.0),
            timeout_seconds: timeout_seconds.unwrap_or(60),
        };

        let start = Instant::now();
        
        let result = self.runtime.block_on(async {
            self.manager.execute(&code, &language, &limits).await
        }).map_err(|e| PyRuntimeError::new_err(format!("Execution failed: {}", e)))?;

        let execution_time = start.elapsed().as_secs_f64();

        Ok(ExecutionResult {
            stdout: result.stdout,
            stderr: result.stderr,
            exit_code: result.exit_code,
            execution_time,
            memory_used: result.memory_used,
            cpu_time: result.cpu_time,
        })
    }

    pub fn cleanup(&self) -> PyResult<()> {
        self.runtime.block_on(async {
            self.manager.cleanup().await
        }).map_err(|e| PyRuntimeError::new_err(format!("Cleanup failed: {}", e)))?;
        
        Ok(())
    }
}

#[pymodule]
fn yuubox_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ContainerExecutor>()?;
    m.add_class::<ExecutionResult>()?;
    Ok(())
}
