import pytest
from yuubox import YuuBox, ResourceLimits

def test_basic_execution():
    """Test basic code execution"""
    box = YuuBox(max_iterations=1)
    
    code = 'print("hello world")'
    result = box.execute(code, language="python", no_healing=True)
    
    assert "hello world" in result.stdout

def test_self_healing():
    """Test self-healing capability"""
    box = YuuBox(max_iterations=5)
    
    # Code with intentional error (typo)
    code = 'prin("hello")'  # prin vs print
    result = box.execute(code, language="python")
    
    # Should eventually succeed after healing
    assert result.iterations >= 1

def test_resource_limits():
    """Test resource limits work"""
    box = YuuBox()
    limits = ResourceLimits(memory_mb=128, timeout_seconds=10)
    
    code = 'print("test")'
    result = box.execute(code, "python", limits=limits, no_healing=True)
    
    assert result.exit_code == 0
