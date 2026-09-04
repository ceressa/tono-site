# -*- coding: utf-8 -*-
"""tono.dozi.app sayfalarini uretir.

    python build.py

Neden uretici: alti dil x (acilis + yasal) elle tutulunca kaciniyor. Bir
cumleyi degistirmek icin alti dosyaya dokunmak, bes tanesinin bayat kalmasi
demek. Icerik burada sozluk, HTML ciktida. Uretilen .html dosyalarini elle
duzenleme.

Sabitler `config.py` icinde, yasal metinler `legal_text.py` icinde.

EKSIK GORSEL YALAN SOYLETMEZ: ekran goruntusu ya da paylasim gorseli diskte
yoksa o bolum yer tutucuya duser ve <meta og:image> hic yazilmaz. Dosya
konulup yeniden derlenince bolum kendiliginden gercege doner.
"""
import io
import os
import re

from config import (APP, DEV, DEV_URL, DOMAIN, LANGS, LEGAL_LANGS, LEGAL_PAGES,
                    PKG, ROOT_LANG, SITE, UPDATED)

HERE = os.path.dirname(os.path.abspath(__file__))

# Vitrindeki dort kare. HENUZ HICBIRI YOK: tool/render/ bos, o yuzden dordu de
# yer tutucuya dusuyor ve olmayan dosyaya baglanti verilmiyor.
SHOTS = ["01_board.webp", "02_pour.webp", "03_result.webp", "04_map.webp"]

SHARE = "assets/tono-share.png"   # 1200x630, magaza feature graphic'inden
ICON_PNG = "assets/tono-icon.png"  # apple-touch-icon, 180x180
MARK = "assets/tono-mark.svg"
LOCKUP = "assets/tono-lockup-h.svg"

T = {}

# Metin oyunun KENDI magaza metninden turetildi
# (android/fastlane/metadata/android/*/full_description.txt), yeniden
# uydurulmadi. Iki sey bilerek disarida birakildi: magaza metnindeki "dort
# bolumde bir reklam" ve "tek seferlik satin alma reklamlari kaldirir"
# satirlari. Bugunku yayin surumunde `haveRealUnits = false` ve reklam HIC
# gosterilmiyor, satin alma da sunulmuyor; siteye yazsaydik urunle celisirdi.

T["en"] = {
    "title": "Tono - One color, seven steps",
    "desc": "A quiet puzzle about tones. Pour until every tube holds a single "
            "tone. Sixty levels, no clock, free undo. Coming soon to Android.",
    "badge": "Coming soon",
    "h1a": "One color,",
    "h1b": "seven steps.",
    "lead": "Tono is a puzzle about tones. Every tube takes four units and "
            "all the pieces are steps of one color, a ladder from light to "
            "dark. Touch a tube, then touch another; if the top tones match, "
            "it pours. When every tube holds a single tone, the level is "
            "done.",
    "small": "Free to play. Works offline. No account.",
    "shotsT": "From the game",
    "shotsS": "Real screenshots, not mock-ups.",
    "caps": ["The board", "A tone pouring", "The end of a level", "The map"],
    "ph": "Screenshot coming",
    "endT": "Not out yet.",
    "endS": "Tono is still in the workshop. This page will carry the store "
            "links the day it is out.",
    "bandAlt": "Tono",
    "legal": ("Privacy", "Terms of use", "Account deletion"),
    "by": "Tono is made by",
    "back": "Back to Tono",
    "upd": "Last updated",
    "e404T": "Nothing here.",
    "e404S": "That page does not exist.",
}

