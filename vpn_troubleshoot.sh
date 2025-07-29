#!/bin/bash

# VPN Troubleshooting Script
# Bu script VPN bağlantı sorunlarını tespit etmek ve çözmek için kullanılır

echo "=== VPN Bağlantı Durumu Kontrolü ==="
echo

# 1. Mevcut IP adresini kontrol et
echo "1. Mevcut IP Adresi:"
echo "External IP: $(curl -s ifconfig.me 2>/dev/null || echo 'Alınamadı')"
echo "IP Detayları:"
curl -s https://ipinfo.io/json 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "IP detayları alınamadı"
echo

# 2. VPN süreçlerini kontrol et
echo "2. VPN Süreçleri:"
vpn_processes=$(ps aux | grep -i vpn | grep -v grep)
if [ -n "$vpn_processes" ]; then
    echo "$vpn_processes"
else
    echo "Aktif VPN süreci bulunamadı"
fi
echo

# 3. Network interface'lerini kontrol et
echo "3. Network Interface'leri:"
if command -v ip >/dev/null 2>&1; then
    ip addr show | grep -E "(tun|tap|vpn)" || echo "VPN interface bulunamadı"
elif command -v ifconfig >/dev/null 2>&1; then
    ifconfig | grep -E "(tun|tap|vpn)" || echo "VPN interface bulunamadı"
else
    ls /sys/class/net/ | grep -E "(tun|tap|vpn)" || echo "VPN interface bulunamadı"
fi
echo

# 4. DNS ayarlarını kontrol et
echo "4. DNS Ayarları:"
echo "Mevcut DNS sunucuları:"
cat /etc/resolv.conf | grep nameserver
echo

# 5. DNS leak test
echo "5. DNS Leak Testi:"
dns_servers=$(dig +short @1.1.1.1 whoami.akamai.net 2>/dev/null || echo "DNS test başarısız")
echo "DNS cevabı: $dns_servers"
echo

# 6. Routing tablosunu kontrol et
echo "6. Routing Tablosu:"
if command -v ip >/dev/null 2>&1; then
    ip route | head -10
elif command -v route >/dev/null 2>&1; then
    route -n | head -10
else
    echo "Routing bilgisi /proc/net/route'dan:"
    cat /proc/net/route 2>/dev/null | head -5
fi
echo

# 7. VPN bağlantı durumunu test et
echo "7. Bağlantı Testi:"
echo "Google'a ping testi:"
ping -c 3 8.8.8.8 2>/dev/null | tail -2 || echo "Ping başarısız"
echo

# 8. Yaygın VPN sorunları ve çözümleri
echo "=== Yaygın VPN Sorunları ve Çözümleri ==="
echo
echo "A) VPN bağlı görünüyor ama IP değişmedi:"
echo "   - VPN servisini yeniden başlatın"
echo "   - Kill switch özelliğini kontrol edin"
echo "   - DNS ayarlarını manuel olarak değiştirin"
echo
echo "B) DNS Leak var:"
echo "   - /etc/resolv.conf dosyasını düzenleyin"
echo "   - VPN sağlayıcısının DNS sunucularını kullanın"
echo
echo "C) VPN bağlantısı düşüyor:"
echo "   - Auto-reconnect özelliğini aktifleştirin"
echo "   - Farklı VPN protokolü deneyin (OpenVPN, WireGuard)"
echo

# 9. Önerilen komutlar
echo "=== Önerilen Çözüm Komutları ==="
echo
echo "VPN'i yeniden başlatmak için:"
echo "sudo systemctl restart openvpn"
echo "# veya"
echo "sudo pkill openvpn && sudo openvpn --config /path/to/config.ovpn"
echo
echo "DNS'i manuel olarak değiştirmek için:"
echo "echo 'nameserver 1.1.1.1' | sudo tee /etc/resolv.conf"
echo "echo 'nameserver 1.0.0.1' >> /etc/resolv.conf"
echo
echo "IP değişimini test etmek için:"
echo "watch -n 5 'curl -s ifconfig.me'"
echo

# 10. Güvenlik kontrolü
echo "=== Güvenlik Kontrolü ==="
echo
echo "WebRTC leak testi için tarayıcıda şu siteyi ziyaret edin:"
echo "https://browserleaks.com/webrtc"
echo
echo "Kapsamlı IP leak testi için:"
echo "https://ipleak.net/"
echo

echo "=== Script tamamlandı ==="
echo "VPN sorunları devam ediyorsa, VPN sağlayıcınızla iletişime geçin."