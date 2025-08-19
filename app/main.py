from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from app.validator import validate_script
from app.executor import execute_script
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class ScriptInput(BaseModel):
    script: str


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route("/execute", methods=["POST"])
def execute():
    try:
        # Parse and validate JSON input via Pydantic
        data = request.get_json(force=True)
        user_input = ScriptInput(**data)

        # Validate the script
        err = validate_script(user_input.script)
        if err:
            logger.warning(f"Script validation failed: {err}")
            return jsonify({"error": err}), 400

        # Execute the script
        result, stdout, error = execute_script(user_input.script)
        if error:
            logger.error(f"Script execution failed: {error}")
            return jsonify({"error": error}), 400

        logger.info("Script executed successfully")
        return jsonify({"result": result, "stdout": stdout})

    except ValidationError as ve:
        logger.error(f"Validation error: {ve.errors()}")
        return jsonify({"error": ve.errors()}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # For development
    app.run(host="0.0.0.0", port=8080, debug=False)
else:
    # For production with gunicorn
    pass