T["tr"] = {
    "title": "Tono - Tek renk, yedi kademe",
    "desc": "Sessiz bir ton bulmacasi. Her tupte tek ton kalana kadar dok. "
            "Altmis bolum, sayac yok, geri alma serbest. Android'de yakinda.",
    "badge": "Çok yakında",
    "h1a": "Tek renk,",
    "h1b": "yedi kademe.",
    "lead": "Tono bir ton bulmacasıdır. Her tüp dört birim alır ve bütün "
            "parçalar tek bir rengin kademeleridir: açıktan koyuya bir "
            "merdiven. Bir tüpe dokun, sonra başkasına dokun; üstteki ton "
            "aynıysa dökülür. Her tüpte tek bir ton kalınca bölüm biter.",
    "small": "Ücretsiz oynanır. İnternetsiz çalışır. Hesap gerekmez.",
    "shotsT": "Oyundan kareler",
    "shotsS": "Hepsi gerçek ekran görüntüsü, temsili değil.",
    "caps": ["Tahta", "Dökülen bir ton", "Bölümün sonu", "Harita"],
    "ph": "Ekran görüntüsü yakında",
    "endT": "Henüz çıkmadı.",
    "endS": "Tono hâlâ atölyede. Çıktığı gün mağaza bağlantıları bu sayfada "
            "olacak.",
    "bandAlt": "Tono",
    "legal": ("Gizlilik", "Kullanım koşulları", "Hesap silme"),
    "by": "Tono'yu yapan",
    "back": "Tono'ya dön",
    "upd": "Son güncelleme",
    "e404T": "Burada bir şey yok.",
    "e404S": "Böyle bir sayfa yok.",
}

T["de"] = {
    "title": "Tono - Eine Farbe, sieben Stufen",
    "desc": "Ein ruhiges Tonrätsel. Gieße, bis jede Röhre nur noch einen Ton "
            "enthält. Sechzig Level, keine Uhr, freies Zurücknehmen.",
    "badge": "Demnächst",
    "h1a": "Eine Farbe,",
    "h1b": "sieben Stufen.",
    "lead": "Tono ist ein Rätsel über Töne. Jede Röhre fasst vier Einheiten, "
            "und alle Stücke sind Stufen einer Farbe: eine Leiter von hell "
            "nach dunkel. Tippe eine Röhre an, dann eine zweite; stimmen die "
            "oberen Töne überein, wird gegossen. Enthält jede Röhre nur noch "
            "einen Ton, ist das Level geschafft.",
    "small": "Kostenlos. Funktioniert offline. Kein Konto.",
    "shotsT": "Aus dem Spiel",
    "shotsS": "Echte Screenshots, keine Attrappen.",
    "caps": ["Das Spielfeld", "Ein Ton wird gegossen", "Das Ende eines Levels",
             "Die Karte"],
    "ph": "Screenshot folgt",
    "endT": "Noch nicht erschienen.",
    "endS": "Tono ist noch in der Werkstatt. Am Tag der Veröffentlichung "
            "stehen die Store-Links auf dieser Seite.",
    "bandAlt": "Tono",
    "legal": ("Datenschutz", "Nutzungsbedingungen", "Kontolöschung"),
    "by": "Tono stammt von",
    "back": "Zurück zu Tono",
    "upd": "Zuletzt aktualisiert",
    "e404T": "Hier ist nichts.",
    "e404S": "Diese Seite gibt es nicht.",
}

T["es"] = {
    "title": "Tono - Un color, siete pasos",
    "desc": "Un puzle tranquilo sobre tonos. Vierte hasta que cada tubo "
            "tenga un solo tono. Sesenta niveles, sin reloj, deshacer libre.",
    "badge": "Muy pronto",
    "h1a": "Un color,",
    "h1b": "siete pasos.",
    "lead": "Tono es un puzle sobre tonos. Cada tubo admite cuatro unidades y "
            "todas las piezas son pasos de un mismo color: una escalera de "
            "claro a oscuro. Toca un tubo y luego otro; si los tonos "
            "superiores coinciden, se vierte. Cuando cada tubo tiene un solo "
            "tono, el nivel termina.",
    "small": "Gratis. Funciona sin conexión. Sin cuenta.",
    "shotsT": "Del juego",
    "shotsS": "Capturas reales, no maquetas.",
    "caps": ["El tablero", "Un tono al verterse", "El final de un nivel",
             "El mapa"],
    "ph": "Captura en camino",
    "endT": "Aún no ha salido.",
    "endS": "Tono sigue en el taller. El día que salga, esta página tendrá "
            "los enlaces a las tiendas.",
    "bandAlt": "Tono",
    "legal": ("Privacidad", "Términos de uso", "Eliminación de cuenta"),
    "by": "Tono está hecho por",
    "back": "Volver a Tono",
    "upd": "Última actualización",
    "e404T": "Aquí no hay nada.",
    "e404S": "Esa página no existe.",
}

