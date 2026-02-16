from yuubox import YuuBox

box = YuuBox()

code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Typo: fibonaci vs fibonacci
print(fibonaci(10))
"""

result = box.execute(code, language="python")

print(f"Success: {result.success}")
print(f"Iterations: {result.iterations}")
print(f"Output: {result.stdout}")
