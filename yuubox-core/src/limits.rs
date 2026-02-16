#[derive(Debug, Clone)]
pub struct ResourceLimits {
    pub memory_bytes: u64,
    pub cpu_quota: f64,
    pub timeout_seconds: u64,
}

impl Default for ResourceLimits {
    fn default() -> Self {
        Self {
            memory_bytes: 256 * 1024 * 1024,
            cpu_quota: 1.0,
            timeout_seconds: 60,
        }
    }
}
