# -*- coding: utf-8 -*-
"""
Pydroid 3 OSINT Aracı
Kullanım: dosyayı Pydroid 3'e yapıştır ve çalıştır.
Sadece standart kütüphane kullanır, pip gerekmez.
Not: Yalnızca yasal / etik kullanım için - hedefe izniniz olmadan kullanmayın.
"""

import urllib.request
import urllib.error
import json
import re
import socket

UA = {"User-Agent": "Mozilla/5.0 (Linux; Android) OSINT-Tool/1.0"}

def istek(url):
    """URL'ye GET isteği atar, durum kodu döndürür."""
    try:
        req = urllib.request.Request(url, headers=UA)
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None

def kullanici_adi_tara(username):
    """Kullanıcı adını popüler platformlarda arar."""
    siteler = {
        "GitHub":       f"https://github.com/{username}",
        "Twitter/X":    f"https://x.com/{username}",
        "Instagram":    f"https://www.instagram.com/{username}/",
        "Reddit":       f"https://www.reddit.com/user/{username}",
        "TikTok":       f"https://www.tiktok.com/@{username}",
        "Telegram":     f"https://t.me/{username}",
        "Pinterest":    f"https://www.pinterest.com/{username}/",
        "Steam":        f"https://steamcommunity.com/id/{username}",
        "SoundCloud":   f"https://soundcloud.com/{username}",
        "Medium":       f"https://medium.com/@{username}",
        "GitLab":       f"https://gitlab.com/{username}",
        "Pastebin":     f"https://pastebin.com/u/{username}",
    }
    print(f"\n[+] '{username}' taranıyor...\n" + "-" * 40)
    bulunan = []
    for ad, url in siteler.items():
        kod = istek(url)
        if kod == 200:
            print(f"  [✓] BULUNDU : {ad} -> {url}")
            bulunan.append(url)
        elif kod in (403, 429):
            print(f"  [?] ENGELLİ: {ad} (elle kontrol et)")
        else:
            print(f"  [✗] yok    : {ad}")
    print("-" * 40)
    print(f"[*] Sonuç: {len(bulunan)} platformda bulundu\n")
    return bulunan

def ip_sorgula(ip):
    """ip-api.com ile IP coğrafi bilgisi çeker."""
    url = f"http://ip-api.com/json/{ip}"
    try:
        req = urllib.request.Request(url, headers=UA)
        data = json.loads(urllib.request.urlopen(req, timeout=10).read())
        if data.get("status") == "success":
            print(f"\n[+] IP: {ip}")
            for k in ("country", "regionName", "city", "isp", "org", "as", "timezone"):
                print(f"    {k:>10}: {data.get(k, 'N/A')}")
            print(f"{'coords':>10}: {data.get('lat')}, {data.get('lon')}")
        else:
            print("[!] Sorgu başarısız (özel IP olabilir)")
    except Exception as e:
        print(f"[!] Hata: {e}")

def domain_sorgula(domain):
    """Domain DNS kayıtlarını ve IP'sini gösterir."""
    print(f"\n[+] {domain} sorgulanıyor...")
    try:
        ip = socket.gethostbyname(domain)
        print(f"    IP adresi: {ip}")
        ip_sorgula(ip)
    except Exception as e:
        print(f"[!] Çözümlenemedi: {e}")
    for sub in ["www", "mail", "ftp", "api"]:
        try:
            print(f"    {sub}.{domain} -> {socket.gethostbyname(sub + '.' + domain)}")
        except Exception:
            pass

def eposta_kontrol(eposta):
    """E-posta formatını ve MX benzeri temel kontrolü yapar."""
    desen = r"^[\w\.\+\-]+@[\w\-]+\.[\w\-\.]+$"
    if re.match(desen, eposta):
        domain = eposta.split("@")[1]
        print(f"[✓] Format geçerli, domain: {domain}")
        try:
            socket.gethostbyname(domain)
            print("[✓] Domain aktif")
        except Exception:
            print("[✗] Domain çözümlenemiyor")
        print("[i] İhlal kontrolü için elle: https://haveibeenpwned.com")
    else:
        print("[✗] Geçersiz e-posta formatı")

def menu():
    while True:
        print("""
========== OSINT ARACI ==========
1) Kullanıcı adı taraması
2) IP sorgulama
3) Domain / DNS sorgulama
4) E-posta kontrolü
0) Çıkış
=================================""")
        sec = input("Seçim: ").strip()
        if sec == "1":
            kullanici_adi_tara(input("Kullanıcı adı: ").strip())
        elif sec == "2":
            ip_sorgula(input("IP adresi: ").strip())
        elif sec == "3":
            domain_sorgula(input("Domain: ").strip())
        elif sec == "4":
            eposta_kontrol(input("E-posta: ").strip())
        elif sec == "0":
            break

if __name__ == "__main__":
    menu()