T["fr"] = {
    "title": "Tono - Une couleur, sept degrés",
    "desc": "Un puzzle calme sur les tons. Verse jusqu'à ce que chaque tube "
            "ne contienne qu'un seul ton. Soixante niveaux, sans chrono.",
    "badge": "Bientôt disponible",
    "h1a": "Une couleur,",
    "h1b": "sept degrés.",
    "lead": "Tono est un puzzle sur les tons. Chaque tube contient quatre "
            "unités et toutes les pièces sont les degrés d'une seule "
            "couleur : une échelle du clair au foncé. Touche un tube, puis un "
            "autre ; si les tons du dessus correspondent, ça se verse. Quand "
            "chaque tube ne contient qu'un ton, le niveau est terminé.",
    "small": "Gratuit. Fonctionne hors ligne. Sans compte.",
    "shotsT": "Du jeu",
    "shotsS": "De vraies captures, pas des maquettes.",
    "caps": ["Le plateau", "Un ton qui se verse", "La fin d'un niveau",
             "La carte"],
    "ph": "Capture à venir",
    "endT": "Pas encore sorti.",
    "endS": "Tono est encore à l'atelier. Le jour de sa sortie, cette page "
            "portera les liens vers les boutiques.",
    "bandAlt": "Tono",
    "legal": ("Confidentialité", "Conditions d'utilisation",
              "Suppression du compte"),
    "by": "Tono est fait par",
    "back": "Retour à Tono",
    "upd": "Dernière mise à jour",
    "e404T": "Il n'y a rien ici.",
    "e404S": "Cette page n'existe pas.",
}

T["pt"] = {
    "title": "Tono - Uma cor, sete degraus",
    "desc": "Um quebra-cabeça calmo sobre tons. Despeje até cada tubo ter um "
            "único tom. Sessenta níveis, sem relógio, desfazer livre.",
    "badge": "Em breve",
    "h1a": "Uma cor,",
    "h1b": "sete degraus.",
    "lead": "Tono é um quebra-cabeça sobre tons. Cada tubo leva quatro "
            "unidades e todas as peças são degraus de uma só cor: uma escada "
            "do claro ao escuro. Toque em um tubo e depois em outro; se os "
            "tons do topo forem iguais, ele despeja. Quando cada tubo tem um "
            "único tom, o nível termina.",
    "small": "Grátis. Funciona offline. Sem conta.",
    "shotsT": "Do jogo",
    "shotsS": "Capturas reais, não maquetes.",
    "caps": ["O tabuleiro", "Um tom sendo despejado", "O fim de um nível",
             "O mapa"],
    "ph": "Captura em breve",
    "endT": "Ainda não saiu.",
    "endS": "Tono ainda está na oficina. No dia em que sair, esta página vai "
            "ter os links das lojas.",
    "bandAlt": "Tono",
    "legal": ("Privacidade", "Termos de uso", "Exclusão de conta"),
    "by": "Tono é feito por",
    "back": "Voltar ao Tono",
    "upd": "Última atualização",
    "e404T": "Não há nada aqui.",
    "e404S": "Essa página não existe.",
}


# ── yollar ──────────────────────────────────────────────────────────────────
#
# URL ile DOSYA ayri: URL dizin bicimindedir (/tr/), dosya her zaman
# index.html'dir. Colmo sitesinde canonical /index.html'i, x-default ise /'i
# gosteriyordu; ayni belge iki adresle isaret ediliyordu.

