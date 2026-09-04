# -*- coding: utf-8 -*-
"""Yasal sayfa metinleri.

Yalnizca Ingilizce ve Turkce tam yazildi; acilis sayfasi alti dilde ama
sozlesme dort dilde daha yarim cevrilmis olsa kimseye faydasi olmazdi.
Diger dillerdeki altbilgi baglantilari Ingilizce surume gider.

METIN URUNUN GERCEK MIMARISINI ANLATIR. palmo-site'in `legal_text.py`
dosyasindan KOPYALANMADI: Palmo'nunki Firebase, bulut kaydi, anonim kimlik,
analitik ve cokme raporu anlatiyor ve Tono'da bunlarin HICBIRI yok.

Kaynak dosyalar ve her iddianin nereden dogrulandigi (2026-09-04'te okundu):
  `pubspec.yaml`            firebase_* YOK, analitik YOK, cokme raporu YOK.
                            Olanlar: shared_preferences, audioplayers,
                            google_mobile_ads, in_app_purchase,
                            app_tracking_transparency, package_info_plus,
                            url_launcher
  `lib/ads.dart`            `haveRealUnits = false` (81. satir).
                            `enabled => (haveRealUnits || kDebugMode)` ve
                            `start()` ilk satiri `if (!enabled) return;`
                            (183-184). YAYIN SURUMUNDE AdMob SDK'si HIC
                            BASLATILMIYOR: UMP riza formu, ATT sorusu ve
                            `MobileAds.initialize` uc de hic calismiyor.
  `lib/billing.dart`        `com.bardino.tono.remove_ads`, non-consumable.
                            `start()` KOSULSUZ calisiyor: uygulama acilista
                            Google Play Faturalandirma'ya sorar.
  `lib/ui/settings_page.dart` 182. satir: reklamsiz satin alma satiri
                            `Ads.enabledInRelease` kapisinda. Bugunku yayin
                            surumunde o satir CIZILMIYOR, yani satin alma
                            oyuncuya sunulmuyor.
  `lib/state/progress.dart` `stars.<n>` anahtarlari, `reset()`
  `lib/state/settings.dart` `music`, `sfx`, `haptics`

BIR SEY BILEREK BOYLE YAZILDI, kisaltilmasin: bu surumde reklam
GOSTERILMIYOR ve satin alma SUNULMUYOR. Metin ikisini de "su an yok, acilirsa
sayfa once guncellenir" diye anlatiyor. `haveRealUnits` true yapilirsa bu
dosya yayindan ONCE degisir; yoksa sayfa uygulamayla celisir ve Play'in veri
guvenligi beyani da yanlis olur.
"""

from config import MAIL, PKG, DEV, APP


def _p(*paras):
    return "".join("<p>%s</p>" % x for x in paras)


def _ul(*items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in items)


def _ol(*items):
    """Numarali adim listesi.

    Google'in veri silme formu "kullanicinin uygulamasi gereken adimlari
    belirgin sekilde goster" diyor ve isaretli liste bir SIRA soylemiyor.
    """
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % x for x in items)


def _mail():
    return '<a href="mailto:%s">%s</a>' % (MAIL, MAIL)


def _h(x):
    return "<h2>%s</h2>" % x


# -- Gizlilik ---------------------------------------------------------------

