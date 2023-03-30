"""Module from main subpackage with routes for common pages"""

__docformat__ = "google"

from flask import render_template, url_for, Blueprint


main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Return the index page.

    Returns:
        Rendered template with the about page.
    """
    return render_template("about.html", title="LambdaTest")


@main.route("/about")
def about():
    """Return the about page.

    Returns:
        Rendered template with the about page.
    """
    return render_template("about.html", title="About")
