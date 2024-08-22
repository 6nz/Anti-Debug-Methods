
# Anti-Debug Methods

This repository contains various methods to detect and mitigate debugging attempts on Windows applications. The focus is on techniques involving DLLs (Dynamic-Link Libraries) and other common anti-debugging strategies.

## "Current Features"

- **DLL Injection Protection**: Implements process mitigation policies to prevent unsigned DLLs from being loaded.
- **Function Inspection**: Periodically checks for function integrity to detect unauthorized modifications.
- **Threaded Monitoring**: Runs protection checks in parallel with the main application, ensuring real-time detection.

## File Descriptions

### 1. `DLL-Related/Anti-DLL-Injection.py`
This script is designed to prevent unauthorized DLLs from being injected into a process by enforcing a process mitigation policy that only allows Microsoft-signed binaries.

- **Key Functions**:
  - `set_process_mitigation_policy(policy, lpBuffer, size)`: Applies the specified mitigation policy to the process.
  - `configure_process_mitigation_policy()`: Configures the process to only load Microsoft-signed DLLs.

- **Usage**:
  - Run the script to apply the policy and prevent DLL injection.
  - The process will sleep for 120 seconds to allow for inspection.

### 2. `DLL-Related/main.py`
This script uses threading to run a continuous check on the `oldprog` function, ensuring that it hasn't been tampered with.

- **Key Functions**:
  - `func_prot()`: Repeatedly checks the source code of `oldprog` to ensure it hasn't been modified.
  
- **Usage**:
  - The script starts a thread to run `func_prot()` in the background while executing `oldprog()`.

### 3. `DLL-Related/code.py`
This simple script reassigns `oldprog` to a new function `newprog`, demonstrating a basic attempt at function replacement.

- **Key Functions**:
  - `newprog()`: A placeholder function.
  - Exception handling demonstrates how to catch and report errors during function reassignment.

## Requirements

- Python 3.9+
- Windows OS


## License

This project is licensed under the BSD3 License - see the [LICENSE](LICENSE) file for details.
