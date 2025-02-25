# Python parser
def parse_python(code):
    import ast
    tree = ast.parse(code)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            input_types = [(arg.arg, arg.annotation.id if arg.annotation else None) for arg in node.args.args]
            return_type = node.returns.id if node.returns else None
            functions.append({
                "name": function_name,
                "inputs": input_types,
                "return_type": return_type
            })
    return functions

# JavaScript parser (using Esprima)
import esprima
def parse_javascript(code):
    try:
        # Parse the JavaScript code into an AST
        tree = esprima.parseScript(code, { "tokens": True, "range": True })
        functions = []

        # Traverse the AST to extract function details
        for node in tree.body:
            if node.type == "FunctionDeclaration":
                function_name = node.id.name
                input_types = [(param.name, None) for param in node.params]  # JavaScript doesn't have type hints
                functions.append({
                    "name": function_name,
                    "inputs": input_types,
                    "return_type": None  # JavaScript doesn't have return type annotations
                })
        return functions
    except Exception as e:
        print(f"JavaScript parsing error: {e}")
        return []

# CPP parser (using clang)
import clang.cindex
clang.cindex.Config.set_library_file("C:/Program Files/LLVM/bin/libclang.dll")
def parse_cpp(code):
    """
    Parses C++ code using Clang AST and extracts function details.
    """
    # 🔹 Create a Clang Index
    index = clang.cindex.Index.create()

    # 🔹 Save the C++ code to a temporary file (Clang requires a file)
    temp_file = "temp.cpp"
    with open(temp_file, "w") as f:
        f.write(code)

    # 🔹 Parse the file
    translation_unit = index.parse(temp_file, args=['-std=c++11'])

    functions = []

    # 🔹 Extract function details
    for node in translation_unit.cursor.walk_preorder():
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            function_name = node.spelling
            input_types = [(arg.spelling, arg.type.spelling) for arg in node.get_arguments()]
            return_type = node.result_type.spelling

            functions.append({
                "name": function_name,
                "inputs": input_types,
                "return_type": return_type
            })

    return functions

# Java parser (using JavaParser)
def parse_java(code):
    import javalang
    try:
        tree = javalang.parse.parse(code)
        functions = []
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            function_name = node.name
            input_types = [(param.name, param.type.name) for param in node.parameters]
            return_type = node.return_type.name if node.return_type else None
            functions.append({
                "name": function_name,
                "inputs": input_types,
                "return_type": return_type
            })
        return functions
    except javalang.parser.JavaSyntaxError as e:
        print(f"Java syntax error: {e}")
        return []
    
# Unified interface
def parse_code(code, language):
    if language == "python":
        return parse_python(code)
    elif language == "javascript":
        return parse_javascript(code)
    elif language == "cpp":
        return parse_cpp(code)
    elif language == "java":
        return parse_java(code)
    else:
        raise ValueError(f"Unsupported language: {language}")

# Example usage
python_code = """
def add(a: int, b: int) -> int:
    return a + b
"""

cpp_code = """
int add(int a, int b) {
    return a + b;
}
"""

java_code = """
public class Main {
    public static int add(int a, int b) {
        return a + b;
    }
}
"""

javascript_code = """
function add(a, b) {
    return a + b;
}
"""

print("Python Functions:", parse_code(python_code, "python"))
print("C++ Functions:", parse_code(cpp_code, "cpp"))
print("Java Functions:", parse_code(java_code, "java"))
print("JavaScript Functions:", parse_code(javascript_code, "javascript"))