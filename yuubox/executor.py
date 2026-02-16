import time
from dataclasses import dataclass, field
from typing import List, Optional

try:
    from yuubox.yuubox_core import ContainerExecutor as RustExecutor
except ImportError:
    RustExecutor = None

from yuubox.analyzer import ErrorAnalyzer
from yuubox.healer import YuukiHealer
from yuubox.exceptions import ExecutionError

@dataclass
class ResourceLimits:
    memory_mb: int = 256
    cpu_quota: float = 1.0
    timeout_seconds: int = 60

@dataclass
class ErrorReport:
    error_type: str
    error_message: str
    iteration: int
    line_number: Optional[int] = None

@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    iterations: int
    execution_time: float
    final_code: str
    error_history: List[ErrorReport] = field(default_factory=list)

class YuuBox:
    """Self-healing code executor (Rust + Python hybrid)"""
    
    def __init__(self, max_iterations: int = 5, yuuki_api_url: Optional[str] = None):
        if RustExecutor is None:
            raise ImportError("Rust core not compiled. Run: maturin develop")
        
        self.max_iterations = max_iterations
        self.rust_executor = RustExecutor()
        self.analyzer = ErrorAnalyzer()
        self.healer = YuukiHealer(yuuki_api_url)
    
    def execute(
        self,
        code: str,
        language: str,
        limits: Optional[ResourceLimits] = None,
        no_healing: bool = False,
    ) -> ExecutionResult:
        limits = limits or ResourceLimits()
        current_code = code
        error_history = []
        start_time = time.time()
        
        for iteration in range(1, self.max_iterations + 1):
            # Execute in Rust (FAST!)
            result = self.rust_executor.execute(
                current_code,
                language,
                limits.memory_mb,
                limits.cpu_quota,
                limits.timeout_seconds,
            )
            
            if result.exit_code == 0:
                return ExecutionResult(
                    success=True,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    exit_code=0,
                    iterations=iteration,
                    execution_time=time.time() - start_time,
                    final_code=current_code,
                    error_history=error_history,
                )
            
            if no_healing:
                return ExecutionResult(
                    success=False,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    exit_code=result.exit_code,
                    iterations=1,
                    execution_time=time.time() - start_time,
                    final_code=current_code,
                    error_history=error_history,
                )
            
            # Analyze error (Python)
            error = self.analyzer.analyze(result.stderr, language, current_code)
            error_report = ErrorReport(
                error_type=error["type"],
                error_message=error["message"],
                iteration=iteration,
                line_number=error.get("line"),
            )
            error_history.append(error_report)
            
            # Heal with Yuuki (Python)
            try:
                fixed_code = self.healer.fix(current_code, error, language, error_history)
                if not fixed_code or fixed_code == current_code:
                    break
                current_code = fixed_code
            except Exception as e:
                break
        
        return ExecutionResult(
            success=False,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            iterations=iteration,
            execution_time=time.time() - start_time,
            final_code=current_code,
            error_history=error_history,
        )
    
    def cleanup(self):
        """Cleanup resources"""
        self.rust_executor.cleanup()
