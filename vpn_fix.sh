#!/bin/bash

# VPN Kurulum ve Düzeltme Script'i
# Bu script VPN sorunlarını çözmek ve yeni VPN bağlantıları kurmak için kullanılır

echo "=== VPN Kurulum ve Düzeltme Aracı ==="
echo

# Gerekli paketleri kontrol et ve kur
install_vpn_tools() {
    echo "Gerekli VPN araçları kontrol ediliyor..."
    
    # Paket yöneticisini tespit et
    if command -v apt-get >/dev/null 2>&1; then
        PKG_MANAGER="apt-get"
    elif command -v yum >/dev/null 2>&1; then
        PKG_MANAGER="yum"
    elif command -v pacman >/dev/null 2>&1; then
        PKG_MANAGER="pacman"
    else
        echo "Paket yöneticisi bulunamadı!"
        return 1
    fi
    
    echo "Paket yöneticisi: $PKG_MANAGER"
    
    # OpenVPN kurulumu
    if ! command -v openvpn >/dev/null 2>&1; then
        echo "OpenVPN kuruluyor..."
        case $PKG_MANAGER in
            "apt-get")
                sudo apt-get update && sudo apt-get install -y openvpn
                ;;
            "yum")
                sudo yum install -y openvpn
                ;;
            "pacman")
                sudo pacman -S --noconfirm openvpn
                ;;
        esac
    else
        echo "OpenVPN zaten kurulu ✓"
    fi
    
    # WireGuard kurulumu
    if ! command -v wg >/dev/null 2>&1; then
        echo "WireGuard kuruluyor..."
        case $PKG_MANAGER in
            "apt-get")
                sudo apt-get install -y wireguard
                ;;
            "yum")
                sudo yum install -y wireguard-tools
                ;;
            "pacman")
                sudo pacman -S --noconfirm wireguard-tools
                ;;
        esac
    else
        echo "WireGuard zaten kurulu ✓"
    fi
    
    # Network araçları
    case $PKG_MANAGER in
        "apt-get")
            sudo apt-get install -y net-tools curl wget dig
            ;;
        "yum")
            sudo yum install -y net-tools curl wget bind-utils
            ;;
        "pacman")
            sudo pacman -S --noconfirm net-tools curl wget bind-tools
            ;;
    esac
}

# DNS ayarlarını düzelt
fix_dns() {
    echo "DNS ayarları düzeltiliyor..."
    
    # Güvenli DNS sunucuları
    cat << EOF | sudo tee /etc/resolv.conf
# VPN DNS ayarları
nameserver 1.1.1.1
nameserver 1.0.0.1
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
    
    echo "DNS ayarları güncellendi ✓"
}

# OpenVPN bağlantısını test et ve düzelt
fix_openvpn() {
    echo "OpenVPN bağlantısı kontrol ediliyor..."
    
    # OpenVPN süreçlerini öldür
    sudo pkill openvpn 2>/dev/null
    sleep 2
    
    # OpenVPN config dosyalarını ara
    config_files=$(find /etc/openvpn /home -name "*.ovpn" 2>/dev/null | head -5)
    
    if [ -n "$config_files" ]; then
        echo "Bulunan OpenVPN config dosyaları:"
        echo "$config_files"
        
        # İlk config dosyasını kullan
        first_config=$(echo "$config_files" | head -1)
        echo "Kullanılacak config: $first_config"
        
        # OpenVPN'i başlat
        echo "OpenVPN başlatılıyor..."
        sudo openvpn --config "$first_config" --daemon
        sleep 5
        
        # Bağlantıyı kontrol et
        if pgrep openvpn >/dev/null; then
            echo "OpenVPN başarıyla başlatıldı ✓"
        else
            echo "OpenVPN başlatılamadı ✗"
        fi
    else
        echo "OpenVPN config dosyası bulunamadı!"
        echo "Lütfen .ovpn dosyanızı /etc/openvpn/ klasörüne kopyalayın"
    fi
}

# WireGuard bağlantısını test et ve düzelt
fix_wireguard() {
    echo "WireGuard bağlantısı kontrol ediliyor..."
    
    # WireGuard interface'lerini kapat
    sudo wg-quick down wg0 2>/dev/null
    
    # WireGuard config dosyalarını ara
    wg_configs=$(find /etc/wireguard /home -name "*.conf" 2>/dev/null | head -5)
    
    if [ -n "$wg_configs" ]; then
        echo "Bulunan WireGuard config dosyaları:"
        echo "$wg_configs"
        
        # İlk config dosyasını kullan
        first_wg_config=$(echo "$wg_configs" | head -1)
        
        # Config dosyasını /etc/wireguard/'a kopyala
        sudo cp "$first_wg_config" /etc/wireguard/wg0.conf
        
        # WireGuard'ı başlat
        echo "WireGuard başlatılıyor..."
        sudo wg-quick up wg0
        
        # Bağlantıyı kontrol et
        if sudo wg show | grep -q interface; then
            echo "WireGuard başarıyla başlatıldı ✓"
        else
            echo "WireGuard başlatılamadı ✗"
        fi
    else
        echo "WireGuard config dosyası bulunamadı!"
        echo "Lütfen .conf dosyanızı /etc/wireguard/ klasörüne kopyalayın"
    fi
}

