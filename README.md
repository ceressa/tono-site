# tono-site

[tono.dozi.app](https://tono.dozi.app) - Tono'nun tanitim sayfasi, gizlilik
politikasi, kullanim kosullari ve hesap silme sayfasi.

Oyun deposu ayri: `com.bardino.tono`, `C:\Users\Ufuk\dev\mobile\tono`,
GitHub'da `ceressa/tono` (private).

Kalip `palmo-site`den alindi. `build.py` iskeleti ve `config.py` duzeni ayni;
**`legal_text.py` kopyalanmadi**, asagida sebebi var.

## Sayfalar elle yazilmaz, uretilir

```powershell
python build.py
```

**Uretilen `.html` dosyalarini elle duzenleme**, bir sonraki derlemede geri
gider. Uretilenler: `index.html`, `tr|de|es|fr|pt/index.html`, `privacy.html`,
`terms.html`, `account-deletion.html` (kokte ve `tr/` altinda), `404.html`,
`sitemap.xml`, `robots.txt`, `manifest.json`, `.nojekyll`.

- Acilis sayfasi alti dilde: **en (kok)**, tr, de, es, fr, pt.
- Yasal sayfalar yalnizca Ingilizce ve Turkce. Yarim cevrilmis bir sozlesme
  cevrilmemis olandan kotudur; diger dillerin altbilgisi Ingilizceye gider.

`build.py` derleme sonunda eksikleri listeler. O liste is listesidir, hata
degil.

Yerelde bakmak icin (mutlak yollar `/css/...` oldugu icin dosyayi cift
tiklamak yetmez):

```powershell
python -m http.server 8099 --bind 127.0.0.1
```

## Yasal metin Palmo'dan KOPYALANMADI

Palmo'nun `legal_text.py` dosyasi Firebase, bulut kaydi, anonim kimlik,
analitik ve cokme raporu anlatiyor. **Tono'da bunlarin hicbiri yok.** Metin
Tono'nun kendi kodundan yazildi ve her iddianin kaynagi `legal_text.py`
basindaki not icinde dosya ve satir olarak yaziyor.

Ozetle bugunku gercek:

| Iddia | Kaynak |
|---|---|
| Hesap yok, sunucu yok, analitik yok | `pubspec.yaml` (firebase_* hic yok) |
| Yayin surumunde reklam GOSTERILMIYOR | `lib/ads.dart:81` `haveRealUnits = false`, `start()` icinde `if (!enabled) return;` |
| AdMob SDK'si hic BASLATILMIYOR | ayni yer: UMP rizasi, ATT sorusu ve `initialize` o donusun arkasinda |
| Reklamsiz satin alma SUNULMUYOR | `lib/ui/settings_page.dart:182`, satir `Ads.enabledInRelease` kapisinda |
| Cihazda saklananlar | `stars.<n>`, `music`, `sfx`, `haptics`, `billing.noAds` |

**`haveRealUnits` true yapilirsa** bu sayfalar ve Play'deki veri guvenligi
beyani, o surum yayimlanmadan **once** guncellenir. Sonra degil.

## Elle guncellenecek dosyalar

Bunlar uretilmiyor, repoda elle duruyor:

| Dosya | Ne zaman |
|---|---|
| `CNAME` | Bir kez, konuldu: `tono.dozi.app` |
| `app-ads.txt` | AdMob listesi degistikce (bkz. dosyanin kendi basligi) |
| `assets/tono-mark.svg`, `assets/tono-lockup-h.svg` | Marka degisirse |
| `assets/shots/*.webp` | Ekran goruntuleri cekilince |
| `assets/tono-share.png` | Feature graphic hazir olunca (1200x630) |
| `assets/tono-icon.png` | apple-touch-icon (180x180) |

## Marka isareti

`assets/tono-mark.svg` geometrisi `lib/design/mark.dart` icindeki `TonoMark`
ile **birebir**: birim kare 200, cubuk `x=20 w=160 h=44`, ustler 14/78/142,
yaricap 12, kontur 7. Renkler `Tone.ramp[2]`, `[4]`, `[6]`. Uygulamada
degisirse burasi da degisir.

Palmo'nun yazi tipi borcu burada **yok**: isarette hic `<text>` yok, yalnizca
uc dikdortgen. Favicon her makinede ayni ciziliyor. Yalniz `tono-lockup-h.svg`
"TONO" kelimesini `<text>` olarak tasiyor, o yuzden kilit sayfaya gomulu
yaziliyor (`build.inline_svg`) ve Nunito boylece uygulaniyor.

`mark.dart` kendi basinda "GECICI YER TUTUCU" diyor. Gercek isaret gelirse
once orasi, sonra burasi degisir.

## Yayin

GitHub Pages, `main` dali, kok dizin. Actions yok: `python build.py`
**yerelde** kosuluyor ve cikti commit ediliyor. `.nojekyll` uretiliyor.

DNS kaydi Ufuk'ta. Gereken tek kayit:

```
Tur   : CNAME
Ad    : tono            (yani tono.dozi.app)
Hedef : ceressa.github.io
TTL   : varsayilan
```

Kayit girilmeden once GitHub Pages "alan adi dogrulanmadi" der ve HTTPS
sertifikasi cikmaz; bu beklenen durumdur, kayit yayildiktan sonra Pages
ayarlarindan **Enforce HTTPS** isaretlenir.

Yayina aldiktan sonra tek tek GET ile geri oku, panelin "basarili" demesine
guvenme: `/`, `/tr/`, `/privacy.html`, `/tr/privacy.html`,
`/account-deletion.html`, `/sitemap.xml`, `/app-ads.txt`, ve olmayan bir yol
(404 dondugunu dogrula).

## Cikinca yapilacak

- Kahraman bolumundeki `.magaza-cip` iki `<span>`, cunku gidilecek yer yok.
  Magaza baglantilari hazir olunca ikisi `<a>` olur; metinler `build.py`
  icindeki `badge`, `endT`, `endS` anahtarlarinda.
- `assets/shots/` gercek karelerle dolar. Bugun `tool/render/` bos, yani
  dordu de yer tutucu.
