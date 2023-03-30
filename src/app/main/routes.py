from flask import render_template, url_for, Blueprint


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("about.html", title="LambdaTest")


@main.route("/about")
def about():
    return render_template("about.html", title="About")