def path_for(code, page):
    """Yayindaki URL yolu. Acilis sayfasi dizin olarak biter."""
    d = "" if code == ROOT_LANG else code + "/"
    return d if page == "index.html" else d + page


def file_for(code, page):
    """Diskteki dosya yolu."""
    return page if code == ROOT_LANG else "%s/%s" % (code, page)


def langs_with(page):
    """Bu sayfanin gercekten uretildigi diller.

    Yasal sayfalar yalnizca LEGAL_LANGS icin uretiliyor. Colmo'da dil cubugu ve
    hreflang bu filtreyi bilmiyordu ve her yasal sayfa uretilmemis dort dosyaya
    baglanti veriyordu: sayfa basina dort olu baglanti, dort hatali alternate.
    """
    if page == "index.html":
        return [c for c, _l, _o, _n in LANGS]
    return [c for c, _l, _o, _n in LANGS if c in LEGAL_LANGS]


def has(rel):
    return os.path.exists(os.path.join(HERE, rel.replace("/", os.sep)))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def inline_svg(rel, cls):
    """SVG'yi HTML'in icine gomer.

    <img> icindeki bir SVG belgenin yazi tiplerine ULASAMAZ. Kilit ve isaret
    Nunito 900 ile cizilmis <text> tasiyor; <img src> olarak konulsalardi
    ziyaretcinin sistem yazi tipiyle render olurlardi ve marka her makinede
    baska turlu gorunurdu. Gomulu SVG sayfanin fontunu kullanir.

    Kalici cozum harfleri outline'a cevirmektir (bkz. README); o gun bu
    fonksiyon durur, yalnizca dosyalar degisir.
    """
    raw = io.open(os.path.join(HERE, rel.replace("/", os.sep)),
                  encoding="utf-8").read().strip()
    m = re.match(r"<svg\b[^>]*>", raw)
    tag = re.sub(r'\s(width|height)="[^"]*"', "", m.group(0))
    tag = tag.replace("<svg", '<svg class="%s" focusable="false"' % cls, 1)
    return tag + raw[m.end():]


# ── iskelet ─────────────────────────────────────────────────────────────────

def head(code, page, title, desc, index=True):
    lang = dict((c, l) for c, l, _o, _n in LANGS)[code]
    loc = dict((c, o) for c, _l, o, _n in LANGS)[code]
    avail = langs_with(page)
    alts = "\n    ".join(
        '<link rel="alternate" hreflang="%s" href="%s/%s">'
        % (c, SITE, path_for(c, page)) for c in avail)
    # x-default sayfa bazli: gizlilik sayfasinin dil-notr karsiligi ana sayfa
    # degil, Ingilizce gizlilik sayfasidir.
    alts += ('\n    <link rel="alternate" hreflang="x-default" href="%s/%s">'
             % (SITE, path_for(ROOT_LANG, page)))

    og = ""
    if has(SHARE):
        og = ('\n    <meta property="og:image" content="%s/%s">'
              '\n    <meta property="og:image:width" content="1200">'
              '\n    <meta property="og:image:height" content="630">'
              '\n    <meta name="twitter:image" content="%s/%s">'
              % (SITE, SHARE, SITE, SHARE))
    touch = ('\n    <link rel="apple-touch-icon" href="/%s">' % ICON_PNG
             if has(ICON_PNG) else "")
    extra_css = ('\n    <link rel="stylesheet" href="/css/legal.css">'
                 if page != "index.html" else "")

    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="%(desc)s">
    <meta name="robots" content="%(robots)s">
    <meta property="og:type" content="website">
    <meta property="og:url" content="%(site)s/%(path)s">
    <meta property="og:title" content="%(title)s">
    <meta property="og:description" content="%(desc)s">
    <meta property="og:locale" content="%(loc)s">
    <meta property="og:site_name" content="%(app)s">%(og)s
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="%(title)s">
    <meta name="twitter:description" content="%(desc)s">
    <meta name="theme-color" content="#FFF4FB">
    <title>%(title)s</title>
