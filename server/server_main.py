from flask import Flask, session, render_template, request, redirect, url_for, flash
from secrets import token_urlsafe
from server.loopback_check import Loopback
from settings.load_settings import LoadSettings
from socket import gethostname, gethostbyname
from artnet.artnet_socket import UDP_PORT
from sacn.sacn_socket import ACN_SDT_MULTICAST_PORT

app = Flask(__name__)


class Server:
    def __init__(self):
        self.username = None
        self.password = None
        self.version = None
        self.ip = None
        self.port = None
        self.loopback = Loopback()
        self.sacndict = {}
        self.artnetdict = {}
        self.sacn_to_artnet = False
        self.artnet_to_sacn = False
        self.merge_sacn = True
        self.merge_artnet = False
        self.artnet_port = None
        self.sacn_port = None
        self.per_channel_priority = True
        self.load_server()
        self.load_artnet()
        self.load_sacn()

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

    def load_sacn(self):
        loading = LoadSettings()
        loading.open_settings("sACN", "sacndict", {})
        self.sacndict = loading.load_settings()
        loading.open_settings("sACN", "sacn_to_artnet", False)
        self.sacn_to_artnet = loading.load_settings()
        loading.open_settings("sACN", "merge_sacn", True)
        self.merge_sacn = loading.load_settings()
        loading.open_settings("sACN", "per_channel_priority", True)
        self.per_channel_priority = loading.load_settings()
        loading.open_settings("sACN", "port", ACN_SDT_MULTICAST_PORT)
        self.artnet_port = loading.load_settings()


    def load_artnet(self):
        loading = LoadSettings()
        loading.open_settings("Art-Net", "artnetdict", {})
        self.artnetdict = loading.load_settings()
        loading.open_settings("sACN", "artnet_to_sacn", False)
        self.artnet_to_sacn = loading.load_settings()
        loading.open_settings("sACN", "merge_artnet", False)
        self.merge_artnet = loading.load_settings()
        loading.open_settings("Art-Net", "port", UDP_PORT)
        self.artnet_port = loading.load_settings()


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
        server_vars.load_sacn()
        return render_template("home.html", sacndict=server_vars.sacndict, artnetdict=server_vars.artnetdict,
                               artnet_to_sacn=server_vars.artnet_to_sacn, sacn_to_artnet=server_vars.sacn_to_artnet)
    else:
        return render_template("login.html")


@app.route("/settings")
def settings():
    if logged_in() is True:
        return render_template("settings.html", merge_sacn=server_vars.merge_sacn, merge_artnet=server_vars.merge_sacn,
                               version=server_vars.version, ip=server_vars.ip, server_port=server_vars.port,
                               artnet_port=server_vars.artnet_port, sacn_port=server_vars.sacn_port)
    else:
        return render_template("login.html")


@app.route("/about")
def about():
    if logged_in() is True:
        return render_template("about.html", version=server_vars.version)
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
    flash("Logout successful!", "info")
    return render_template("login.html")


def main():
    app.config["SECRET_KEY"] = token_urlsafe(16)
    app.run(debug=True, use_reloader=True, host=server_vars.ip, port=server_vars.port)


if __name__ == "__main__":
    main()
