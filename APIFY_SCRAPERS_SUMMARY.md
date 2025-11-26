# Apify Scrapers - Test Sonuçları

## ✅ TikTok Profil Bilgileri

**Actor ID:** `xtdata~tiktok-user-information-scraper`

### Input Formatı:
```json
{
  "usernames": ["mancity", "arsenal", "realmadrid"]
}
```

### Output Örneği:
```json
{
  "unique_id": "arsenal",
  "follower_count": 10751287,
  "following_count": 30,
  "nickname": "Arsenal",
  "bio_url": "...",
  "aweme_count": 780
}
```

### Test Sonuçları:
- ✅ **Arsenal**: 10.7M takipçi, 30 takip
- ✅ **Man City**: 33.2M takipçi, 129 takip
- ✅ **Real Madrid**: 68.7M takipçi, 27 takip

**Durum:** Mükemmel çalışıyor! 🎉

---

## ❌ Twitter/X Profil Bilgileri

**Denenen Actor:** `apidojo~twitter-user-scraper`

### Sorun:
Actor çalıştırıldı ama FAILED durumuna düştü. Muhtemelen:
1. Ücretli bir actor olabilir (Pay Per Result)
2. Twitter API değişiklikleri nedeniyle çalışmıyor olabilir
3. Ek authentication gerekiyor olabilir

### Alternatif Çözümler:

#### Seçenek 1: Farklı Ücretsiz Actor Dene
- `epctex~twitter-profile-scraper`
- `logical_scrapers~x-twitter-user-profile-tweets-scraper`
- `crawlerbros~twitter-profile-scraper`

#### Seçenek 2: Twitter API Kullan
- Twitter'ın resmi API'sini kullan (ücretli)
- API key gerektirir

#### Seçenek 3: Manuel Veri Toplama
- Profil bilgilerini manuel olarak topla ve JSON'a kaydet

---

## Önerilen Yaklaşım

### TikTok için:
```python
TIKTOK_ACTOR_ID = "xtdata~tiktok-user-information-scraper"

input_data = {
    "usernames": ["kullanici_adi1", "kullanici_adi2"]
}
```

### Twitter için:
Farklı actor'ları test etmek gerekiyor. Eğer hiçbiri çalışmazsa:
1. Twitter API kullanımını değerlendir
2. Manuel veri toplama düşün
3. Sadece TikTok verilerini kullan

---

## API Kullanımı

```python
import requests

APIFY_API_TOKEN = "your_token_here"
APIFY_BASE_URL = "https://api.apify.com/v2"

# Actor'ı çalıştır
url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs"
headers = {
    "Authorization": f"Bearer {APIFY_API_TOKEN}",
    "Content-Type": "application/json"
}
response = requests.post(url, headers=headers, json=input_data)
run_id = response.json()['data']['id']

# Sonuçları al
dataset_id = run_result['data']['defaultDatasetId']
url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items"
items = requests.get(url, headers=headers).json()
```