%(canon)s    %(alts)s
    <link rel="icon" type="image/svg+xml" href="/%(mark)s">%(touch)s
    <link rel="manifest" href="/manifest.json">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">%(extra)s
</head>
<body>
""" % dict(lang=lang, desc=esc(desc), site=SITE, path=path_for(code, page),
           title=esc(title), loc=loc, alts=alts, og=og, touch=touch,
           app=APP, mark=MARK, extra=extra_css,
           robots="index, follow" if index else "noindex, follow",
           canon=('    <link rel="canonical" href="%s/%s">\n'
                  % (SITE, path_for(code, page)) if index else ""))


def lang_bar(code, page):
    avail = set(langs_with(page))
    out = []
    for c, _l, _o, name in LANGS:
        if c not in avail:
            continue
        cur = ' aria-current="page"' if c == code else ""
        out.append('<a href="/%s" hreflang="%s"%s>%s</a>'
                   % (path_for(c, page), c, cur, esc(name)))
    return '<div class="diller">%s</div>' % "".join(out)


def header(code, page):
    return """<header class="ust">
    <div class="kap">
        <a class="marka" href="/%(home)s">%(lockup)s</a>
        %(bar)s
    </div>
</header>
""" % dict(home=path_for(code, "index.html"), bar=lang_bar(code, page),
           lockup=inline_svg(LOCKUP, "kilit"))


def footer(code, t):
    p, tm, ad = t["legal"]
    lc = code if code in LEGAL_LANGS else ROOT_LANG
    return """<footer>
    <div class="kap">
        <span>%(by)s <a href="%(devurl)s">%(dev)s</a>.</span>
        <div class="f-baglantilar">
            <a href="/%(lp)s">%(p)s</a>
            <a href="/%(lt)s">%(tm)s</a>
            <a href="/%(la)s">%(ad)s</a>
        </div>
    </div>
    <div class="kap f-alt">&copy; 2026 %(dev)s &middot; %(pkg)s</div>
</footer>

</body>
</html>
""" % dict(by=esc(t["by"]), p=esc(p), tm=esc(tm), ad=esc(ad), pkg=PKG,
           dev=DEV, devurl=DEV_URL,
           lp=path_for(lc, "privacy.html"), lt=path_for(lc, "terms.html"),
           la=path_for(lc, "account-deletion.html"))


# ── acilis sayfasi ──────────────────────────────────────────────────────────

def _shot(rel, cap, ph, eager=False):
    """Kare varsa gercek goruntu, yoksa yer tutucu.

    Siteye oyun cizilmiyor. Yer tutucu bir ekran goruntusu taklidi degil, acikca
    bos bir cerceve: olmayan goruntuye baglanti vermek 404 uretir, temsili bir
    kare cizmek ise yalan olur.
    """
    if has("assets/shots/" + rel):
        return ('<img src="/assets/shots/%s" alt="%s" width="390" height="844" '
                'loading="%s">' % (rel, esc(cap), "eager" if eager else "lazy"))
    return ('<div class="yer-tutucu" role="img" aria-label="%s"><span>%s</span>'
            '</div>' % (esc(cap), esc(ph)))


def landing(code, t):
    """Acilis sayfasi.

    Iki kural Colmo'dan devralindi. SAYI VERILMIYOR: "24 bolum", "0 reklam"
    gibi sayilar sayfayi bir ozellik listesine cevirir ve bolum sayisi zaten
    degisecek. GORSEL UYDURULMUYOR: gorunen her kare oyunun kendi ekran
    goruntusu, yoksa acikca bos bir cerceve.

    Colmo'dan ayrilan yer: orada kural hic anlatilmiyordu. Tono'nun kurali tek
    cumlede soyleniyor cunku "tohumdaki rakam bolgenin buyuklugudur" bir ozellik
    listesi degil, oyunun ne oldugunun kendisi. Bunun otesine gecilmiyor.
    """
    caps = t["caps"]
    shots = "".join(
        '<figure>%s<figcaption>%s</figcaption></figure>'
        % (_shot(f, c, t["ph"]), esc(c))
        for f, c in zip(SHOTS, caps))

    band = ""
    if has(SHARE):
        band = """
