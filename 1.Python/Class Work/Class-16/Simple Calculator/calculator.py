from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def cal_page():
    return render_template("index.html")


@app.route("/math", methods= ['POST'])
def calculator_test():
    ops = request.form['operation']
    first_num = int(request.form.get("num1"))
    second_num = int(request.form.get("num2"))

    if ops == "add":
        return f"addition of {first_num} and {second_num} is {first_num + second_num}"
    elif ops == "subtract":
        return f"subtraction of {first_num} and {second_num} is {first_num - second_num}"
    elif ops == "multiply":
        return f"multiplication of {first_num} and {second_num} is {first_num * second_num}"
    elif ops == "divide":
        return f"divition of {first_num} and {second_num} is {first_num / second_num}"
    


if __name__ == "__main__":
    app.run(host="0.0.0.0")