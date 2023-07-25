from web.app.routers.main import main
from flask.templating import render_template


@main.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html")