PRIVACY_EN = (
    _p("%s is a puzzle game published by %s. This policy describes what the "
       "game does with data. It is short because the game does very little: "
       "it has no account, no sign-in, no server of its own, and it does not "
       "build a profile of you." % (APP, DEV))

    + _h("The short version")
    + _p("%s does not collect personal data, and nothing you do in the game "
         "is sent to us. There is no analytics SDK and no crash reporting "
         "SDK in the build. We never see your progress, your settings, or "
         "that you installed the game at all." % APP)

    + _h("What is stored on your device")
    + _p("Everything the game remembers is written to your phone's own app "
         "storage and stays there. Nothing in this list leaves the device:")
    + _ul("your progress: for each level you finished, the best star count "
          "(<code>stars.1</code>, <code>stars.2</code> and so on);",
          "your settings: music level, sound-effects level and whether "
          "haptics are on;",
          "a flag recording whether the ad-free purchase was made, and two "
          "counters the ad pacing would use. In this version nothing sets "
          "them, because no ads are shown.")
    + _p("This data has no name, no e-mail and no identifier attached to it. "
         "Deleting the app removes all of it. You can also clear the "
         "progress from inside the game, see the deletion page.")

    + _h("Advertising: none in this version")
    + _p("The build carries Google's Mobile Ads library, but it is switched "
         "off. In the code the switch is <code>haveRealUnits</code> and it is "
         "<code>false</code>, and the ad system returns before it starts. "
         "The practical consequences are worth stating plainly:")
    + _ul("no ad is ever requested and no ad is ever shown;",
          "the Google Mobile Ads SDK is <strong>never initialised</strong>, "
          "so it makes no network request and reads no advertising ID;",
          "you are never shown a consent form, and on iOS the app never asks "
          "for App Tracking Transparency permission, because that request "
          "only happens on the code path that starts the ad system.")
    + _p("If ads are ever switched on, this page will be updated and the "
         "store's data safety declaration corrected <em>before</em> that "
         "version is published, not after.")

    + _h("Purchases")
    + _p("The game contains a one-time, non-consumable product "
         "(<code>%s.remove_ads</code>) that removes ads. In this version it "
         "is <strong>not offered</strong>: the settings row that would sell "
         "it is hidden while ads are off, so there is nothing to buy."
         % PKG)
    + _p("The game does still ask Google Play Billing whether the product "
         "exists and whether you already own it, which happens when the app "
         "starts. That conversation is between your device and Google Play. "
         "We never receive your payment details: card numbers and billing "
         "addresses go to Google, never to us, and we could not see them if "
         "we wanted to.")

    + _h("Children")
    + _p("%s is suitable for all ages, and because it collects nothing it "
         "collects nothing from children either. There is no chat, no "
         "user-generated content, no social feature and no link out to a "
         "social network." % APP)

    + _h("Permissions")
    + _p("The game asks for no runtime permissions. It needs no camera, no "
         "microphone, no contacts, no location and no files. It plays "
         "offline; an internet connection is only used by Google Play "
         "Billing, and the game works without one.")

    + _h("Third parties")
    + _p("Two Google services can be involved and neither receives anything "
         "we send them:")
    + _ul("<strong>Google Play</strong> distributes the app and handles "
          "billing, under Google's own privacy policy;",
          "<strong>Google Mobile Ads</strong> ships inside the app but is "
          "dormant in this version, as described above.")

    + _h("Changes")
    + _p("If this policy changes, the date at the top of the page changes "
         "with it. The pages are generated from a single source, so a date "
         "here means that page actually changed.")

    + _h("Contact")
    + _p("Questions, or a request about your data: %s." % _mail())
)

