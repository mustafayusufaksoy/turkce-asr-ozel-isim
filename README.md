# Türkçe Whisper Özel İsim Düzeltici

**Whisper ve WhisperX transkriptlerindeki yanlış yazılan Türkçe kişi ve şirket adlarını düzelten açık kaynak Python aracı ve sözlüğü.** Altyazı, podcast, YouTube ve Reels üretenler için.

*Turkish proper name correction for Whisper and WhisperX: fixes misheard people and company names in speech-to-text transcripts and subtitles. [English below](#english).*

[![test](https://github.com/mustafayusufaksoy/turkce-asr-ozel-isim/actions/workflows/test.yml/badge.svg)](https://github.com/mustafayusufaksoy/turkce-asr-ozel-isim/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/turkce-asr-ozel-isim.svg)](https://pypi.org/project/turkce-asr-ozel-isim/)
[![Kod: MIT](https://img.shields.io/badge/kod-MIT-blue.svg)](LICENSE)
[![Veri: CC0](https://img.shields.io/badge/veri-CC0-lightgrey.svg)](LICENSE-DATA)

## Sorun

Whisper Türkçeyi iyi tanır, ama özel isimleri tutarlı biçimde yanlış yazar. Gerçek bir podcast transkriptinden:

| Whisper'ın yazdığı | Doğrusu |
|---|---|
| `Mustafa Ulan Moğlu` | `Mustafa Namoğlu` |
| `Siz Mustafa Anamoğlu'sunuz.` | `Siz Mustafa Namoğlu'sunuz.` |
| `Ben İkaz diye bir şirket kurdum` | `Ben ikas diye bir şirket kurdum` |
| `Oğuz Alper Öktan ve Marta şirketi` | `Oğuz Alper Öktem ve Martı şirketi` |
| `Martır'ın kurucusu` | `Martı'nın kurucusu` |
| `Ben Ferhat Duraşakır.` | `Ben Ferhat Tuğra Çakır.` |

Bir dil modeline "düzelt" demek yetmez: model adı tanımıyorsa aynı yanlışı okur ya da yeni bir ad uydurur. Bu eksik bir bilgi sorunu, o yüzden çözüm bir sözlük.

## Nasıl çalışır

1. **Aday bulma:** Sözlük ve benzerlik araması düzeltilebilecek yerleri bulur. LLM kullanılmaz.
2. **Seçim:** Bir seçici, yalnız aday **numarası** döndürür. Model metin yazmadığı için ad uyduramaz.
3. **Uygulama:** Metni kod değiştirir. Noktalama ve ekler korunur (`Martır'a` → `Martı'ya`), kelime zaman damgaları bozulmaz. İki kelimenin bire inmesi (`Ulan Moğlu` → `Namoğlu`) de desteklenir.

`ikaz` gibi gerçek bir kelime olan yanlış yazımlar, yalnız o şirket aynı transkriptte anılıyorsa aday olur.

## Kurulum

```bash
pip install "turkce-asr-ozel-isim[claude]"
```

Python 3.9 ve üzeri. Çekirdeğin bağımlılığı yok; `[claude]` yalnız Claude ile seçim için gerekir.

## Kullanım

Komut satırı, `segments[].words[]` içeren Whisper / WhisperX JSON dosyasıyla çalışır:

```bash
# Yalnız adayları listele, API gerekmez
turkce-asr-ozel-isim transkript.json

# Claude seçsin (ANTHROPIC_API_KEY gerekir)
turkce-asr-ozel-isim transkript.json --selector claude -o duzeltilmis.json
```

Python:

```python
from turkce_asr_ozel_isim import Lexicon, correct
from turkce_asr_ozel_isim.claude import claude_selector

kelimeler = {"klip1": [{"word": "Mustafa", "start": 0.0, "end": 0.4},
                       {"word": "Anamoğlu", "start": 0.4, "end": 1.0}]}
duzeltilmis, rapor = correct(kelimeler, Lexicon.default(), claude_selector())
```

Başka bir model kullanmak için `ask(sistem, metin)` imzasında bir fonksiyon verin. Kendi adlarınızı `--lexicon benim.json` ile ekleyebilirsiniz.

## Ölçüm

Claude Haiku 5.5 ile, gerçek podcast kliplerinde. Küçük bir örneklem, kesin bir kıyas olarak okumayın; daha geniş ölçüm yol haritasında.

| Deneme | Aday | Kabul | Sonuç |
|---|---|---|---|
| Bir video (11 hatalı yer), tam sözlük | 11 | 10 | 10/11 düzeltildi |
| Aynı video, bu videodan öğrenilen yazımlar sözlükten çıkarılmış | 7 | 7 | 7/11 düzeltildi |
| Dört başka video (43 klip) | 3 | 2 | yanlış kabul 0 |

Gerçekçi beklenti ikinci satırdır: ilk satırda sözlük o videoyu görmüştü. Tek bir video için maliyet yaklaşık 0,001 dolar.

## Sözlük

`src/turkce_asr_ozel_isim/data/lexicon.json`: **179 kayıt** (128 kişi, 51 şirket), 51 yanlış yazım. Yalnız adı Wikidata'da ya da kendi röportajının başlığında veya kanalında geçen kişi ve şirketler var. Transkript, video ya da iletişim bilgisi içermez.

## Katkı: isim ekle, isim kaldır

Whisper'ın bozduğu bir ad mı gördünüz? [İsim ekle formunu](https://github.com/mustafayusufaksoy/turkce-asr-ozel-isim/issues/new?template=isim-ekle.yml) doldurun ya da pull request açın, ayrıntılar [CONTRIBUTING](CONTRIBUTING.md) dosyasında. Her ekleme otomatik testlerden ve insan incelemesinden geçer.

Adınızın listeden çıkarılmasını istiyorsanız [kaldırma formunu](https://github.com/mustafayusufaksoy/turkce-asr-ozel-isim/issues/new?template=isim-kaldir.yml) kullanın; gerekçe istemiyoruz.

## Sınırlar

- Sözlükte olmayan yeni yanlış yazım yalnız kişilerde, ad + soyad birlikte geçiyorsa bulunur. Şirketlerde yazımın sözlükte kayıtlı olması gerekir.
- Sözlük Türkiye girişim ve iş dünyası ağırlıklı.
- Model seçimleri her çalıştırmada birebir aynı olmayabilir.

## Sık sorulanlar

**Whisper Türkçe isimleri neden yanlış yazıyor?** Modelin eğitim verisinde az geçen adları sesçe en yakın bildiği kelimelere benzetir. `initial_prompt` ya da `hotwords` yardımcı olur, ama uzun bir ad listesi vermek pratik değildir.

**WhisperX ve faster-whisper ile çalışır mı?** Evet. Kelime zaman damgalı JSON çıktısı olan her araçla çalışır.

**Altyazı (SRT, ASS) dosyası ile çalışır mı?** Doğrudan değil. Düzeltilmiş JSON'dan altyazınızı üretin; zaman damgaları korunur.

**Claude zorunlu mu?** Hayır. Adayları kendiniz inceleyebilir ya da başka bir model bağlayabilirsiniz.

## Yol haritası

- Daha fazla videoda önce/sonra ölçümü
- Şirketlerde bilinmeyen yazım araması
- Kendi transkript arşivinizden sözlük çıkaran araç

## Lisans

Kod [MIT](LICENSE). Ad listesi [CC0 1.0](LICENSE-DATA).

---

## English

**Open source Python tool and lexicon that fixes misheard Turkish people and company names in Whisper and WhisperX transcripts.** Useful for subtitles, podcasts, YouTube and short-form video.

Speech-to-text models consistently misspell Turkish proper nouns, and asking an LLM to fix them fails when the model does not know the name. This project uses a three-step pipeline: a lexicon and fuzzy matching propose candidates, a selector returns only candidate **numbers** so it cannot invent a name, and code applies the change while preserving punctuation, Turkish suffixes and word timestamps.

```bash
pip install "turkce-asr-ozel-isim[claude]"
turkce-asr-ozel-isim transcript.json --selector claude -o fixed.json
```

Measured on real podcast clips with Claude Haiku 5.5: 10 of 11 errors fixed with the full lexicon, 7 of 11 when spellings learned from that video were removed, and no false accepts across 43 clips from four other videos. This is a small sample.

The lexicon has 179 records of public figures and companies and contains no transcripts or contact details. Code is MIT, the name list is CC0. Contributions and removal requests are welcome through GitHub issues.
