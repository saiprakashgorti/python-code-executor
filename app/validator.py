import ast
import json


def validate_script(script):
    try:
        tree = ast.parse(script)
        func_names = [
            node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        ]

        if "main" not in func_names:
            return "Script must define a 'main()' function"

        main_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                main_func = node
                break

        if main_func:
            has_return = any(isinstance(n, ast.Return) for n in ast.walk(main_func))
            if not has_return:
                return "main() function must have a return statement"

        dangerous_imports = ["subprocess", "os.system", "eval", "exec", "__import__"]
        script_lower = script.lower()
        for dangerous in dangerous_imports:
            if dangerous in script_lower:
                return f"Script contains potentially dangerous operation: {dangerous}"

    except SyntaxError as e:
        return f"Syntax error in script: {str(e)}"
    except Exception as e:
        return f"Validation error: {str(e)}"

    return None