PRIVACY_TR = (
    _p("%s, %s tarafindan yayimlanan bir bulmaca oyunudur. Bu politika oyunun "
       "veriyle ne yaptigini anlatir. Kisa olmasinin sebebi oyunun cok az sey "
       "yapmasi: hesap yok, giris yok, kendi sunucusu yok ve hakkinizda bir "
       "profil olusturmuyor." % (APP, DEV))

    + _h("Kisa hali")
    + _p("%s kisisel veri toplamaz ve oyunda yaptiginiz hicbir sey bize "
         "gonderilmez. Pakette analitik SDK'si ve cokme raporu SDK'si yoktur. "
         "Ilerlemenizi, ayarlarinizi, hatta oyunu kurdugunuzu bile gormeyiz."
         % APP)

    + _h("Cihazinizda ne saklaniyor")
    + _p("Oyunun hatirladigi her sey telefonunuzun kendi uygulama alanina "
         "yazilir ve orada kalir. Bu listedeki hicbir sey cihazdan cikmaz:")
    + _ul("ilerlemeniz: bitirdiginiz her bolum icin en iyi yildiz sayisi "
          "(<code>stars.1</code>, <code>stars.2</code> gibi);",
          "ayarlariniz: muzik kademesi, ses efekti kademesi ve titresimin "
          "acik olup olmadigi;",
          "reklamsiz satin almanin yapilip yapilmadigini tutan bir isaret ve "
          "reklam araligini olcecek iki sayac. Bu surumde ikisini de hicbir "
          "sey yazmiyor, cunku reklam gosterilmiyor.")
    + _p("Bu verinin yaninda isim, e-posta ya da bir tanimlayici yoktur. "
         "Uygulamayi kaldirmak hepsini siler. Ilerlemeyi oyunun icinden de "
         "temizleyebilirsiniz, bkz. silme sayfasi.")

    + _h("Reklam: bu surumde yok")
    + _p("Pakette Google'in Mobile Ads kutuphanesi var ama kapali. Koddaki "
         "anahtarin adi <code>haveRealUnits</code> ve degeri <code>false</code>; "
         "reklam sistemi baslamadan geri donuyor. Bunun pratikte anlami "
         "acikca yazilmaya deger:")
    + _ul("hicbir reklam istenmiyor ve hicbir reklam gosterilmiyor;",
          "Google Mobile Ads SDK'si <strong>hic baslatilmiyor</strong>, yani "
          "ag istegi atmiyor ve reklam kimligini okumuyor;",
          "size hicbir riza formu gosterilmiyor ve iOS'ta uygulama App "
          "Tracking Transparency izni hic istemiyor, cunku o istek yalnizca "
          "reklam sistemini baslatan yolda yapiliyor.")
    + _p("Reklam ileride acilirsa bu sayfa guncellenir ve magazadaki veri "
         "guvenligi beyani duzeltilir; bunlar o surum yayimlanmadan "
         "<em>once</em> olur, sonra degil.")

    + _h("Satin alma")
    + _p("Oyunda reklamlari kaldiran tek seferlik, tuketilmeyen bir urun var "
         "(<code>%s.remove_ads</code>). Bu surumde <strong>sunulmuyor</strong>: "
         "onu satacak ayar satiri, reklamlar kapaliyken cizilmiyor, yani "
         "satin alinacak bir sey yok." % PKG)
    + _p("Oyun yine de acilista Google Play Faturalandirma'ya urunun var olup "
         "olmadigini ve sizin zaten sahip olup olmadiginizi sorar. Bu "
         "konusma cihazinizla Google Play arasindadir. Odeme bilgilerinizi "
         "biz hicbir zaman almayiz: kart numarasi ve fatura adresi Google'a "
         "gider, bize gelmez; istesek de goremeyiz.")

    + _h("Cocuklar")
    + _p("%s her yasa uygundur ve hicbir sey toplamadigi icin cocuklardan da "
         "hicbir sey toplamaz. Sohbet yok, kullanici uretimi icerik yok, "
         "sosyal ozellik yok ve sosyal aga cikan bir baglanti yok." % APP)

    + _h("Izinler")
    + _p("Oyun calisma zamaninda hicbir izin istemez. Kamera, mikrofon, "
         "rehber, konum ve dosya erisimi gerekmez. Cevrimdisi oynanir; "
         "internet yalnizca Google Play Faturalandirma icin kullanilir ve "
         "oyun internetsiz de calisir.")

    + _h("Ucuncu taraflar")
    + _p("Iki Google hizmeti devreye girebilir ve ikisi de bizim "
         "gonderdigimiz bir sey almaz:")
    + _ul("<strong>Google Play</strong> uygulamayi dagitir ve faturalandirmayi "
          "yurutur, kendi gizlilik politikasi altinda;",
          "<strong>Google Mobile Ads</strong> uygulamanin icinde gelir ama bu "
          "surumde uykudadir, yukarida anlatildigi gibi.")

    + _h("Degisiklikler")
    + _p("Bu politika degisirse sayfanin ustundeki tarih de degisir. Sayfalar "
         "tek kaynaktan uretiliyor, yani buradaki bir tarih o sayfanin "
         "gercekten degistigi anlamina gelir.")

    + _h("Iletisim")
    + _p("Soru ya da verinizle ilgili bir talep: %s." % _mail())
)


# -- Kullanim kosullari -----------------------------------------------------

