class YuuBoxError(Exception):
    """Base exception"""
    pass

class ExecutionError(YuuBoxError):
    """Execution failed"""
    pass

class DockerError(YuuBoxError):
    """Docker error"""
    pass

class HealingError(YuuBoxError):
    """Healing failed"""
    pass
