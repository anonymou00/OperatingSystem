#!/bin/bash

# Hızlı VPN Düzeltme Script'i (Root gerektirmez)
# VPN sorunlarını hızlıca tespit etmek ve geçici çözümler sunmak için

echo "=== Hızlı VPN Sorun Tespiti ve Çözümü ==="
echo

# Mevcut durumu kontrol et
echo "1. Mevcut IP ve bağlantı durumu:"
current_ip=$(curl -s ifconfig.me 2>/dev/null || echo "Alınamadı")
echo "   Mevcut IP: $current_ip"

# IP bilgilerini detaylı al
ip_info=$(curl -s https://ipinfo.io/json 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   Konum: $(echo "$ip_info" | grep -o '"city":"[^"]*' | cut -d'"' -f4), $(echo "$ip_info" | grep -o '"country":"[^"]*' | cut -d'"' -f4)"
    echo "   ISP: $(echo "$ip_info" | grep -o '"org":"[^"]*' | cut -d'"' -f4)"
else
    echo "   IP detayları alınamadı"
fi
echo

# VPN süreçlerini kontrol et
echo "2. VPN süreçleri:"
vpn_procs=$(ps aux | grep -E "(openvpn|wireguard|wg-quick)" | grep -v grep)
if [ -n "$vpn_procs" ]; then
    echo "   Aktif VPN süreçleri bulundu:"
    echo "$vpn_procs" | while read line; do echo "   $line"; done
else
    echo "   Aktif VPN süreci bulunamadı ⚠️"
fi
echo

# DNS kontrolü
echo "3. DNS durumu:"
dns_servers=$(cat /etc/resolv.conf | grep nameserver | cut -d' ' -f2)
echo "   Mevcut DNS sunucuları:"
echo "$dns_servers" | while read dns; do echo "   - $dns"; done

# DNS leak test
echo "   DNS leak testi:"
dns_leak=$(dig +short @1.1.1.1 whoami.akamai.net 2>/dev/null)
if [ -n "$dns_leak" ]; then
    echo "   DNS cevabı: $dns_leak"
else
    echo "   DNS test başarısız ⚠️"
fi
echo

# Network interface kontrolü
echo "4. Network interface'leri:"
if ls /sys/class/net/ | grep -E "(tun|tap|wg)" >/dev/null 2>&1; then
    echo "   VPN interface'leri:"
    ls /sys/class/net/ | grep -E "(tun|tap|wg)" | while read iface; do echo "   - $iface ✓"; done
else
    echo "   VPN interface bulunamadı ⚠️"
fi
echo

# Basit bağlantı testi
echo "5. Bağlantı testi:"
if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo "   İnternet bağlantısı: Çalışıyor ✓"
else
    echo "   İnternet bağlantısı: Çalışmıyor ✗"
fi

if ping -c 1 1.1.1.1 >/dev/null 2>&1; then
    echo "   DNS sunucusu erişimi: Çalışıyor ✓"
else
    echo "   DNS sunucusu erişimi: Çalışmıyor ✗"
fi
echo

# Yaygın sorunlar ve öneriler
echo "=== Tespit Edilen Sorunlar ve Öneriler ==="
echo

problems_found=false

# VPN süreci yok
if ! ps aux | grep -E "(openvpn|wireguard)" | grep -v grep >/dev/null; then
    echo "❌ SORUN: VPN süreci çalışmıyor"
    echo "   ÇÖZÜMLER:"
    echo "   - VPN uygulamanızı yeniden başlatın"
    echo "   - Bağlantıyı disconnect edip tekrar connect edin"
    echo "   - Farklı bir sunucu lokasyonu deneyin"
    echo
    problems_found=true
fi

# VPN interface yok
if ! ls /sys/class/net/ | grep -E "(tun|tap|wg)" >/dev/null 2>&1; then
    echo "❌ SORUN: VPN network interface bulunamadı"
    echo "   ÇÖZÜMLER:"
    echo "   - VPN bağlantınızı tamamen kapatıp yeniden açın"
    echo "   - Sistem yöneticisi olarak VPN'i çalıştırın"
    echo "   - VPN yazılımını yeniden yükleyin"
    echo
    problems_found=true
fi

# DNS leak kontrolü
if echo "$ip_info" | grep -q "Amazon\|Google\|Microsoft"; then
    echo "⚠️  UYARI: Bulut sunucu IP'si tespit edildi"
    echo "   BU NORMAL OLABİLİR eğer VPN sunucusu bulut sağlayıcısında barındırılıyorsa"
    echo
fi

# İnternet bağlantısı yok
if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo "❌ SORUN: İnternet bağlantısı yok"
    echo "   ÇÖZÜMLER:"
    echo "   - VPN kill switch'i devre dışı bırakın"
    echo "   - VPN'i kapatıp normal interneti test edin"
    echo "   - Modem/router'ınızı yeniden başlatın"
    echo
    problems_found=true
fi

if [ "$problems_found" = false ]; then
    echo "✅ Önemli bir sorun tespit edilmedi"
    echo "   VPN bağlantınız çalışıyor gibi görünüyor"
    echo
fi

# Önerilen test siteleri
echo "=== Kapsamlı Test Siteleri ==="
echo "Bu siteleri tarayıcınızda ziyaret ederek detaylı testler yapabilirsiniz:"
echo
echo "1. IP Leak Test:"
echo "   https://ipleak.net/"
echo
echo "2. DNS Leak Test:"
echo "   https://dnsleaktest.com/"
echo
echo "3. WebRTC Leak Test:"
echo "   https://browserleaks.com/webrtc"
echo
echo "4. Genel VPN Test:"
echo "   https://whatismyipaddress.com/"
echo

# Pratik çözümler
echo "=== Hızlı Çözüm Önerileri ==="
echo
echo "A) VPN yeniden bağlantısı için:"
echo "   1. VPN uygulamanızı tamamen kapatın"
echo "   2. 10 saniye bekleyin"
echo "   3. VPN'i yeniden açıp farklı bir sunucu seçin"
echo "   4. Bağlantıyı test edin"
echo
echo "B) DNS ayarlarını manuel değiştirmek için:"
echo "   1. Network ayarlarınızı açın"
echo "   2. DNS sunucularını manuel olarak ayarlayın:"
echo "      Primary: 1.1.1.1"
echo "      Secondary: 1.0.0.1"
echo
echo "C) VPN yazılımı sorunları için:"
echo "   1. VPN uygulamasını tamamen silin"
echo "   2. Sistemi yeniden başlatın"
echo "   3. VPN yazılımını en son sürümle yeniden yükleyin"
echo

echo "=== IP Değişim Takibi ==="
echo "IP değişimini gerçek zamanlı takip etmek için bu komutu kullanın:"
echo "watch -n 5 'curl -s ifconfig.me'"
echo
echo "Ctrl+C ile durdurun."