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
