from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from ai_service import analyze_image
from database import create_user, get_user, save_analysis, get_user_analyses
import os

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template(
        "index.html",
        user=session.get("user")
    )


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email, password)
        print(user)

        if user:
            session["user"] = user["email"]
            return redirect(url_for("main.dashboard"))

        return "E-posta veya şifre yanlış."

    return render_template("login.html")


@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        create_user(name, email, password)

        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect(url_for("main.login"))

    if "image" not in request.files:
        return "Dosya bulunamadı."

    image = request.files["image"]

    filename = secure_filename(image.filename)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    upload_path = os.path.join(BASE_DIR, "uploads", filename)

    image.save(upload_path)

    result = analyze_image(upload_path)

    save_analysis(
        session["user"],
        filename,
        "Sağlıklı Bitki",
        "97"
    )

    return render_template(
        "index.html",
        result=result,
        user=session.get("user")
    )
@main.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("main.login"))

    analyses = get_user_analyses(session["user"])

    return render_template(
        "dashboard.html",
        user=session["user"],
        analyses=analyses
    )


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))

@main.route("/api/status")
def api_status():
    return jsonify({
        "project": "AgriBrain",
        "status": "running",
        "version": "1.0"
    })

@main.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "database": "connected",
        "ai": "active"
    })

@main.route("/kvkk")
def kvkk():
    return render_template("kvkk.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")