TERMS_EN = (
    _p("These terms cover %s, the mobile game published by %s. Installing or "
       "playing the game means you accept them." % (APP, DEV))

    + _h("Licence")
    + _p("You get a personal, non-exclusive, non-transferable licence to "
         "install and play %s on devices you control, for as long as you "
         "keep to these terms. The game and everything in it stays ours." % APP)

    + _h("What you may not do")
    + _ul("take the game apart, decompile it, or try to derive its source, "
          "except where the law says you may;",
          "redistribute, resell, rent or sublicense the app or its assets;",
          "modify the app to change how progress or purchases work.")

    + _h("Price and purchases")
    + _p("%s is free to play. The game contains a single optional one-time "
         "product that removes ads. In the current version that product is "
         "not offered for sale, because the version shows no ads. If it is "
         "offered later, it will be a non-consumable purchase: bought once, "
         "restored on the same store account." % APP)
    + _p("Every purchase and every refund is handled by the store you "
         "installed from, under that store's rules. We cannot issue a refund "
         "ourselves. On Google Play, refund requests go to Google Play.")

    + _h("Your progress")
    + _p("Progress lives only on your device. There is no account and no "
         "cloud save, and that has a consequence worth being blunt about: "
         "<strong>if you uninstall the game, change phone, or clear the "
         "app's data, your progress is gone and we cannot restore it.</strong> "
         "We have no copy, because we never had one.")

    + _h("No warranty")
    + _p("The game is provided as it is. We do not promise it is free of "
         "faults or that it will run on every device. To the extent the law "
         "allows, %s is not liable for indirect or consequential loss "
         "arising from using the game. Nothing here limits rights you have "
         "under consumer law that cannot be limited." % DEV)

    + _h("Ending the licence")
    + _p("You can end it at any time by deleting the app. We may end it if "
         "you break these terms. If the game is withdrawn from a store, "
         "copies already installed keep working; we do not switch them off "
         "remotely.")

    + _h("Changes")
    + _p("These terms can change as the game changes. The date at the top of "
         "this page tells you when it last did.")

    + _h("Contact")
    + _p("%s. Written questions get written answers: %s." % (DEV, _mail()))
)

TERMS_TR = (
    _p("Bu kosullar, %s tarafindan yayimlanan mobil oyun %s icin gecerlidir. "
       "Oyunu kurmak ya da oynamak kosullari kabul ettiginiz anlamina gelir."
       % (DEV, APP))

    + _h("Lisans")
    + _p("%s'yu kendi kontrolunuzdeki cihazlara kurup oynamak icin kisisel, "
         "munhasir olmayan ve devredilemez bir lisans alirsiniz; bu kosullara "
         "uydugunuz surece gecerlidir. Oyun ve icindeki her sey bizde kalir."
         % APP)

    + _h("Yapamayacaklariniz")
    + _ul("oyunu parcalarina ayirmak, tersine derlemek ya da kaynagini "
          "cikarmaya calismak (kanunun izin verdigi haller disinda);",
          "uygulamayi ya da varliklarini yeniden dagitmak, satmak, kiralamak "
          "veya alt lisanslamak;",
          "ilerlemenin ya da satin almalarin isleyisini degistirmek icin "
          "uygulamayi degistirmek.")

    + _h("Fiyat ve satin alma")
    + _p("%s ucretsiz oynanir. Oyunda reklamlari kaldiran, istege bagli ve "
         "tek seferlik bir urun vardir. Su anki surumde bu urun satisa "
         "sunulmuyor, cunku surum hic reklam gostermiyor. Ileride sunulursa "
         "tuketilmeyen bir satin alma olacak: bir kez alinir, ayni magaza "
         "hesabinda geri yuklenir." % APP)
    + _p("Her satin alma ve her iade, uygulamayi kurdugunuz magaza tarafindan "
         "ve o magazanin kurallarina gore yurutulur. Iadeyi biz veremeyiz. "
         "Google Play'de iade talepleri Google Play'e gider.")

    + _h("Ilerlemeniz")
    + _p("Ilerleme yalnizca cihazinizda durur. Hesap yok, bulut kaydi yok ve "
         "bunun acikca soylenmesi gereken bir sonucu var: <strong>oyunu "
         "kaldirirsaniz, telefon degistirirseniz ya da uygulamanin verisini "
         "temizlerseniz ilerlemeniz gider ve biz geri getiremeyiz.</strong> "
         "Bizde bir kopyasi yok, cunku hic olmadi.")

    + _h("Garanti yok")
    + _p("Oyun oldugu gibi sunulur. Hatasiz oldugunu ya da her cihazda "
         "calisacagini vaat etmiyoruz. Kanunun izin verdigi olcude, %s oyunun "
         "kullanimindan dogan dolayli zararlardan sorumlu degildir. Buradaki "
         "hicbir ifade, tuketici mevzuatindan dogan ve sinirlandirilamayan "
         "haklarinizi sinirlamaz." % DEV)

    + _h("Lisansin sona ermesi")
    + _p("Uygulamayi silerek istediginiz zaman bitirebilirsiniz. Bu kosullari "
         "ihlal ederseniz biz bitirebiliriz. Oyun bir magazadan cekilirse "
         "kurulu kopyalar calismaya devam eder; uzaktan kapatmayiz.")

    + _h("Degisiklikler")
    + _p("Oyun degistikce bu kosullar da degisebilir. Sayfanin ustundeki "
         "tarih en son ne zaman degistigini soyler.")

    + _h("Iletisim")
    + _p("%s. Yazili soruya yazili cevap: %s." % (DEV, _mail()))
)


