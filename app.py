from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home_page():
    list = ["","Patient1", "Patient2", "Patient3"]

    return render_template("home.html", patients=list)

if __name__ == '__main__':
    app.run()
