from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Geeta!"

@app.route('/name')
def home():
    name="Geeta"
    age=25
    return f"Hello {name}, you are {age} years old!"

@app.route('/list')
def show_students():
    students = ["geeta", "trupti", "payal", "rutu"]
    output = "<h3>Student List:</h3>"
    for s in students:
        output += f"{s}<br>"
    return output  # ✅ move this outside the for lo

@app.route('/add/<int:a>/<int:b>')
def add(a,b):
    result=a+b
    return f"the sum of {a} and {b} is {result}"

@app.route('/multiply/<int:a>/<int:b>')
def miltiply(a,b):
    result=a*b
    return result


@app.route('/cal/<int:num>')
def calc(num):
    square=num ** 2
    cube= num**3
    return f"for{num},square={square},cube={cube}"

@app.route('/age/<int:age>')
def check_age(age):
    if age>=18:
        return f"you are {age} year old =eligible to vote!"
    else:
        return f" you are {age} yerar old -not eligible to vote!"
  
@app.route('/reverse/<text>')
def reverse_text(text):
    reverse_text=text[::-1]
    return reverse_text


@app.route('/count/<word>')
def count_letters(word):
    count = len(word)
    return f"The number of letters in '{word}' is {count}"
    
def factorial(n):
    fact=1
    for i in range(1,n+1):
        fact*=i
    return fact

@app.route('/fact/<int:n>')
def fact_route(n):
    result=factorial(n)
    return f"the factorial of {n} is {result}"


if __name__ == '__main__':
    app.run(debug=True)




