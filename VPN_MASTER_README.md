# 🔐 VPN MASTER CONTROL SYSTEM

## Gelişmiş VPN Yönetim ve Güvenlik Sistemi

Bu karmaşık sistem, VPN bağlantınızı her açıdan kontrol etmek, tarayıcı seviyesinde koruma sağlamak ve sistem genelinde güvenlik sağlamak için tasarlanmış profesyonel bir araçtır.

## 🚀 ÖZELLIKLER

### ✅ Sistem Geneli VPN Kontrolü
- **Otomatik VPN algılama** ve yönetimi
- **OpenVPN ve WireGuard** desteği
- **Kill Switch** teknolojisi
- **DNS Leak** koruması
- **Real-time IP monitoring**

### ✅ Tarayıcı Seviyesinde Koruma
- **Chrome/Firefox proxy** ayarları
- **WebRTC leak** önleme
- **Browser fingerprint** koruması
- **Automatic proxy injection**

### ✅ Gelişmiş Güvenlik Özellikleri
- **Emergency block** sistemi
- **Network interface** analizi
- **Port scanning** koruması
- **Bandwidth monitoring**
- **Route manipulation**

### ✅ Karmaşık Web Arayüzü
- **Responsive design** (mobil uyumlu)
- **Real-time dashboard**
- **Interactive controls**
- **Advanced logging system**
- **Multi-tab interface**

## 📁 DOSYA YAPISI

```
workspace/
├── vpn_web_gui.py           # Ana web GUI uygulaması
├── start_web_vpn_gui.sh     # Web GUI başlatma script'i
├── vpn_manager_gui.py       # Desktop GUI (tkinter)
├── start_vpn_gui.sh         # Desktop GUI başlatma script'i
├── vpn_fix.sh               # Kapsamlı VPN düzeltme araçları
├── vpn_troubleshoot.sh      # Detaylı analiz araçları
├── quick_vpn_fix.sh         # Hızlı tanı ve çözüm
├── requirements.txt         # Python bağımlılıkları
└── VPN_SORUN_COZUM.md      # Detaylı sorun çözüm rehberi
```

## 🚀 HIZLI BAŞLATMA

### Web Tabanlı GUI (ÖNERİLEN)
```bash
./start_web_vpn_gui.sh
```
- **Web arayüz**: http://localhost:8888
- **Otomatik tarayıcı açılımı**
- **Mobile responsive**
- **Advanced features**

### Desktop GUI (tkinter gerekli)
```bash
./start_vpn_gui.sh
```

### Komut Satırı Araçları
```bash
# Hızlı tanı
./quick_vpn_fix.sh

# Kapsamlı düzeltme
sudo ./vpn_fix.sh

# Detaylı analiz
./vpn_troubleshoot.sh
```

## 🔧 KURULUM

### Otomatik Kurulum
Script'ler gerekli bağımlılıkları otomatik yükler:
```bash
chmod +x *.sh
./start_web_vpn_gui.sh
```

### Manuel Kurulum
```bash
# Python paketleri
pip3 install --user requests psutil

# VPN araçları
sudo apt-get install openvpn wireguard-tools

# Network araçları
sudo apt-get install net-tools curl wget dnsutils
```

## 🌐 WEB ARAYÜZÜ KULLANIMI

### Ana Panel
- **VPN Durumu**: Real-time bağlantı izleme
- **IP Bilgileri**: Mevcut IP ve lokasyon
- **DNS Durumu**: Leak kontrolü
- **Browser Koruması**: Proxy durumu

### Hızlı Kontroller
- 🔄 **VPN RESTART**: VPN'i yeniden başlat
- 🛠️ **AUTO FIX**: Otomatik sorun giderme
- 🌐 **DNS FIX**: DNS ayarlarını düzelt
- 🔒 **KILL SWITCH**: Acil trafik kesme
- 🌍 **BROWSER PROXY**: Tarayıcı proxy'si
- 🚫 **CLEAR PROXY**: Proxy ayarlarını temizle

### Gelişmiş Sekmeler

#### 📋 LOGLAR
- Real-time sistem logları
- Renk kodlu mesajlar
- Otomatik scroll
- Log temizleme

#### 🔍 TESTLER
- **IP Analizi**: Detaylı IP inceleme
- **DNS Leak Test**: DNS sızıntı kontrolü
- **Hız Testi**: Bandwidth ölçümü
- **WebRTC Test**: Tarayıcı sızıntı kontrolü

#### 🌍 BROWSER
- **Chrome Proxy**: Chrome proxy ayarları
- **Firefox Proxy**: Firefox proxy ayarları
- **WebRTC Kapatma**: WebRTC devre dışı
- **Acil Blok**: Tüm trafiği durdur
- **Config Upload**: VPN dosyası yükleme

#### 📊 NETWORK
- **Network Scan**: Interface analizi
- **Port Scan**: Açık port kontrolü
- **Route Analiz**: Routing tablosu
- **Bandwidth Test**: Hız ölçümü

## 🤖 OTOMASYON ÖZELLİKLERİ

### Sürekli İzleme
- 5 saniyede bir durum kontrolü
- VPN kopma algılama
- IP değişim takibi
- DNS leak izleme

