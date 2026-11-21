# Katkı

Liste, Türkçe konuşma tanımayla çalışan herkesin kullanabileceği ortak bir sözlük olsun diye açık.

## İsim eklemek

En kolay yol **Issues › İsim ekle** formu. Pull request açmak istersen `src/turkce_asr_ozel_isim/data/lexicon.json` dosyasına kayıt ekle:

```json
{"name": "Mustafa Namoğlu", "type": "person", "company": "ikas",
 "misspellings": ["Anamoğlu", "Ramoğlu"], "source": ["youtube-title"]}
```

| alan | anlamı |
|---|---|
| `name` | doğru yazım; kişide ad ve soyad |
| `type` | `person` ya da `company` |
| `company` | kişinin bağlı olduğu şirket (isteğe bağlı) |
| `misspellings` | modelin yazdığı yanlış halleri |
| `context_required` | gerçek bir kelime olan yanlış yazımlar ("ikaz"); yalnız şirket aynı transkriptte geçiyorsa aday olur |
| `source` | `wikidata`, `youtube-title`, `youtube-channel`, `news`, `company-site` |
| `wikidata` | Wikidata kimliği: `Q` ve rakam, ör. `Q12071778` (isteğe bağlı; kaydı yoksa yazılmaz) |
| `image` | Wikidata'nın kişiye bağladığı resim (P18): Commons dosya adı, ör. `Portrait of Hamdi Ulukaya.jpg` (P18 yoksa yazılmaz) |
| `image_license` | fotoğrafın Commons'taki lisansı, ör. `CC BY-SA 3.0`; `image` varsa zorunlu |
| `image_author` | fotoğrafçı (Commons'taki yazar bilgisi); `image` varsa zorunlu |

Fotoğraf dosyası eklenmez, yalnız bilgisi: liste CC0, Commons fotoğrafları çoğunlukla CC BY-SA, dosya eklenirse lisanslar çakışır. Fotoğraf yalnız Wikidata'daki P18'den alınır; böylece fotoğrafın o kişiye ait olduğunu Wikidata doğrulamış olur. Lisans ve fotoğrafçı Commons API'den (`prop=imageinfo&iiprop=extmetadata`: `LicenseShortName`, `Artist`) alınır.

Kayıt kuralları testlerde (`tests/test_lexicon.py`), her pull request'te otomatik çalışır.

## Kim eklenir

- Girişimci, yönetici, yatırımcı gibi kamuya açık biçimde tanınan kişiler ve şirketler.
- Doğru yazımı herkese açık bir kaynakta gösterilebilenler.

Özel kişiler, telefon, e-posta, sosyal medya hesabı ve transkript metni eklenmez.

Her ekleme bir insan tarafından incelenir; otomatik birleştirme yoktur. Yanlış bir kayıt bu sözlüğü kullanan herkesin altyazısını bozar.

## Listeden çıkmak

Adınızın çıkarılmasını istiyorsanız **Issues › İsmimi kaldır** formunu doldurun. Gerekçe istemiyoruz.

## Sürüm çıkarmak

Bakımcılar için: [docs/surum-cikarma.md](docs/surum-cikarma.md).
