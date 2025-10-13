# Import required modules from Flask
from flask import Flask, request, jsonify

# Create a Flask app instance
app = Flask(__name__)

# -------------------------------
# HOME ROUTE (GET)
# -------------------------------
@app.route('/')
def home():
    """
    This route is called when the user visits the root URL ('/').
    It returns a welcome message and lists all supported operations.
    """
    return jsonify({
        "message": "Welcome to Calculator API! Use POST /calculate with a, b, and operation.",
        "operations": ["add", "subtraction", "multiply", "divide", "power"]
    })


# -------------------------------
# CALCULATE ROUTE (POST)
# -------------------------------
@app.route('/calculate', methods=['POST'])
def calculate():
    """
    This route handles POST requests to perform a mathematical operation.
    JSON input format example:
    {
        "a": 10,
        "b": 5,
        "operation": "add"
    }
    """

    # Get the JSON data from the request body
    data = request.get_json()

    # ✅ Validate that JSON data is provided
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Extract values from JSON body
    a = data.get('a')
    b = data.get('b')
    operation = data.get('operation', '').lower()  # Convert to lowercase for consistency

    # ✅ Check if 'a' and 'b' are present
    if a is None or b is None:
        return jsonify({"error": "Please provide both 'a' and 'b' values"}), 400

    # ✅ Try to convert a and b into numbers (float allows decimals)
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return jsonify({"error": "'a' and 'b' must be numbers"}), 400

    # Define valid operations
    valid_ops = ['add', 'subtraction', 'multiply', 'divide', 'power']

    # ✅ Check if the operation is valid
    if operation not in valid_ops:
        return jsonify({
            "error": f"Invalid operation '{operation}'. Choose from {valid_ops}"
        }), 400

    # -------------------------------
    # PERFORM THE OPERATION
    # -------------------------------
    if operation == 'add':
        result = a + b

    elif operation == 'subtraction':
        result = a - b

    elif operation == 'multiply':
        result = a * b

    elif operation == 'divide':
        # Prevent division by zero
        if b == 0:
            return jsonify({"error": "Division by zero not allowed"}), 400
        result = a / b

    elif operation == 'power':
        result = a ** b

    # -------------------------------
    # RETURN RESPONSE AS JSON
    # -------------------------------
    return jsonify({
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    })


# -------------------------------
# MAIN FUNCTION TO RUN APP
# -------------------------------
if __name__ == '__main__':
    # Run the Flask app in debug mode so it auto-reloads on code changes
    app.run(debug=True)
