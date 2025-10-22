# 🚀 CRYPTOMATCH - ADIM ADIM KURULUM REHBERİ

Bu rehber sizi sıfırdan başlayarak CryptoMatch uygulamasını çalıştırmaya kadar götürecek.

## 📋 GEREKSINIMLER

✅ **İhtiyacınız Olanlar:**
- Windows 10/11 (PowerShell)
- Anaconda veya Miniconda
- OpenAI API Key (opsiyonel ama önerilen)
- Internet bağlantısı

## 🔧 ADIM 1: ANACONDA KURULUMU

Eğer Anaconda kurulu değilse:

1. https://www.anaconda.com/download adresine gidin
2. Windows için Anaconda'yı indirin
3. Kurulum sırasında "Add to PATH" seçeneğini işaretleyin
4. Kurulumu tamamlayın

**Kontrol:**
```powershell
conda --version
```
Versiyon numarası görmeli siniz (örn: conda 23.9.0)

## 📁 ADIM 2: PROJE DOSYALARINI HAZIRLA

### Seçenek A: GitHub'dan Clone (Önerilen)

```powershell
# Proje klasörüne git
cd C:\Users\KULLANICI_ADINIZ\Desktop

# Repository'yi clone et
git clone https://github.com/wonra16/crypto-match.git

# Klasöre gir
cd crypto-match
```

### Seçenek B: ZIP Dosyasından

1. Proje ZIP dosyasını masaüstüne kaydet
2. ZIP'i çıkart
3. PowerShell'i aç
4. Klasöre git:
```powershell
cd C:\Users\KULLANICI_ADINIZ\Desktop\crypto-match-complete
```

## 🐍 ADIM 3: CONDA ENVIRONMENT OLUŞTUR

```powershell
# Environment oluştur
conda create -n cryptomatch python=3.9 -y

# Environment'ı aktif et
conda activate cryptomatch
```

**Başarılı olduğunda komut satırında şunu görmelisiniz:**
```
(cryptomatch) PS C:\...\crypto-match-complete>
```

## 📦 ADIM 4: BAĞIMLILIKLARI YÜKLE

```powershell
# Tüm paketleri yükle
pip install -r requirements.txt
```

**Beklenen süre:** 2-5 dakika

**Başarılı olursa şunları görmelisiniz:**
```
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 ...
```

## 🔑 ADIM 5: OPENAI API KEY ALMA (Opsiyonel ama Önerilen)

### OpenAI API Key Nasıl Alınır?

1. https://platform.openai.com/signup adresine git
2. Hesap oluştur (ücretsiz deneme var)
3. https://platform.openai.com/api-keys adresine git
4. "Create new secret key" butonuna tıkla
5. Key'i kopyala (sk-... ile başlar)

**ÖNEMLİ:** API key'i kimseyle paylaşma!

### API Key'i Ayarla

```powershell
# .env dosyası oluştur
copy .env.example .env

# .env dosyasını düzenle
notepad .env
```

**Notepad'de şunu bul:**
```
OPENAI_API_KEY=your_openai_api_key_here
```

**Şununla değiştir:**
```
OPENAI_API_KEY=sk-SENIN_GERCEK_KEY_IN
```

Kaydet ve kapat.

**NOT:** OpenAI API key'iniz yoksa da uygulama çalışır ama komedi metinleri önceden hazırlanmış şablonlardan gelir.

## ✅ ADIM 6: KURULUMU TEST ET

```powershell
# Test scriptini çalıştır
python test_installation.py
```

**Başarılı test çıktısı:**
```
============================================================
🚀 CRYPTOMATCH TEST SUITE
============================================================
🔍 Testing imports...
  ✅ FastAPI installed
  ✅ Uvicorn installed
  ...
============================================================
📊 TEST SUMMARY
============================================================
✅ PASS - Imports
✅ PASS - Config
✅ PASS - Personality
✅ PASS - Matchmaking
✅ PASS - Comedy
✅ PASS - Image Generator
✅ PASS - API
============================================================
Result: 7/7 tests passed
🎉 All tests passed! Your installation is ready!
```

## 🚀 ADIM 7: UYGULAMAYI BAŞLAT

### Yöntem 1: Manuel Başlatma

```powershell
# Uygulamayı başlat
python main.py
```

### Yöntem 2: Quick Start Script (Otomatik)

```powershell
# PowerShell scriptini çalıştır
.\start.ps1
```

**Başarılı başlatma çıktısı:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## 🌐 ADIM 8: UYGULAMAYI TEST ET

### Browser'da Test

1. Chrome/Edge/Firefox'u aç
2. http://localhost:8000 adresine git
3. "Find My Match" butonunu görmelisiniz

### Komut Satırında Test

**Yeni bir PowerShell penceresi aç** (uygulamayı kapatma!) ve:

```powershell
# Health check
curl http://localhost:8000/health

# API test
curl http://localhost:8000/api/personalities
```

