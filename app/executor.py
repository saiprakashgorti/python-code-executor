import subprocess
import tempfile
import os
import json
import sys
import signal
import threading
import shutil
from io import StringIO


def check_nsjail_available():
    """Check if nsjail is available on the system"""
    return shutil.which("nsjail") is not None


def execute_script(script):
    # Save to temp file
    with tempfile.TemporaryDirectory() as tmpdirname:
        script_path = os.path.join(tmpdirname, "user_script.py")
        with open(script_path, "w") as f:
            f.write(script)

        # Check if nsjail is available
        use_nsjail = check_nsjail_available()

        if use_nsjail:
            # Use nsjail for secure execution
            nsjail_cmd = [
                "nsjail",
                "--quiet",
                "--mode",
                "o",
                "--time_limit",
                "10",
                "--exec",
                "/usr/bin/python3",
                "--",
                script_path,
            ]
        else:
            # Fall back to regular Python execution
            nsjail_cmd = ["python3", script_path]

        try:
            proc = subprocess.Popen(
                nsjail_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Use communicate with timeout
            try:
                out, err = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate()
                return None, "", "Script execution timed out (10 seconds)"

        except Exception as e:
            return None, "", f"Error running script: {str(e)}"

        # Execute the script and capture both stdout and the return value
        try:
            if use_nsjail:
                result_cmd = [
                    "nsjail",
                    "--quiet",
                    "--mode",
                    "o",
                    "--time_limit",
                    "10",
                    "--exec",
                    "/usr/bin/python3",
                    "--",
                    "-c",
                    f"""
import sys
import json
import os
import io
sys.path.insert(0, '{tmpdirname}')
import user_script

# Capture stdout to collect print statements
stdout_capture = io.StringIO()
old_stdout = sys.stdout
sys.stdout = stdout_capture

try:
    result = user_script.main()
    
    # Get the captured stdout
    captured_stdout = stdout_capture.getvalue()
    sys.stdout.close()
    sys.stdout = old_stdout
    
    # Return both the result and stdout
    output = {{
        "result": result,
        "stdout": captured_stdout
    }}
    print(json.dumps(output))
except Exception as e:
    sys.stdout.close()
    sys.stdout = old_stdout
    print(json.dumps({{"error": str(e)}}))
""",
                ]
            else:
                result_cmd = [
                    "python3",
                    "-c",
                    f"""
import sys
import json
import os
import io
sys.path.insert(0, '{tmpdirname}')
import user_script

# Capture stdout to collect print statements
stdout_capture = io.StringIO()
old_stdout = sys.stdout
sys.stdout = stdout_capture

try:
    result = user_script.main()
    
    # Get the captured stdout
    captured_stdout = stdout_capture.getvalue()
    sys.stdout.close()
    sys.stdout = old_stdout
    
    # Return both the result and stdout
    output = {{
        "result": result,
        "stdout": captured_stdout
    }}
    print(json.dumps(output))
except Exception as e:
    sys.stdout.close()
    sys.stdout = old_stdout
    print(json.dumps({{"error": str(e)}}))
""",
                ]

            result_proc = subprocess.Popen(
                result_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            try:
                result_out, result_err = result_proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                result_proc.kill()
                result_proc.communicate()
                return None, "", "main() function execution timed out (10 seconds)"

            if result_err:
                return None, "", f"Error executing main(): {result_err}"

            result_str = result_out.strip()
            output_data = json.loads(result_str)

            if "error" in output_data:
                return None, "", output_data["error"]

            return output_data["result"], output_data["stdout"], None
        except Exception as e:
            return (
                None,
                "",
                f"Could not run main() or output is not valid JSON: {str(e)}",
            )
