import subprocess
import esprima

def check_js_syntax(code):
    """
    Check the syntax of the provided JavaScript code using Esprima.
    
    Args:
        code (str): JavaScript code to check.
    
    Returns:
        dict: A dictionary containing the status and error message if any.
    """
    try:
        esprima.parseScript(code)  # Parse JS code using Esprima
        return {"status": "success"}
    except Exception as e:
        # Clean up the error message to remove unnecessary details
        error_message = str(e)
        if "Line" in error_message:
            # Extract the relevant part of the error message
            error_message = error_message.split("Line")[1].strip()
        return {"status": "syntax_error", "error": f"Syntax Error: {error_message}"}

def run_js_code(code, timeout=5):
    """
    Run the provided JavaScript code using Node.js.
    
    Args:
        code (str): JavaScript code to execute.
        timeout (int): Maximum execution time in seconds.
    
    Returns:
        dict: A dictionary containing the status, output, and error message if any.
    """
    try:
        process = subprocess.run(
            ["node", "-e", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if process.returncode != 0:
            # Clean up the error message to remove unnecessary details
            error_message = process.stderr.strip()
            if "Error" in error_message:
                error_message = error_message.split("Error:")[1].strip()
            return {"status": "runtime_error", "error": f"Runtime Error: {error_message}"}
        return {"status": "success", "output": process.stdout.strip()}
    except subprocess.TimeoutExpired:
        return {"status": "timeout_error", "error": "Execution timed out"}
    except Exception as e:
        # Clean up the error message to remove unnecessary details
        error_message = str(e)
        if "Error" in error_message:
            error_message = error_message.split("Error:")[1].strip()
        return {"status": "runtime_error", "error": f"Runtime Error: {error_message}"}

def debug_js_code(code, timeout=5):
    """
    Debug JavaScript code by first checking syntax and then running it.
    
    Args:
        code (str): JavaScript code to debug.
        timeout (int): Maximum execution time in seconds.
    
    Returns:
        dict: A dictionary containing the status, output, and error message if any.
    """
    syntax_result = check_js_syntax(code)
    if syntax_result["status"] == "syntax_error":
        return syntax_result
    return run_js_code(code, timeout)

# Example JavaScript Code
js_code = """
function add(a, b) {
    return a + b;
}
console.log(add(2, 3));
"""

# Debug the JavaScript code
result = debug_js_code(js_code)
print(result)