from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Flask API! Use endpoints like /sum_even, /sum_odd, etc."})


# ✅ Correct: 'methods' not 'method'
@app.route('/sum_even', methods=['POST'])
def sum_even():
    numbers = request.json.get('numbers')
    num_list = [int(x) for x in numbers.split(',') if x.strip().isdigit()]
    even_sum = sum([n for n in num_list if n % 2 == 0])
    return jsonify({
        "numbers": num_list,
        "sum_even": even_sum
    })


@app.route('/sum_odd', methods=['POST'])
def sum_odd():
    numbers = request.json.get('numbers')
    num_list = [int(x) for x in numbers.split(',') if x.strip().isdigit()]
    odd_sum = sum([n for n in num_list if n % 2 != 0])
    return jsonify({
        "numbers": num_list,
        "sum_odd": odd_sum
    })


@app.route('/natural_sum', methods=['POST'])
def natural_sum():
    n = int(request.json.get('num'))
    total = n * (n + 1) // 2
    return jsonify({
        "n": n,
        "sum_natural": total
    })


@app.route('/prime_list', methods=['POST'])
def prime_list():
    numbers = request.json.get('numbers')
    num_list = [int(x) for x in numbers.split(',') if x.strip().isdigit()]

    primes = []
    for n in num_list:
        if n < 2:
            continue
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                break
        else:
            primes.append(n)

    return jsonify({
        "numbers": num_list,
        "primes": primes,
        "sum_primes": sum(primes)
    })


@app.route('/string_ops', methods=['POST'])
def string_ops():
    text = request.json.get('text')
    reversed_text = text[::-1]
    length = len(text)
    upper = text.upper()
    lower = text.lower()
    vowel_count = sum(1 for ch in text.lower() if ch in 'aeiou')
    palindrome = text.lower() == reversed_text.lower()

    return jsonify({
        "original": text,
        "reversed": reversed_text,
        "length": length,
        "uppercase": upper,
        "lowercase": lower,
        "vowel_count": vowel_count,
        "is_palindrome": palindrome
    })


@app.route('/square', methods=['GET'])
def square():
    num = request.args.get('num')
    if not num:
        return jsonify({"error": "'num' parameter is required"}), 400
    try:
        n = int(num)
    except ValueError:
        return jsonify({"error": "'num' must be an integer"}), 400
    return jsonify({"num": n, "square": n ** 2})


@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello, {name}!"})


if __name__ == '__main__':
    app.run(debug=True)
