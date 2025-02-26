# CodePulse_GGH

## Overview  
**CodePulse** is an **AI-powered real-time debugging** and **test case optimization** tool that supports multiple programming languages. It helps developers **catch errors instantly, optimize test cases, and improve code efficiency**.

---

## 🔥 Features  
✅ **Real-Time Debugging**: Instantly detects syntax and logical errors in **Python, C++, Java, and JavaScript**.  
✅ **Multi-Language Support**: Uses **AST-based parsers** (Python AST, Clang AST for C++, Esprima for JavaScript, JavaLang for Java).  
✅ **Test Case Optimization**: AI-driven test generation and optimization for better code coverage.  
✅ **Cloud Deployment**: Hosted on **Render** with a **Docker-based backend**.  
✅ **User-Friendly UI**: Web interface powered by **Streamlit**.  

---

## 🛠️ Tech Stack  
- **Backend**: Python, Flask/FastAPI  
- **Frontend**: Streamlit  
- **Compiler & Parsing**: AST (Python), Clang AST (C++), Esprima (JavaScript), JavaLang (Java)  
- **Deployment**: Docker, Render  
- **AI & Optimization**: NLP-based error detection & test case optimization  


## Project Structure
CodePulse_GGH/
│── debugging/           # Language-specific debuggers
│   │── cpp_debugger.py       # C++ debugging logic
│   │── javascript_debugger.py # JavaScript debugging logic
│   │── python_debugger.py     # Python debugging logic
│   └── __init__.py            # Module initialization
│
│── testing/             # Test case optimization
│   │── test_generator.py      # AI-driven test case generation
│   └── __init__.py            # Module initialization
│
│── .venv/               # Virtual environment (ignored)
│── Dockerfile           # Deployment configuration
│── .dockerignore        # Files to ignore in Docker builds
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
│── main.py              # Streamlit application entry point
│── unused_fastapi.py    # Unused FastAPI backend (for potential future use)
└── __pycache__/         # Compiled Python cache files (ignored)