## 📊 ADIM 9: FARCASTER FRAME TEST (Opsiyonel)

### Ngrok ile Test

1. Ngrok indir: https://ngrok.com/download
2. Ngrok'u başlat:
```powershell
ngrok http 8000
```

3. Ngrok URL'ini kopyala (örn: https://abc123.ngrok.io)
4. Farcaster Frame Validator'da test et: https://warpcast.com/~/developers/frames

## 🚢 ADIM 10: VERCEL'E DEPLOY

### GitHub'a Push

```powershell
# Git reposunu başlat (eğer yoksa)
git init

# Dosyaları ekle
git add .

# Commit
git commit -m "CryptoMatch production ready"

# GitHub remote ekle (kendi repo URL'iniz)
git remote add origin https://github.com/KULLANICI_ADINIZ/crypto-match.git

# Push
git push -u origin main
```

### Vercel'de Deploy

1. https://vercel.com adresine git
2. GitHub ile giriş yap
3. "New Project" butonuna tıkla
4. "crypto-match" repository'sini seç
5. Environment Variables ekle:
   - `OPENAI_API_KEY`: (OpenAI key'iniz)
   - `BASE_URL`: (otomatik ayarlanır)
   - `ENVIRONMENT`: production
6. "Deploy" butonuna tıkla
7. 2-3 dakika bekle
8. Deploy tamamlandığında URL'i kopyala

### Deploy'u Test Et

```powershell
# Vercel URL'inizi test edin
curl https://your-app.vercel.app/health
```

## 🎯 KULLANIM

### Yerel Kullanım

1. Environment'ı aktif et:
```powershell
conda activate cryptomatch
```

2. Uygulamayı başlat:
```powershell
python main.py
```

3. Browser'da aç: http://localhost:8000

### Durdurma

Uygulamayı durdurmak için:
```
Ctrl + C
```

## 🐛 SORUN ÇÖZME

### Hata: "ModuleNotFoundError: No module named 'fastapi'"

**Çözüm:**
```powershell
conda activate cryptomatch
pip install -r requirements.txt
```

### Hata: "Port 8000 already in use"

**Çözüm 1:** Farklı port kullan
```powershell
# main.py'yi düzenle, port=8000 yerine port=8001 yaz
```

**Çözüm 2:** Mevcut işlemi durdur
```powershell
# Port 8000'i kullanı process'i bul
netstat -ano | findstr :8000
# Çıkan PID ile işlemi durdur
taskkill /PID XXXXX /F
```

### Hata: "OpenAI API key not found"

**Durum:** Uygulama çalışır ama AI komedi yerine şablon kullanır

**Çözüm:**
1. OpenAI key alın
2. .env dosyasına ekleyin
3. Uygulamayı yeniden başlatın

### Hata: "conda: command not found"

**Çözüm:** Anaconda'yı yeniden kurun ve PATH'e ekleyin

## 📝 SONRAKI ADIMLAR

✅ **Başarıyla kurulum yaptınız!** Şimdi:

1. **Farcaster'da Paylaş:** 
   - Uygulamanızı Warpcast'te paylaşın
   - Frame'i embed edin

2. **Özelleştir:**
   - Personality type'ları düzenleyin
   - Komedi şablonlarını genişletin
   - Görsel tasarımı değiştirin

3. **Geliştir:**
   - Redis cache ekleyin
   - PostgreSQL database entegre edin
   - Analytics ekleyin

## 💡 FAYDALI KOMUTLAR

```powershell
# Environment'ları listele
conda env list

# Environment'ı aktif et
conda activate cryptomatch

# Environment'ı deaktif et
conda deactivate

# Uygulamayı başlat
python main.py

# Testleri çalıştır
python test_installation.py

# Paketleri güncelle
pip install -r requirements.txt --upgrade

# Git status
git status

# Git commit
git add .
git commit -m "Update message"
git push
```

## 📞 DESTEK

Sorun mu yaşıyorsunuz?

1. README.md dosyasını okuyun
2. GitHub Issues'da sorun bildirin
3. Test scriptini çalıştırın: `python test_installation.py`

## 🎉 TEBRİKLER!

CryptoMatch'i başarıyla kurdunuz ve çalıştırdınız! 

**Artık hazırsınız:**
- ✅ Yerel development yapabilirsiniz
- ✅ Vercel'e deploy edebilirsiniz
- ✅ Farcaster'da paylaşabilirsiniz
- ✅ Viral dating app'iniz var!

**Başarılar! 🚀💕**

---

**Ekstra İpuçları:**

🔥 **Viral Olması İçin:**
- Komik ve shareable içerik üretin
- Farcaster influencer'larla paylaşın
- Frame'i optimize edin

💰 **Monetization:**
- Premium features ekleyin
- Sponsorlu matchler
- NFT integrations

📊 **Analytics:**
- User behavior tracking
- Match success rates
- Viral coefficient ölçümü

**İYİ ŞANSLAR! 🎯**