# Routing tablosunu düzelt
fix_routing() {
    echo "Routing tablosu düzeltiliyor..."
    
    # Varsayılan gateway'i VPN üzerinden yönlendir
    if command -v ip >/dev/null 2>&1; then
        # Mevcut default route'u sil
        sudo ip route del default 2>/dev/null
        
        # VPN interface'ini tespit et
        vpn_interface=$(ip addr show | grep -E "(tun|tap|wg)" | head -1 | cut -d: -f2 | tr -d ' ')
        
        if [ -n "$vpn_interface" ]; then
            # VPN üzerinden default route ekle
            vpn_gateway=$(ip route show dev "$vpn_interface" | grep -oP 'via \K[^ ]+' | head -1)
            if [ -n "$vpn_gateway" ]; then
                sudo ip route add default via "$vpn_gateway" dev "$vpn_interface"
                echo "Default route VPN üzerinden ayarlandı ✓"
            fi
        fi
    fi
}

# Kill switch aktifleştir
enable_kill_switch() {
    echo "Kill switch aktifleştiriliyor..."
    
    # Firewall kuralları ile sadece VPN trafiğine izin ver
    sudo iptables -F
    sudo iptables -P INPUT DROP
    sudo iptables -P FORWARD DROP
    sudo iptables -P OUTPUT DROP
    
    # Loopback'e izin ver
    sudo iptables -A INPUT -i lo -j ACCEPT
    sudo iptables -A OUTPUT -o lo -j ACCEPT
    
    # VPN interface'ine izin ver
    vpn_interface=$(ip addr show | grep -E "(tun|tap|wg)" | head -1 | cut -d: -f2 | tr -d ' ')
    if [ -n "$vpn_interface" ]; then
        sudo iptables -A INPUT -i "$vpn_interface" -j ACCEPT
        sudo iptables -A OUTPUT -o "$vpn_interface" -j ACCEPT
        echo "Kill switch aktifleştirildi (sadece $vpn_interface trafiğine izin veriliyor) ✓"
    else
        echo "VPN interface bulunamadı, kill switch ayarlanamadı ✗"
    fi
}

# IP değişimini test et
test_ip_change() {
    echo "IP değişimi test ediliyor..."
    
    old_ip=$(curl -s ifconfig.me 2>/dev/null)
    echo "Mevcut IP: $old_ip"
    
    sleep 3
    
    new_ip=$(curl -s ifconfig.me 2>/dev/null)
    echo "Yeni IP: $new_ip"
    
    if [ "$old_ip" != "$new_ip" ]; then
        echo "IP başarıyla değişti ✓"
    else
        echo "IP değişmedi, VPN çalışmıyor olabilir ✗"
    fi
    
    # IP bilgilerini detaylı göster
    echo "Detaylı IP bilgisi:"
    curl -s https://ipinfo.io/json | python3 -m json.tool 2>/dev/null || echo "IP detayları alınamadı"
}

# Otomatik VPN yeniden bağlantı
setup_auto_reconnect() {
    echo "Otomatik yeniden bağlantı ayarlanıyor..."
    
    # Cron job oluştur
    cron_entry="*/5 * * * * /workspace/vpn_monitor.sh"
    (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -
    
    # Monitoring script'i oluştur
    cat << 'EOF' > /workspace/vpn_monitor.sh
#!/bin/bash
# VPN bağlantısını kontrol et ve gerekirse yeniden başlat

# VPN interface'ini kontrol et
if ! ip addr show | grep -q -E "(tun|tap|wg)"; then
    echo "VPN interface bulunamadı, yeniden başlatılıyor..."
    
    # OpenVPN'i dene
    if [ -f /etc/openvpn/*.ovpn ]; then
        sudo systemctl restart openvpn
    fi
    
    # WireGuard'ı dene
    if [ -f /etc/wireguard/wg0.conf ]; then
        sudo wg-quick down wg0 2>/dev/null
        sudo wg-quick up wg0
    fi
fi
EOF
    
    chmod +x /workspace/vpn_monitor.sh
    echo "Otomatik yeniden bağlantı ayarlandı ✓"
}

# Ana menü
main_menu() {
    echo "VPN Düzeltme Seçenekleri:"
    echo "1) Gerekli araçları kur"
    echo "2) DNS ayarlarını düzelt"
    echo "3) OpenVPN'i düzelt"
    echo "4) WireGuard'ı düzelt"
    echo "5) Routing'i düzelt"
    echo "6) Kill switch aktifleştir"
    echo "7) IP değişimini test et"
    echo "8) Otomatik yeniden bağlantı kur"
    echo "9) Hepsini otomatik yap"
    echo "0) Çıkış"
    echo
    read -p "Seçiminizi yapın (0-9): " choice
    
    case $choice in
        1) install_vpn_tools ;;
        2) fix_dns ;;
        3) fix_openvpn ;;
        4) fix_wireguard ;;
        5) fix_routing ;;
        6) enable_kill_switch ;;
        7) test_ip_change ;;
        8) setup_auto_reconnect ;;
        9) 
            install_vpn_tools
            fix_dns
            fix_openvpn
            fix_wireguard
            fix_routing
            test_ip_change
            ;;
        0) echo "Çıkılıyor..."; exit 0 ;;
        *) echo "Geçersiz seçim!"; main_menu ;;
    esac
}

# Script'i root olarak çalıştır
if [ "$EUID" -ne 0 ]; then
    echo "Bu script root yetkileri gerektirir. Sudo ile çalıştırın:"
    echo "sudo $0"
    exit 1
fi

# Ana menüyü göster
main_menu