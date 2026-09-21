import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Wix'ten gelen isteklere izin verir

@app.route('/', methods=['GET'])
def home():
    return jsonify({'durum': 'aktif', 'sirket': 'AgriBrain'}), 200

@app.route('/api/sohbet', methods=['POST'])
def sohbet():
    data = request.get_json() or {}
    mesaj = data.get('mesaj', '').strip()

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj boş olamaz.'}), 400

    msg_lower = mesaj.lower()

    # Chatbot Yanıt Mekanizması
    if "agrigrow" in msg_lower:
        cevap = "AgriGrow, topraksız (hidroponik) akıllı tarım ve otomasyon kitimizdir. Otomatik sulama ve ışık yönetimi sağlar."
    elif "ürün" in msg_lower or "urun" in msg_lower:
        cevap = "AgriBrain ürün portföyünde AgriGrow Hidroponik Tarım Kiti, IoT Sensörler ve Mobil Takip Yazılımları yer almaktadır."
    elif "hakkın" in msg_lower or "hakkin" in msg_lower or "agribrain" in msg_lower:
        cevap = "AgriBrain; yapay zekâ ve IoT teknolojilerini tarımla buluşturan yenilikçi bir teknoloji şirketidir."
    elif "iletişim" in msg_lower or "iletisim" in msg_lower:
        cevap = "Bizimle sitemizdeki İletişim bölümünden veya info@agribrain.com adresinden bağlantı kurabilirsiniz."
    elif "sss" in msg_lower or "soru" in msg_lower:
        cevap = "AgriGrow sistemleri ev içi kullanıma ve seralara tam uyumludur. %90'a varan su tasarrufu sağlar."
    else:
        cevap = f"AgriBrain Asistanı: '{mesaj}' hakkındaki sorunuzu aldım. AgriGrow veya akıllı tarım teknolojilerimiz hakkında size nasıl yardımcı olabilirim?"

    return jsonify({'basari': True, 'cevap': cevap}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)