#!/bin/bash

# VPN Master Control GUI Başlatma Script'i
# Karmaşık sistem geneli VPN kontrolü için GUI

echo "🔐 VPN MASTER CONTROL GUI başlatılıyor..."
echo "======================================"

# Python3 kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Yükleniyor..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-tk
fi

# Gerekli Python paketlerini yükle
echo "📦 Gerekli paketler kontrol ediliyor..."
pip3 install --user requests psutil

# GUI uygulamasını başlat
echo "🚀 VPN Master Control GUI başlatılıyor..."
echo "💡 Bu uygulama:"
echo "   ✅ Sistem geneli VPN kontrolü"
echo "   ✅ Tarayıcı seviyesinde koruma"
echo "   ✅ Gerçek zamanlı IP takibi"
echo "   ✅ DNS leak koruması"
echo "   ✅ WebRTC leak önleme"
echo "   ✅ Kill switch yönetimi"
echo "   ✅ Otomatik VPN düzeltme"
echo ""

# Gerekli izinleri ayarla
chmod +x vpn_manager_gui.py

# GUI'yi başlat
python3 vpn_manager_gui.py

echo "👋 VPN Master Control kapatıldı."