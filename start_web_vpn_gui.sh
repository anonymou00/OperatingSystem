#!/bin/bash

# VPN Master Control Web GUI Başlatma Script'i
# Karmaşık web tabanlı sistem geneli VPN kontrolü

echo "🔐 VPN MASTER CONTROL WEB GUI başlatılıyor..."
echo "=============================================="

# Python3 kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Yükleniyor..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Gerekli Python paketlerini yükle
echo "📦 Gerekli paketler kontrol ediliyor..."
pip3 install --user requests psutil

# Port kontrolü
PORT=8888
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️ Port $PORT zaten kullanımda! Kapatılıyor..."
    sudo kill -9 $(lsof -t -i:$PORT) 2>/dev/null
    sleep 2
fi

# Gerekli izinleri ayarla
chmod +x vpn_web_gui.py

echo "🚀 VPN Master Control Web GUI başlatılıyor..."
echo "💡 Bu WEB uygulama:"
echo "   ✅ Sistem geneli VPN kontrolü"
echo "   ✅ Tarayıcı seviyesinde koruma"
echo "   ✅ Gerçek zamanlı IP takibi"
echo "   ✅ DNS leak koruması"
echo "   ✅ WebRTC leak önleme"
echo "   ✅ Kill switch yönetimi"
echo "   ✅ Otomatik VPN düzeltme"
echo "   ✅ Network analiz araçları"
echo "   ✅ Karmaşık web arayüzü"
echo "   ✅ Responsive mobile destek"
echo ""
echo "🌐 Web arayüz: http://localhost:8888"
echo "🔥 Tarayıcınız otomatik açılacak..."
echo ""

# Web GUI'yi başlat
python3 vpn_web_gui.py

echo "👋 VPN Master Control Web GUI kapatıldı."