<section class="bant">
    <img src="/%(share)s" alt="%(alt)s" width="1200" height="630" loading="lazy">
</section>
""" % dict(share=SHARE, alt=esc(t["bandAlt"]))

    hero_gorsel = _shot(SHOTS[0], caps[0], t["ph"], eager=True)
    if not has("assets/shots/" + SHOTS[0]):
        # Ekran goruntusu yokken kahraman bos kalmasin: marka isareti bir
        # ekran taklidi degil, kendi varligimiz.
        hero_gorsel = inline_svg(MARK, "isaret")

    return (head(code, "index.html", t["title"], t["desc"])
            + header(code, "index.html")
            + """
<section class="kahraman">
    <div class="kap">
        <div>
            <span class="rozet">%(badge)s</span>
            <h1>%(h1a)s<br><em>%(h1b)s</em></h1>
            <p class="alt">%(lead)s</p>
            <p class="kucuk">%(small)s</p>
            <div class="magaza">
                <span class="magaza-cip">Google Play <b>%(badge)s</b></span>
                <span class="magaza-cip">App Store <b>%(badge)s</b></span>
            </div>
        </div>
        <div class="telefon">%(hero)s</div>
    </div>
</section>
%(band)s
<section class="duvar-bolum">
    <div class="kap">
        <h2>%(shotsT)s</h2>
        <p class="bolum-alt">%(shotsS)s</p>
        <div class="vitrin">%(shots)s</div>
    </div>
</section>

<section class="kapanis">
    <div class="kap">
        <div class="kutu">
            <h2>%(endT)s</h2>
            <p class="bolum-alt">%(endS)s</p>
        </div>
    </div>
</section>
""" % dict(badge=esc(t["badge"]), h1a=esc(t["h1a"]), h1b=esc(t["h1b"]),
           lead=esc(t["lead"]), small=esc(t["small"]), hero=hero_gorsel,
           band=band, shotsT=esc(t["shotsT"]), shotsS=esc(t["shotsS"]),
           shots=shots, endT=esc(t["endT"]), endS=esc(t["endS"]))
            + """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "%(app)s",
  "applicationCategory": "GameApplication",
  "operatingSystem": "Android, iOS",
  "url": "%(site)s/%(path)s",
  "inLanguage": "%(code)s",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TRY"},
  "publisher": {"@type": "Organization", "name": "%(dev)s"}
}
</script>
""" % dict(site=SITE, app=APP, dev=DEV, code=code,
           path=path_for(code, "index.html"))
            + footer(code, t))


def legal(code, t, page, title, desc, body):
    return (head(code, page, "%s - %s" % (title, APP), desc)
            + header(code, page)
            + """
<section class="yasal">
    <div class="kap">
        <a class="geri" href="/%(home)s">&larr; %(back)s</a>
        <h1>%(title)s</h1>
        <p class="tarih">%(upd)s: %(date)s</p>
        <div class="govde">%(body)s</div>
    </div>
