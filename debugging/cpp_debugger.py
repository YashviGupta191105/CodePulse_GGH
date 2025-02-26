import subprocess
import os
import tempfile
import sys

# Define a safe temp directory inside the app
TEMP_DIR = "/app/tmp"
os.makedirs(TEMP_DIR, exist_ok=True)

# MinGW Include Paths (Update paths based on your installation)
MINGW_INCLUDE_PATHS = [
    "-Ic:/mingw64/include",
    "-Ic:/mingw64/lib/gcc/x86_64-w64-mingw32/14.2.0/include",
    "-Ic:/mingw64/lib/gcc/x86_64-w64-mingw32/14.2.0/include/c++",
    "-Ic:/mingw64/lib/gcc/x86_64-w64-mingw32/14.2.0/include/c++/x86_64-w64-mingw32",
]

def clean_error_message(error):
    """
    Clean up error messages by removing file paths and unnecessary details.
    """
    if isinstance(error, str):
        lines = error.split("\n")
        cleaned_lines = [f"❌ {line.split('error:')[-1].strip()}" for line in lines if "error:" in line]
        return "\n".join(cleaned_lines)
    return str(error)

def check_cpp_syntax(code):
    """
    Check the syntax of the C++ code using GCC.
    Returns a dictionary with status and error details (if any).
    """
    temp_cpp_path = None

    try:
        with tempfile.NamedTemporaryFile(dir=TEMP_DIR, suffix=".cpp", delete=False, mode="w") as temp_cpp:
            temp_cpp_path = temp_cpp.name
            temp_cpp.write(code)

        compile_process = subprocess.run(
            ["g++", "-fsyntax-only", temp_cpp_path] + MINGW_INCLUDE_PATHS,
            capture_output=True,
            text=True,
            timeout=10
        )

        if compile_process.returncode != 0:
            return {"status": "syntax_error", "error": clean_error_message(compile_process.stderr.strip())}
        return {"status": "success"}
    
    except subprocess.TimeoutExpired:
        return {"status": "timeout_error", "error": "Syntax check timed out"}
    except Exception as e:
        return {"status": "parser_error", "error": str(e)}
    finally:
        if temp_cpp_path and os.path.exists(temp_cpp_path):
            os.remove(temp_cpp_path)

def run_cpp_code(code, input_data=None):
    """
    Compile and run C++ code with error handling and timeouts.
    """
    temp_cpp_path = None
    temp_exe_path = os.path.join(TEMP_DIR, "temp.out")

    try:
        with tempfile.NamedTemporaryFile(dir=TEMP_DIR, suffix=".cpp", delete=False, mode="w") as temp_cpp:
            temp_cpp_path = temp_cpp.name
            temp_cpp.write(code)

        compile_process = subprocess.run(
            ["g++", temp_cpp_path, "-o", temp_exe_path] + MINGW_INCLUDE_PATHS,
            capture_output=True,
            text=True,
            timeout=10
        )

        if compile_process.returncode != 0:
            return {"status": "compile_error", "error": clean_error_message(compile_process.stderr.strip())}

        run_process = subprocess.run(
            [temp_exe_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        return {"status": "success", "output": run_process.stdout.strip()}
    
    except subprocess.TimeoutExpired:
        return {"status": "timeout_error", "error": "Compilation or execution timed out"}
    except Exception as e:
        return {"status": "runtime_error", "error": str(e)}
    finally:
        if temp_cpp_path and os.path.exists(temp_cpp_path):
            os.remove(temp_cpp_path)
        if temp_exe_path and os.path.exists(temp_exe_path):
            try:
                import time
                time.sleep(0.5)
                os.remove(temp_exe_path)
            except PermissionError:
                print(f"Warning: Could not delete {temp_exe_path}, file may still be in use.")

def debug_cpp_code(code, input_data=None):
    """
    Debug the provided C++ code by checking syntax and running it.
    """
    syntax_result = check_cpp_syntax(code)
    if syntax_result["status"] == "syntax_error":
        return syntax_result
    return run_cpp_code(code, input_data)

# Example C++ Code
cpp_code = """
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
"""

# Debug and run the C++ code
result = debug_cpp_code(cpp_code)
print(result)