### Otomatik Düzeltme
- VPN koptuğunda otomatik restart
- DNS ayarlarını otomatik düzeltme
- Kill switch otomatik aktifleştirme
- Browser proxy otomatik ayarlama

## 🔒 GÜVENLİK ÖZELLİKLERİ

### Kill Switch
```bash
# Manuel aktifleştirme
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP
# VPN interface hariç tüm trafik kesilir
```

### DNS Koruma
```bash
# Güvenli DNS sunucuları
1.1.1.1    # Cloudflare
1.0.0.1    # Cloudflare Secondary
8.8.8.8    # Google
8.8.4.4    # Google Secondary
```

### Browser Koruma
- **Proxy injection**: Tüm trafik VPN üzerinden
- **WebRTC blocking**: IP sızıntısı önleme
- **DNS over HTTPS**: Şifreli DNS sorguları

## 🚨 ACİL DURUM PROSEDÜRLERİ

### VPN Tamamen Koptu
1. **Acil Blok** butonuna bas
2. **Auto Fix** çalıştır
3. Farklı server dene
4. VPN yazılımını yeniden başlat

### IP Sızıntısı Tespit Edildi
1. **Kill Switch** aktifleştir
2. **DNS Fix** uygula
3. **Browser Proxy** ayarla
4. **WebRTC** kapat

### İnternet Bağlantısı Yok
1. **Kill Switch** devre dışı bırak
2. VPN'i kapat
3. Normal bağlantıyı test et
4. VPN'i farklı ayarlarla başlat

## 🔍 SORUN GİDERME

### Yaygın Problemler

#### VPN Bağlı Ama IP Değişmedi
```bash
# Kontrol edilecekler:
- VPN süreci çalışıyor mu?
- Network interface aktif mi?
- Routing doğru mu?
- DNS leak var mı?
```

#### Browser'da Leak Var
```bash
# Çözümler:
- WebRTC'yi kapat
- Proxy ayarlarını kontrol et
- DNS ayarlarını güncelle
- Browser'ı yeniden başlat
```

### Log Analizi
```bash
# Sistem logları
tail -f /var/log/openvpn.log
journalctl -u openvpn@client

# Network durumu
ip addr show
ip route show
iptables -L
```

## 📊 PERFORMANS İZLEME

### Real-time Metrikler
- **Ping**: Bağlantı gecikmesi
- **Speed**: Download hızı
- **Uptime**: Bağlantı süresi
- **Data Transfer**: Veri miktarı

### Bandwidth Testing
```bash
# Manual test
curl -o /dev/null -s -w "%{speed_download}\n" http://speedtest.ftp.otenet.gr/files/test10Mb.db
```

## 🌐 DESTEKLENEN VPN TİPLERİ

### OpenVPN
- **Config**: `.ovpn` dosyaları
- **Protokol**: UDP/TCP
- **Şifreleme**: AES-256
- **Lokasyon**: `/etc/openvpn/`

### WireGuard
- **Config**: `.conf` dosyaları
- **Protokol**: UDP
- **Şifreleme**: ChaCha20
- **Lokasyon**: `/etc/wireguard/`

### Ticari VPN'ler
- **NordVPN**: Otomatik algılama
- **ExpressVPN**: Config import
- **Surfshark**: Manual ayar
- **Diğerleri**: Generic OpenVPN

## 📱 MOBİL DESTEK

Web arayüzü tam responsive:
- **Phone**: Optimize edilmiş layout
- **Tablet**: Grid düzeni
- **Desktop**: Full feature set

## 🔧 GELİŞMİŞ AYARLAR

### Custom DNS
```bash
# Özel DNS sunucuları
nameserver 9.9.9.9      # Quad9
nameserver 208.67.222.222 # OpenDNS
```

### Firewall Rules
```bash
# Özel iptables kuralları
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p udp --dport 1194 -j ACCEPT
```

### Routing Manipulation
```bash
# Özel routing
ip route add 0.0.0.0/1 via VPN_GATEWAY
ip route add 128.0.0.0/1 via VPN_GATEWAY
```

## 🆘 DESTEK VE YARDIM

### Test Siteleri
- **IP Leak**: https://ipleak.net/
- **DNS Leak**: https://dnsleaktest.com/
- **WebRTC**: https://browserleaks.com/webrtc
- **Speed Test**: https://speedtest.net/

### Useful Commands
```bash
# VPN durumu
systemctl status openvpn@client
wg show

# Network debugging
netstat -rn
ss -tulpn
nslookup google.com
```

## 📝 LİSANS VE SORUMLULUK

Bu araç eğitim amaçlı geliştirilmiştir. Kullanıcılar:
- Yerel yasalara uymalı
- VPN sağlayıcı ToS'a uymalı  
- Güvenlik için kendi sorumluluğunda kullanmalı

## 🔄 GÜNCELLEMELER

Düzenli olarak kontrol edin:
- Security patches
- VPN protocol updates
- Browser compatibility
- Feature improvements

---

**🔐 VPN Master Control System - Professional VPN Management Solution**

*Güvenli ve özel internete giden yolunuz!*