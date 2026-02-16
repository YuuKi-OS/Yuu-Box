from typing import Optional, List, Dict, Any
import requests

class YuukiHealer:
    """Heals code using Yuuki AI"""
    
    DEFAULT_API = "https://opceanai-yuuki-api.hf.space"
    
    def __init__(self, api_url: Optional[str] = None):
        self.api_url = (api_url or self.DEFAULT_API).rstrip("/")
        self.session = requests.Session()
    
    def fix(
        self,
        code: str,
        error: Dict[str, Any],
        language: str,
        error_history: List,
    ) -> str:
        prompt = self._build_prompt(code, error, language, error_history)
        
        try:
            response = self.session.post(
                f"{self.api_url}/generate",
                json={
                    "prompt": prompt,
                    "max_new_tokens": 1000,
                    "temperature": 0.3,
                    "model": "yuuki-best",
                },
                timeout=30,
            )
            
            if not response.ok:
                return code
            
            data = response.json()
            fixed = self._extract_code(data)
            return fixed if fixed else code
            
        except Exception:
            return code
    
    def _build_prompt(self, code: str, error: Dict, language: str, history: List) -> str:
        parts = [
            f"Fix this {language} code that has an error.",
            "",
            "Code:",
            f"```{language}",
            code,
            "```",
            "",
            f"Error: {error['type']}",
            f"Message: {error['message']}",
        ]
        
        if len(history) > 1:
            parts.append(f"\nPrevious {len(history)-1} attempts failed.")
        
        parts.extend([
            "",
            "Provide ONLY the corrected code without explanations.",
        ])
        
        return "\n".join(parts)
    
    def _extract_code(self, data) -> str:
        if isinstance(data, str):
            code = data
        elif isinstance(data, dict):
            code = data.get("generated_text") or data.get("response") or ""
        else:
            return ""
        
        code = code.strip()
        if code.startswith("```"):
            lines = code.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)
        
        for cutoff in ["User:", "System:", "\nUser", "\nSystem"]:
            if cutoff in code:
                idx = code.index(cutoff)
                if idx > 0:
                    code = code[:idx].strip()
                    break
        
        return code.strip()