# -- Hesap silme ------------------------------------------------------------
# Google'in "veri silme" gereksinimi hesap OLMAYAN uygulamalar icin de bir
# adres istiyor. Sayfa bu yuzden once "hesap yok" diyor, sonra veriyi gercekten
# silen iki yolu numarali adimlarla veriyor.

DELETE_EN = (
    _p("Google asks every app to publish a page explaining how to delete your "
       "account and your data. For %s the first half of that answer is "
       "short." % APP)

    + _h("There is no account to delete")
    + _p("%s has no sign-up, no sign-in and no user account. We hold no "
         "server-side record of you: not a profile, not your progress, not "
         "an e-mail address. There is nothing on our side to delete, because "
         "nothing was ever created." % APP)

    + _h("Deleting the data on your device")
    + _p("Everything the game stores is on your phone. There are two ways to "
         "remove it, and they remove different amounts.")
    + _p("<strong>To clear your progress but keep the game:</strong>")
    + _ol("open %s;" % APP,
          "tap the settings button (the gear) on the main screen;",
          "scroll to <em>Reset progress</em> and tap it;",
          "confirm. Every level goes back to unfinished and every star is "
          "cleared.")
    + _p("<strong>To remove everything:</strong>")
    + _ol("uninstall %s the way you uninstall any app (on Android: press and "
          "hold the icon, then <em>Uninstall</em>; or Settings &rarr; Apps "
          "&rarr; %s &rarr; Uninstall);" % (APP, APP),
          "that deletes the app's storage with it: progress, settings and "
          "the purchase flag. Nothing is left behind.")
    + _p("On Android you can also clear the data without uninstalling: "
         "Settings &rarr; Apps &rarr; %s &rarr; Storage &rarr; "
         "<em>Clear data</em>." % APP)

    + _h("What survives, and where")
    + _p("Two things are outside the game and deleting the app does not touch "
         "them, because they belong to the store rather than to us:")
    + _ul("your purchase history at Google Play, if you ever buy the ad-free "
          "product. That record is Google's, is kept under Google's policy, "
          "and is what lets the purchase be restored if you reinstall;",
          "the fact that you installed the app, which Google Play records "
          "against your Google account, again under Google's policy.")
    + _p("Neither of these is something we can delete for you. To act on "
         "them, use your Google account settings.")

    + _h("How long we keep your data")
    + _p("We keep none of it, so there is no retention period to state. The "
         "data lives on your device for exactly as long as you keep the app.")

    + _h("If you would rather ask us")
    + _p("Write to %s and we will answer. Be aware of what we can honestly "
         "offer: we can explain and confirm the above, but we cannot delete "
         "data from your phone remotely and we have no copy of it to delete."
         % _mail())
)

