from yuubox import YuuBox, ResourceLimits

box = YuuBox(max_iterations=5)

limits = ResourceLimits(
    memory_mb=512,
    cpu_quota=1.0,
    timeout_seconds=30,
)

code = "print('Hello from YuuBox!')"
result = box.execute(code, "python", limits=limits)

print(f"Success: {result.success}")
print(f"Output: {result.stdout}")
