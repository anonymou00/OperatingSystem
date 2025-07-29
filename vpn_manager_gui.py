#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VPN Master Control GUI
Gelişmiş VPN Yönetim ve Düzeltme Sistemi
Tarayıcı ve sistem geneli VPN kontrolü
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import time
import json
import os
import requests
import webbrowser
from datetime import datetime
import psutil

class VPNManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 VPN Master Control - Gelişmiş VPN Yönetim Sistemi")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # VPN durumu değişkenleri
        self.vpn_status = tk.StringVar(value="❌ Bağlı Değil")
        self.current_ip = tk.StringVar(value="Kontrol ediliyor...")
        self.vpn_location = tk.StringVar(value="Bilinmiyor")
        self.dns_status = tk.StringVar(value="Kontrol ediliyor...")
        self.browser_protection = tk.StringVar(value="❌ Korumasız")
        
        # Monitoring durumu
        self.monitoring = False
        self.auto_fix = False
        
        self.create_gui()
        self.start_monitoring()
        
    def create_gui(self):
        # Ana stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Status.TLabel', font=('Arial', 12), background='#2c3e50', foreground='#ecf0f1')
        style.configure('Success.TLabel', font=('Arial', 10, 'bold'), background='#2c3e50', foreground='#27ae60')
        style.configure('Error.TLabel', font=('Arial', 10, 'bold'), background='#2c3e50', foreground='#e74c3c')
        
        # Üst başlık
        title_frame = tk.Frame(self.root, bg='#34495e', height=60)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, text="🔐 VPN MASTER CONTROL SYSTEM 🔐", style='Title.TLabel')
        title_label.pack(expand=True)
        
        # Ana konteyner
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Sol panel - Durum ve kontroller
        left_panel = tk.Frame(main_container, bg='#34495e', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Sağ panel - Loglar ve gelişmiş özellikler
        right_panel = tk.Frame(main_container, bg='#34495e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_status_panel(left_panel)
        self.create_control_panel(left_panel)
        self.create_advanced_panel(right_panel)
        
    def create_status_panel(self, parent):
        # Durum paneli
        status_frame = tk.LabelFrame(parent, text="🔍 VPN DURUMU", bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        status_frame.pack(fill='x', padx=10, pady=10)
        
        # VPN bağlantı durumu
        tk.Label(status_frame, text="VPN Durumu:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        status_label = tk.Label(status_frame, textvariable=self.vpn_status, bg='#34495e', fg='#e74c3c', font=('Arial', 12, 'bold'))
        status_label.pack(anchor='w', padx=20)
        
        # Mevcut IP
        tk.Label(status_frame, text="Mevcut IP:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        ip_label = tk.Label(status_frame, textvariable=self.current_ip, bg='#34495e', fg='#3498db', font=('Arial', 11))
        ip_label.pack(anchor='w', padx=20)
        
        # Lokasyon
        tk.Label(status_frame, text="Lokasyon:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        location_label = tk.Label(status_frame, textvariable=self.vpn_location, bg='#34495e', fg='#f39c12', font=('Arial', 11))
        location_label.pack(anchor='w', padx=20)
        
        # DNS durumu
        tk.Label(status_frame, text="DNS Durumu:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        dns_label = tk.Label(status_frame, textvariable=self.dns_status, bg='#34495e', fg='#9b59b6', font=('Arial', 11))
        dns_label.pack(anchor='w', padx=20)
        
        # Tarayıcı koruması
        tk.Label(status_frame, text="Tarayıcı Koruması:", bg='#34495e', fg='white', font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        browser_label = tk.Label(status_frame, textvariable=self.browser_protection, bg='#34495e', fg='#e67e22', font=('Arial', 11))
        browser_label.pack(anchor='w', padx=20, pady=(0, 10))
        
    def create_control_panel(self, parent):
        # Kontrol paneli
        control_frame = tk.LabelFrame(parent, text="⚡ HIZLI KONTROLLER", bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Ana kontrol butonları
        btn_frame1 = tk.Frame(control_frame, bg='#34495e')
        btn_frame1.pack(fill='x', padx=10, pady=5)
        
        self.create_button(btn_frame1, "🔄 VPN YENİDEN BAŞLAT", self.restart_vpn, '#e74c3c', 0, 0)
        self.create_button(btn_frame1, "🛠️ OTOMATİK DÜZ", self.auto_fix_vpn, '#27ae60', 0, 1)
        
        btn_frame2 = tk.Frame(control_frame, bg='#34495e')
        btn_frame2.pack(fill='x', padx=10, pady=5)
        
        self.create_button(btn_frame2, "🌐 DNS DÜZ", self.fix_dns, '#3498db', 0, 0)
        self.create_button(btn_frame2, "🔒 KILL SWITCH", self.toggle_kill_switch, '#9b59b6', 0, 1)
        
        # VPN yapılandırma
        config_frame = tk.LabelFrame(control_frame, text="VPN YAPILANDIRMA", bg='#34495e', fg='white')
        config_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_button(config_frame, "📁 CONFIG YÜK", self.load_config, '#f39c12', 0, 0, 2)
        self.create_button(config_frame, "⚙️ GELIŞMIŞ AYAR", self.advanced_settings, '#34495e', 1, 0, 2)
        
        # Monitoring kontrolleri
        monitor_frame = tk.LabelFrame(control_frame, text="İZLEME VE OTOMASYON", bg='#34495e', fg='white')
        monitor_frame.pack(fill='x', padx=10, pady=10)
        
        self.monitor_var = tk.BooleanVar()
        self.auto_fix_var = tk.BooleanVar()
        
        monitor_check = tk.Checkbutton(monitor_frame, text="🔄 Sürekli İzleme", variable=self.monitor_var, 
                                     command=self.toggle_monitoring, bg='#34495e', fg='white', selectcolor='#2c3e50')
        monitor_check.pack(anchor='w', padx=10, pady=2)
        
        autofix_check = tk.Checkbutton(monitor_frame, text="🤖 Otomatik Düzeltme", variable=self.auto_fix_var,
                                     command=self.toggle_auto_fix, bg='#34495e', fg='white', selectcolor='#2c3e50')
        autofix_check.pack(anchor='w', padx=10, pady=2)
        
    def create_advanced_panel(self, parent):
        # Notebook (sekmeli panel)
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Log sekmesi
        log_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(log_frame, text="📋 LOGLAR")
        
        # Log text widget
        self.log_text = scrolledtext.ScrolledText(log_frame, bg='#1e1e1e', fg='#00ff00', font=('Consolas', 10),
                                                height=20, wrap=tk.WORD)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # IP Test sekmesi
        test_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(test_frame, text="🌐 IP TEST")
        
        self.create_ip_test_panel(test_frame)
        
        # Browser Control sekmesi
        browser_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(browser_frame, text="🌍 BROWSER KONTROL")
        
        self.create_browser_control_panel(browser_frame)
        
        # Network Analysis sekmesi
        network_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(network_frame, text="📊 NETWORK ANALİZ")
        
        self.create_network_analysis_panel(network_frame)
        
    def create_ip_test_panel(self, parent):
        # IP test paneli
        test_control_frame = tk.Frame(parent, bg='#34495e')
        test_control_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_button(test_control_frame, "🔍 IP ANALİZ", self.analyze_ip, '#3498db', 0, 0)
        self.create_button(test_control_frame, "🛡️ DNS LEAK TEST", self.dns_leak_test, '#e67e22', 0, 1)
        self.create_button(test_control_frame, "🌐 WEBRTC TEST", self.webrtc_test, '#9b59b6', 0, 2)
        
        # Test sonuçları
        self.test_results = scrolledtext.ScrolledText(parent, bg='#1e1e1e', fg='#ffffff', font=('Consolas', 10),
                                                    height=15, wrap=tk.WORD)
        self.test_results.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_browser_control_panel(self, parent):
        browser_control_frame = tk.Frame(parent, bg='#34495e')
        browser_control_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(browser_control_frame, text="🌍 BROWSER VPN KONTROL", bg='#34495e', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Browser proxy ayarları
        proxy_frame = tk.LabelFrame(browser_control_frame, text="PROXY AYARLARI", bg='#34495e', fg='white')
        proxy_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(proxy_frame, text="Proxy IP:", bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.proxy_ip = tk.Entry(proxy_frame, bg='#2c3e50', fg='white', width=15)
        self.proxy_ip.grid(row=0, column=1, padx=5, pady=2)
        self.proxy_ip.insert(0, "127.0.0.1")
        
        tk.Label(proxy_frame, text="Port:", bg='#34495e', fg='white').grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.proxy_port = tk.Entry(proxy_frame, bg='#2c3e50', fg='white', width=8)
        self.proxy_port.grid(row=0, column=3, padx=5, pady=2)
        self.proxy_port.insert(0, "8080")
        
        # Browser kontrol butonları
        browser_btn_frame = tk.Frame(browser_control_frame, bg='#34495e')
        browser_btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_button(browser_btn_frame, "🔧 CHROME PROXY", lambda: self.set_browser_proxy('chrome'), '#4285f4', 0, 0)
        self.create_button(browser_btn_frame, "🦊 FIREFOX PROXY", lambda: self.set_browser_proxy('firefox'), '#ff9500', 0, 1)
        self.create_button(browser_btn_frame, "🚫 PROXY TEMİZLE", self.clear_browser_proxy, '#e74c3c', 1, 0, 2)
        
        # WebRTC kontrolü
        webrtc_frame = tk.LabelFrame(browser_control_frame, text="WEBRTC KORUMA", bg='#34495e', fg='white')
        webrtc_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_button(webrtc_frame, "🛡️ WEBRTC KAPAT", self.disable_webrtc, '#27ae60', 0, 0)
        self.create_button(webrtc_frame, "🔍 WEBRTC TEST", self.test_webrtc_leak, '#f39c12', 0, 1)
        
    def create_network_analysis_panel(self, parent):
        analysis_frame = tk.Frame(parent, bg='#34495e')
        analysis_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(analysis_frame, text="📊 NETWORK ANALİZ ARAÇLARI", bg='#34495e', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Analiz butonları
        analysis_btn_frame = tk.Frame(analysis_frame, bg='#34495e')
        analysis_btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_button(analysis_btn_frame, "📡 INTERFACE ANALİZ", self.analyze_interfaces, '#3498db', 0, 0)
        self.create_button(analysis_btn_frame, "🛣️ ROUTE ANALİZ", self.analyze_routes, '#e67e22', 0, 1)
        self.create_button(analysis_btn_frame, "🔍 PORT SCAN", self.port_scan, '#9b59b6', 1, 0)
        self.create_button(analysis_btn_frame, "📈 BANDWIDTH TEST", self.bandwidth_test, '#27ae60', 1, 1)
        
        # Analiz sonuçları
        self.analysis_results = scrolledtext.ScrolledText(parent, bg='#1e1e1e', fg='#00ff41', font=('Consolas', 9),
                                                        height=15, wrap=tk.WORD)
        self.analysis_results.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_button(self, parent, text, command, color, row, column, columnspan=1):
        btn = tk.Button(parent, text=text, command=command, bg=color, fg='white', 
                       font=('Arial', 9, 'bold'), relief='raised', bd=2,
                       activebackground='#1abc9c', activeforeground='white')
        btn.grid(row=row, column=column, columnspan=columnspan, padx=2, pady=2, sticky='ew')
        parent.grid_columnconfigure(column, weight=1)
        return btn
        
    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {"INFO": "#00ff00", "ERROR": "#ff0000", "WARNING": "#ffff00", "SUCCESS": "#00ff41"}
        color = colors.get(level, "#ffffff")
        
        self.log_text.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
        self.log_text.see(tk.END)
        
        # Son satırı renklendir
        line_start = self.log_text.index("end-2c linestart")
        line_end = self.log_text.index("end-1c")
        tag_name = f"color_{timestamp}"
        self.log_text.tag_add(tag_name, line_start, line_end)
        self.log_text.tag_config(tag_name, foreground=color)
        
    def run_command(self, command, shell=True):
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Komut zaman aşımına uğradı"
        except Exception as e:
            return False, "", str(e)
            
    def get_current_ip(self):
        try:
            response = requests.get("https://ipinfo.io/json", timeout=10)
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip', 'Bilinmiyor')
                city = data.get('city', '')
                country = data.get('country', '')
                org = data.get('org', '')
                
                self.current_ip.set(ip)
                self.vpn_location.set(f"{city}, {country}")
                
                # VPN durumunu güncelle
                if 'Amazon' in org or 'Google' in org or 'DigitalOcean' in org:
                    self.vpn_status.set("⚠️ VPN Şüpheli")
                    self.log_message(f"Şüpheli VPN durumu tespit edildi: {org}", "WARNING")
                else:
                    self.vpn_status.set("✅ VPN Aktif")
                    
                return data
        except Exception as e:
            self.log_message(f"IP kontrolü başarısız: {e}", "ERROR")
            self.current_ip.set("Kontrol başarısız")
            return None
            
    def check_vpn_processes(self):
        vpn_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if any(vpn in proc.info['name'].lower() for vpn in ['openvpn', 'wireguard', 'nordvpn', 'expressvpn']):
                    vpn_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return vpn_processes
        
    def check_dns_status(self):
        try:
            with open('/etc/resolv.conf', 'r') as f:
                dns_content = f.read()
            
            secure_dns = ['1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4']
            if any(dns in dns_content for dns in secure_dns):
                self.dns_status.set("✅ Güvenli DNS")
            else:
                self.dns_status.set("⚠️ Varsayılan DNS")
                
        except Exception as e:
            self.dns_status.set("❌ DNS Kontrol Edilemedi")
            
    def start_monitoring(self):
        def monitor():
            while True:
                if self.monitoring:
                    self.get_current_ip()
                    self.check_dns_status()
                    
                    # VPN süreçlerini kontrol et
                    vpn_procs = self.check_vpn_processes()
                    if not vpn_procs:
                        self.vpn_status.set("❌ VPN Süreci Yok")
                        if self.auto_fix:
                            self.log_message("VPN süreci bulunamadı, otomatik düzeltme başlatılıyor...", "WARNING")
                            self.auto_fix_vpn()
                    
                time.sleep(5)
                
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def toggle_monitoring(self):
        self.monitoring = self.monitor_var.get()
        status = "başlatıldı" if self.monitoring else "durduruldu"
        self.log_message(f"Sürekli izleme {status}", "INFO")
        
    def toggle_auto_fix(self):
        self.auto_fix = self.auto_fix_var.get()
        status = "aktifleştirildi" if self.auto_fix else "devre dışı bırakıldı"
        self.log_message(f"Otomatik düzeltme {status}", "INFO")
        
    def restart_vpn(self):
        self.log_message("VPN yeniden başlatılıyor...", "INFO")
        
        # VPN süreçlerini sonlandır
        success, stdout, stderr = self.run_command("sudo pkill -f 'openvpn|wireguard'")
        
        # OpenVPN'i yeniden başlat
        config_files = [
            "/etc/openvpn/*.ovpn",
            "/home/*/.config/*/*.ovpn",
            "~/vpn/*.ovpn"
        ]
        
        for pattern in config_files:
            success, stdout, stderr = self.run_command(f"ls {pattern} 2>/dev/null | head -1")
            if success and stdout.strip():
                config_file = stdout.strip()
                self.log_message(f"OpenVPN config bulundu: {config_file}", "SUCCESS")
                self.run_command(f"sudo openvpn --config '{config_file}' --daemon")
                break
                
        self.log_message("VPN yeniden başlatma tamamlandı", "SUCCESS")
        
    def auto_fix_vpn(self):
        self.log_message("Otomatik VPN düzeltme başlatılıyor...", "INFO")
        
        # DNS düzelt
        self.fix_dns()
        
        # VPN yeniden başlat
        self.restart_vpn()
        
        # Kill switch aktifleştir
        self.toggle_kill_switch()
        
        # Browser korumasını aktifleştir
        self.set_browser_proxy('chrome')
        
        self.log_message("Otomatik düzeltme tamamlandı", "SUCCESS")
        
    def fix_dns(self):
        self.log_message("DNS ayarları düzeltiliyor...", "INFO")
        
        dns_config = """# VPN DNS ayarları
nameserver 1.1.1.1
nameserver 1.0.0.1
nameserver 8.8.8.8
nameserver 8.8.4.4"""
        
        success, stdout, stderr = self.run_command(f"echo '{dns_config}' | sudo tee /etc/resolv.conf")
        if success:
            self.log_message("DNS ayarları başarıyla güncellendi", "SUCCESS")
        else:
            self.log_message(f"DNS güncelleme başarısız: {stderr}", "ERROR")
            
    def toggle_kill_switch(self):
        self.log_message("Kill switch ayarları yapılandırılıyor...", "INFO")
        
        commands = [
            "sudo iptables -F",
            "sudo iptables -P INPUT DROP",
            "sudo iptables -P FORWARD DROP", 
            "sudo iptables -P OUTPUT DROP",
            "sudo iptables -A INPUT -i lo -j ACCEPT",
            "sudo iptables -A OUTPUT -o lo -j ACCEPT"
        ]
        
        for cmd in commands:
            self.run_command(cmd)
            
        # VPN interface'ine izin ver
        success, stdout, stderr = self.run_command("ip addr show | grep -E '(tun|tap|wg)' | head -1")
        if success and stdout:
            interface = stdout.split(':')[1].strip()
            self.run_command(f"sudo iptables -A INPUT -i {interface} -j ACCEPT")
            self.run_command(f"sudo iptables -A OUTPUT -o {interface} -j ACCEPT")
            self.log_message(f"Kill switch aktifleştirildi ({interface})", "SUCCESS")
        else:
            self.log_message("VPN interface bulunamadı, kill switch ayarlanamadı", "WARNING")
            
    def load_config(self):
        file_path = filedialog.askopenfilename(
            title="VPN Config Dosyası Seç",
            filetypes=[("OpenVPN", "*.ovpn"), ("WireGuard", "*.conf"), ("Tüm", "*.*")]
        )
        
        if file_path:
            self.log_message(f"Config dosyası yüklendi: {file_path}", "SUCCESS")
            # Config dosyasını uygun konuma kopyala
            if file_path.endswith('.ovpn'):
                self.run_command(f"sudo cp '{file_path}' /etc/openvpn/")
            elif file_path.endswith('.conf'):
                self.run_command(f"sudo cp '{file_path}' /etc/wireguard/wg0.conf")
                
    def advanced_settings(self):
        # Gelişmiş ayarlar penceresi
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Gelişmiş VPN Ayarları")
        settings_window.geometry("600x400")
        settings_window.configure(bg='#2c3e50')
        
        # VPN protokol seçimi
        protocol_frame = tk.LabelFrame(settings_window, text="VPN PROTOKOL", bg='#34495e', fg='white')
        protocol_frame.pack(fill='x', padx=10, pady=10)
        
        self.protocol_var = tk.StringVar(value="OpenVPN")
        protocols = ["OpenVPN", "WireGuard", "IKEv2", "L2TP"]
        
        for protocol in protocols:
            tk.Radiobutton(protocol_frame, text=protocol, variable=self.protocol_var, value=protocol,
                          bg='#34495e', fg='white', selectcolor='#2c3e50').pack(anchor='w', padx=10)
                          
    def analyze_ip(self):
        self.test_results.delete(1.0, tk.END)
        self.test_results.insert(tk.END, "🔍 IP ANALİZİ BAŞLATILIYOR...\n\n")
        
        def analyze():
            ip_data = self.get_current_ip()
            if ip_data:
                result = f"""
📍 IP ADRESİ: {ip_data.get('ip', 'N/A')}
🌍 LOKASYON: {ip_data.get('city', 'N/A')}, {ip_data.get('region', 'N/A')}, {ip_data.get('country', 'N/A')}
🏢 SAĞLAYICI: {ip_data.get('org', 'N/A')}
📮 POSTA KODU: {ip_data.get('postal', 'N/A')}
🕐 ZAMAN DİLİMİ: {ip_data.get('timezone', 'N/A')}
📍 KOORDİNATLAR: {ip_data.get('loc', 'N/A')}

🛡️ GÜVENLİK ANALİZİ:
"""
                
                # Güvenlik kontrolü
                org = ip_data.get('org', '').lower()
                if any(provider in org for provider in ['amazon', 'google', 'microsoft', 'digitalocean']):
                    result += "⚠️ BULUT SUNUCU TESPİT EDİLDİ - VPN olabilir\n"
                else:
                    result += "✅ Normal ISP bağlantısı tespit edildi\n"
                    
                self.test_results.delete(1.0, tk.END)
                self.test_results.insert(tk.END, result)
                
        threading.Thread(target=analyze, daemon=True).start()
        
    def dns_leak_test(self):
        self.test_results.delete(1.0, tk.END)
        self.test_results.insert(tk.END, "🛡️ DNS LEAK TESTİ BAŞLATILIYOR...\n\n")
        
        def test_dns():
            dns_servers = [
                "1.1.1.1", "8.8.8.8", "208.67.222.222", "9.9.9.9"
            ]
            
            result = "DNS SUNUCULARINDAN CEVAPLAR:\n\n"
            
            for dns in dns_servers:
                success, stdout, stderr = self.run_command(f"dig +short @{dns} whoami.akamai.net")
                if success:
                    result += f"📡 {dns}: {stdout.strip()}\n"
                else:
                    result += f"❌ {dns}: Test başarısız\n"
                    
            # Mevcut DNS ayarlarını kontrol et
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    resolv_content = f.read()
                result += f"\n📋 MEVCUT DNS AYARLARI:\n{resolv_content}\n"
            except:
                result += "\n❌ DNS ayarları okunamadı\n"
                
            self.test_results.delete(1.0, tk.END)
            self.test_results.insert(tk.END, result)
            
        threading.Thread(target=test_dns, daemon=True).start()
        
    def webrtc_test(self):
        webbrowser.open("https://browserleaks.com/webrtc")
        self.log_message("WebRTC leak test sayfası açıldı", "INFO")
        
    def set_browser_proxy(self, browser):
        proxy_ip = self.proxy_ip.get()
        proxy_port = self.proxy_port.get()
        
        if browser == 'chrome':
            cmd = f"google-chrome --proxy-server=socks5://{proxy_ip}:{proxy_port} &"
        elif browser == 'firefox':
            # Firefox proxy ayarları için profile düzenleme gerekli
            cmd = f"firefox --new-instance &"
            
        self.run_command(cmd)
        self.log_message(f"{browser.title()} proxy ayarlandı: {proxy_ip}:{proxy_port}", "SUCCESS")
        self.browser_protection.set("✅ Korumalı")
        
    def clear_browser_proxy(self):
        # Browser süreçlerini sonlandır ve normal modda başlat
        self.run_command("pkill -f chrome")
        self.run_command("pkill -f firefox")
        time.sleep(2)
        self.run_command("google-chrome &")
        self.log_message("Browser proxy ayarları temizlendi", "INFO")
        self.browser_protection.set("❌ Korumasız")
        
    def disable_webrtc(self):
        # Chrome için WebRTC devre dışı bırakma
        chrome_flags = "--disable-webrtc --disable-web-security --disable-features=WebRTC"
        self.run_command(f"pkill -f chrome")
        time.sleep(2)
        self.run_command(f"google-chrome {chrome_flags} &")
        self.log_message("WebRTC devre dışı bırakıldı", "SUCCESS")
        
    def test_webrtc_leak(self):
        webbrowser.open("https://browserleaks.com/webrtc")
        self.log_message("WebRTC leak test başlatıldı", "INFO")
        
    def analyze_interfaces(self):
        self.analysis_results.delete(1.0, tk.END)
        self.analysis_results.insert(tk.END, "📡 NETWORK INTERFACE ANALİZİ\n\n")
        
        success, stdout, stderr = self.run_command("ip addr show")
        if success:
            self.analysis_results.insert(tk.END, stdout)
        else:
            # Alternatif komut
            success, stdout, stderr = self.run_command("cat /proc/net/dev")
            self.analysis_results.insert(tk.END, stdout)
            
    def analyze_routes(self):
        self.analysis_results.delete(1.0, tk.END)
        self.analysis_results.insert(tk.END, "🛣️ ROUTING TABLOSU ANALİZİ\n\n")
        
        success, stdout, stderr = self.run_command("ip route show")
        if success:
            self.analysis_results.insert(tk.END, stdout)
        else:
            success, stdout, stderr = self.run_command("cat /proc/net/route")
            self.analysis_results.insert(tk.END, stdout)
            
    def port_scan(self):
        self.analysis_results.delete(1.0, tk.END)
        self.analysis_results.insert(tk.END, "🔍 PORT TARAMA BAŞLATILIYOR...\n\n")
        
        def scan():
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 1080, 8080]
            result = "AÇIK PORTLAR:\n\n"
            
            for port in common_ports:
                success, stdout, stderr = self.run_command(f"timeout 2 bash -c '</dev/tcp/127.0.0.1/{port}'")
                status = "AÇIK" if success else "KAPALI"
                result += f"Port {port}: {status}\n"
                
            self.analysis_results.delete(1.0, tk.END)
            self.analysis_results.insert(tk.END, result)
            
        threading.Thread(target=scan, daemon=True).start()
        
    def bandwidth_test(self):
        self.analysis_results.delete(1.0, tk.END)
        self.analysis_results.insert(tk.END, "📈 BANDWIDTH TEST BAŞLATILIYOR...\n\n")
        
        def test():
            # Basit download test
            test_url = "http://speedtest.ftp.otenet.gr/files/test10Mb.db"
            start_time = time.time()
            
            try:
                response = requests.get(test_url, timeout=30, stream=True)
                if response.status_code == 200:
                    total_size = 0
                    for chunk in response.iter_content(chunk_size=1024):
                        total_size += len(chunk)
                        if time.time() - start_time > 10:  # 10 saniye limit
                            break
                            
                    elapsed = time.time() - start_time
                    speed_mbps = (total_size * 8) / (elapsed * 1000000)
                    
                    result = f"""
BANDWIDTH TEST SONUÇLARI:
📥 İndirilen Veri: {total_size / 1024 / 1024:.2f} MB
⏱️ Süre: {elapsed:.2f} saniye
🚀 Hız: {speed_mbps:.2f} Mbps
"""
                else:
                    result = "❌ Bandwidth test başarısız"
                    
            except Exception as e:
                result = f"❌ Test hatası: {e}"
                
            self.analysis_results.delete(1.0, tk.END)
            self.analysis_results.insert(tk.END, result)
            
        threading.Thread(target=test, daemon=True).start()

def main():
    root = tk.Tk()
    app = VPNManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()