DELETE_TR = (
    _p("Google her uygulamadan, hesabin ve verinin nasil silinecegini "
       "anlatan bir sayfa yayimlamasini istiyor. %s icin bu cevabin ilk "
       "yarisi kisa." % APP)

    + _h("Silinecek bir hesap yok")
    + _p("%s'da kayit yok, giris yok ve kullanici hesabi yok. Sunucu "
         "tarafinda hakkinizda hicbir kayit tutmuyoruz: ne profil, ne "
         "ilerleme, ne e-posta adresi. Bizim tarafta silinecek bir sey yok, "
         "cunku hicbir zaman olusmadi." % APP)

    + _h("Cihazinizdaki veriyi silmek")
    + _p("Oyunun sakladigi her sey telefonunuzda. Silmenin iki yolu var ve "
         "ikisi farkli miktarda siliyor.")
    + _p("<strong>Ilerlemeyi temizleyip oyunu tutmak icin:</strong>")
    + _ol("%s'yu acin;" % APP,
          "ana ekrandaki ayarlar dugmesine (disli) dokunun;",
          "<em>Ilerlemeyi sifirla</em> satirina kadar inin ve dokunun;",
          "onaylayin. Butun bolumler bitmemis hale doner ve butun yildizlar "
          "silinir.")
    + _p("<strong>Her seyi silmek icin:</strong>")
    + _ol("%s'yu her uygulamayi kaldirdiginiz gibi kaldirin (Android'de: "
          "simgeye basili tutun, sonra <em>Kaldir</em>; ya da Ayarlar &rarr; "
          "Uygulamalar &rarr; %s &rarr; Kaldir);" % (APP, APP),
          "bu islem uygulamanin deposunu da siler: ilerleme, ayarlar ve satin "
          "alma isareti. Geride bir sey kalmaz.")
    + _p("Android'de kaldirmadan da temizleyebilirsiniz: Ayarlar &rarr; "
         "Uygulamalar &rarr; %s &rarr; Depolama &rarr; <em>Verileri temizle</em>."
         % APP)

    + _h("Ne kaliyor, nerede kaliyor")
    + _p("Iki sey oyunun disinda ve uygulamayi silmek onlara dokunmuyor, "
         "cunku bize degil magazaya aitler:")
    + _ul("reklamsiz urunu satin alirsaniz Google Play'deki satin alma "
          "gecmisiniz. O kayit Google'in, Google'in politikasi altinda "
          "tutulur ve yeniden kurdugunuzda satin almanin geri yuklenmesini "
          "saglayan sey odur;",
          "uygulamayi kurdugunuz bilgisi; Google Play bunu Google hesabiniza "
          "isler, yine Google'in politikasi altinda.")
    + _p("Bu ikisini sizin adiniza silemeyiz. Islem yapmak icin Google hesap "
         "ayarlarinizi kullanin.")

    + _h("Veriyi ne kadar sakliyoruz")
    + _p("Hicini saklamiyoruz, o yuzden belirtilecek bir saklama suresi de "
         "yok. Veri, uygulamayi tuttugunuz sure boyunca cihazinizda durur.")

    + _h("Bize sormayi tercih ederseniz")
    + _p("%s adresine yazin, cevaplayalim. Durustce ne sunabilecegimizi "
         "bilerek yazin: yukaridakileri aciklayabilir ve teyit edebiliriz ama "
         "telefonunuzdaki veriyi uzaktan silemeyiz ve silecek bir kopyamiz "
         "yok." % _mail())
)


_PAGES = {
    "en": [
        ("privacy.html", "Privacy policy",
         "What %s keeps on your device and why nothing leaves it: no account, "
         "no analytics, no crash reporting, and an ad library that is never "
         "started in this version." % APP,
         PRIVACY_EN),
        ("terms.html", "Terms of use",
         "The licence, the one optional purchase that is not currently "
         "offered, and the blunt fact that progress lives only on your "
         "device.",
         TERMS_EN),
        ("account-deletion.html", "Account deletion",
         "%s has no account. Numbered steps to reset progress inside the "
         "game or remove every trace from the device, and what stays with "
         "Google Play." % APP,
         DELETE_EN),
    ],
    "tr": [
        ("privacy.html", "Gizlilik politikası",
         "%s'nun cihazınızda ne sakladığı ve hiçbirinin neden dışarı "
         "çıkmadığı: hesap yok, analitik yok, çökme raporu yok ve bu sürümde "
         "hiç başlatılmayan bir reklam kütüphanesi." % APP,
         PRIVACY_TR),
        ("terms.html", "Kullanım koşulları",
         "Lisans, şu an satışa sunulmayan tek isteğe bağlı satın alma, ve "
         "ilerlemenin yalnızca cihazınızda durduğu gerçeği.",
         TERMS_TR),
        ("account-deletion.html", "Hesap silme",
         "%s'da hesap yoktur. Oyun içinden ilerlemeyi sıfırlamak ya da "
         "cihazdaki her izi silmek için numaralı adımlar, ve Google Play'de "
         "ne kaldığı." % APP,
         DELETE_TR),
    ],
}


def pages(code):
    """(dosya, baslik, meta aciklama, govde) dortlulerini dondurur."""
    return _PAGES.get(code, _PAGES["en"])
