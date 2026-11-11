# Sürüm çıkarma ve PyPI yayını

Paket PyPI'da: <https://pypi.org/project/turkce-asr-ozel-isim/>. İlk sürüm `v0.1.0`, 11 Kasım 2026.

## Yeni sürüm nasıl çıkar

1. `pyproject.toml` içindeki `version` değerini artır, `main`'e birleştir.
2. GitHub'da aynı numarayla bir release yayımla (`v0.2.0` gibi):

   ```bash
   gh release create v0.2.0 --target main --title "v0.2.0" --notes "..."
   ```

3. `publish` iş akışı paketi derleyip PyPI'a yollar. Bittiğini `gh run list --workflow publish.yml` ile gör.

PyPI aynı sürüm numarasını ikinci kez kabul etmez; hatalı bir sürüm silinse bile numarası yeniden kullanılamaz. Sözlüğe isim eklemek de yeni sürüm ister: `pip` ile kuranlar sözlüğü paketin içinden alır.

## Yayın nasıl çalışıyor

- Şifre ya da API anahtarı yok. PyPI, GitHub Actions'a "trusted publisher" olarak güvenir; repoda saklanan bir gizli değer bulunmaz.
- PyPI'daki tanım: sahip `mustafayusufaksoy`, repo `turkce-asr-ozel-isim`, iş akışı `publish.yml`, ortam `pypi`. Bu dört değerden biri değişirse (dosya adı, ortam adı, repo taşınması) yayın reddedilir; PyPI'da proje ayarlarındaki Publishing sayfasından güncellenir.
- İş akışı yalnız release **yayımlanınca** çalışır; `main`'e push yayın yapmaz.
- PyPI hesabında iki adımlı doğrulama açık olmalı, yoksa yayıncı ayarlarına girilemez.

## Lisans dosyaları

Kod MIT (`LICENSE`), sözlük CC0 (`LICENSE-DATA`). İkisini tek dosyada birleştirme: GitHub lisansı tanıyamaz ve repo sayfasında "Other" yazar. İki dosya da pakete kendiliğinden girer.

## Testler ve Python 3.9

`test` iş akışı `ubuntu-24.04`'e sabit. `ubuntu-latest` (26.04) Python 3.9 sunmuyor ve kurulum adımında düşüyor. GitHub 24.04 runner'ını kaldırdığında en düşük sürümü 3.10'a çek: `pyproject.toml` → `requires-python`, test matrisi ve README'deki "Python 3.9 ve üzeri" birlikte değişir.
