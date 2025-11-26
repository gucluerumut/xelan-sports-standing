# Diğer Bilgisayara Kurulum Rehberi

## ✅ Proje GitHub'a Yüklendi!

Repository: https://github.com/gucluerumut/xelan-sports-standing

---

## Diğer Bilgisayarda Kurulum

### Adım 1: Projeyi Klonlayın

Terminal'i açın ve şu komutları çalıştırın:

```bash
# İstediğiniz bir klasöre gidin (örnek: Desktop)
cd ~/Desktop

# Projeyi klonlayın
git clone https://github.com/gucluerumut/xelan-sports-standing.git

# Proje klasörüne girin
cd xelan-sports-standing
```

---

### Adım 2: Node.js Dependencies Kurun

```bash
npm install
```

Bu komut tüm gerekli paketleri kuracak (~5 dakika sürebilir).

---

### Adım 3: Environment Variables (Opsiyonel)

Eğer Apify scriptlerini çalıştıracaksanız:

```bash
# .env dosyası oluşturun
echo "APIFY_API_TOKEN=apify_api_8YXjcrdCIMuvbIdb9HdVXSOILePkyo06tZLh" > .env
```

---

### Adım 4: Geliştirme Sunucusunu Başlatın

```bash
npm run dev
```

Uygulama şu adreste açılacak: **http://localhost:3000**

---

## Manuel Veri Girişi (Twitter)

### Twitter Screenshot'ları

Screenshot'lar proje ile birlikte geldi:
```
xelan-sports-standing/twitter-screenshots/
```

### Veri Giriş Dosyası

```
xelan-sports-standing/TWITTER_MANUEL_VERI.txt
```

**Nasıl Doldurulur:**
1. `TWITTER_MANUEL_VERI.txt` dosyasını açın
2. `twitter-screenshots/` klasöründeki screenshot'lara bakın
3. Her kulüp için takipçi sayısını yazın
4. Dosyayı kaydedin

**Örnek:**
```
1. @1913parmacalcio (Parma)
   Takipçi: 450K

2. @AJA (Auxerre)
   Takipçi: 125K
```

---

## Değişiklikleri Geri Gönderme

Veri girişini tamamladıktan sonra:

```bash
# Değişiklikleri kaydedin
git add -A
git commit -m "Twitter follower data completed"

# GitHub'a gönderin
git push
```

---

## Bu Bilgisayarda Değişiklikleri Alma

Diğer bilgisayarda değişiklik yaptıktan sonra, bu bilgisayarda:

```bash
cd /Users/umutgucluer/.gemini/antigravity/scratch/xelan-sports-standing

# Değişiklikleri çekin
git pull
```

---

## Proje Yapısı

```
xelan-sports-standing/
├── app/                          # Next.js sayfaları
│   ├── page.tsx                 # Ana sayfa
│   ├── league/[slug]/page.tsx   # Lig sayfaları
│   ├── global/page.tsx          # Global sıralama
│   └── battle/page.tsx          # Battle mode
├── components/                   # React komponentleri
│   ├── SocialMediaLinks.tsx     # Sosyal medya ikonları ⭐
│   ├── ClubCard.tsx             # Kulüp kartı
│   └── StandingsTable.tsx       # Sıralama tablosu
├── lib/                         # Veri ve servisler
│   ├── club-data-real.ts        # 113 kulübün tüm verileri ⭐
│   ├── types.ts                 # TypeScript tipleri
│   └── apify-service.ts         # Apify servisi
├── twitter-screenshots/          # 113 Twitter screenshot (36 MB)
├── TWITTER_MANUEL_VERI.txt      # Veri giriş dosyası ⭐
└── Python scriptleri            # Veri toplama scriptleri
```

---

## Önemli Dosyalar

**Sosyal Medya İkonları:**
- `components/SocialMediaLinks.tsx` - Tıklanabilir ikonlar
- `lib/club-data-real.ts` - Tüm kulüp verileri (Instagram, TikTok, Twitter)

**Manuel Veri:**
- `TWITTER_MANUEL_VERI.txt` - Doldurulacak dosya
- `twitter-screenshots/` - Screenshot'lar

---

## Sorun Giderme

### Port 3000 kullanımda hatası:
```bash
# Farklı port kullanın
npm run dev -- -p 3001
```

### npm install hatası:
```bash
# Cache temizle ve tekrar dene
npm cache clean --force
npm install
```

### Git pull çakışması:
```bash
# Yerel değişiklikleri kaydet
git stash

# Pull yap
git pull

# Değişiklikleri geri getir
git stash pop
```

---

## Sonraki Adımlar

1. ✅ Projeyi klonlayın
2. ✅ `npm install` çalıştırın
3. ✅ `npm run dev` ile başlatın
4. ⏳ `TWITTER_MANUEL_VERI.txt` dosyasını doldurun
5. ⏳ Değişiklikleri GitHub'a gönderin
6. ⏳ Bu bilgisayarda `git pull` yapın

---

## Yardım

Herhangi bir sorun olursa:
1. Terminal'deki hata mesajını kontrol edin
2. `npm install` komutunu tekrar çalıştırın
3. Node.js versiyonunu kontrol edin: `node --version` (v18+ olmalı)

İyi çalışmalar! 🚀
