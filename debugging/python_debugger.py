import ast
import sys
import traceback
import io
from contextlib import redirect_stdout
import threading

class TimeoutError(Exception):
    """Custom exception for execution timeout."""
    pass

def run_with_timeout(func, args=(), kwargs={}, timeout=5):
    """
    Run a function with a timeout using threading.
    """
    result = None
    exception = None

    def target():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # If the thread is still alive after the timeout, raise TimeoutError
        raise TimeoutError("Execution timed out")
    if exception is not None:
        # If an exception occurred in the thread, re-raise it
        raise exception
    return result

def check_python_syntax(code):
    """
    Check the syntax of the provided Python code using AST.
    """
    try:
        ast.parse(code)  # Parse the code using Python AST
        return {"status": "success"}
    except SyntaxError as e:
        # Safely get the context line
        context = None
        lines = code.split("\n")  # Split code into lines
        if e.lineno and len(lines) >= e.lineno:
            context = lines[e.lineno - 1].strip()
        return {
            "status": "syntax_error",
            "error": f"Syntax Error: {e.msg} at line {e.lineno}",
            "line": e.lineno,
            "context": context,
        }

def run_python_code(code, input_data=None, timeout=5):
    """
    Execute the provided Python code.
    Supports input redirection and handles timeouts.
    """
    try:
        # Capture standard output
        output_capture = io.StringIO()
        exec_globals = {}
        exec_locals = {}

        def execute_code():
            with redirect_stdout(output_capture):
                if input_data:
                    # Redirect input if provided
                    original_input = sys.stdin
                    sys.stdin = io.StringIO(input_data)
                    exec(code, exec_globals, exec_locals)
                    sys.stdin = original_input
                else:
                    exec(code, exec_globals, exec_locals)

        # Run the code with a timeout
        run_with_timeout(execute_code, timeout=timeout)

        # Get the output and split it into lines
        output = output_capture.getvalue().strip()
        output_lines = output.split("\n") if output else []

        return {
            "status": "success",
            "output": output_lines,
            "locals": exec_locals,
        }
    except TimeoutError as e:
        return {"status": "timeout_error", "error": str(e)}
    except Exception as e:
        # Extract clean error message (type and message only)
        error_type = e.__class__.__name__
        error_message = str(e)
        clean_error = f"{error_type}: {error_message}"

        # Get the line number and context (if available)
        tb = traceback.extract_tb(sys.exc_info()[2])
        line_number = tb[-1].lineno if tb else None
        context = None
        lines = code.split("\n")  # Split code into lines
        if line_number and len(lines) >= line_number:
            context = lines[line_number - 1].strip()

        return {
            "status": "runtime_error",
            "error": clean_error,  # Clean error message
            "line": line_number,
            "context": context,
        }

def debug_python_code(code, input_data=None, timeout=5):
    """
    Debug the provided Python code by checking syntax and running it.
    """
    syntax_result = check_python_syntax(code)
    if syntax_result["status"] == "syntax_error":
        return syntax_result
    return run_python_code(code, input_data, timeout)