</section>
""" % dict(home=path_for(code, "index.html"), back=esc(t["back"]),
           title=esc(title), date=UPDATED[page], body=body,
           upd=esc(t["upd"]))
            + footer(code, t))


# ── yazma ───────────────────────────────────────────────────────────────────

def write(rel, text):
    p = os.path.join(HERE, rel.replace("/", os.sep))
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)
    return rel


def main():
    import legal_text

    made = []
    for code, _l, _o, _n in LANGS:
        t = T[code]
        made.append(write(file_for(code, "index.html"), landing(code, t)))
        if code in LEGAL_LANGS:
            for page, title, desc, body in legal_text.pages(code):
                made.append(write(file_for(code, page),
                                  legal(code, t, page, title, desc, body)))

    # ── sabit dosyalar ──────────────────────────────────────────────────
    made.append(write(".nojekyll", ""))
    made.append(write("robots.txt",
                      "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"
                      % SITE))

    urls = []
    for c, _l, _o, _n in LANGS:
        urls.append("  <url><loc>%s/%s</loc></url>\n"
                    % (SITE, path_for(c, "index.html")))
        if c in LEGAL_LANGS:
            for p in LEGAL_PAGES:
                urls.append("  <url><loc>%s/%s</loc><lastmod>%s</lastmod>"
                            "</url>\n" % (SITE, path_for(c, p), UPDATED[p]))
    made.append(write("sitemap.xml",
                      '<?xml version="1.0" encoding="UTF-8"?>\n'
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                      '%s</urlset>\n' % "".join(urls)))

    # Ikon listesi: yalnizca diskte VAR olan dosyalar. Olmayan ikonu manifeste
    # yazmak tarayicida 404 uretir.
    icons = ['    {"src": "/%s", "sizes": "any", "type": "image/svg+xml"}'
             % MARK]
    for rel, size in (("assets/tono-icon-192.png", "192x192"),
                      ("assets/tono-icon-512.png", "512x512")):
        if has(rel):
            icons.append('    {"src": "/%s", "sizes": "%s", "type": '
                         '"image/png", "purpose": "any maskable"}'
                         % (rel, size))
    made.append(write("manifest.json",
                      '{\n'
                      '  "id": "/",\n'
                      '  "name": "%s",\n'
                      '  "short_name": "%s",\n'
                      '  "description": %s,\n'
                      '  "lang": "%s",\n'
                      '  "start_url": "/",\n'
                      '  "scope": "/",\n'
                      '  "display": "standalone",\n'
                      '  "background_color": "#FFF4FB",\n'
                      '  "theme_color": "#FFF4FB",\n'
                      '  "icons": [\n%s\n  ]\n}\n'
                      % (APP, APP,
                         '"%s"' % T[ROOT_LANG]["desc"].replace('"', '\\"'),
                         ROOT_LANG, ",\n".join(icons))))

    t = T[ROOT_LANG]
    made.append(write("404.html",
                      head(ROOT_LANG, "index.html", "404 - %s" % APP,
                           t["e404S"], index=False)
                      + header(ROOT_LANG, "index.html")
                      + '\n<section class="kapanis"><div class="kap">'
                        '<div class="kutu"><h2>%s</h2>'
                        '<p class="bolum-alt">%s <a href="/">%s</a>.</p>'
                        '</div></div></section>\n'
                        % (esc(t["e404T"]), esc(t["e404S"]), esc(t["back"]))
                      + footer(ROOT_LANG, t)))

    print("uretilen dosya: %d" % len(made))
    for m in sorted(made):
        print("  " + m)

    # ── derleme sonrasi uyarilar ────────────────────────────────────────
    warn = []
    cname = os.path.join(HERE, "CNAME")
    if not os.path.exists(cname):
        warn.append("CNAME yok. Icine tek satir yaz: %s (bkz. README)" % DOMAIN)
    else:
        got = io.open(cname, encoding="utf-8").read().strip()
        if got != DOMAIN:
            warn.append("CNAME icerigi '%s', config.DOMAIN ise '%s'"
                        % (got, DOMAIN))
    if not has(SHARE):
        warn.append("%s yok: og:image ve bant bolumu yazilmadi" % SHARE)
    if not has(ICON_PNG):
        warn.append("%s yok: apple-touch-icon yazilmadi" % ICON_PNG)
    eksik = [s for s in SHOTS if not has("assets/shots/" + s)]
    if eksik:
        warn.append("ekran goruntusu eksik (yer tutucuya dusuldu): %s"
                    % ", ".join(eksik))
    if warn:
        print("\nyapilacaklar:")
        for w in warn:
            print("  - " + w)


if __name__ == "__main__":
    main()
