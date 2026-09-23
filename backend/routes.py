from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from ai_service import analyze_image
from database import (
    create_user,
    get_user,
    save_analysis,
    get_user_analyses,
    save_contact,
    get_contacts,
)
import os


main = Blueprint("main", __name__)


# =========================================================
# ANA SAYFA
# =========================================================

@main.route("/")
def home():
    return render_template(
        "index.html",
        user=session.get("user")
    )


# =========================================================
# LOGIN
# =========================================================

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


# =========================================================
# REGISTER
# =========================================================

@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        create_user(name, email, password)

        return redirect(url_for("main.login"))

    return render_template("register.html")


# =========================================================
# FOTOĞRAF YÜKLEME / AI ANALİZ
# =========================================================

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


# =========================================================
# FLASK DASHBOARD
# =========================================================

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


# =========================================================
# LOGOUT
# =========================================================

@main.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("main.login"))


# =========================================================
# API STATUS
# =========================================================

@main.route("/api/status")
def api_status():

    return jsonify({
        "project": "AgriBrain",
        "status": "running",
        "version": "1.0"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@main.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "database": "connected",
        "ai": "active"
    })


# =========================================================
# KVKK
# =========================================================

@main.route("/kvkk")
def kvkk():

    return render_template("kvkk.html")


# =========================================================
# PRIVACY
# =========================================================

@main.route("/privacy")
def privacy():

    return render_template("privacy.html")


# =========================================================
# WIX İLETİŞİM FORMU API
# =========================================================

@main.route("/api/iletisim", methods=["POST"])
def iletisim_ekle():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "Veri gönderilmedi."
            }), 400

        ad_soyad = data.get("adSoyad", "").strip()
        email = data.get("email", "").strip()
        mesaj = data.get("mesaj", "").strip()

        if not ad_soyad:
            return jsonify({
                "success": False,
                "message": "Ad soyad alanı zorunludur."
            }), 400

        if not email:
            return jsonify({
                "success": False,
                "message": "E-posta alanı zorunludur."
            }), 400

        if not mesaj:
            return jsonify({
                "success": False,
                "message": "Mesaj alanı zorunludur."
            }), 400

        # Sayfa kodu atlatilabilir, dogrulama burada da yapilir.
        # Veri artik print edilmiyor, veritabanina yaziliyor.
        yeni_id = save_contact(ad_soyad, email, mesaj)

        return jsonify({
            "success": True,
            "message": "Mesaj başarıyla alındı.",
            "data": {
                "id": yeni_id,
                "adSoyad": ad_soyad,
                "email": email,
                "mesaj": mesaj
            }
        }), 201

    except Exception as error:

        print("İletişim API hatası:", error)

        return jsonify({
            "success": False,
            "message": "Sunucu tarafında bir hata oluştu."
        }), 500


# =========================================================
# WIX DASHBOARD - KAYIT LISTESI
#
# KVKK: bu uc ad, e-posta ve mesaj dondurur, yani kisisel veridir.
# Su an herkese aciktir. Teslimden once Wix'te Dashboard sayfasi
# uye girisi arkasina alinmalidir.
# =========================================================

@main.route("/api/iletisim", methods=["GET"])
def iletisim_listesi():

    try:

        kayitlar = get_contacts()

        return jsonify({
            "success": True,
            "count": len(kayitlar),
            "data": kayitlar
        }), 200

    except Exception as error:

        print("İletişim listesi hatası:", error)

        return jsonify({
            "success": False,
            "message": "Kayıtlara şu an ulaşılamıyor."
        }), 500
