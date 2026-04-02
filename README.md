# TikTok Streak Bot

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.44-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

Telegram bot üzerinden yönetilen, Playwright tabanlı TikTok seri (streak) otomasyon sistemi. Her gece 00:01'de otomatik tetiklenir; `/seri` komutuyla manuel olarak da çalıştırılabilir.

---

## Proje Yapısı

```
tiktok-streak-bot/
├── core/
│   ├── __init__.py
│   └── tiktok.py          # Playwright otomasyon modülü
├── main.py                # Telegram bot + scheduler giriş noktası
├── requirements.txt
├── .env.example           # Ortam değişkeni şablonu
├── cookies.json.example   # Çerez şablonu
└── README.md
```

---

## Kurulum

### 1. Repoyu klonla / dosyaları yükle

```bash
git clone https://github.com/Patr10on/tiktok-streak-bot.git
cd tiktok-streak-bot
```

### 2. Sanal ortam oluştur

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
playwright install chromium
playwright install-deps chromium
```

### 4. `.env` dosyasını oluştur

```bash
cp .env.example .env
nano .env
```

| Değişken | Açıklama |
|---|---|
| `TELEGRAM_BOT_TOKEN` | @BotFather'dan alınan bot token |
| `ADMIN_CHAT_ID` | Yetkili Telegram kullanıcısının chat ID'si |
| `TARGET_USERNAME` | TikTok hedef kullanıcı adı (@ olmadan) |
| `COOKIES_PATH` | Çerez dosyasının yolu (varsayılan: `cookies.json`) |

### 5. `cookies.json` dosyasını oluştur

```bash
cp cookies.json.example cookies.json
```

TikTok oturumunu tarayıcıdan dışa aktar (EditThisCookie veya DevTools → Application → Cookies). `sessionid` ve `tt_chain_token` alanları zorunludur.

---

## Çalıştırma

```bash
python main.py
```

---

## Telegram Komutları

| Komut | Açıklama |
|---|---|
| `/seri` | Otomasyonu anında başlatır |
| `/durum` | Bot durumunu ve ping değerini döner |

---

## 7/24 Sunucu Deployment (Linux VPS / PythonAnywhere)

### Systemd ile (önerilen — VPS)

```bash
sudo nano /etc/systemd/system/streak-bot.service
```

```ini
[Unit]
Description=TikTok Streak Bot
After=network.target

[Service]
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER/tiktok-streak-bot
ExecStart=/home/YOUR_USER/tiktok-streak-bot/venv/bin/python main.py
Restart=always
RestartSec=10
EnvironmentFile=/home/YOUR_USER/tiktok-streak-bot/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable streak-bot
sudo systemctl start streak-bot
sudo systemctl status streak-bot
```

Log takibi:

```bash
journalctl -u streak-bot -f
```

### Screen ile (PythonAnywhere / basit VPS)

```bash
screen -S streak-bot
source venv/bin/activate
python main.py
# Ctrl+A D ile detach
```

Yeniden bağlanmak için:

```bash
screen -r streak-bot
```

---

## Hata Yönetimi

- Element bulunamadığında veya oturum geçersiz olduğunda `screenshot_error.png` alınır.
- Ekran görüntüsü otomatik olarak Telegram üzerinden iletilir.
- Tüm hatalar `try/except` blokları ile yakalanır; tarayıcı her senaryoda temiz kapatılır.

---

## Notlar

- PythonAnywhere ücretsiz planı `playwright install-deps` için yeterli sistem iznine sahip olmayabilir. Paid plan veya harici bir VPS (DigitalOcean, Hetzner) önerilir.
- Çerezler periyodik olarak sona erer; `cookies.json`'u düzenli güncelle.
- Headless Chromium sunucu ortamında `--no-sandbox` ve `--disable-dev-shm-usage` flagleri zorunludur.
