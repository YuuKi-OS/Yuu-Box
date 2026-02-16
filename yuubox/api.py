from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from yuubox import YuuBox, ResourceLimits

app = FastAPI(title="YuuBox API", version="1.0.0")

class ExecuteRequest(BaseModel):
    code: str
    language: str
    max_iterations: Optional[int] = 5
    timeout: Optional[int] = 60
    memory_mb: Optional[int] = 256
    no_healing: Optional[bool] = False

@app.post("/execute")
async def execute(request: ExecuteRequest):
    """Execute code with self-healing"""
    box = YuuBox(max_iterations=request.max_iterations)
    
    result = box.execute(
        code=request.code,
        language=request.language,
        limits=ResourceLimits(
            memory_mb=request.memory_mb,
            timeout_seconds=request.timeout,
        ),
        no_healing=request.no_healing,
    )
    
    return {
        "success": result.success,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "iterations": result.iterations,
        "execution_time": result.execution_time,
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
