# VPN Sorun Çözüm Rehberi

## Problem
VPN bağlı görünüyor ama IP adresiniz değişmedi ve IP bulucu siteler gerçek IP'nizi gösteriyor. Bu durum VPN'inizin제대로 çalışmadığını gösterir.

## Tespit Edilen Sorunlar
Analiz sonucunda şu sorunlar tespit edildi:
- ❌ VPN süreci çalışmıyor
- ❌ VPN network interface bulunamadı  
- ❌ DNS leak var
- ⚠️ İnternet bağlantısı sorunları

## Çözüm Script'leri

### 1. Hızlı Tanı ve Çözüm
```bash
./quick_vpn_fix.sh
```
Bu script VPN sorunlarınızı hızlıca tespit eder ve çözüm önerileri sunar.

### 2. Kapsamlı VPN Düzeltme (Root gerekli)
```bash
sudo ./vpn_fix.sh
```
Bu script VPN'inizi tamamen düzeltmek için kapsamlı araçlar sunar.

### 3. Detaylı VPN Analizi
```bash
./vpn_troubleshoot.sh
```
Bu script VPN bağlantınızı detaylı analiz eder.

## Hızlı Çözümler

### A) Acil VPN Düzeltme
1. VPN uygulamanızı tamamen kapatın
2. 10 saniye bekleyin
3. Farklı bir sunucu lokasyonu seçin
4. VPN'i yeniden açın
5. IP değişimini test edin: `curl ifconfig.me`

### B) DNS Leak Düzeltme
DNS ayarlarınızı manuel olarak değiştirin:
- Primary DNS: `1.1.1.1`
- Secondary DNS: `1.0.0.1`

### C) Gerçek Zamanlı IP Takibi
```bash
watch -n 5 'curl -s ifconfig.me'
```

## Test Siteleri
Bu siteleri tarayıcınızda ziyaret ederek VPN'inizi test edin:

1. **IP Leak Test**: https://ipleak.net/
2. **DNS Leak Test**: https://dnsleaktest.com/
3. **WebRTC Leak Test**: https://browserleaks.com/webrtc
4. **Genel VPN Test**: https://whatismyipaddress.com/

## Yaygın VPN Sorunları ve Çözümleri

### 1. VPN Bağlı Ama IP Değişmedi
**Nedenler:**
- VPN kill switch aktif
- DNS leak var
- WebRTC leak
- VPN süreci düzgün çalışmıyor

**Çözümler:**
- VPN'i tamamen kapatıp açın
- Farklı sunucu deneyin
- DNS ayarlarını manuel yapın
- Tarayıcıda WebRTC'yi devre dışı bırakın

### 2. DNS Leak Sorunu
**Nedir?** DNS sorgularınız VPN üzerinden geçmiyor.

**Çözüm:**
```bash
# DNS'i manuel olarak değiştirin
echo 'nameserver 1.1.1.1' | sudo tee /etc/resolv.conf
echo 'nameserver 1.0.0.1' | sudo tee -a /etc/resolv.conf
```

### 3. WebRTC IP Leak
**Nedir?** Tarayıcınız WebRTC ile gerçek IP'nizi sızdırıyor.

**Çözüm:**
- Chrome: `chrome://flags/#enable-webrtc-hide-local-ips-with-mdns`
- Firefox: `media.peerconnection.enabled = false` (about:config)

### 4. VPN Bağlantısı Sürekli Düşüyor
**Çözümler:**
- Auto-reconnect özelliğini aktifleştirin
- Farklı VPN protokolü deneyin (OpenVPN → WireGuard)
- İnternet bağlantınızı kontrol edin

## VPN Türleri ve Ayarları

### OpenVPN
- Config dosyası: `.ovpn`
- Konum: `/etc/openvpn/`
- Başlatma: `sudo openvpn --config dosya.ovpn`

### WireGuard
- Config dosyası: `.conf`
- Konum: `/etc/wireguard/`
- Başlatma: `sudo wg-quick up wg0`

## Güvenlik İpuçları

1. **VPN'i test edin**: Her bağlantıdan sonra IP'nizi kontrol edin
2. **Kill switch kullanın**: VPN düştüğünde internet bağlantısını kesin
3. **DNS leak test yapın**: Düzenli olarak DNS sızıntısı kontrol edin
4. **Güvenilir VPN kullanın**: Ücretsiz VPN'lerden kaçının
5. **Logları kontrol edin**: VPN sağlayıcısının log tutmadığından emin olun

## Sorun Devam Ederse

1. VPN sağlayıcınızla iletişime geçin
2. Farklı bir VPN protokolü deneyin
3. VPN yazılımını yeniden yükleyin
4. İşletim sisteminizi güncelleyin
5. Firewall ayarlarınızı kontrol edin

## Dosyalar
- `quick_vpn_fix.sh` - Hızlı sorun tespiti
- `vpn_fix.sh` - Kapsamlı VPN düzeltme
- `vpn_troubleshoot.sh` - Detaylı analiz
- `vpn_monitor.sh` - Otomatik bağlantı kontrolü

Herhangi bir sorunuz olursa script'leri çalıştırın ve çıktıları kontrol edin.