import re
from typing import Dict, Any, Optional

class ErrorAnalyzer:
    """Analyzes execution errors"""
    
    def analyze(self, stderr: str, language: str, code: str) -> Dict[str, Any]:
        if language == "python":
            return self._analyze_python(stderr)
        elif language in ["javascript", "js", "node"]:
            return self._analyze_javascript(stderr)
        elif language == "rust":
            return self._analyze_rust(stderr)
        else:
            return self._generic_analysis(stderr)
    
    def _analyze_python(self, stderr: str) -> Dict[str, Any]:
        lines = stderr.split("\n")
        for i, line in enumerate(lines):
            if "Traceback" in line:
                last_line = lines[-1] if lines[-1].strip() else lines[-2]
                match = re.match(r"(\w+Error): (.+)", last_line)
                if match:
                    line_match = re.search(r'line (\d+)', stderr)
                    return {
                        "type": match.group(1),
                        "message": match.group(2),
                        "line": int(line_match.group(1)) if line_match else None,
                        "stack_trace": stderr,
                    }
        return self._generic_analysis(stderr)
    
    def _analyze_javascript(self, stderr: str) -> Dict[str, Any]:
        match = re.search(r"(\w+Error): (.+)", stderr)
        if match:
            return {
                "type": match.group(1),
                "message": match.group(2),
                "stack_trace": stderr,
            }
        return self._generic_analysis(stderr)
    
    def _analyze_rust(self, stderr: str) -> Dict[str, Any]:
        if "error[E" in stderr:
            match = re.search(r"error\[E\d+\]: (.+)", stderr)
            if match:
                return {
                    "type": "CompilerError",
                    "message": match.group(1),
                    "stack_trace": stderr,
                }
        return self._generic_analysis(stderr)
    
    def _generic_analysis(self, stderr: str) -> Dict[str, Any]:
        return {
            "type": "ExecutionError",
            "message": stderr[:300].strip(),
            "stack_trace": stderr,
        }
