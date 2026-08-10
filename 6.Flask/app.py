from flask import Flask, render_template, request, redirect, url_for, jsonify

#creates a simple flask app
app = Flask(__name__)

#app routing
@app.route("/", methods=["GET"])
def home():
    return "Welcome to home"

#app routing
@app.route("/profile", methods=["GET"])
def profile():
    return "Welcome to the profile"

#app routing with parameter & rule
@app.route('/success/<int:score>')
def success(score):
    return "Total marks scored: " + str(score)

#app routing with parameter
@app.route('/profile/<data>')
def user_profile(data):
    return "Hello my name is " + data

#Rendering html page
@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        physics = float(request.form["physics"])
        chemistry = float(request.form["chemistry"])
        maths = float(request.form["maths"])
        average_marks = (physics + chemistry + maths)/3
        
        return render_template('form.html', score=average_marks)
    

#Creating API
@app.route('/api', methods=["POST"])
def calculate_sum():
    data=request.get_json()
    a = float(dict(data)['a'])
    b = float(dict(data)['b'])
    return jsonify(a + b)

if  __name__ == "__main__":
    app.run(debug=True)