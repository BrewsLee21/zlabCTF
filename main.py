from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html,")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/ctf")
def ctf():
    return render_template("ctf.html")

if __name__ == "__main__":
    app.run(debug=True)

