import streamlit as st
from streamlit_ace import st_ace
import debugging.python_debugger
import debugging.javascript_debugger
import debugging.cpp_debugger
import time

# Custom CSS for full-screen background and title styling
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://i.pinimg.com/736x/c9/da/c8/c9dac850c279322c2b52b0be31aced63.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    .title-main {
        color: #00FFFF; /* Neon Cyan */
        text-align: center;
        font-size: 80px;
        font-weight: 900;
        margin-bottom: -10px;
    }
    .title-sub {
        color: #FFD700; /* Gold */
        text-align: center;
        font-size: 28px;
        font-weight: 500;
    }
    .error-message {
        color: #FF0000; /* Red */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Styled Title
st.markdown('<h1 class="title-main">CodePulse</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="title-sub">Debug Smarter, Debug Faster</h2>', unsafe_allow_html=True)

# Initialize session state variables
if "last_active" not in st.session_state:
    st.session_state.last_active = time.time()
if "parser_triggered" not in st.session_state:
    st.session_state.parser_triggered = False
if "debug_output" not in st.session_state:
    st.session_state.debug_output = []
if "code" not in st.session_state:
    st.session_state.code = ""
if "language" not in st.session_state:
    st.session_state.language = "Python"

# JavaScript to track user activity and reset idle timer
idle_script = """
<script>
var timeout;
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
document.onclick = resetTimer;
document.onscroll = resetTimer;

function resetTimer() {
    window.parent.postMessage('active', '*');
    clearTimeout(timeout);
    timeout = setTimeout(goIdle, 5000); // 5s idle
}

function goIdle() {
    window.parent.postMessage('idle', '*');
}
</script>
"""
st.components.v1.html(idle_script, height=0)

# Function to clean error messages
def clean_error_message(error):
    """
    Clean up error messages by removing file paths and unnecessary details.
    """
    if isinstance(error, str):
        # Remove file paths and other unnecessary details
        if "File" in error and "line" in error:
            # Extract the error message after the last occurrence of "Error:"
            error = error.split("Error:")[-1].strip()
        return error
    return str(error)

# Function to debug code
def debug_code(code, language):
    if language == "Python":
        result = debugging.python_debugger.run_python_code(code)
    elif language == "JavaScript":
        result = debugging.javascript_debugger.run_js_code(code)
    elif language == "C++":
        result = debugging.cpp_debugger.run_cpp_code(code)
    else:
        return [f"❌ Unsupported language: {language}"]

    # Extract the output from the result dictionary
    if isinstance(result, dict):
        if result.get("status") == "success":
            output = result.get("output", "")
            # Ensure output is a list
            if isinstance(output, str):
                output = output.split("\n")  # Convert string to list of lines
            elif isinstance(output, list):
                pass  # Already a list
            else:
                output = []  # Default to empty list
            return output + ["✅ No errors found!"]  # Return output + success message
        elif "error" in result:
            # Clean the error message
            clean_error = clean_error_message(result["error"])
            return [f"❌ {clean_error}"]  # Return clean error message
    elif isinstance(result, str):
        return result.split("\n")  # If result is already a string, split it
    else:
        return [f"❌ Unexpected result format: {result}"]

# Function to check idle time and trigger debugging
def check_idle():
    current_time = time.time()
    if current_time - st.session_state.last_active > 5:
        if not st.session_state.parser_triggered:
            st.session_state.parser_triggered = True
            st.session_state.debug_output = debug_code(st.session_state.code, st.session_state.language)
            st.rerun()  # Auto-refresh the app when idle

# Language Selection - Reset code when language changes
selected_language = st.selectbox("🔍 Select Programming Language:", ["Python", "C++", "JavaScript"], index=["Python", "C++", "JavaScript"].index(st.session_state.language))

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.session_state.code = ""  # Reset code when language is changed

# Language Mappings for Ace Editor
language_modes = {
    "Python": "python",
    "C++": "c_cpp",
    "JavaScript": "javascript"
}

# VS Code-like Editor using `st_ace`
st.session_state.code = st_ace(
    value=st.session_state.code,
    language=language_modes[st.session_state.language],
    theme="monokai",  # Other themes: dracula, github, solarized_dark, etc.
    keybinding="vscode",
    font_size=16,
    tab_size=4,
    show_gutter=True,
    show_print_margin=False,
    wrap=True,
    height=400
)

# Debug Button
if st.button("Debug Code"):
    if st.session_state.code.strip():
        with st.spinner("Debugging in progress..."):
            st.session_state.debug_output = debug_code(st.session_state.code, st.session_state.language)
        st.session_state.parser_triggered = False  # Reset parser flag
    else:
        st.warning("⚠️ Please enter some code to debug.")

# Auto-refresh if idle for 5 seconds
check_idle()

# Display debugging output line by line
st.subheader("🐞 Debugging Output")
if st.session_state.debug_output:
    for line in st.session_state.debug_output:
        if line.startswith("❌"):
            st.markdown(f'<p class="error-message">{line}</p>', unsafe_allow_html=True)
        else:
            st.text(line)
else:
    st.text("No debugging output yet.")

