<div align="center">

<br>

<img src="https://img.shields.io/badge/%E2%9C%A6-YUUBOX-000000?style=for-the-badge&labelColor=000000" alt="YuuBox" height="50">

<br><br>

# Self-Healing Code Execution System

**Rust core with Python orchestration. AI-powered automatic debugging.**<br>
**Docker isolation. Resource limits. Sequential execution with maximum safety.**

<br>

<a href="#features"><img src="https://img.shields.io/badge/FEATURES-000000?style=for-the-badge" alt="Features"></a>
&nbsp;&nbsp;
<a href="#quick-start"><img src="https://img.shields.io/badge/QUICK_START-000000?style=for-the-badge" alt="Quick Start"></a>
&nbsp;&nbsp;
<a href="https://docs.yuuki.dev/yuubox"><img src="https://img.shields.io/badge/DOCUMENTATION-000000?style=for-the-badge" alt="Documentation"></a>

<br><br>

[![License](https://img.shields.io/badge/Apache_2.0-222222?style=flat-square&logo=apache&logoColor=white)](LICENSE)
&nbsp;
[![Python](https://img.shields.io/badge/Python_3.9+-222222?style=flat-square&logo=python&logoColor=white)](https://python.org)
&nbsp;
[![Rust](https://img.shields.io/badge/Rust_1.75+-222222?style=flat-square&logo=rust&logoColor=white)](https://rust-lang.org)
&nbsp;
[![Docker](https://img.shields.io/badge/Docker_20.10+-222222?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
&nbsp;
[![PyPI](https://img.shields.io/badge/PyPI-222222?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/yuubox)
&nbsp;
[![FastAPI](https://img.shields.io/badge/FastAPI-222222?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

<br>

---

<br>

<table>
<tr>
<td width="50%" valign="top">

**Hybrid Rust + Python architecture.**<br><br>
Rust core for container execution.<br>
Python layer for AI orchestration.<br>
PyO3 bindings with zero overhead.<br>
Docker isolation per execution.<br>
Yuuki AI integration for healing.<br>
Sequential execution (1 container).<br>
Resource limits enforcement.<br>
Complete error analysis.

</td>
<td width="50%" valign="top">

**Production-ready from day one.**<br><br>
Memory-safe Rust implementation.<br>
Full type safety in both languages.<br>
Comprehensive error handling.<br>
CLI with beautiful Rich output.<br>
FastAPI server for HTTP access.<br>
<br>
Built for reliability and safety.

</td>
</tr>
</table>

<br>

</div>

---

<br>

<div align="center">

## What is YuuBox?

</div>

<br>

**YuuBox** is a self-healing code execution system that combines the performance of Rust with the flexibility of Python to create a production-ready platform for executing untrusted code safely. The system takes code as input, executes it in an isolated Docker container, and if errors occur, automatically fixes them using Yuuki AI until the code runs successfully or reaches the maximum iteration limit of five attempts.

The architecture is deliberately hybrid. The performance-critical components—container management, resource enforcement, stream handling, and Docker orchestration—are implemented in Rust for maximum speed and memory safety. The high-level orchestration, error analysis, and AI integration are handled in Python for rapid development and easy integration with external services. The two layers communicate through PyO3 bindings, which provide zero-cost interoperability between Rust and Python.

YuuBox operates with a sequential execution model, creating and destroying one Docker container per execution. This design prioritizes security and isolation over raw throughput. Each execution gets a completely clean environment with no state contamination from previous runs. The container is configured with strict resource limits on CPU usage, memory allocation, disk space, network access, and execution time. Once the execution completes—whether successfully or with errors—the container is immediately destroyed and all resources are freed.

The self-healing mechanism integrates with the Yuuki AI code generation platform hosted on HuggingFace Spaces. When code fails to execute, YuuBox captures the complete error output, analyzes it with language-specific parsers to extract structured information like error types and line numbers, then constructs an intelligent prompt for Yuuki that includes the failing code, the error details, and the history of previous fix attempts. Yuuki generates corrected code, which YuuBox extracts and executes in a fresh container. This loop continues for up to five iterations, with each attempt learning from previous failures.

Built with modern tooling across both languages. The Rust core uses tokio for async runtime, bollard for Docker API interaction, and PyO3 for Python bindings. The Python layer uses Click for CLI, Rich for terminal UI, FastAPI for HTTP API, and requests for Yuuki integration. The entire system is packaged with maturin, which handles the complex build process of creating Python wheels from Rust code.

<br>

---

<br>

<div align="center">

## Features

</div>

<br>

<table>
<tr>
<td width="50%" valign="top">

<h3>Rust Core Engine</h3>

The execution engine is implemented entirely in Rust using the bollard Docker client library and tokio async runtime. Each execution creates a fresh Docker container with a specified base image for the target programming language. The container is configured with a HostConfig that enforces memory limits through cgroups, CPU quotas through nano_cpus, and network isolation by setting network mode to none. The filesystem is mounted as read-only except for a size-limited tmpfs at /tmp. All Linux capabilities are dropped for the container process. The Rust code spawns the container, attaches to its output streams, waits for completion with a configurable timeout, captures all stdout and stderr output, retrieves the exit code, and finally removes the container. All of this happens asynchronously using tokio, allowing for proper timeout handling and cancellation. The Rust core exposes a simple synchronous interface to Python through PyO3, hiding all the async complexity behind a blocking facade.

<br>

<h3>Python Orchestration</h3>

The Python layer implements the high-level self-healing loop. The main YuuBox class accepts code and language parameters, then enters an iteration loop that can run up to five times. In each iteration, it calls the Rust executor through PyO3, receives back the execution result with exit code and output streams, and checks for success. On failure, it invokes the ErrorAnalyzer to parse the stderr output and extract structured error information. The analyzer has language-specific parsers for Python tracebacks, JavaScript error stacks, and Rust compiler messages. The structured error is then passed to the YuukiHealer, which constructs a context-aware prompt that includes the current code, the error details, and a summary of previous attempts. The healer calls the Yuuki API, parses the response to extract corrected code, and returns it to the main loop. The loop updates the current code and begins the next iteration. This continues until either the code succeeds, five iterations complete, or the healer fails to generate a fix.

<br>

<h3>Language Support</h3>

YuuBox supports five major programming languages with dedicated Docker images and execution strategies. Python code executes using the python:3.11-slim image with the command python -c followed by the code string. JavaScript runs on node:20-slim using node -e. Rust compilation and execution happens in rust:1.75-slim using a shell script that writes the code to a temporary file, invokes rustc to compile it, then runs the resulting binary. Go uses golang:1.21-alpine with a similar pattern of writing to a temp file and running with go run. Java support uses openjdk:17-slim with javac compilation followed by java execution. Each language has a corresponding error parser in the analyzer that understands that language's error message format and can extract meaningful structured information from stack traces and compiler output.

<br>

<h3>Resource Limits</h3>

Every container execution is subject to strict resource limits configured through Docker's HostConfig. Memory limits are specified in bytes and enforced by Linux cgroups, with a default of 256MB. CPU quotas are specified as a fraction of one core converted to nano_cpus for Docker, with a default allowing full use of one core. Execution timeouts are enforced using tokio's timeout future wrapper, with a default of 60 seconds. On timeout, the Rust code sends a kill signal to the container and proceeds with cleanup. Disk space is limited by mounting the root filesystem as read-only and providing only a size-limited tmpfs at /tmp with a default of 100MB. Network access is controlled by the network mode setting, defaulting to disabled which prevents all network communication. These limits can be customized per execution through the ResourceLimits dataclass passed from Python.

</td>
<td width="50%" valign="top">

<h3>Error Analysis</h3>

The ErrorAnalyzer class provides sophisticated parsing of execution errors across multiple programming languages. For Python, it searches stderr for the Traceback marker, extracts all lines from there to the end, parses the final line to separate error type from message using a regex pattern, and searches the traceback for line number references. For JavaScript, it looks for patterns like SyntaxError: or TypeError: and extracts the error class and message. For Rust, it detects compiler error patterns like error[E0308]: and extracts the compiler's message. All analyzers produce a standardized error dictionary containing type, message, optional line number, and the full stack trace. This structured representation allows the healer to construct precise prompts that guide Yuuki toward relevant fixes.

<br>

<h3>Yuuki Integration</h3>

Integration with the Yuuki AI platform happens through the YuukiHealer class, which manages HTTP communication with the HuggingFace Spaces API endpoint. The healer constructs prompts by combining the failing code wrapped in markdown code fences, the error type and message, optional line number information, and a summary of how many previous attempts have been made. The prompt explicitly instructs Yuuki to provide only the corrected code without explanations, which simplifies parsing. The healer makes a POST request to the generate endpoint with parameters including the prompt, a max token count of 1000, a low temperature of 0.3 for more deterministic debugging output, and the yuuki-best model identifier. Response parsing handles multiple formats that the API might return, extracting text from string responses or dictionary fields like generated_text or response. The healer strips markdown code fences and cleans conversational artifacts like "User:" or "System:" markers that sometimes appear in responses.

<br>

<h3>CLI Interface</h3>

The command-line interface is built with Click for command parsing and Rich for beautiful terminal output. The main command yuubox run accepts a file path and automatically detects the programming language from the file extension. Optional flags control the maximum iteration count, disable healing for single-shot execution, set timeout and memory limits, and explicitly specify the language. When execution begins, Rich displays a spinner with status text. Progress updates show which iteration is running. On success, a green checkmark appears with the iteration count and any stdout output. On failure after all iterations, a red X shows with the final error message truncated to 500 characters. The entire experience is designed to feel responsive and informative without overwhelming the user with technical details about Docker or Rust internals.

<br>

<h3>HTTP API</h3>

The FastAPI server provides HTTP access to YuuBox functionality for integration with web applications and automated systems. The main endpoint accepts POST requests at /execute with a JSON body containing code, language, and optional parameters for max iterations, timeout, memory limit, and healing control. The server creates a YuuBox instance, calls its execute method with the provided parameters, and returns a JSON response with success status, stdout and stderr output, the number of iterations used, and total execution time. A health check endpoint at /health returns a simple status message for monitoring and load balancer health checks. The API is fully documented with automatic OpenAPI schema generation from FastAPI, accessible at the /docs endpoint when the server is running.

<br>

<h3>Security Model</h3>

Security is enforced through multiple layers of isolation. Docker containers provide process-level isolation with separate PID namespaces preventing container processes from seeing or interacting with host processes. The network is disabled by default, eliminating data exfiltration and external command-and-control risks. The filesystem is read-only except for a size-limited temporary directory, preventing persistence of malicious code or data. Containers run as a non-root user with UID 1000, removing privilege escalation vectors. All Linux capabilities are explicitly dropped, disabling operations like loading kernel modules or modifying system time. Resource limits prevent resource exhaustion attacks like fork bombs or memory allocation attacks. Execution timeouts prevent infinite loops or deliberate hanging. After each execution, the container is unconditionally removed, ensuring no state persists between runs. The Rust implementation provides additional safety through compile-time memory safety checks and absence of data races.

</td>
</tr>
</table>

<br>

---

<br>

<div align="center">

## Architecture

</div>

<br>

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         YuuBox System                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Python Layer                           │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │ │
│  │  │  YuuBox     │  │ ErrorAnalyzer│  │ YuukiHealer   │  │ │
│  │  │  Executor   │  │              │  │               │  │ │
│  │  │             │  │ - Python     │  │ - Prompt      │  │ │
│  │  │ - Main loop │  │ - JavaScript │  │ - API call    │  │ │
│  │  │ - Iteration │  │ - Rust       │  │ - Parse       │  │ │
│  │  │ - Result    │  │ - Generic    │  │ - Extract     │  │ │
│  │  └──────┬──────┘  └──────────────┘  └────────────────┘  │ │
│  │         │                                                │ │
│  │         │ PyO3 Bindings (zero-cost)                      │ │
│  │         ▼                                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                     Rust Core                             │ │
│  │                                                           │ │
│  │  ┌──────────────────────────────────────────────────┐    │ │
│  │  │          ContainerExecutor                       │    │ │
│  │  │                                                  │    │ │
│  │  │  - Create container with limits                 │    │ │
│  │  │  - Start execution                               │    │ │
│  │  │  - Capture stdout/stderr streams                │    │ │
│  │  │  - Wait with timeout                             │    │ │
│  │  │  - Collect exit code                             │    │ │
│  │  │  - Remove container                              │    │ │
│  │  └──────────────────┬───────────────────────────────┘    │ │
│  │                     │                                     │ │
│  │                     │ bollard (Docker API client)         │ │
│  │                     │ tokio (async runtime)               │ │
│  │                     ▼                                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│                         ▼                                       │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   Docker Engine                           │ │
│  │                                                           │ │
│  │  - Container creation and lifecycle                      │ │
│  │  - Resource limits enforcement (cgroups)                 │ │
│  │  - Network isolation                                     │ │
│  │  - Filesystem mounting and permissions                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTPS
                                ▼
                   ┌────────────────────────┐
                   │    Yuuki AI API        │
                   │  (HuggingFace Spaces)  │
                   │                        │
                   │  - Code generation     │
                   │  - Error fixing        │
                   └────────────────────────┘
```

<br>

### Execution Flow

```
User submits code
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│  Iteration 1                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Python → Rust: execute(code, "python", limits)     │
│                                                         │
│  2. Rust creates Docker container                      │
│     - Image: python:3.11-slim                          │
│     - Memory: 256MB limit                              │
│     - CPU: 1.0 quota (100% of one core)               │
│     - Timeout: 60 seconds                              │
│     - Network: disabled                                │
│     - Filesystem: read-only + /tmp (100MB)            │
│     - User: 1000:1000 (non-root)                      │
│     - Capabilities: ALL dropped                        │
│                                                         │
│  3. Rust executes command: python -c "<code>"          │
│                                                         │
│  4. Rust captures streams asynchronously               │
│     - stdout → buffer                                  │
│     - stderr → buffer                                  │
│                                                         │
│  5. Container completes (or times out)                 │
│     - Exit code: 1 (error)                            │
│     - stdout: ""                                       │
│     - stderr: "Traceback...\nNameError: 'x'..."       │
│                                                         │
│  6. Rust removes container                             │
│                                                         │
│  7. Rust → Python: ExecutionResult                     │
│                                                         │
│  8. Python checks exit_code                            │
│     - Not 0, so execution failed                       │
│                                                         │
│  9. Python calls ErrorAnalyzer                         │
│     - Detects "NameError"                             │
│     - Extracts message                                │
│     - Identifies line 3                                │
│                                                         │
│ 10. Python calls YuukiHealer                           │
│     - Builds prompt with code + error                  │
│     - POST to Yuuki API                                │
│     - Receives fixed code                              │
│                                                         │
│ 11. Python updates current_code                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│  Iteration 2                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1-7. Same process with fixed code                     │
│                                                         │
│  8. Python checks exit_code                            │
│     - Exit code: 0 (success!)                         │
│                                                         │
│  9. Return ExecutionResult                             │
│     - success: true                                    │
│     - iterations: 2                                    │
│     - stdout: "Result: 42"                            │
│     - final_code: <fixed version>                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

<br>

### Component Interactions

```
CLI/API Request
      │
      ├── CLI (yuubox run script.py)
      │   └── Click + Rich UI
      │
      └── HTTP API (POST /execute)
          └── FastAPI server
                │
                ▼
          ┌─────────────────┐
          │   YuuBox        │
          │   Executor      │
          │                 │
          │  for i in 1..5: │
          │    ├─ execute   │
          │    ├─ analyze   │
          │    └─ heal      │
          └────┬────────────┘
               │
               ├─────────────────────┬──────────────────────┐
               │                     │                      │
               ▼                     ▼                      ▼
    ┌──────────────────┐  ┌─────────────────┐  ┌──────────────────┐
    │ ContainerExecutor│  │ ErrorAnalyzer   │  │ YuukiHealer      │
    │ (Rust)           │  │ (Python)        │  │ (Python)         │
    │                  │  │                 │  │                  │
    │ - Docker ops     │  │ - Parse stderr  │  │ - Build prompt   │
    │ - Async runtime  │  │ - Extract info  │  │ - HTTP request   │
    │ - Stream capture │  │ - Classify type │  │ - Parse response │
    └────┬─────────────┘  └─────────────────┘  └────┬─────────────┘
         │                                            │
         ▼                                            ▼
    Docker Engine                          Yuuki API (HF Spaces)
```

<br>

---

<br>

<div align="center">

## Installation

</div>

<br>

### Prerequisites

YuuBox requires three main dependencies before installation. First, Docker version 20.10 or later provides the container runtime. Installation instructions available at docs.docker.com/get-docker. Second, Python 3.9 or later runs the orchestration layer, downloadable from python.org. Third, Rust 1.75 or later builds the core engine, installable via rustup from rust-lang.org.

<br>

### Quick Installation

```bash
git clone https://github.com/yuuki-os/yuubox
cd yuubox/yuubox-hybrid
chmod +x install.sh
./install.sh
```

The installation script checks for Rust, installs maturin, compiles the Rust core with PyO3 bindings, builds a Python wheel, and installs it. After completion, the yuubox command is available in your shell.

<br>

### Manual Installation

```bash
# Verify Rust
cargo --version

# Install maturin
pip install maturin

# Development build
cd yuubox-hybrid
maturin develop

# Or production build
maturin build --release
pip install target/wheels/yuubox-*.whl

# Install extras
pip install -e ".[api]"  # For HTTP API
pip install -e ".[dev]"  # For development
```

<br>

### Docker Setup

On Linux, add your user to the docker group to avoid requiring sudo:

```bash
sudo usermod -aG docker $USER
# Log out and back in

# Verify
docker ps
```

On macOS and Windows, Docker Desktop handles permissions automatically. YuuBox will automatically pull necessary base images (python:3.11-slim, node:20-slim, etc.) on first use.

<br>

### Verification

```bash
# Check CLI installation
yuubox --version

# Test execution
echo 'print(undefined_variable)' > test.py
yuubox run test.py

# Test Python API
python -c "from yuubox import YuuBox; box = YuuBox(); print(box.execute('print(\"test\")', 'python').success)"
```

<br>

---

<br>

<div align="center">

## Quick Start

</div>

<br>

### Basic Python Usage

```python
from yuubox import YuuBox

# Create instance
box = YuuBox(max_iterations=5)

# Code with error (typo: prin vs print)
code = """
def greet(name):
    prin(f"Hello, {name}!")

greet("World")
"""

# Execute with self-healing
result = box.execute(code, language="python")

if result.success:
    print(f"✓ Success after {result.iterations} iterations")
    print(f"Output: {result.stdout}")
    print(f"Fixed code:\n{result.final_code}")
else:
    print(f"✗ Failed after {result.iterations} iterations")
    print(f"Error: {result.stderr}")
```

Output shows YuuBox detected the NameError, called Yuuki to fix the typo, and successfully executed the corrected code on iteration 2.

<br>

### CLI Usage

```bash
# Execute Python file
yuubox run script.py

# Custom settings
yuubox run buggy.py --max-iterations 3 --timeout 30 --memory 512

# Explicit language
yuubox run code.txt --language python

# No healing
yuubox run test.py --no-healing

# Other languages
yuubox run app.js
yuubox run main.rs
```

<br>

### HTTP API Server

```bash
# Start server
uvicorn yuubox.api:app --host 0.0.0.0 --port 8000

# Or with auto-reload
uvicorn yuubox.api:app --reload --port 8000
```

Make requests:

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(hello_world)",
    "language": "python",
    "max_iterations": 5,
    "timeout": 60,
    "memory_mb": 256
  }'

# Response
{
  "success": true,
  "stdout": "Hello, World!\n",
  "stderr": "",
  "iterations": 2,
  "execution_time": 3.24
}
```

Visit http://localhost:8000/docs for interactive API documentation.

<br>

### Resource Limits

```python
from yuubox import YuuBox, ResourceLimits

box = YuuBox()

# Custom limits
limits = ResourceLimits(
    memory_mb=128,
    cpu_quota=0.5,
    timeout_seconds=30,
)

code = "print('Limited execution')"
result = box.execute(code, "python", limits=limits)
```

<br>

### Disabling Self-Healing

```python
result = box.execute(
    code="print(undefined)",
    language="python",
    no_healing=True
)
# No Yuuki calls, iterations=1
```

<br>

---

<br>

<div align="center">

## Advanced Usage

</div>

<br>

### Multiple Languages

**Python:**

```python
from yuubox import YuuBox

box = YuuBox()

python_code = """
import math

def calculate_area(radius):
    return math.pi * radius ** 2

# Error: wrong function name
print(f"Area: {circle_area(5)}")
"""

result = box.execute(python_code, "python")
print(f"Iterations: {result.iterations}")  # 2
print(f"Output: {result.stdout}")
```

<br>

**JavaScript:**

```python
javascript_code = """
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Syntax error: missing )
console.log(fibonacci(10);
"""

result = box.execute(javascript_code, "javascript")
# Detects SyntaxError, fixes missing parenthesis
```

<br>

**Rust:**

```python
rust_code = """
fn main() {
    let numbers = vec![1, 2, 3, 4, 5];
    
    // Type error: sum needs mut
    let sum = 0;
    for num in numbers {
        sum += num;
    }
    
    println!("Sum: {}", sum);
}
"""

result = box.execute(rust_code, "rust")
# Detects mutability error, adds mut keyword
```

<br>

**Go:**

```python
go_code = """
package main

import "fmt"

func main() {
    // Error: Printf needs format string
    fmt.Printf("Number:", 42)
}
"""

result = box.execute(go_code, "go")
```

<br>

**Java:**

```python
java_code = """
public class Main {
    public static void main(String[] args) {
        // Error: wrong method name
        system.out.println("Hello");
    }
}
"""

result = box.execute(java_code, "java")
```

<br>

### Error Analysis Deep Dive

```python
from yuubox.analyzer import ErrorAnalyzer

analyzer = ErrorAnalyzer()

python_stderr = """
Traceback (most recent call last):
  File "<string>", line 7, in <module>
  File "<string>", line 4, in calculate
ZeroDivisionError: division by zero
"""

error_info = analyzer.analyze(python_stderr, "python", "")

print(f"Type: {error_info['type']}")
print(f"Message: {error_info['message']}")
print(f"Line: {error_info.get('line')}")
print(f"Stack: {error_info['stack_trace']}")
```

<br>

### Custom Healing

```python
from yuubox import YuuBox
from yuubox.healer import YuukiHealer

class CustomHealer(YuukiHealer):
    def _build_prompt(self, code, error, language, history):
        prompt = f"Expert {language} debugger.\n\n"
        prompt += f"Fix:\n```{language}\n{code}\n```\n\n"
        prompt += f"Error: {error['type']}: {error['message']}\n\n"
        prompt += "Provide ONLY corrected code."
        return prompt

box = YuuBox(max_iterations=5)
box.healer = CustomHealer()
result = box.execute(buggy_code, "python")
```

<br>

### Batch Execution

```python
from yuubox import YuuBox
from pathlib import Path

def batch_execute(files, language="python"):
    box = YuuBox()
    results = []
    
    for file_path in files:
        with open(file_path) as f:
            code = f.read()
        
        result = box.execute(code, language)
        results.append({
            "file": file_path,
            "success": result.success,
            "iterations": result.iterations,
            "output": result.stdout,
        })
    
    return results

files = Path("./scripts").glob("*.py")
results = batch_execute(files)

for r in results:
    status = "✓" if r["success"] else "✗"
    print(f"{status} {r['file']} - {r['iterations']} iterations")
```

<br>

### Monitoring

```python
from yuubox import YuuBox
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('yuubox.monitor')

def monitored_execute(code, language):
    box = YuuBox()
    start = time.time()
    
    logger.info(f"Starting: {language}")
    result = box.execute(code, language)
    duration = time.time() - start
    
    logger.info(f"Complete in {duration:.2f}s")
    logger.info(f"Success: {result.success}")
    logger.info(f"Iterations: {result.iterations}")
    
    if not result.success:
        logger.error(f"Error: {result.stderr[:200]}")
    
    return result

result = monitored_execute("print('test')", "python")
```

<br>

---

<br>

<div align="center">

## API Reference

</div>

<br>

### YuuBox Class

Main entry point for code execution with self-healing.

```python
class YuuBox:
    def __init__(
        self,
        max_iterations: int = 5,
        yuuki_api_url: Optional[str] = None
    ):
        """
        Initialize YuuBox executor.
        
        Parameters:
            max_iterations: Maximum healing attempts (default: 5)
            yuuki_api_url: Custom Yuuki endpoint (optional)
        """
```

<br>

### Execute Method

Primary method for code execution.

```python
def execute(
    self,
    code: str,
    language: str,
    limits: Optional[ResourceLimits] = None,
    no_healing: bool = False,
) -> ExecutionResult:
    """
    Execute code with optional self-healing.
    
    Parameters:
        code: Source code as string
        language: "python", "javascript", "js", "node",
                 "rust", "go", "java"
        limits: Optional ResourceLimits
        no_healing: If True, execute once without healing
    
    Returns:
        ExecutionResult object
    
    Example:
        result = box.execute(
            code='print("hello")',
            language="python",
            limits=ResourceLimits(memory_mb=512)
        )
    """
```

<br>

### ResourceLimits Dataclass

```python
@dataclass
class ResourceLimits:
    """Resource constraints for execution."""
    
    memory_mb: int = 256
    """Memory limit in MB. Range: 64-2048. Default: 256."""
    
    cpu_quota: float = 1.0
    """CPU quota as fraction of one core.
    Range: 0.1-4.0. Default: 1.0 (100%)."""
    
    timeout_seconds: int = 60
    """Execution timeout in seconds.
    Range: 1-300. Default: 60."""

# Usage
limits = ResourceLimits(
    memory_mb=512,
    cpu_quota=2.0,
    timeout_seconds=120
)
```

<br>

### ExecutionResult Dataclass

```python
@dataclass
class ExecutionResult:
    """Complete execution result."""
    
    success: bool
    """True if code executed successfully."""
    
    stdout: str
    """Complete stdout from container."""
    
    stderr: str
    """Complete stderr from container."""
    
    exit_code: int
    """Process exit code. 0 = success."""
    
    iterations: int
    """Number of attempts made."""
    
    execution_time: float
    """Total time in seconds."""
    
    final_code: str
    """Final code version (possibly healed)."""
    
    error_history: List[ErrorReport]
    """Errors from each iteration."""

# Accessing
result = box.execute(code, "python")
if result.success:
    print(result.stdout)
    if result.iterations > 1:
        print(f"Fixed in {result.iterations} attempts")
else:
    print(f"Failed: {result.stderr}")
    for err in result.error_history:
        print(f"Attempt {err.iteration}: {err.error_type}")
```

<br>

### ErrorReport Dataclass

```python
@dataclass
class ErrorReport:
    """Structured error information."""
    
    error_type: str
    """Error class (e.g., 'NameError')."""
    
    error_message: str
    """Human-readable error message."""
    
    iteration: int
    """Iteration number where error occurred."""
    
    line_number: Optional[int]
    """Line number if available."""
```

<br>

### ErrorAnalyzer Class

```python
class ErrorAnalyzer:
    def analyze(
        self,
        stderr: str,
        language: str,
        code: str
    ) -> Dict[str, Any]:
        """
        Extract structured error information.
        
        Parameters:
            stderr: Error output from container
            language: Programming language
            code: Original code (for context)
        
        Returns:
            Dict with keys: type, message, line, stack_trace
        """
```

<br>

### YuukiHealer Class

```python
class YuukiHealer:
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize healer.
        
        Parameters:
            api_url: Custom Yuuki endpoint (optional)
        """
    
    def fix(
        self,
        code: str,
        error: Dict[str, Any],
        language: str,
        error_history: List[ErrorReport]
    ) -> str:
        """
        Request code fix from Yuuki.
        
        Parameters:
            code: Current failing code
            error: Structured error from analyzer
            language: Programming language
            error_history: Previous errors
        
        Returns:
            Fixed code or original if healing fails
        """
```

<br>

---

<br>

<div align="center">

## Deployment

</div>

<br>

### Docker Compose

```yaml
version: '3.8'

services:
  yuubox-api:
    image: yuubox:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - YUUKI_API_URL=https://opceanai-yuuki-api.hf.space
      - YUUBOX_MAX_ITERATIONS=5
      - YUUBOX_LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Deploy:

```bash
docker-compose up -d
docker-compose logs -f yuubox-api
```

<br>

### Dockerfile

```dockerfile
# Build stage
FROM rust:1.75 as builder

WORKDIR /build
COPY yuubox-core ./yuubox-core
COPY pyproject.toml ./

RUN apt-get update && \
    apt-get install -y python3-dev python3-pip && \
    pip3 install maturin

RUN maturin build --release --manifest-path yuubox-core/Cargo.toml

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /build/target/wheels/*.whl ./
COPY yuubox ./yuubox
COPY pyproject.toml ./

RUN pip install --no-cache-dir *.whl && \
    pip install --no-cache-dir ".[api]"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "yuubox.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t yuubox:latest .
docker run -p 8000:8000 -v /var/run/docker.sock:/var/run/docker.sock yuubox:latest
```

<br>

### Kubernetes

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: yuubox

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: yuubox
  namespace: yuubox
spec:
  replicas: 3
  selector:
    matchLabels:
      app: yuubox
  template:
    metadata:
      labels:
        app: yuubox
    spec:
      containers:
      - name: yuubox
        image: yuubox:latest
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: YUUKI_API_URL
          value: "https://opceanai-yuuki-api.hf.space"
        - name: YUUBOX_LOG_LEVEL
          value: "INFO"
        volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
          type: Socket

---

apiVersion: v1
kind: Service
metadata:
  name: yuubox
  namespace: yuubox
spec:
  type: LoadBalancer
  selector:
    app: yuubox
  ports:
  - port: 80
    targetPort: 8000
    name: http
```

Deploy:

```bash
kubectl apply -f yuubox-k8s.yaml
kubectl get pods -n yuubox
kubectl logs -f -n yuubox deployment/yuubox
```

<br>

### Systemd Service

```ini
[Unit]
Description=YuuBox API Server
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=yuubox
Group=yuubox
WorkingDirectory=/opt/yuubox
Environment="YUUKI_API_URL=https://opceanai-yuuki-api.hf.space"
Environment="YUUBOX_LOG_LEVEL=INFO"
ExecStart=/usr/local/bin/uvicorn yuubox.api:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Install:

```bash
sudo cp yuubox.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable yuubox
sudo systemctl start yuubox
journalctl -u yuubox -f
```

<br>

### Environment Configuration

```bash
# Yuuki settings
export YUUKI_API_URL="https://opceanai-yuuki-api.hf.space"

# Execution settings
export YUUBOX_MAX_ITERATIONS=5
export YUUBOX_DEFAULT_TIMEOUT=60
export YUUBOX_DEFAULT_MEMORY=256

# Docker settings
export YUUBOX_DOCKER_SOCKET="unix:///var/run/docker.sock"

# Logging
export YUUBOX_LOG_LEVEL=INFO

# API server
export YUUBOX_API_HOST=0.0.0.0
export YUUBOX_API_PORT=8000
```

<br>

---

<br>

<div align="center">

## Performance

</div>

<br>

### Execution Metrics

**Container Lifecycle:**
- Cold start (pulling image): 2.5 - 3.5 seconds
- Warm start (cached): 0.3 - 0.5 seconds
- Container creation: 0.2 - 0.3 seconds
- Container removal: 0.1 - 0.2 seconds
- Code execution: 0.1 - 2.0 seconds (varies by code)
- Yuuki API call: 2.0 - 5.0 seconds (network dependent)

**Throughput:**
- Without healing: 12 - 20 executions/minute
- With healing (avg 2 iterations): 8 - 12 executions/minute
- Full 5 iterations: 10 - 25 seconds total

The sequential model limits throughput but provides maximum isolation. For higher throughput, run multiple YuuBox instances in parallel.

<br>

### Resource Usage

**Memory per execution:**
- Container: 256MB (default, configurable)
- Rust runtime: ~10MB
- Python overhead: ~30MB
- Total host impact: ~300MB per execution

**CPU usage:**
- Container: Limited by quota (default 100% one core)
- Rust async runtime: Minimal overhead
- Python orchestration: Negligible

**Disk usage:**
- Base images: 180MB (Python), 250MB (Node), 1.2GB (Rust), 300MB (Go), 350MB (Java)
- Temporary storage: Up to 100MB per execution
- Container overhead: ~10MB

<br>

### Optimization Strategies

**Pre-pull images:**

```bash
docker pull python:3.11-slim
docker pull node:20-slim
docker pull rust:1.75-slim
docker pull golang:1.21-alpine
docker pull openjdk:17-slim
```

**Tune resource limits:**

```python
# Minimal for simple scripts
light = ResourceLimits(memory_mb=64, cpu_quota=0.25, timeout_seconds=10)

# Heavy for complex tasks
heavy = ResourceLimits(memory_mb=1024, cpu_quota=2.0, timeout_seconds=300)
```

**Parallel instances:**

```python
from concurrent.futures import ProcessPoolExecutor

def execute_file(path):
    box = YuuBox()
    with open(path) as f:
        return box.execute(f.read(), "python")

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(execute_file, file_paths))
```

<br>

---

<br>

<div align="center">

## Security

</div>

<br>

### Isolation Mechanisms

**Process Isolation:**
Docker containers use PID namespaces. Processes inside cannot see or interact with host processes or other containers. The container's process tree appears complete and isolated.

**Network Isolation:**
Default network mode is "none", disabling all network interfaces except loopback. This prevents:
- Outbound connections to external services
- Data exfiltration over network
- Command-and-control communication
- Network attacks on other systems
- DNS queries and hostname resolution

**Filesystem Isolation:**
Root filesystem is read-only, preventing:
- Modification of system files
- Installation of software
- Persistence between executions
- Unauthorized data storage

Only /tmp is writable (in-memory tmpfs, 100MB limit). Contents lost when container removed.

**User Privileges:**
Containers run as UID 1000:1000 (non-root) with no privileges. Cannot:
- Install packages
- Modify system config
- Access /proc or /sys meaningfully
- Bind to privileged ports
- Change file ownership

**Capability Dropping:**
All Linux capabilities dropped via cap_drop: ["ALL"]. Removed abilities include:
- CAP_NET_RAW (raw socket access)
- CAP_SYS_ADMIN (system administration)
- CAP_SYS_MODULE (kernel module loading)
- CAP_SYS_TIME (system time modification)

**Resource Limits:**
Cgroups enforce strict limits preventing:
- Memory exhaustion attacks
- CPU hogging
- Denial of service
- Fork bombs

Timeouts prevent infinite loops or deliberate hanging.

<br>

### Threat Model

**Code Injection:**
Threat: Malicious code attempts container escape or host attack.
Mitigation: Multiple isolation layers (namespace, read-only filesystem, dropped capabilities) make escape extremely difficult.

**Resource Exhaustion:**
Threat: Code consumes all CPU, memory, or disk.
Mitigation: Strict cgroup limits. Timeouts. Sequential execution limits impact to one execution.

**Data Exfiltration:**
Threat: Steal data or credentials from host.
Mitigation: Network isolation. Read-only filesystem. User isolation. No host filesystem access.

**Privilege Escalation:**
Threat: Exploit vulnerability to gain root.
Mitigation: Already non-root. All capabilities dropped. Container isolated from host.

**Container Escape:**
Threat: Exploit Docker/kernel vulnerability to break out.
Mitigation: Keep Docker and kernel updated. Monitor security advisories. Read-only filesystem limits post-escape damage.

<br>

### Best Practices

**System Updates:**
Regularly update Docker, Linux kernel, and YuuBox. Enable automatic security updates. Subscribe to security mailing lists.

**Least Privilege:**
Run YuuBox process as non-root on host. Grant Docker socket access only to specific user. Don't run entire system as root.

**Network Segmentation:**
Place behind firewall or reverse proxy. Implement rate limiting. Use authentication if exposed to untrusted networks.

**Audit Logging:**
Enable comprehensive execution logging. Include code, user, outcome, errors. Retain logs for auditing. Forward to centralized, immutable logging system.

**Resource Monitoring:**
Monitor CPU, memory, disk. Detect abnormal patterns. Set up alerts for unusual usage.

**Code Review:**
For sensitive deployments, review code before execution. Store submitted code. Consider content filtering for obvious malicious patterns.

<br>

---

<br>

<div align="center">

## Troubleshooting

</div>

<br>

### Common Issues

**Docker Connection Errors:**

"Failed to connect to Docker" or "Cannot connect to Docker daemon"

Solution:
- Verify Docker running: `docker ps`
- Linux: Ensure user in docker group: `groups | grep docker`
- Add to group: `sudo usermod -aG docker $USER` (then log out/in)
- macOS/Windows: Ensure Docker Desktop running
- Check socket exists: `ls -la /var/run/docker.sock`
- Test: `docker run hello-world`

<br>

**Maturin Build Failures:**

Build errors during `maturin develop`

Solution:
- Verify Rust: `rustc --version`, `cargo --version`
- Update Rust: `rustup update stable`
- Install Python headers: `sudo apt install python3-dev` (Ubuntu)
- Update maturin: `pip install --upgrade maturin`
- Clean rebuild: `rm -rf target/` then rebuild

<br>

**Import Errors:**

"No module named yuubox_core" after installation

Solution:
- Rebuild: `maturin develop`
- Check for error messages during build
- Ensure using correct virtual environment
- Try clean rebuild: remove target directory
- Verify installation: `pip list | grep yuubox`

<br>

**Timeout Errors:**

Execution times out

Solution:
- Increase timeout: `ResourceLimits(timeout_seconds=120)`
- Check for infinite loops in code
- Check if code waits for input
- Consider if computation appropriate for YuuBox

<br>

**Memory Limit Exceeded:**

Container killed with exit code 137

Solution:
- Increase memory: `ResourceLimits(memory_mb=512)`
- Optimize code to use less memory
- Check for memory leaks
- Ensure host has sufficient RAM

<br>

**Yuuki API Errors:**

Healing failures or API unavailable

Solution:
- Check network: `curl https://opceanai-yuuki-api.hf.space/health`
- Verify API endpoint correct
- Increase timeout in healer
- Check API status on HuggingFace Spaces

<br>

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

from yuubox import YuuBox

box = YuuBox()
result = box.execute(code, language)
```

Shows container creation, execution, error analysis, and healing attempts.

<br>

### Getting Help

- Check GitHub Issues for known bugs
- Search existing issues for error messages
- Open new issue with:
  - Minimal reproducible example
  - Python version, Rust version, Docker version
  - Operating system
  - Complete error message with stack trace
- For usage questions, open discussion thread

<br>

---

<br>

<div align="center">

## Development

</div>

<br>

### Building from Source

```bash
# Clone
git clone https://github.com/yuuki-os/yuubox
cd yuubox/yuubox-hybrid

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install maturin
pip install -e ".[dev]"

# Build Rust core (debug)
maturin develop

# Make Python changes - see immediately
# Rust changes require: maturin develop
```

<br>

### Testing

```bash
# Python tests
pytest tests/ -v

# Rust tests
cargo test --manifest-path yuubox-core/Cargo.toml

# With coverage
pytest --cov=yuubox --cov-report=html tests/

# Specific test
pytest tests/test_executor.py::test_basic_execution -v
```

<br>

### Code Quality

```bash
# Format Python
black yuubox/

# Lint Python
ruff check yuubox/

# Type check
mypy yuubox/

# Format Rust
cargo fmt --manifest-path yuubox-core/Cargo.toml

# Lint Rust
cargo clippy --manifest-path yuubox-core/Cargo.toml

# All checks
make lint
```

<br>

### Project Structure

```
yuubox-hybrid/
├── yuubox-core/              # Rust crate
│   ├── Cargo.toml           # Rust dependencies
│   ├── src/
│   │   ├── lib.rs           # PyO3 bindings
│   │   ├── container.rs     # Docker management
│   │   ├── limits.rs        # Resource limits
│   │   └── monitor.rs       # Monitoring
│   └── tests/
│
├── yuubox/                   # Python package
│   ├── __init__.py
│   ├── executor.py          # Main loop
│   ├── analyzer.py          # Error analysis
│   ├── healer.py            # Yuuki integration
│   ├── cli.py               # CLI
│   ├── api.py               # FastAPI
│   └── exceptions.py
│
├── tests/                    # Python tests
├── examples/                 # Usage examples
├── pyproject.toml           # Package config
├── Makefile
├── Dockerfile
└── LICENSE
```

<br>

### Adding Language Support

To add new language support:

**1. Update Rust core (yuubox-core/src/container.rs):**

```rust
fn get_image(&self, language: &str) -> Result<String> {
    let image = match language.to_lowercase().as_str() {
        // ... existing ...
        "ruby" => "ruby:3.2-slim",
        _ => return Err(anyhow!("Unsupported: {}", language)),
    };
    Ok(image.to_string())
}

fn build_command(&self, code: &str, language: &str) -> Result<Vec<String>> {
    let command = match language.to_lowercase().as_str() {
        // ... existing ...
        "ruby" => vec!["ruby".to_string(), "-e".to_string(), code.to_string()],
        _ => return Err(anyhow!("Unsupported: {}", language)),
    };
    Ok(command)
}
```

**2. Add error parser (yuubox/analyzer.py):**

```python
def analyze(self, stderr, language, code):
    # ... existing ...
    elif language == "ruby":
        return self._analyze_ruby(stderr, code)
    else:
        return self._generic_analysis(stderr, code)

def _analyze_ruby(self, stderr, code):
    match = re.search(r"(\w+Error): (.+)", stderr)
    if match:
        return {
            "type": match.group(1),
            "message": match.group(2),
            "stack_trace": stderr,
        }
    return self._generic_analysis(stderr, code)
```

**3. Add tests (tests/test_executor.py):**

```python
def test_ruby():
    box = YuuBox(max_iterations=1)
    result = box.execute('puts "Hello"', "ruby", no_healing=True)
    assert result.success
    assert "Hello" in result.stdout

def test_ruby_healing():
    box = YuuBox()
    result = box.execute('puts undefined', "ruby")
    # Should eventually succeed
```

**4. Rebuild:**

```bash
maturin develop
pytest tests/
```

<br>

---

<br>

<div align="center">

## Contributing

</div>

<br>

### Development Setup

```bash
git clone https://github.com/yourusername/yuubox
cd yuubox/yuubox-hybrid
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
maturin develop
```

<br>

### Code Standards

- Python: format with `black`, lint with `ruff`
- Rust: format with `rustfmt`, lint with `clippy`
- Docstrings required for all public functions
- Type hints required for Python signatures
- Tests required for new functionality
- Existing tests must pass

<br>

### Pull Request Process

1. Create feature branch from main
2. Make changes with clear commits
3. Add tests for new functionality
4. Update documentation if needed
5. Run test suite and linters
6. Push to fork and open PR
7. Respond to review feedback
8. Maintainer merges when approved

<br>

---

<br>

<div align="center">

## Related Projects

</div>

<br>

| Project | Description |
|:--------|:------------|
| [Yuu (Python SDK)](https://github.com/yuuki-os/yuu) | Official Python SDK for Yuuki code generation |
| [Yuu.js (JavaScript SDK)](https://github.com/yuuki-os/yuu.js) | Official JavaScript/TypeScript SDK for Yuuki |
| [Yuu-rs (Rust SDK)](https://github.com/yuuki-os/yuu-rs) | Official Rust SDK for Yuuki |
| [Yuuki API](https://huggingface.co/spaces/OpceanAI/Yuuki-api) | Open inference API on HuggingFace Spaces |
| [Yuuki Models](https://huggingface.co/OpceanAI/Yuuki-best) | Pre-trained model weights |

<br>

---

<br>

<div align="center">

## License

</div>

<br>

```
Apache License 2.0

Copyright 2026 Yuuki Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

See [LICENSE](LICENSE) for the full license text.

<br>

---

<br>

<div align="center">

**Self-healing code execution. Built with Rust and Python.**

<br>

[![YuuBox](https://img.shields.io/badge/YuuBox-2026-000000?style=for-the-badge)](https://github.com/yuuki-os/yuubox)

<br>

</div>
