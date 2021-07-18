from flask import Flask, session, render_template, request, redirect, url_for, flash
from secrets import token_urlsafe
from server.loopback_check import Loopback
from settings.load_settings import LoadSettings
from socket import gethostname, gethostbyname

app = Flask(__name__)


class Server:
    def __init__(self):
        self.username = None
        self.password = None
        self.version = None
        self.ip = None
        self.port = None
        self.loopback = Loopback()
        self.load_server()

    def load_server(self):
        """
        This will load all the settings for the Server from the settings.dat. If no values are stored, the
        default value will be used
        :return: None
        """
        loading = LoadSettings()
        loading.open_settings("Server", "username", "admin")
        self.username = loading.load_settings()
        loading.open_settings("Server", "password", "password")
        self.password = loading.load_settings()
        loading.open_settings("Server", "ip", gethostbyname(gethostname()))
        self.ip = loading.load_settings()
        loading.open_settings("Server", "port", 4000)
        self.port = loading.load_settings()
        loading.open_settings("Server", "version", "v0.0.0e")
        self.version = loading.load_settings()


server_vars = Server()


def logged_in():
    if session.get("logged_in"):
        return True
    else:
        return False


@app.route("/")
@app.route("/home")
def home():
    if logged_in() is True:
        return render_template("home.html")
    else:
        return render_template("login.html")


@app.route("/settings")
def settings():
    if logged_in() is True:
        return render_template("settings.html")
    else:
        return render_template("login.html")


@app.route("/about")
def about():
    if logged_in() is True:
        return render_template("about.html")
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if request.form["username"] == server_vars.username and request.form["password"] == server_vars.password:
        session['logged_in'] = True
        flash(f"Login for {request.form['username']} was successful!", "success")
        return redirect(url_for("home"))
    else:
        flash("Login failed.", "danger")
        return render_template("login.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash("Logout successful!", "success")
    return render_template("login.html")

def main():
    app.config["SECRET_KEY"] = token_urlsafe(16)
    app.run(debug=True, use_reloader=True, host=server_vars.ip, port=server_vars.port)


if __name__ == "__main__":
    main()
