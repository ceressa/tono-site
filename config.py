# -*- coding: utf-8 -*-
"""Sitenin TEK sabit kaynagi.

Kalip palmo-site'den alindi: `build.py` ve `legal_text.py` ikisi de buradan
okur, boylece bir sabit iki dosyada ayri ayri yazilip aralarinda ayrisamaz.

Alan adi da tek yerde: `CNAME` dosyasi elle konuldugu icin (bkz. README)
icerigi `DOMAIN` ile ayni olmali, `build.py` derlemede bunu kontrol eder.
"""

SITE = "https://tono.dozi.app"
DOMAIN = SITE.split("//", 1)[1]
PKG = "com.bardino.tono"
MAIL = "info@dozi.app"
DEV = "Bardino Technology"
DEV_URL = "https://dozi.app"
APP = "Tono"

# Sayfa basina son guncelleme. Bir sayfa degisince yalnizca onun tarihi
# yukseltilir; tek global tarih, degismemis sayfaya da yeni tarih yazdirir ve
# bu okuyan icin bir yalandir.
UPDATED = {
    "privacy.html": "2026-09-04",
    "terms.html": "2026-09-04",
    "account-deletion.html": "2026-09-04",
}

# Dil kodu -> (html lang, og locale, kendi dilindeki adi)
# Sira ve adlar uygulamanin `lib/l10n/strings.dart` dosyasindaki dil listesiyle
# ayni; iki taraf ayrismasin diye oradan alindi.
LANGS = [
    ("en", "en", "en_US", "English"),
    ("tr", "tr", "tr_TR", "Türkçe"),
    ("de", "de", "de_DE", "Deutsch"),
    ("es", "es", "es_ES", "Español"),
    ("fr", "fr", "fr_FR", "Français"),
    ("pt", "pt", "pt_BR", "Português"),
]

# Kok dizinin dili. Magaza kaydi varsayilan olarak Ingilizce listelenecek ve
# koke gelen ziyaretcinin cogu Turkce bilmiyor.
ROOT_LANG = "en"

# Yasal metin yalnizca bu dillerde tam yazildi. Yarim cevrilmis bir sozlesme,
# cevrilmemis olandan kotudur; diger dillerin altbilgisi Ingilizceye gider.
LEGAL_LANGS = {"en", "tr"}

LEGAL_PAGES = ("privacy.html", "terms.html", "account-deletion.html")
