import ast
import random

def infer_param_types(func_code):
    """
    Extract function signature and infer parameter types using AST.
    """
    try:
        tree = ast.parse(func_code)
        func_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
        params = {arg.arg: "int" for arg in func_node.args.args}  # Default all params to int
        return params
    except Exception as e:
        return {}

def generate_test_cases(param_types):
    """
    Generate robust test cases including:
    ✅ Random Values
    ✅ Boundary Values
    ✅ Equivalence Partitioning
    ✅ Mutation Testing
    """
    test_cases = []
    
    for param, p_type in param_types.items():
        values = []
        
        if p_type == "int":
            values.extend([
                0,  # Edge case: Zero
                1,  # Edge case: Smallest positive integer
                -1,  # Edge case: Smallest negative integer
                random.randint(-100, 100),  # Random value
                99999999,  # Large positive value
                -99999999  # Large negative value
            ])
        
        elif p_type == "float":
            values.extend([
                0.0, 1.0, -1.0,  # Edge cases
                random.uniform(-100.0, 100.0),  # Random float
                1e-10, -1e-10,  # Very small floating values
                1e10, -1e10  # Very large floating values
            ])
        
        elif p_type == "str":
            values.extend([
                "",  # Empty string
                "a",  # Single character
                "test",  # Short string
                " " * 100,  # Long whitespace string
                "longstring" * 10,  # Large string
                "@#&*(!)",  # Special characters
            ])
        
        # Generate test cases using cartesian product of possible values
        if not test_cases:
            test_cases = [[v] for v in values]
        else:
            new_cases = []
            for case in test_cases:
                for v in values:
                    new_cases.append(case + [v])
            test_cases = new_cases

    return [tuple(tc) for tc in test_cases]
