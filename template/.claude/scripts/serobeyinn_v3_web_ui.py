"""Static page, style and script of the optional web view (serobeyinn_v3_web.py).

Shipped as Python text because the update package carries only serobeyinn_v3*.py runtime files.
Nothing here loads from the network: no CDN, no web font, no remote image. The script builds
every element with textContent, never innerHTML, so vault text cannot become markup; the CSP
in serobeyinn_v3_web.py allows only these same-origin files. The palette follows the contributed
"Citrus" design (#423): dark slate surfaces with a lemon accent.
"""
import html

APP_CSS = r"""
:root {
  --zemin: #0a0e14; --panel: #161b22; --panel-2: #1c2026; --cizgi: #30363d;
  --metin: #dfe2eb; --soluk: #8b949e; --limon: #f9d71c; --limon-koyu: #f5c518;
  --yesil: #67df70; --kirmizi: #ffb4ab; --mavi: #8ab4f8;
  --yazi: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--zemin); color: var(--metin); font: 14px/1.5 var(--yazi); }
a { color: var(--limon); }
button, input, select, textarea { font: inherit; color: inherit; }
button { background: var(--limon); color: var(--zemin); border: 0; border-radius: 4px; padding: 6px 12px;
  font-weight: 600; cursor: pointer; }
button:hover { background: var(--limon-koyu); }
button:disabled { opacity: .5; cursor: not-allowed; }
button.ikincil { background: transparent; color: var(--metin); border: 1px solid var(--cizgi); }
button.ikincil:hover { border-color: var(--limon); color: var(--limon); }
input, select, textarea { background: var(--zemin); border: 1px solid var(--cizgi); border-radius: 4px; padding: 6px 8px; }
input:focus, select:focus, textarea:focus, button:focus-visible { outline: 2px solid var(--limon); outline-offset: 1px; }
.kabuk { display: grid; grid-template-columns: 220px 1fr; min-height: 100vh; }
.yan { background: var(--zemin); border-right: 1px solid var(--cizgi); padding: 16px 12px; display: flex;
  flex-direction: column; gap: 16px; position: sticky; top: 0; height: 100vh; }
.marka { display: flex; gap: 10px; align-items: flex-start; }
.marka .limon { font-size: 26px; line-height: 1.1; }
.marka-govde { min-width: 0; flex: 1; }
.marka-satir { display: flex; align-items: center; gap: 6px; }
.marka-satir strong { overflow-wrap: anywhere; line-height: 1.25; }
.marka-duzenle { background: transparent; color: var(--soluk); border: 1px solid transparent; padding: 1px 5px;
  font-size: 12px; border-radius: 4px; opacity: .7; }
.marka-duzenle:hover { background: var(--panel); border-color: var(--cizgi); color: var(--limon); opacity: 1; }
.marka-form { display: flex; flex-wrap: wrap; gap: 4px; margin: 4px 0; }
.marka-form input { width: 100%; padding: 4px 6px; font-size: 13px; }
.marka-form button { padding: 3px 8px; font-size: 12px; }
.marka small { display: block; color: var(--soluk); font-family: var(--mono); font-size: 11px; word-break: break-all; }
.yan nav { display: flex; flex-direction: column; gap: 2px; }
.yan nav a { color: var(--metin); text-decoration: none; padding: 7px 10px; border-radius: 4px; }
.yan nav a:hover { background: var(--panel); color: var(--limon); }
.yan nav a.secili { background: var(--panel-2); color: var(--limon); box-shadow: inset 2px 0 0 var(--limon); font-weight: 600; }
.yan .alt { margin-top: auto; display: flex; flex-direction: column; gap: 8px; }
main { padding: 20px 24px; min-width: 0; }
h1 { font-size: 20px; margin: 0 0 4px; }
h2 { font-size: 15px; margin: 0 0 10px; color: var(--limon); }
.aciklama { color: var(--soluk); margin: 0 0 16px; }
[hidden] { display: none !important; }
.izgara { display: grid; grid-template-columns: repeat(auto-fit, minmax(185px, 1fr)); gap: 12px; margin-bottom: 18px; }
.kart { background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 12px 14px; }
.kart-bag { display: flex; flex-direction: column; gap: 5px; text-decoration: none; color: inherit; }
.kart-bag:hover, .kart-bag:focus-visible { border-color: var(--limon); background: var(--panel-2); }
.kart .etiket { color: var(--soluk); font-size: 11px; text-transform: uppercase; letter-spacing: .04em; }
.kart .deger { font-family: var(--mono); font-size: 20px; font-weight: 600; line-height: 1.25; }
.kart .alt-not { color: var(--soluk); font-size: 12px; }
.kokpit-ust { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 10px; }
.kokpit-ust-sol { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
.kokpit-ust-sag { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.kokpit-arama { display: flex; gap: 6px; align-items: center; }
.kokpit-arama input { width: 210px; }
.kokpit-ikili { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 18px; align-items: start; }
.kokpit-sutun { display: flex; flex-direction: column; gap: 18px; min-width: 0; }
.kokpit-bolum { background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 14px; }
.bolum-baslik { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 10px; }
.bolum-baslik h2 { margin: 0; }
.bolum-baslik a { font-size: 12px; text-decoration: none; }
.bolum-baslik a:hover { text-decoration: underline; }
.hizli-form { display: flex; gap: 8px; margin-bottom: 10px; }
.hizli-form input { flex: 1; min-width: 0; }
.odak-satir { display: flex; justify-content: space-between; align-items: center; gap: 10px; }
.odak-bilgi { min-width: 0; flex: 1; }
.odak-bilgi strong { display: block; overflow-wrap: anywhere; }
.odak-satir select { width: auto; min-width: 112px; }
.dikkat-izgara { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.dikkat-kutu { display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 9px 11px;
  border-radius: 5px; border: 1px solid var(--cizgi); background: var(--panel-2); color: inherit; text-decoration: none; }
.dikkat-kutu:hover { border-color: var(--limon); }
.dikkat-kutu .sayi { font-family: var(--mono); font-size: 15px; font-weight: 600; }
.hafiza-alt { margin-top: 10px; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }
.rozet { display: inline-block; font-family: var(--mono); font-size: 11px; padding: 1px 7px; border-radius: 10px;
  border: 1px solid var(--cizgi); color: var(--soluk); }
.rozet.iyi { color: var(--yesil); border-color: var(--yesil); }
.rozet.uyari { color: var(--limon); border-color: var(--limon); }
.rozet.kotu { color: var(--kirmizi); border-color: var(--kirmizi); }
.liste { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.liste li { background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 10px 12px; }
.ust-bilgi { color: var(--soluk); font-family: var(--mono); font-size: 11px; display: flex; gap: 8px; flex-wrap: wrap; }
.ozet { white-space: pre-wrap; overflow-wrap: anywhere; }
.arac-cubugu { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 12px; }
.pano { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; align-items: start; padding-bottom: 8px; }
.sutun { background: var(--panel); border: 1px solid var(--cizgi); border-top: 3px solid var(--cizgi); border-radius: 6px; padding: 10px; min-height: 160px; transition: border-color .15s, background .15s; }
.sutun.s-inbox { border-top-color: var(--mavi); }
.sutun.s-active { border-top-color: var(--limon); }
.sutun.s-waiting { border-top-color: #a371f7; }
.sutun.s-blocked { border-top-color: var(--kirmizi); }
.sutun.s-done { border-top-color: var(--yesil); }
.sutun.s-cancelled { border-top-color: var(--soluk); }
.sutun.hedef { border-color: var(--limon); background: rgba(249, 215, 28, 0.06); }
.sutun h3 { font-size: 12px; margin: 0 0 6px; color: var(--metin); text-transform: uppercase; letter-spacing: .05em;
  display: flex; justify-content: space-between; align-items: center; }
.sutun-aciklama { color: var(--soluk); font-size: 11px; margin: 0 0 10px; line-height: 1.35; }
.sutun .bos-sutun { color: var(--soluk); font-size: 12px; font-style: italic; text-align: center; padding: 18px 8px;
  border: 1px dashed var(--cizgi); border-radius: 5px; }
.gorev { background: var(--panel-2); border: 1px solid var(--cizgi); border-radius: 6px; padding: 10px; margin-bottom: 8px;
  display: flex; flex-direction: column; gap: 6px; transition: border-color .15s, opacity .15s; }
.gorev:hover { border-color: #485260; }
.gorev[draggable="true"] { cursor: grab; }
.gorev.surukleniyor { opacity: .45; border-color: var(--limon); }
.gorev-baslik { background: transparent; border: 0; padding: 0; color: var(--metin); text-align: left; font-weight: 600;
  cursor: pointer; overflow-wrap: anywhere; line-height: 1.35; }
.gorev-baslik:hover { background: transparent; color: var(--limon); text-decoration: underline; }
.gorev-ozet { color: var(--soluk); font-size: 12px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden; }
.gorev-alt { display: flex; gap: 6px; align-items: center; margin-top: 2px; }
.gorev-alt select { flex: 1; font-size: 12px; padding: 4px 6px; }
.gorev-ozet-serit { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.gorev-detay { background: var(--panel); border: 1px solid var(--limon); border-radius: 6px; padding: 14px; margin-bottom: 14px; }
.gorev-detay pre.onizleme { max-height: 36vh; margin-top: 8px; }
.gorev-arac { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 12px; }
.gorev-arac input[type="search"] { min-width: 190px; flex: 1; max-width: 300px; }
form.form { display: grid; gap: 8px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); align-items: end;
  background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 12px; margin-bottom: 16px; }
form.form label { display: flex; flex-direction: column; gap: 4px; color: var(--soluk); font-size: 12px; }
form.form .genis { grid-column: 1 / -1; }
.ikili { display: grid; grid-template-columns: minmax(260px, 1fr) minmax(300px, 1.3fr); gap: 16px; align-items: start; }
.gozden-sol { display: flex; flex-direction: column; gap: 14px; min-width: 0; }
.gozden-sag { position: sticky; top: 18px; min-width: 0; }
button.kaynak-btn { background: transparent; color: var(--limon); border: 1px solid var(--cizgi); border-radius: 4px;
  padding: 1px 7px; font-family: var(--mono); font-size: 11px; font-weight: 500; }
button.kaynak-btn:hover { border-color: var(--limon); background: var(--panel-2); }
.sonuc { cursor: pointer; transition: border-color .15s, background .15s; }
.sonuc:hover, .sonuc:focus { border-color: var(--limon); outline: none; }
.sonuc.secili { border-color: var(--limon); background: var(--panel-2); box-shadow: inset 2px 0 0 var(--limon); }
.arama-panel { margin-bottom: 14px; }
.arama-kutu { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.arama-kutu input { flex: 1; min-width: 220px; padding: 8px 10px; font-size: 14px; }
#onizleme-meta { margin-bottom: 8px; }
.arama-meta { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 10px; }
.arama-ozet { color: var(--soluk); font-size: 13px; margin-top: 4px; line-height: 1.45; }
mark.vurgu { background: rgba(249, 215, 28, 0.22); color: var(--limon); border-radius: 2px; padding: 0 2px; }
.onizleme { background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 14px 16px;
  overflow-wrap: anywhere; max-height: 70vh; overflow: auto; margin: 0; line-height: 1.65; }
.md-okuma h1, .md-okuma h2, .md-okuma h3, .md-okuma h4 { color: var(--limon); margin: 14px 0 6px; line-height: 1.3; }
.md-okuma h1 { font-size: 18px; border-bottom: 1px solid var(--cizgi); padding-bottom: 4px; }
.md-okuma h2 { font-size: 15px; }
.md-okuma h3, .md-okuma h4 { font-size: 14px; color: var(--mavi); }
.md-okuma > :first-child { margin-top: 0; }
.md-okuma p { margin: 0 0 10px; }
.md-okuma ul, .md-okuma ol { margin: 0 0 10px; padding-left: 20px; }
.md-okuma li { margin: 3px 0; }
.md-okuma blockquote { margin: 8px 0; padding: 4px 12px; border-left: 3px solid var(--limon); color: var(--soluk); background: var(--panel-2); border-radius: 0 4px 4px 0; }
.md-okuma pre { background: var(--zemin); border: 1px solid var(--cizgi); border-radius: 5px; padding: 10px 12px; overflow-x: auto; margin: 8px 0; }
.md-okuma code { font-family: var(--mono); font-size: 12px; background: var(--panel-2); padding: 1px 5px; border-radius: 3px; color: var(--mavi); }
.md-okuma pre code { background: transparent; padding: 0; color: var(--metin); }
.md-okuma hr { border: 0; border-top: 1px solid var(--cizgi); margin: 12px 0; }
.md-okuma table { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 13px; }
.md-okuma th, .md-okuma td { border: 1px solid var(--cizgi); padding: 5px 8px; text-align: left; }
.md-okuma th { background: var(--panel-2); color: var(--limon); }
.md-okuma .md-wiki { color: var(--limon); background: var(--panel-2); padding: 1px 6px; border-radius: 4px; font-size: 13px; }
.md-okuma .md-bag { color: var(--mavi); text-decoration: underline; }
.makbuz-gun { margin: 16px 0 8px; display: flex; align-items: center; gap: 8px; color: var(--limon); font-size: 13px; font-weight: 600; }
.makbuz-gun::after { content: ''; flex: 1; height: 1px; background: var(--cizgi); }
.makbuz-kart { display: flex; flex-direction: column; gap: 8px; }
.makbuz-ust { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
.makbuz-saat { font-family: var(--mono); font-size: 12px; color: var(--limon); }
.makbuz-kaynaklar { display: flex; gap: 6px; flex-wrap: wrap; }
.kaynak-etiket { font-family: var(--mono); font-size: 11px; padding: 2px 7px; border-radius: 4px;
  background: var(--panel-2); border: 1px solid var(--cizgi); color: var(--mavi); word-break: break-all; }
.makbuz-ozet { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.55; color: var(--metin); }
.makbuz-ozet.gizli { color: var(--soluk); font-style: italic; }
.hafiza-rehber { background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 12px 14px; margin-bottom: 16px; }
.hafiza-rehber summary { cursor: pointer; font-weight: 600; color: var(--limon); list-style: none; display: flex; align-items: center; justify-content: space-between; }
.hafiza-rehber summary::after { content: 'Aç / Gizle'; font-size: 11px; color: var(--soluk); font-weight: 400; }
.hafiza-rehber p { margin: 8px 0; color: var(--metin); line-height: 1.55; }
.hafiza-rehber ul { margin: 8px 0 4px; padding-left: 18px; display: grid; gap: 4px; color: var(--soluk); font-size: 13px; }
.hafiza-rehber strong { color: var(--metin); }
.doluluk-cubuk { width: 100%; height: 8px; background: var(--zemin); border: 1px solid var(--cizgi); border-radius: 99px; overflow: hidden; margin-top: 6px; }
.doluluk-ic { height: 100%; background: var(--yesil); border-radius: 99px; transition: width .2s ease; }
.doluluk-ic.uyari { background: var(--limon); }
.doluluk-ic.kotu { background: var(--kirmizi); }
.hafiza-aksiyon { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--cizgi); }
a.dugme-bag { display: inline-flex; align-items: center; text-decoration: none; background: transparent;
  color: var(--metin); border: 1px solid var(--cizgi); border-radius: 4px; padding: 6px 12px; font-weight: 600; }
a.dugme-bag:hover { border-color: var(--limon); color: var(--limon); }
.yardim-izgara { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 12px; margin-bottom: 16px; }
.yardim-kart { background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; padding: 14px 16px; }
.yardim-kart h3 { margin: 0 0 6px; font-size: 14px; color: var(--limon); display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.yardim-kart p { margin: 0 0 8px; color: var(--metin); font-size: 13px; line-height: 1.55; }
.yardim-kart ul { margin: 0; padding-left: 18px; display: grid; gap: 5px; color: var(--soluk); font-size: 13px; line-height: 1.5; }
.yardim-kart strong { color: var(--metin); }
.yardim-kart code { font-family: var(--mono); font-size: 12px; background: var(--panel-2); color: var(--mavi); padding: 1px 5px; border-radius: 3px; }
.yardim-tablo { width: 100%; border-collapse: collapse; font-size: 13px; background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px; overflow: hidden; margin-bottom: 16px; }
.yardim-tablo th, .yardim-tablo td { border-bottom: 1px solid var(--cizgi); padding: 9px 12px; text-align: left; vertical-align: top; }
.yardim-tablo th { background: var(--panel-2); color: var(--limon); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }
.yardim-tablo code { font-family: var(--mono); font-size: 12px; color: var(--mavi); background: var(--panel-2); padding: 1px 5px; border-radius: 3px; }
button.gelistirici-btn { background: #070d0a; color: #00ff41; border: 1px solid #1a3a1a; font-family: var(--mono);
  font-size: 12px; font-weight: 700; padding: 6px 10px; border-radius: 6px; }
button.gelistirici-btn:hover { background: #0d200d; border-color: #00ff41; box-shadow: 0 0 10px rgba(0, 255, 65, .28); }
dialog.gelistirici-modal { padding: 14px; border: 1px solid #1a3a1a; border-radius: 12px; background: #0a0a0a;
  background-image: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 255, 65, .02) 2px, rgba(0, 255, 65, .02) 4px);
  color: #00ff41; max-width: 760px; width: calc(100% - 24px); max-height: 90vh; overflow: auto;
  box-shadow: 0 0 0 1px rgba(0, 255, 65, .10), 0 0 35px rgba(0, 255, 65, .14), 0 24px 60px rgba(0, 0, 0, .82); }
dialog.gelistirici-modal::backdrop { background: rgba(0, 0, 0, .82); }
.dev-card { border: 1px solid #1a3a1a; background: #0f1a0f;
  box-shadow: 0 0 0 1px rgba(0, 255, 65, .08), 0 0 30px rgba(0, 255, 65, .10); }
.dev-ust { display: flex; align-items: center; justify-content: space-between; padding: 8px 14px;
  background: #0d200d; border-bottom: 1px solid #1a3a1a; font-family: var(--mono); font-size: 11px; color: #4a8a4a; letter-spacing: .05em; }
.dev-noktalar { display: flex; align-items: center; gap: 7px; }
.dev-nokta { width: 11px; height: 11px; border-radius: 50%; display: inline-block; }
.dev-nokta.k { background: #3a1a1a; border: 1px solid #5a2a2a; }
.dev-nokta.s { background: #2a2a0a; border: 1px solid #4a4a0a; }
.dev-nokta.y { background: #0a2a0a; border: 1px solid #1a3a1a; }
.dev-kapat { background: transparent; color: #4a8a4a; border: 1px solid #1a3a1a; padding: 1px 8px; font-size: 15px; line-height: 1.2; }
.dev-kapat:hover { background: #143214; border-color: #00ff41; color: #00ff41; }
.dev-govde { padding: 24px 28px 20px; font-family: var(--mono); }
.dev-komut { font-size: 13px; color: #4a8a4a; margin-bottom: 4px; }
.dev-komut span { color: #00ff41; }
.dev-ad { font-size: 42px; line-height: 1.05; letter-spacing: 2px; font-weight: 700; color: #00ff41;
  text-shadow: 0 0 8px #00ff41, 0 0 20px rgba(0, 255, 65, .35); animation: devFlicker 6s infinite; }
@keyframes devFlicker { 0%, 95%, 100% { opacity: 1; } 96% { opacity: .92; } 97% { opacity: 1; } 98% { opacity: .95; } }
.dev-mahlas { font-size: 14px; color: #00c832; margin-top: 4px; letter-spacing: .15em; }
.dev-mahlas::before { content: '> '; color: #4a8a4a; }
.dev-unvan { font-size: 12px; color: #4a8a4a; margin-top: 6px; letter-spacing: .08em; }
.dev-unvan::before { content: '# '; }
.dev-divider { border: 0; border-top: 1px solid #1a3a1a; margin: 20px 0; position: relative; }
.dev-divider::before { content: attr(data-label); position: absolute; top: -9px; left: 16px; background: #0f1a0f;
  padding: 0 8px; font-size: 11px; color: #4a8a4a; letter-spacing: .1em; }
.dev-metin { font-size: 12px; color: #4a8a4a; line-height: 1.75; margin: 0; }
.dev-metin strong { color: #00ff41; font-weight: 600; }
.dev-ikili { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.dev-beceri { margin-bottom: 10px; }
.dev-beceri-ust { display: flex; justify-content: space-between; font-size: 11px; color: #4a8a4a; margin-bottom: 4px; }
.dev-beceri-ust span:last-child { color: #00ff41; }
.dev-cubuk { height: 8px; background: #0d200d; border: 1px solid #1a3a1a; position: relative; overflow: hidden; }
.dev-dolgu { height: 100%; width: 0; background: linear-gradient(90deg, #005a15, #00ff41);
  transition: width 1.1s cubic-bezier(.4, 0, .2, 1); box-shadow: 0 0 8px rgba(0, 255, 65, .35); position: relative; }
.dev-dolgu::after { content: ''; position: absolute; top: 0; right: -20px; width: 20px; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 65, .45)); animation: devScan 2s linear infinite; }
@keyframes devScan { from { transform: translateX(-100px); } to { transform: translateX(100px); } }
.dev-rozetler { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 12px; }
.dev-rozet { font-size: 11px; padding: 3px 9px; border: 1px solid #1a3a1a; color: #4a8a4a; background: transparent;
  letter-spacing: .05em; transition: all .2s; }
.dev-rozet:hover { border-color: #00ff41; color: #00ff41; box-shadow: 0 0 6px rgba(0, 255, 65, .35); }
.dev-qr-alan { display: flex; flex-direction: column; align-items: center; gap: 10px; margin-bottom: 14px; }
.dev-qr-sekmeler { display: flex; gap: 8px; }
.dev-qr-tab { font-size: 11px; padding: 3px 10px; border: 1px solid #1a3a1a; background: transparent; color: #4a8a4a;
  font-family: var(--mono); font-weight: 500; border-radius: 0; }
.dev-qr-tab.secili, .dev-qr-tab:hover { border-color: #00ff41; color: #00ff41; background: #0d200d; }
#dev-qr { border: 2px solid #1a3a1a; padding: 6px; background: #0a0a0a; box-shadow: 0 0 10px rgba(0, 255, 65, .35); display: block; }
.dev-qr-etiket { font-size: 11px; color: #4a8a4a; letter-spacing: .08em; }
.dev-qr-etiket::after { content: '█'; color: #00ff41; animation: devBlink 1s step-end infinite; margin-left: 2px; }
@keyframes devBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
.dev-iletisim { display: flex; flex-direction: column; gap: 8px; }
.dev-bag { display: flex; align-items: center; gap: 10px; padding: 7px 10px; border: 1px solid transparent;
  background: transparent; color: #4a8a4a; text-decoration: none; font-size: 12px; width: 100%; font-family: var(--mono);
  font-weight: 500; border-radius: 0; text-align: left; }
.dev-bag:hover { border-color: #1a3a1a; color: #00ff41; background: #0d200d; box-shadow: inset 0 0 10px rgba(0, 255, 65, .06); }
.dev-bag small { color: #4a8a4a; font-size: 10px; margin-left: auto; }
.dev-alt { margin-top: 20px; padding-top: 14px; border-top: 1px solid #1a3a1a; display: flex; justify-content: space-between;
  align-items: center; flex-wrap: wrap; gap: 8px; font-size: 12px; color: #4a8a4a; }
.dev-alinti { font-style: italic; }
.dev-alinti::before { content: '> '; color: #1a4a1a; }
.dev-sayac { font-size: 11px; color: #1a4a1a; }
@media (max-width: 640px) { .dev-ikili { grid-template-columns: 1fr; } .dev-ad { font-size: 32px; } .dev-govde { padding: 18px 16px; } }
meter { width: 100%; height: 10px; }
.bos { color: var(--soluk); font-style: italic; }
#bildirim { position: fixed; right: 16px; bottom: 16px; display: flex; flex-direction: column; gap: 6px; z-index: 10; }
#bildirim div { background: var(--panel); border: 1px solid var(--limon); border-radius: 6px; padding: 8px 12px; max-width: 420px; }
#bildirim div.hata { border-color: var(--kirmizi); }
.kilit { min-height: 100vh; display: flex; align-items: center; justify-content: center; }
.kilit .marka { justify-content: center; }
.kilit .kart { max-width: 420px; width: 100%; text-align: center; padding: 28px; }
.kilit form { display: flex; flex-direction: column; gap: 10px; margin-top: 14px; }
.kapandi { position: fixed; inset: 0; background: rgba(10, 14, 20, .94); display: flex; align-items: center; justify-content: center;
  font-size: 18px; z-index: 20; }
.graf-kutu { position: relative; background: var(--panel); border: 1px solid var(--cizgi); border-radius: 6px;
  overflow: hidden; height: 68vh; min-height: 360px; }
.graf-kutu.beyin { background: radial-gradient(ellipse 58% 64% at 50% 50%, rgba(16, 76, 172, 0.28) 0%, rgba(8, 22, 52, 0.14) 48%, transparent 78%);
  border-color: transparent; }
#graf-tuval { display: block; width: 100%; height: 100%; cursor: grab; touch-action: none; }
#graf-tuval:active { cursor: grabbing; }
.graf-ikili { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(300px, 1fr); gap: 16px; align-items: start; }
.graf-sag { display: flex; flex-direction: column; gap: 10px; min-width: 0; }
#graf-icerik { max-height: 68vh; margin: 0; }
.graf-aciklama { margin-top: 10px; }
.graf-lejant { display: flex; gap: 6px; flex-wrap: wrap; color: var(--soluk); font-size: 12px; }
.graf-lejant .graf-filtre { background: transparent; color: var(--soluk); border: 1px solid var(--cizgi);
  border-radius: 12px; padding: 3px 9px; font-weight: 500; font-size: 12px; display: inline-flex; align-items: center; gap: 5px; }
.graf-lejant .graf-filtre:hover { border-color: var(--limon); color: var(--metin); background: var(--panel); }
.graf-lejant .graf-filtre.secili { border-color: var(--limon); color: var(--limon); background: var(--panel-2); font-weight: 600; }
.graf-lejant i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; }
.graf-lejant .n-knowledge { background: #f9d71c; }
.graf-lejant .n-daily { background: #8ab4f8; }
.graf-lejant .n-receipts { background: #67df70; }
.graf-lejant .n-companion { background: #ffb4ab; }
.graf-lejant .n-diger { background: #7dd3fc; }
@media (max-width: 1100px) { .graf-ikili { grid-template-columns: 1fr; } #graf-icerik { max-height: 50vh; } }
@media (max-width: 960px) { .kokpit-ikili { grid-template-columns: 1fr; } }
@media (max-width: 760px) { .kabuk { grid-template-columns: 1fr; } .yan { position: static; height: auto; } .ikili { grid-template-columns: 1fr; } .kokpit-arama input { width: 150px; } }
"""

APP_JS = r"""
'use strict';
(function () {
  const meta = function (name) { const node = document.querySelector('meta[name="' + name + '"]'); return node ? node.content : ''; };
  const CSRF = meta('serobeyinn-csrf');
  const SALT_OKUNUR = meta('serobeyinn-salt-okunur') === '1';
  const DURUM = { inbox: 'Gelen', active: 'Aktif', waiting: 'Bekliyor', blocked: 'Engellendi', done: 'Bitti', cancelled: 'İptal' };
  const DURUM_ACIKLAMA = {
    inbox: 'Yeni eklenen, henüz başlanmamış işler',
    active: 'Şu an üzerinde çalışılan işler',
    waiting: 'Bir yanıt, onay veya koşul bekleyenler',
    blocked: 'Önünde hata veya engel olan işler',
    done: 'Tamamlanmış işler',
    cancelled: 'Vazgeçilen veya kapatılan işler'
  };
  const TUR = { task: 'görev', note: 'not', receipt: 'receipt', inference: 'çıkarım', preference: 'tercih' };
  // The statuses `serobeyinn.py doctor` reports, and those of `serobeyinn.py sync`.
  const DOKTOR = { observed_metadata: ['Sağlıklı', 'iyi'], pending: ['İşlenmemiş hook olayı var', 'uyari'],
    never_seen: ['Hook henüz çalışmadı', 'uyari'], needs_attention: ['Dikkat gerekiyor', 'kotu'] };
  const ESITLEME = { succeeded: 'tamamlandı', degraded: 'uyarılarla tamamlandı', conflict: 'çakışma var' };
  const HAFIZA = { within_limit: 'Sınır içinde', limit_off: 'Sınır kapalı', planned: 'Taşınacak', needs_rewrite: 'Elle kısaltılmalı',
    needs_attention: 'Dikkat', compacted: 'Taşındı', ok: 'Sağlıklı', dry_run: 'Önizleme', conflict: 'Başka bir işlem sürüyor' };
  if (!CSRF) { return; }

  function el(tag, props) {
    const node = document.createElement(tag);
    Object.entries(props || {}).forEach(function (pair) {
      const key = pair[0], value = pair[1];
      if (value === undefined || value === null) { return; }
      if (key === 'text') { node.textContent = String(value); }
      else if (key === 'class') { node.className = value; }
      else if (key in node) { node[key] = value; }
      else { node.setAttribute(key, String(value)); }
    });
    for (let i = 2; i < arguments.length; i += 1) {
      const child = arguments[i];
      if (child === null || child === undefined || child === false) { continue; }
      node.append(child instanceof Node ? child : document.createTextNode(String(child)));
    }
    return node;
  }
  function bosalt(node) { while (node.firstChild) { node.removeChild(node.firstChild); } return node; }
  function $(id) { return document.getElementById(id); }
  function zaman(value) {
    if (!value) { return ''; }
    const date = new Date(value);
    return isNaN(date) ? String(value) : date.toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' });
  }
  function bildir(text, hata) {
    const item = el('div', { class: hata ? 'hata' : '', role: hata ? 'alert' : 'status', text: text });
    $('bildirim').append(item);
    setTimeout(function () { item.remove(); }, hata ? 7000 : 3500);
  }

  async function api(path, body) {
    const options = { method: body === undefined ? 'GET' : 'POST', credentials: 'same-origin', headers: { Accept: 'application/json' } };
    if (body !== undefined) {
      options.headers['Content-Type'] = 'application/json';
      options.headers['X-SeroBeyinn-CSRF'] = CSRF;
      options.body = JSON.stringify(body);
    }
    const response = await fetch(path, options);
    let data = null;
    try { data = await response.json(); } catch (error) { data = null; }
    if (response.status === 401) { window.location.replace('/'); }
    if (!response.ok) { throw new Error((data && data.mesaj) || ('HTTP ' + response.status)); }
    return data;
  }

  // --- kokpit -----------------------------------------------------------
  let sonKokpitYukleme = 0;
  function kart(etiket, deger, rozet, hedef, altNot) {
    const icerik = [el('div', { class: 'etiket', text: etiket }), el('div', { class: 'deger', text: deger })];
    if (rozet) { icerik.push(el('div', {}, rozet)); }
    if (altNot) { icerik.push(el('div', { class: 'alt-not', text: altNot })); }
    if (hedef) { return el.apply(null, ['a', { class: 'kart kart-bag', href: hedef }].concat(icerik)); }
    return el.apply(null, ['div', { class: 'kart' }].concat(icerik));
  }
  function odakGorevSatiri(g, durumlar) {
    const secim = durumSecici(g.durum, durumlar);
    secim.addEventListener('change', async function () {
      secim.disabled = true;
      try {
        await api('/api/gorev/durum', { id: g.id, revizyon: g.revizyon, durum: secim.value });
        bildir('Görev güncellendi: ' + g.baslik);
      } catch (error) { bildir('Güncellenemedi: ' + error.message, true); }
      kokpit();
    });
    const bilgi = el('div', { class: 'ust-bilgi' },
      el('span', { class: 'rozet ' + (g.durum === 'blocked' ? 'kotu' : (g.durum === 'active' ? 'uyari' : '')), text: DURUM[g.durum] || g.durum }));
    if (g.proje) { bilgi.append(el('span', { text: '#' + g.proje })); }
    if (g.sorumlu) { bilgi.append(el('span', { text: '@' + g.sorumlu })); }
    if (g.bitis) { bilgi.append(el('span', { text: 'bitiş ' + String(g.bitis).slice(0, 10) })); }
    return el('li', { class: 'odak-satir', title: g.kaynak || '' },
      el('div', { class: 'odak-bilgi' }, el('strong', { text: g.baslik }), bilgi),
      secim);
  }
  async function kokpitHizliGorev(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const girdi = form.querySelector('input[name="baslik"]');
    const baslik = girdi.value.trim();
    if (!baslik) { return; }
    const dugme = form.querySelector('button');
    dugme.disabled = true;
    try {
      const sonuc = await api('/api/gorev', { baslik: baslik, sorumlu: 'ben', proje: '', durum: 'inbox', aciklama: '' });
      bildir('Görev oluşturuldu: ' + sonuc.gorev.baslik);
      girdi.value = '';
      kokpit();
    } catch (error) { bildir('Görev oluşturulamadı: ' + error.message, true); }
    dugme.disabled = SALT_OKUNUR;
  }
  function kokpitAramaGit(event) {
    event.preventDefault();
    const sorgu = $('kokpit-arama-sorgu').value.trim();
    if (sorgu.length < 2) { bildir('Arama için en az iki harf yaz.', true); return; }
    $('arama-sorgu').value = sorgu;
    window.location.hash = '#arama';
    ara({ preventDefault: function () {} });
  }
  async function kokpit() {
    const istek = ++sonKokpitYukleme;
    const alan = bosalt($('kokpit-kartlar'));
    alan.append(el('p', { class: 'bos', text: 'Yükleniyor…' }));
    const sonuclar = await Promise.allSettled([
      api('/api/doktor'), api('/api/gorevler'), api('/api/makbuzlar'),
      api('/api/hafiza'), api('/api/gozden-gecir'), api('/api/graf')
    ]);
    if (istek !== sonKokpitYukleme) { return; }
    bosalt(alan);

    // 1) Sistem sağlığı kartı
    if (sonuclar[0].status === 'fulfilled') {
      const d = sonuclar[0].value;
      const durum = DOKTOR[d.durum] || [d.durum || 'Bilinmiyor', 'uyari'];
      const bekleyen = d.bekleyen_olay ?? 0;
      const gizli = d.ayiklanan_gizli ?? 0;
      alan.append(kart('Sistem Sağlığı', durum[0],
        el('span', { class: 'rozet ' + durum[1], text: bekleyen ? bekleyen + ' bekleyen olay' : 'Olay kuyruğu temiz' }),
        '#gozden-gecir', gizli + ' gizli bilgi korundu'));
    } else {
      alan.append(kart('Sistem Sağlığı', 'Okunamadı', el('span', { class: 'rozet kotu', text: sonuclar[0].reason.message }), '#gozden-gecir'));
    }

    // 2) Açık görevler kartı + odak görev listesi
    const odakListe = bosalt($('kokpit-odak-gorevler'));
    if (sonuclar[1].status === 'fulfilled') {
      const veri = sonuclar[1].value;
      const sayim = {};
      veri.gorevler.forEach(function (g) { sayim[g.durum] = (sayim[g.durum] || 0) + 1; });
      const acik = (sayim.inbox || 0) + (sayim.active || 0) + (sayim.waiting || 0) + (sayim.blocked || 0);
      const aktifSayi = sayim.active || 0, engelSayi = sayim.blocked || 0;
      alan.append(kart('Açık Görevler', String(acik),
        el('span', { class: 'rozet ' + (engelSayi ? 'kotu' : (aktifSayi ? 'uyari' : 'iyi')), text: aktifSayi + ' aktif · ' + engelSayi + ' engelli' }),
        '#gorevler', (sayim.inbox || 0) + ' gelen · ' + (sayim.waiting || 0) + ' bekliyor'));
      const oncelikSira = { blocked: 0, active: 1, inbox: 2, waiting: 3 };
      const odak = veri.gorevler
        .filter(function (g) { return g.durum in oncelikSira; })
        .sort(function (a, b) { return oncelikSira[a.durum] - oncelikSira[b.durum]; })
        .slice(0, 6);
      if (!odak.length) {
        odakListe.append(el('li', { class: 'bos', text: 'Açık görev yok. Yukarıdan hızlıca ekleyebilirsin.' }));
      } else {
        odak.forEach(function (g) { odakListe.append(odakGorevSatiri(g, veri.durumlar)); });
      }
    } else {
      odakListe.append(el('li', { class: 'bos', text: sonuclar[1].reason.message }));
    }

    // 3) Hafıza kartı + doluluk çubukları
    const hafizaListe = bosalt($('kokpit-hafiza-liste'));
    const hafizaAlt = bosalt($('kokpit-hafiza-alt'));
    if (sonuclar[3].status === 'fulfilled') {
      const h = sonuclar[3].value;
      const dosyalar = h.dosyalar || [];
      const asanSayi = dosyalar.filter(function (f) { return f.durum === 'planned' || f.durum === 'needs_rewrite' || f.durum === 'needs_attention'; }).length;
      alan.append(kart('Hafıza', asanSayi ? asanSayi + ' dosya dolu' : 'Sınır içinde',
        el('span', { class: 'rozet ' + (asanSayi ? 'uyari' : 'iyi'), text: HAFIZA[h.durum] || h.durum || 'tamam' }),
        '#hafiza', dosyalar.length + ' izlenen dosya'));
      if (!dosyalar.length) {
        hafizaListe.append(el('li', { class: 'bos', text: 'Sınırı olan hafıza dosyası yok.' }));
      } else {
        dosyalar.forEach(function (f) {
          const oran = f.sinir ? Math.round(((f.karakter || 0) / f.sinir) * 100) : 0;
          const olcu = el('meter', { min: 0, max: f.sinir || 1, value: Math.min(f.karakter || 0, f.sinir || 1) });
          hafizaListe.append(el('li', {},
            el('div', { class: 'odak-satir' },
              el('strong', { text: f.ad }),
              el('span', { class: 'rozet ' + (oran >= 90 ? 'uyari' : 'iyi'), text: (f.sinir ? '%' + oran : 'sınırsız') })),
            el('div', { class: 'ust-bilgi' },
              el('span', { text: (f.karakter ?? 0) + ' / ' + (f.sinir || 'sınırsız') + ' karakter' }),
              el('span', { text: HAFIZA[f.durum] || f.durum || '' })),
            olcu));
        });
      }
      if (asanSayi && !SALT_OKUNUR) {
        const sikistirBtn = el('button', { type: 'button', text: 'Hafızayı sıkıştır' });
        sikistirBtn.addEventListener('click', async function () {
          await sikistir();
          kokpit();
        });
        hafizaAlt.append(el('span', { class: 'alt-not', text: 'Eski girdiler silinmeden arşive taşınır.' }), sikistirBtn);
      }
    } else if (sonuclar[0].status === 'fulfilled') {
      const asan = (sonuclar[0].value.hafiza && sonuclar[0].value.hafiza.asan) || [];
      alan.append(kart('Hafıza', asan.length ? asan.length + ' dosya dolu' : 'Sınır içinde',
        el('span', { class: 'rozet ' + (asan.length ? 'uyari' : 'iyi'), text: asan.join(', ') || 'tamam' }), '#hafiza'));
      hafizaListe.append(el('li', { class: 'bos', text: sonuclar[3].reason.message }));
    }

    // 4) Dikkat bekleyenler (Triage) kartı + kutular
    const dikkatAlan = bosalt($('kokpit-dikkat'));
    if (sonuclar[4].status === 'fulfilled') {
      const r = sonuclar[4].value;
      const gelenSayi = (r.inbox && r.inbox.count) || 0;
      const bayatKonu = (r.bayat_konular || []).length;
      const bayatGorev = (r.gorevler && r.gorevler.stale_count) || 0;
      const taslakSayi = (r.taslaklar || []).length;
      const toplamDikkat = gelenSayi + bayatKonu + bayatGorev + taslakSayi;
      alan.append(kart('Gözden Geçir', String(toplamDikkat),
        el('span', { class: 'rozet ' + (toplamDikkat ? 'uyari' : 'iyi'), text: toplamDikkat ? 'Bakım bekliyor' : 'Her şey güncel' }),
        '#gozden-gecir', bayatKonu + ' bayat konu · ' + taslakSayi + ' taslak'));
      const kalemler = [
        ['Gelen kutusu', gelenSayi],
        ['Bayat konular', bayatKonu],
        ['Bayat görevler', bayatGorev],
        ['Taslak notlar', taslakSayi]
      ];
      kalemler.forEach(function (pair) {
        dikkatAlan.append(el('a', { class: 'dikkat-kutu', href: '#gozden-gecir' },
          el('span', { text: pair[0] }),
          el('span', { class: 'sayi rozet ' + (pair[1] ? 'uyari' : 'iyi'), text: String(pair[1]) })));
      });
    } else {
      dikkatAlan.append(el('p', { class: 'bos', text: sonuclar[4].reason.message }));
    }

    // 5) Beyin Haritası özet kartı
    if (sonuclar[5].status === 'fulfilled') {
      const g = sonuclar[5].value;
      alan.append(kart('Beyin Haritası', (g.dugumler || []).length + ' not',
        el('span', { class: 'rozet', text: (g.kenarlar || []).length + ' bağlantı' }),
        '#graf', 'Haritayı aç'));
    }

    // Son kayıtlar (Receipt'ler)
    const liste = bosalt($('kokpit-makbuzlar'));
    if (sonuclar[2].status === 'fulfilled') {
      const items = sonuclar[2].value.makbuzlar.slice(0, 5);
      if (!items.length) { liste.append(el('li', { class: 'bos', text: 'Son ' + sonuclar[2].value.gun + ' günde kayıt yok.' })); }
      items.forEach(function (m) { liste.append(makbuzSatiri(m)); });
    } else {
      liste.append(el('li', { class: 'bos', text: sonuclar[2].reason.message }));
    }

    $('kokpit-zaman').textContent = 'Son güncelleme: ' + new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  }

  // --- görevler ---------------------------------------------------------
  let gorevVerisi = null;
  let gorevKapaliGoster = false;
  let suruklenenGorev = null;
  let sonGorevDetay = 0;

  function durumSecici(secili, durumlar) {
    const secim = el('select', { 'aria-label': 'Durum', disabled: SALT_OKUNUR });
    durumlar.forEach(function (d) { secim.append(el('option', { value: d, text: DURUM[d] || d, selected: d === secili })); });
    return secim;
  }
  async function gorevDurumDegistir(g, yeniDurum) {
    if (!g || g.durum === yeniDurum) { return; }
    try {
      await api('/api/gorev/durum', { id: g.id, revizyon: g.revizyon, durum: yeniDurum });
      bildir('Görev taşındı (' + (DURUM[yeniDurum] || yeniDurum) + '): ' + g.baslik);
    } catch (error) { bildir('Güncellenemedi: ' + error.message, true); }
    gorevler();
  }
  async function gorevDetayAc(g) {
    const istek = ++sonGorevDetay;
    const kutu = $('gorev-detay');
    kutu.hidden = false;
    $('gorev-detay-baslik').textContent = g.baslik;
    $('gorev-detay-meta').textContent = (DURUM[g.durum] || g.durum) +
      (g.proje ? ' · #' + g.proje : '') + (g.sorumlu ? ' · @' + g.sorumlu : '') +
      (g.kaynak ? ' · ' + g.kaynak : '');
    $('gorev-detay-metin').textContent = 'Yükleniyor…';
    try {
      const kayit = await api('/api/kayit?id=' + encodeURIComponent(g.id));
      if (istek !== sonGorevDetay) { return; }
      $('gorev-detay-metin').textContent = kayit.metin + (kayit.kisaltildi ? '\n\n[Kısaltıldı]' : '');
    } catch (error) {
      if (istek === sonGorevDetay) { $('gorev-detay-metin').textContent = error.message; }
    }
  }
  function gorevKarti(g, durumlar) {
    const secim = durumSecici(g.durum, durumlar);
    secim.addEventListener('change', function () {
      secim.disabled = true;
      gorevDurumDegistir(g, secim.value);
    });
    const baslikBtn = el('button', { type: 'button', class: 'gorev-baslik', text: g.baslik });
    baslikBtn.addEventListener('click', function () { gorevDetayAc(g); });
    const bugun = new Date().toISOString().slice(0, 10);
    const bilgi = el('div', { class: 'ust-bilgi' });
    if (g.proje) { bilgi.append(el('span', { class: 'rozet', text: '#' + g.proje })); }
    if (g.sorumlu) { bilgi.append(el('span', { text: '@' + g.sorumlu })); }
    if (g.bitis) {
      const gun = String(g.bitis).slice(0, 10);
      const gecikmis = gun < bugun && g.durum !== 'done' && g.durum !== 'cancelled';
      bilgi.append(el('span', { class: gecikmis ? 'rozet kotu' : '', text: (gecikmis ? 'gecikti ' : 'bitiş ') + gun }));
    }
    if (g.oncelik) { bilgi.append(el('span', { class: 'rozet uyari', text: 'öncelik ' + g.oncelik })); }
    if (g.kati) { bilgi.append(el('span', { class: 'rozet', text: 'kanıtlı kapanış' })); }
    const ozetMetin = (g.ozet || '').trim();
    const ozetGoster = ozetMetin && ozetMetin.toLowerCase() !== g.baslik.trim().toLowerCase();
    const kart = el('div', { class: 'gorev', title: g.kaynak || '', draggable: !SALT_OKUNUR },
      baslikBtn,
      ozetGoster ? el('div', { class: 'gorev-ozet', text: ozetMetin }) : null,
      bilgi,
      el('div', { class: 'gorev-alt' }, secim));
    if (!SALT_OKUNUR) {
      kart.addEventListener('dragstart', function (olay) {
        suruklenenGorev = g;
        kart.classList.add('surukleniyor');
        if (olay.dataTransfer) { olay.dataTransfer.effectAllowed = 'move'; olay.dataTransfer.setData('text/plain', g.id); }
      });
      kart.addEventListener('dragend', function () {
        suruklenenGorev = null;
        kart.classList.remove('surukleniyor');
        document.querySelectorAll('.sutun.hedef').forEach(function (s) { s.classList.remove('hedef'); });
      });
    }
    return kart;
  }
  function panoyuCiz() {
    if (!gorevVerisi) { return; }
    const projeFiltre = $('proje-filtre').value;
    const sorumluFiltre = $('sorumlu-filtre').value;
    const arama = $('gorev-ara').value.trim().toLocaleLowerCase('tr-TR');
    const pano = bosalt($('gorev-pano'));
    const gorunenDurumlar = gorevKapaliGoster
      ? gorevVerisi.durumlar
      : gorevVerisi.durumlar.filter(function (d) { return d !== 'done' && d !== 'cancelled'; });
    const sayim = {};
    gorevVerisi.gorevler.forEach(function (g) { sayim[g.durum] = (sayim[g.durum] || 0) + 1; });
    const kapaliSayi = (sayim.done || 0) + (sayim.cancelled || 0);
    const acikSayi = gorevVerisi.gorevler.length - kapaliSayi;
    $('gorev-kapali-goster').textContent = gorevKapaliGoster
      ? 'Kapalıları gizle (' + kapaliSayi + ')'
      : 'Kapalıları göster (' + kapaliSayi + ')';
    const ozetSerit = bosalt($('gorev-ozet'));
    ozetSerit.append(
      el('span', { class: 'rozet', text: acikSayi + ' açık' }),
      el('span', { class: 'rozet uyari', text: (sayim.active || 0) + ' aktif' }),
      el('span', { class: 'rozet ' + ((sayim.blocked || 0) ? 'kotu' : ''), text: (sayim.blocked || 0) + ' engelli' }),
      el('span', { class: 'rozet iyi', text: (sayim.done || 0) + ' bitti' })
    );
    gorunenDurumlar.forEach(function (d) {
      const kartlar = gorevVerisi.gorevler.filter(function (g) {
        if (g.durum !== d) { return false; }
        if (projeFiltre && g.proje !== projeFiltre) { return false; }
        if (sorumluFiltre && g.sorumlu !== sorumluFiltre) { return false; }
        if (arama) {
          const metin = [g.baslik, g.proje, g.sorumlu, g.ozet].filter(Boolean).join(' ').toLocaleLowerCase('tr-TR');
          if (!metin.includes(arama)) { return false; }
        }
        return true;
      });
      const sutun = el('div', { class: 'sutun s-' + d, 'data-durum': d },
        el('h3', {}, el('span', { text: DURUM[d] || d }), el('span', { class: 'rozet', text: String(kartlar.length) })),
        DURUM_ACIKLAMA[d] ? el('p', { class: 'sutun-aciklama', text: DURUM_ACIKLAMA[d] }) : null);
      if (!SALT_OKUNUR) {
        sutun.addEventListener('dragover', function (olay) {
          if (!suruklenenGorev || suruklenenGorev.durum === d) { return; }
          olay.preventDefault();
          sutun.classList.add('hedef');
        });
        sutun.addEventListener('dragleave', function () { sutun.classList.remove('hedef'); });
        sutun.addEventListener('drop', function (olay) {
          olay.preventDefault();
          sutun.classList.remove('hedef');
          if (suruklenenGorev && suruklenenGorev.durum !== d) {
            const hedefGorev = suruklenenGorev;
            suruklenenGorev = null;
            gorevDurumDegistir(hedefGorev, d);
          }
        });
      }
      if (!kartlar.length) {
        sutun.append(el('div', { class: 'bos-sutun', text: 'Görev yok' }));
      } else {
        kartlar.forEach(function (g) { sutun.append(gorevKarti(g, gorevVerisi.durumlar)); });
      }
      pano.append(sutun);
    });
  }
  async function gorevler() {
    try { gorevVerisi = await api('/api/gorevler'); }
    catch (error) { bosalt($('gorev-pano')).append(el('p', { class: 'bos', text: error.message })); return; }
    const projeler = Array.from(new Set(gorevVerisi.gorevler.map(function (g) { return g.proje; }).filter(Boolean))).sort();
    const filtre = $('proje-filtre'); const onceki = filtre.value;
    bosalt(filtre).append(el('option', { value: '', text: 'Tüm projeler' }));
    projeler.forEach(function (p) { filtre.append(el('option', { value: p, text: p, selected: p === onceki })); });
    const sorumlular = Array.from(new Set(gorevVerisi.gorevler.map(function (g) { return g.sorumlu; }).filter(Boolean))).sort();
    const sFiltre = $('sorumlu-filtre'); const sOnceki = sFiltre.value;
    bosalt(sFiltre).append(el('option', { value: '', text: 'Tüm sorumlular' }));
    sorumlular.forEach(function (s) { sFiltre.append(el('option', { value: s, text: '@' + s, selected: s === sOnceki })); });
    const liste = bosalt($('proje-onerileri'));
    projeler.forEach(function (p) { liste.append(el('option', { value: p })); });
    const yeniDurum = $('yeni-durum');
    if (!yeniDurum.options.length) {
      gorevVerisi.durumlar.forEach(function (d) { yeniDurum.append(el('option', { value: d, text: DURUM[d] || d, selected: d === 'inbox' })); });
    }
    const not = [];
    if (gorevVerisi.eski) { not.push(gorevVerisi.eski + ' görev dosyası dizinden sonra değişti; Eşitle ile güncelle.'); }
    if (gorevVerisi.kisaltildi) { not.push('İlk ' + gorevVerisi.gorevler.length + ' görev gösteriliyor (toplam ' + gorevVerisi.toplam + ').'); }
    $('gorev-notu').textContent = not.join(' ');
    panoyuCiz();
  }
  async function gorevOlustur(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const veri = { baslik: form.baslik.value, aciklama: form.aciklama.value, sorumlu: form.sorumlu.value,
      proje: form.proje.value, durum: form.durum.value };
    form.querySelector('button').disabled = true;
    try {
      const sonuc = await api('/api/gorev', veri);
      bildir('Görev oluşturuldu: ' + sonuc.gorev.baslik);
      form.baslik.value = ''; form.aciklama.value = '';
      gorevler();
    } catch (error) { bildir('Görev oluşturulamadı: ' + error.message, true); }
    form.querySelector('button').disabled = false;
  }

  // --- arama ------------------------------------------------------------
  let sonAramaOnizleme = 0;
  function vurguluMetin(metin, sorgu) {
    const kap = el('div', { class: 'arama-ozet ozet' });
    const yazi = String(metin || '');
    const kelimeler = Array.from(new Set(String(sorgu || '').split(/\s+/).filter(function (w) { return w.length >= 2; })));
    if (!kelimeler.length || !yazi) { kap.textContent = yazi; return kap; }
    const kacan = kelimeler.map(function (w) { return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|');
    const re = new RegExp('(' + kacan + ')', 'gi');
    yazi.split(re).forEach(function (parca, idx) {
      if (!parca) { return; }
      kap.append(idx % 2 === 1 ? el('mark', { class: 'vurgu', text: parca }) : document.createTextNode(parca));
    });
    return kap;
  }
  async function ara(event) {
    event.preventDefault();
    const sorgu = $('arama-sorgu').value.trim();
    const liste = bosalt($('arama-sonuclari'));
    const durum = $('arama-durum');
    if (sorgu.length < 2) {
      durum.textContent = '';
      liste.append(el('li', { class: 'bos', text: 'Aramak için en az iki harf yaz.' }));
      return;
    }
    durum.textContent = 'Aranıyor…';
    try {
      const veri = await api('/api/ara?q=' + encodeURIComponent(sorgu));
      durum.textContent = veri.sonuclar.length + ' sonuç bulundu';
      if (!veri.sonuclar.length) {
        liste.append(el('li', { class: 'bos', text: '"' + sorgu + '" için sonuç bulunamadı.' }));
        return;
      }
      veri.sonuclar.forEach(function (s) {
        const bilgi = el('div', { class: 'ust-bilgi' },
          el('span', { class: 'rozet', text: TUR[s.tur] || s.tur || 'not' }));
        if (s.durum) { bilgi.append(el('span', { class: 'rozet', text: DURUM[s.durum] || s.durum })); }
        if (s.kaynak) { bilgi.append(el('span', { text: s.kaynak })); }
        const satir = el('li', { class: 'sonuc', tabIndex: 0 },
          el('strong', { text: s.baslik }),
          bilgi,
          vurguluMetin(s.ozet, sorgu));
        const ac = function () {
          liste.querySelectorAll('.sonuc.secili').forEach(function (n) { n.classList.remove('secili'); });
          satir.classList.add('secili');
          onizle(s.id);
        };
        satir.addEventListener('click', ac);
        satir.addEventListener('keydown', function (e) { if (e.key === 'Enter') { ac(); } });
        liste.append(satir);
      });
    } catch (error) {
      durum.textContent = '';
      liste.append(el('li', { class: 'bos', text: error.message }));
    }
  }
  function mdSatir(metin) {
    const frag = document.createDocumentFragment();
    const re = /(`[^`\n]+`|\*\*[^*\n]+\*\*|\*[^*\n]+\*|\[\[[^\]\n]+\]\]|\[[^\]\n]+\]\([^)\n]+\))/g;
    let son = 0, m;
    while ((m = re.exec(metin)) !== null) {
      if (m.index > son) { frag.append(document.createTextNode(metin.slice(son, m.index))); }
      const parca = m[0];
      if (parca.startsWith('`')) { frag.append(el('code', { text: parca.slice(1, -1) })); }
      else if (parca.startsWith('**')) { frag.append(el('strong', { text: parca.slice(2, -2) })); }
      else if (parca.startsWith('*')) { frag.append(el('em', { text: parca.slice(1, -1) })); }
      else if (parca.startsWith('[[')) {
        const ic = parca.slice(2, -2);
        const etiket = ic.includes('|') ? ic.split('|').slice(1).join('|') : ic;
        frag.append(el('span', { class: 'md-wiki', text: etiket.trim() }));
      } else {
        const ayir = parca.indexOf('](');
        frag.append(el('span', { class: 'md-bag', text: parca.slice(1, ayir) }));
      }
      son = m.index + parca.length;
    }
    if (son < metin.length) { frag.append(document.createTextNode(metin.slice(son))); }
    return frag;
  }

  function mdCiz(hedef, metin) {
    bosalt(hedef);
    let kaynak = String(metin || '').replace(/\r\n/g, '\n');
    if (kaynak.startsWith('---\n')) {
      const bitis = kaynak.indexOf('\n---\n', 4);
      if (bitis !== -1) { kaynak = kaynak.slice(bitis + 5); }
    }
    const satirlar = kaynak.split('\n');
    let i = 0;
    while (i < satirlar.length) {
      const s = satirlar[i];
      if (!s.trim()) { i += 1; continue; }
      if (s.trim().startsWith('```')) {
        const kod = [];
        i += 1;
        while (i < satirlar.length && !satirlar[i].trim().startsWith('```')) { kod.push(satirlar[i]); i += 1; }
        if (i < satirlar.length) { i += 1; }
        hedef.append(el('pre', {}, el('code', { text: kod.join('\n') })));
        continue;
      }
      const baslik = s.match(/^(#{1,4})\s+(.*)$/);
      if (baslik) {
        hedef.append(el('h' + baslik[1].length, {}, mdSatir(baslik[2].trim())));
        i += 1; continue;
      }
      if (/^(\*\s*\*\s*\*|-\s*-\s*-|_\s*_\s*_)\s*$/.test(s.trim())) {
        hedef.append(el('hr'));
        i += 1; continue;
      }
      if (s.trim().startsWith('>')) {
        const alinti = [];
        while (i < satirlar.length && satirlar[i].trim().startsWith('>')) {
          alinti.push(satirlar[i].replace(/^\s*>\s?/, ''));
          i += 1;
        }
        hedef.append(el('blockquote', {}, mdSatir(alinti.join(' '))));
        continue;
      }
      if (s.includes('|') && i + 1 < satirlar.length && /^\s*\|?[\s:-]+\|[\s|:-]*$/.test(satirlar[i + 1])) {
        const hucre = function (sat) { return sat.trim().replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); }); };
        const bas = hucre(s);
        const thead = el('thead', {}, el('tr', {}, ...bas.map(function (c) { return el('th', {}, mdSatir(c)); })));
        const tbody = el('tbody');
        i += 2;
        while (i < satirlar.length && satirlar[i].includes('|') && satirlar[i].trim()) {
          const vals = hucre(satirlar[i]);
          tbody.append(el('tr', {}, ...vals.map(function (c) { return el('td', {}, mdSatir(c)); })));
          i += 1;
        }
        hedef.append(el('table', {}, thead, tbody));
        continue;
      }
      if (/^\s*[-*+]\s+/.test(s)) {
        const ul = el('ul');
        while (i < satirlar.length && /^\s*[-*+]\s+/.test(satirlar[i])) {
          let ic = satirlar[i].replace(/^\s*[-*+]\s+/, '');
          if (ic.startsWith('[x] ') || ic.startsWith('[X] ')) { ic = '☑ ' + ic.slice(4); }
          else if (ic.startsWith('[ ] ')) { ic = '☐ ' + ic.slice(4); }
          ul.append(el('li', {}, mdSatir(ic)));
          i += 1;
        }
        hedef.append(ul);
        continue;
      }
      if (/^\s*\d+\.\s+/.test(s)) {
        const ol = el('ol');
        while (i < satirlar.length && /^\s*\d+\.\s+/.test(satirlar[i])) {
          ol.append(el('li', {}, mdSatir(satirlar[i].replace(/^\s*\d+\.\s+/, ''))));
          i += 1;
        }
        hedef.append(ol);
        continue;
      }
      const para = [];
      while (i < satirlar.length && satirlar[i].trim() && !/^(#{1,4}\s|```|\s*[-*+]\s|\s*\d+\.\s|\s*>)/.test(satirlar[i])) {
        para.push(satirlar[i].trim());
        i += 1;
      }
      hedef.append(el('p', {}, mdSatir(para.join(' '))));
    }
    if (!hedef.firstChild) { hedef.append(el('p', { class: 'bos', text: '(boş not)' })); }
  }

  async function onizle(id) {
    const istek = ++sonAramaOnizleme;
    const alan = $('onizleme'); const baslik = $('onizleme-baslik'); const metaAlan = $('onizleme-meta');
    bosalt(alan).append(el('p', { class: 'bos', text: 'Yükleniyor…' }));
    try {
      const kayit = await api('/api/kayit?id=' + encodeURIComponent(id));
      if (istek !== sonAramaOnizleme) { return; }
      baslik.textContent = kayit.baslik;
      metaAlan.textContent = (TUR[kayit.tur] || kayit.tur || 'not') + (kayit.kaynak ? ' · ' + kayit.kaynak : '');
      mdCiz(alan, kayit.metin + (kayit.kisaltildi ? '\n\n*[Kısaltıldı]*' : ''));
    } catch (error) {
      if (istek !== sonAramaOnizleme) { return; }
      baslik.textContent = 'Önizleme';
      metaAlan.textContent = '';
      bosalt(alan).append(el('p', { class: 'bos', text: error.message }));
    }
  }

  // --- işlem kayıtları (receipts) -----------------------------------------
  let makbuzVerisi = null;
  function makbuzGunu(iso) {
    if (!iso) { return 'Tarihsiz'; }
    const d = new Date(iso);
    if (isNaN(d)) { return String(iso).slice(0, 10); }
    const bugun = new Date();
    const dun = new Date(bugun.getFullYear(), bugun.getMonth(), bugun.getDate() - 1);
    const ayniGun = function (a, b) {
      return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
    };
    if (ayniGun(d, bugun)) { return 'Bugün'; }
    if (ayniGun(d, dun)) { return 'Dün'; }
    return d.toLocaleDateString('tr-TR', { dateStyle: 'medium' });
  }
  function makbuzSaati(iso) {
    if (!iso) { return ''; }
    const d = new Date(iso);
    return isNaN(d) ? String(iso) : d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  }
  function makbuzSatiri(m, sadeceSaat) {
    const ust = el('div', { class: 'makbuz-ust' },
      el('span', { class: 'makbuz-saat', text: sadeceSaat ? makbuzSaati(m.zaman) : zaman(m.zaman) }));
    const gizli = m.gizlenen || {};
    if (gizli.private) { ust.append(el('span', { class: 'rozet uyari', text: gizli.private + ' gizli kaynak saklandı' })); }
    const kaynakAlan = el('div', { class: 'makbuz-kaynaklar' });
    (m.kaynaklar || []).slice(0, 8).forEach(function (k) { kaynakAlan.append(el('span', { class: 'kaynak-etiket', text: k })); });
    if ((m.kaynaklar || []).length > 8) {
      kaynakAlan.append(el('span', { class: 'rozet', text: '+' + (m.kaynaklar.length - 8) + ' kaynak daha' }));
    }
    const ozet = el('div', { class: m.ozet_gizli ? 'makbuz-ozet gizli' : 'makbuz-ozet',
      text: m.ozet_gizli ? 'Özet gizli bir kaynağa bağlı; gösterilmiyor.' : (m.ozet || '(özet yok)') });
    return el('li', { class: 'makbuz-kart' }, ust, ozet, kaynakAlan.childNodes.length ? kaynakAlan : null);
  }
  function makbuzListesiniCiz() {
    const kapsayici = bosalt($('makbuz-listesi'));
    if (!makbuzVerisi) { return; }
    const q = ($('makbuz-ara').value || '').trim().toLocaleLowerCase('tr-TR');
    const secilen = makbuzVerisi.makbuzlar.filter(function (m) {
      if (!q) { return true; }
      const metin = ((m.ozet_gizli ? '' : (m.ozet || '')) + ' ' + (m.kaynaklar || []).join(' ')).toLocaleLowerCase('tr-TR');
      return metin.includes(q);
    });
    $('makbuz-sayac').textContent = q
      ? secilen.length + ' / ' + makbuzVerisi.makbuzlar.length + ' kayıt'
      : makbuzVerisi.toplam + ' kayıt';
    if (!secilen.length) {
      kapsayici.append(el('p', { class: 'bos', text: q ? '"' + $('makbuz-ara').value.trim() + '" ile eşleşen kayıt yok.' : 'Son ' + makbuzVerisi.gun + ' günde işlem kaydı yok.' }));
      return;
    }
    let sonGun = null;
    let gunUl = null;
    secilen.forEach(function (m) {
      const gun = makbuzGunu(m.zaman);
      if (gun !== sonGun) {
        sonGun = gun;
        kapsayici.append(el('div', { class: 'makbuz-gun', text: gun }));
        gunUl = el('ul', { class: 'liste' });
        kapsayici.append(gunUl);
      }
      gunUl.append(makbuzSatiri(m, true));
    });
  }
  async function makbuzlar() {
    const ozetAlan = bosalt($('makbuz-ozet'));
    const kapsayici = bosalt($('makbuz-listesi'));
    kapsayici.append(el('p', { class: 'bos', text: 'Yükleniyor…' }));
    try {
      makbuzVerisi = await api('/api/makbuzlar');
      $('makbuz-notu').textContent = 'Son ' + makbuzVerisi.gun + ' gündeki ajan işlem özetleri. Özetler ajan beyanıdır; kaynak dosyalarla doğrula.';
      const kaynakSet = new Set();
      let gizliSayi = 0;
      makbuzVerisi.makbuzlar.forEach(function (m) {
        (m.kaynaklar || []).forEach(function (k) { kaynakSet.add(k); });
        gizliSayi += (m.gizlenen && m.gizlenen.private) || 0;
      });
      const sonZaman = makbuzVerisi.makbuzlar.length ? zaman(makbuzVerisi.makbuzlar[0].zaman) : 'Yok';
      ozetAlan.append(
        kart('Toplam kayıt', String(makbuzVerisi.toplam), el('span', { class: 'rozet', text: 'Son ' + makbuzVerisi.gun + ' gün' })),
        kart('Dokunulan kaynak', String(kaynakSet.size), el('span', { class: 'rozet', text: 'Farklı dosya' })),
        kart('Son kayıt', sonZaman, el('span', { class: 'rozet ' + (makbuzVerisi.makbuzlar.length ? 'iyi' : ''), text: makbuzVerisi.makbuzlar.length ? 'Güncel' : 'Boş' })),
        kart('Saklanan gizli kaynak', String(gizliSayi), el('span', { class: 'rozet ' + (gizliSayi ? 'uyari' : 'iyi'), text: gizliSayi ? 'Gizlilik koruması' : 'Temiz' }))
      );
      makbuzListesiniCiz();
    } catch (error) {
      bosalt(kapsayici).append(el('p', { class: 'bos', text: error.message }));
    }
  }

  // --- hafıza -----------------------------------------------------------
  const HAFIZA_ACIKLAMA = {
    'Core.md': 'Kimlik, çalışma biçimi ve temel bağlam',
    'Kurallar.md': 'Ajanların her oturumda uyması gereken kurallar',
    'Last-Session.md': 'Son oturum özetleri ve devir notları',
    'Threads.md': 'Açık kalan konular ve takip başlıkları',
    'Journal.md': 'Dönemsel gözlemler ve çalışma günlüğü'
  };
  let sonHafizaOnizleme = 0;
  async function hafizaOnizle(yol, ad) {
    const istek = ++sonHafizaOnizleme;
    const baslik = $('hafiza-onizleme-baslik');
    const metaAlan = $('hafiza-onizleme-meta');
    const alan = $('hafiza-onizleme');
    baslik.textContent = ad || 'Önizleme';
    metaAlan.textContent = yol || '';
    bosalt(alan).append(el('p', { class: 'bos', text: 'Yükleniyor…' }));
    try {
      const not = await api('/api/not?yol=' + encodeURIComponent(yol));
      if (istek !== sonHafizaOnizleme) { return; }
      mdCiz(alan, (not.metin || '') + (not.kisaltildi ? '\n\n*… (not kısaltıldı)*' : ''));
    } catch (error) {
      if (istek !== sonHafizaOnizleme) { return; }
      bosalt(alan).append(el('p', { class: 'bos', text: error.message }));
    }
  }
  function hafizaSatiriBagla(satir, yol, ad) {
    if (!yol) { return; }
    satir.classList.add('sonuc');
    satir.tabIndex = 0;
    const ac = function () {
      document.querySelectorAll('#gorunum-hafiza .sonuc.secili').forEach(function (n) { n.classList.remove('secili'); });
      satir.classList.add('secili');
      hafizaOnizle(yol, ad);
    };
    satir.addEventListener('click', ac);
    satir.addEventListener('keydown', function (e) { if (e.key === 'Enter') { ac(); } });
  }
  async function hafiza() {
    const ozetAlan = bosalt($('hafiza-ozet'));
    const liste = bosalt($('hafiza-listesi'));
    const cekirdekListe = bosalt($('hafiza-cekirdek'));
    liste.append(el('li', { class: 'bos', text: 'Yükleniyor…' }));
    try {
      const veri = await api('/api/hafiza');
      bosalt(liste);
      const durumMetin = HAFIZA[veri.durum] || veri.durum || '';
      const durumSinif = veri.durum === 'within_limit' || veri.durum === 'ok' ? 'iyi'
        : (veri.durum === 'needs_attention' || veri.durum === 'needs_rewrite' ? 'kotu' : 'uyari');
      $('hafiza-notu').textContent = (veri.dizin ? veri.dizin + ': ' : '') + durumMetin + (veri.neden ? ' · ' + veri.neden : '');
      const dosyalar = veri.dosyalar || [];
      const cekirdek = veri.cekirdek || [];
      let topKarakter = 0, topSinir = 0, topTasinacak = 0;
      dosyalar.forEach(function (f) {
        topKarakter += f.karakter || 0;
        topSinir += f.sinir || 0;
        topTasinacak += f.tasinacak || 0;
      });
      const yuzdeTop = topSinir ? Math.round((topKarakter / topSinir) * 100) : 0;
      const dolulukSinif = yuzdeTop >= 95 ? 'kotu' : (yuzdeTop >= 70 ? 'uyari' : 'iyi');
      ozetAlan.append(
        kart('Genel durum', durumMetin || 'Bilinmiyor', el('span', { class: 'rozet ' + durumSinif, text: veri.durum || '?' })),
        kart('Limit doluluğu', topSinir ? '%' + yuzdeTop : 'Sınırsız',
          el('span', { class: 'rozet ' + dolulukSinif, text: topKarakter + ' / ' + (topSinir || 'sınırsız') + ' karakter' })),
        kart('Arşive taşınacak', topTasinacak ? topTasinacak + ' kar.' : '0',
          el('span', { class: 'rozet ' + (topTasinacak ? 'uyari' : 'iyi'), text: topTasinacak ? 'Sıkıştırma hazır' : 'Gerekmiyor' })),
        kart('Hafıza dosyaları', String(dosyalar.length + cekirdek.length),
          el('span', { class: 'rozet', text: veri.dizin || 'Companion' }))
      );
      const sikistirBtn = $('sikistir');
      const sikistirNot = $('hafiza-sikistir-not');
      sikistirBtn.disabled = SALT_OKUNUR || !topTasinacak;
      sikistirNot.textContent = SALT_OKUNUR
        ? 'Salt okunur modda sıkıştırma kapalı.'
        : (topTasinacak ? topTasinacak + ' karakter arşive taşınacak; hiçbir girdi silinmez.' : 'Tüm dosyalar sınır içinde; şu an sıkıştırma gerekmiyor.');

      if (!dosyalar.length) {
        liste.append(el('li', { class: 'bos', text: 'Sınırı olan hafıza dosyası yok.' }));
      }
      dosyalar.forEach(function (f) {
        const yuzde = f.sinir ? Math.min(100, Math.round(((f.karakter || 0) / f.sinir) * 100)) : 0;
        const renkSinif = yuzde >= 95 ? 'kotu' : (yuzde >= 70 ? 'uyari' : '');
        const ic = el('div', { class: 'doluluk-ic ' + renkSinif });
        ic.style.width = yuzde + '%';
        const tasinacak = f.tasinacak ? ' · taşınacak ' + f.tasinacak + ' kar.' : '';
        const aciklama = HAFIZA_ACIKLAMA[f.ad] ? el('div', { class: 'sutun-aciklama', text: HAFIZA_ACIKLAMA[f.ad] }) : null;
        const satir = el('li', {},
          el('strong', { text: f.ad }),
          aciklama,
          el('div', { class: 'ust-bilgi' },
            el('span', { text: (f.karakter ?? 0) + ' / ' + (f.sinir || 'sınırsız') + ' karakter (' + (f.sinir ? '%' + yuzde : 'sınırsız') + ')' + tasinacak }),
            el('span', { class: 'rozet ' + (renkSinif || 'iyi'), text: HAFIZA[f.durum] || f.durum || '' })),
          el('div', { class: 'doluluk-cubuk' }, ic));
        hafizaSatiriBagla(satir, f.yol, f.ad);
        liste.append(satir);
      });

      if (!cekirdek.length) {
        cekirdekListe.append(el('li', { class: 'bos', text: 'Başka görünür hafıza dosyası yok (önce Eşitle çalıştırabilirsin).' }));
      }
      cekirdek.forEach(function (c) {
        const aciklama = HAFIZA_ACIKLAMA[c.ad] ? el('div', { class: 'sutun-aciklama', text: HAFIZA_ACIKLAMA[c.ad] }) : null;
        const satir = el('li', {},
          el('strong', { text: c.ad }),
          aciklama,
          el('div', { class: 'ust-bilgi' },
            el('span', { text: (c.karakter ?? 0) + ' karakter' }),
            el('span', { class: 'rozet', text: 'Salt okunur' })));
        hafizaSatiriBagla(satir, c.yol, c.ad);
        cekirdekListe.append(satir);
      });
    } catch (error) {
      bosalt(liste).append(el('li', { class: 'bos', text: error.message }));
    }
  }
  async function sikistir() {
    if (!window.confirm('Eski Last-Session/Threads girdileri arşive aynen taşınacak; hiçbir şey silinmez. Devam edilsin mi?')) { return; }
    try {
      const sonuc = await api('/api/hafiza/sikistir', {});
      bildir('Sıkıştırma: ' + (HAFIZA[sonuc.durum] || sonuc.durum) + (sonuc.neden ? ' · ' + sonuc.neden : ''));
    } catch (error) { bildir('Sıkıştırılamadı: ' + error.message, true); }
    hafiza();
  }

  // --- gözden geçir -----------------------------------------------------
  let sonGozdenYukleme = 0;
  let sonGozdenOnizleme = 0;
  async function gozdenOnizle(id) {
    const istek = ++sonGozdenOnizleme;
    const alan = $('gozden-onizleme'); const baslik = $('gozden-onizleme-baslik');
    try {
      const kayit = await api('/api/kayit?id=' + encodeURIComponent(id));
      if (istek !== sonGozdenOnizleme) { return; }
      baslik.textContent = kayit.baslik + ' (' + kayit.kaynak + ')';
      mdCiz(alan, kayit.metin + (kayit.kisaltildi ? '\n\n*[Kısaltıldı]*' : ''));
    } catch (error) {
      if (istek !== sonGozdenOnizleme) { return; }
      baslik.textContent = 'Önizleme';
      bosalt(alan).append(el('p', { class: 'bos', text: error.message }));
    }
  }
  function gozdenKaynak(row) {
    if (!row.record_id) { return el('span', { text: row.path }); }
    const dugme = el('button', { type: 'button', class: 'kaynak-btn', text: row.path });
    dugme.addEventListener('click', function () { gozdenOnizle(row.record_id); });
    return dugme;
  }

  async function gozgecir() {
    const istek = ++sonGozdenYukleme;
    sonGozdenOnizleme += 1;
    $('gozden-onizleme-baslik').textContent = 'Önizleme';
    $('gozden-onizleme').textContent = 'Kayıt seçin…';
    const inboxDiv = bosalt($('gozden-inbox'));
    const konularList = bosalt($('gozden-konular'));
    const gorevDiv = bosalt($('gozden-gorevler'));
    const taslaklarList = bosalt($('gozden-taslaklar'));
    const ozet = bosalt($('gozden-ozet'));
    try {
      const veri = await api('/api/gozden-gecir');
      if (istek !== sonGozdenYukleme) { return; }
      const inbox = veri.inbox || {};
      const inboxSayi = inbox.count ?? 0;
      $('gozden-sayi-inbox').textContent = String(inboxSayi);
      inboxDiv.append(el('p', { text: 'Öğe sayısı: ' + inboxSayi + (inbox.status ? ' (' + inbox.status + ')' : '') }));
      if (inbox.folders && inbox.folders.length) {
        const ul = el('ul', { class: 'liste' });
        inbox.folders.forEach(function (f) {
          ul.append(el('li', {}, el('strong', { text: f.folder }), el('div', { class: 'ust-bilgi', text: 'Öğe: ' + (f.notes ?? 0) +
            (f.oldest_days == null ? '' : ' · En eski: ' + f.oldest_days + ' gün') })));
        });
        inboxDiv.append(ul);
      }
      const bayat = veri.bayat_konular || [];
      $('gozden-sayi-konular').textContent = String(bayat.length);
      if (!bayat.length) {
        konularList.append(el('li', { class: 'bos', text: 'Bayat konu yok.' }));
      } else {
        bayat.forEach(function (k) {
          konularList.append(el('li', {},
            el('strong', { text: k.title }),
            el('div', { class: 'ust-bilgi' },
              gozdenKaynak(k),
              el('span', { text: k.age_days == null ? '' : 'Yaş: ' + k.age_days + ' gün' }),
              el('span', { text: k.last_date ? 'Son: ' + k.last_date : '' }))
          ));
        });
      }
      const gorevlerData = veri.gorevler || {};
      const bayatGorevSayi = gorevlerData.stale_count ?? 0;
      $('gozden-sayi-gorevler').textContent = String(bayatGorevSayi);
      gorevDiv.append(el('p', { text: 'Açık: ' + (gorevlerData.open_count ?? 0) + ' · Bayat: ' + bayatGorevSayi }));
      const staleTasks = gorevlerData.stale_tasks || [];
      if (staleTasks.length) {
        const ul = el('ul', { class: 'liste' });
        staleTasks.forEach(function (st) {
          ul.append(el('li', {}, el('strong', { text: st.title }),
            el('div', { class: 'ust-bilgi' }, gozdenKaynak(st),
              el('span', { class: 'rozet', text: DURUM[st.status] || st.status || '' }),
              el('span', { text: st.age_days == null ? '' : 'Yaş: ' + st.age_days + ' gün' }))));
        });
        gorevDiv.append(ul);
      }
      const taslaklar = veri.taslaklar || [];
      $('gozden-sayi-taslaklar').textContent = String(taslaklar.length);
      if (!taslaklar.length) {
        taslaklarList.append(el('li', { class: 'bos', text: 'Taslak not yok.' }));
      } else {
        taslaklar.forEach(function (t) {
          const satir = el('li', { class: 'sonuc', tabIndex: 0 },
            el('strong', { text: t.baslik }),
            el('div', { class: 'ust-bilgi' }, el('span', { class: 'rozet', text: t.durum || 'taslak' }), el('span', { text: t.kaynak || '' }), el('span', { text: zaman(t.tarih) }))
          );
          const ac = function () { gozdenOnizle(t.id); };
          satir.addEventListener('click', ac);
          satir.addEventListener('keydown', function (e) { if (e.key === 'Enter') { ac(); } });
          taslaklarList.append(satir);
        });
      }
      const toplam = inboxSayi + bayat.length + bayatGorevSayi + taslaklar.length;
      ozet.append(
        el('span', { class: 'rozet ' + (toplam ? 'uyari' : 'iyi'), text: toplam ? toplam + ' dikkat öğesi' : 'Her şey güncel' }),
        el('span', { class: 'rozet', text: inboxSayi + ' gelen kutusu' }),
        el('span', { class: 'rozet', text: bayat.length + ' bayat konu' }),
        el('span', { class: 'rozet', text: taslaklar.length + ' taslak' })
      );
    } catch (error) {
      if (istek === sonGozdenYukleme) {
        inboxDiv.append(el('p', { class: 'bos', text: error.message }));
      }
    }
  }

  // --- graf -------------------------------------------------------------
  const GRAF_RENK = { knowledge: '#f9d71c', daily: '#8ab4f8', receipts: '#67df70', companion: '#ffb4ab', 'kök': '#7dd3fc' };
  const GRAF_ETIKET = { knowledge: 'Bilgi', daily: 'Günlük', receipts: 'Kayıtlar', companion: 'Hafıza', diger: 'Diğer' };
  function grafKategori(tur) { return (tur in GRAF_ETIKET && tur !== 'diger') ? tur : 'diger'; }
  function grafEtiket(tur) { return GRAF_ETIKET[grafKategori(tur)] || 'Diğer'; }
  const BEYIN_SAG = [
    [0.03, -0.84], [0.11, -0.96], [0.24, -0.99], [0.35, -0.95], [0.48, -0.92],
    [0.57, -0.84], [0.69, -0.77], [0.75, -0.65], [0.85, -0.54], [0.87, -0.40],
    [0.95, -0.26], [0.92, -0.12], [0.98, 0.03], [0.94, 0.17], [0.93, 0.31],
    [0.86, 0.43], [0.82, 0.56], [0.73, 0.67], [0.64, 0.78], [0.53, 0.85],
    [0.43, 0.94], [0.31, 0.96], [0.19, 0.99], [0.09, 0.93], [0.03, 0.82],
    [0.04, 0.56], [0.03, 0.28], [0.04, 0.00], [0.03, -0.28], [0.04, -0.56]
  ];
  const BEYIN_IC = BEYIN_SAG.map(function (p) {
    return [0.46 + (p[0] - 0.46) * 0.82, p[1] * 0.85];
  });
  const BEYIN_DEVRE = [
    [[0.84, -0.56], [1.14, -0.56], [1.26, -0.68], [1.46, -0.68]],
    [[0.94, -0.22], [1.18, -0.22], [1.28, -0.32], [1.44, -0.32]],
    [[0.95, 0.04], [1.48, 0.04]],
    [[0.86, 0.36], [1.14, 0.36], [1.26, 0.48], [1.44, 0.48]],
    [[0.70, 0.66], [1.04, 0.66], [1.18, 0.78], [1.42, 0.78]]
  ];
  let aktifGraf = null;
  let grafMod = 'beyin';
  let grafDinleyiciKuruldu = false;
  function grafRenk(tur) { return GRAF_RENK[tur] || '#7dd3fc'; }

  function metinHash(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i += 1) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return (h >>> 0);
  }

  function cokgendeMi(px, py, poly) {
    let ic = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
      if (((yi > py) !== (yj > py)) && (px < (xj - xi) * (py - yi) / ((yj - yi) || 1e-9) + xi)) { ic = !ic; }
    }
    return ic;
  }

  function enYakinNokta(px, py, poly) {
    let enX = poly[0][0], enY = poly[0][1], enD = Infinity;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const ax = poly[j][0], ay = poly[j][1], bx = poly[i][0], by = poly[i][1];
      const dx = bx - ax, dy = by - ay;
      const len2 = dx * dx + dy * dy || 1e-9;
      const t = Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / len2));
      const qx = ax + t * dx, qy = ay + t * dy;
      const d = (px - qx) * (px - qx) + (py - qy) * (py - qy);
      if (d < enD) { enD = d; enX = qx; enY = qy; }
    }
    return [enX, enY];
  }

  function beyinMetrik(genislik, yukseklik) {
    const ry = Math.min(yukseklik * 0.46, genislik * 0.38);
    const rx = ry * 0.82;
    return { cx: genislik / 2, cy: yukseklik / 2, rx: rx, ry: ry };
  }

  function beyinSinirla(n, m) {
    const taraf = n.taraf;
    let ax = (n.x - m.cx) / m.rx * taraf;
    let ny = (n.y - m.cy) / m.ry;
    if (!cokgendeMi(ax, ny, BEYIN_IC)) {
      const p = enYakinNokta(ax, ny, BEYIN_IC);
      ax = p[0]; ny = p[1];
      n.vx *= 0.45; n.vy *= 0.45;
    }
    n.x = m.cx + ax * taraf * m.rx;
    n.y = m.cy + ny * m.ry;
  }

  function beyinHedef(tur, hash, solSayi, sagSayi) {
    let taraf, yMerkez, yYay;
    if (tur === 'knowledge') { taraf = -1; yMerkez = -0.22; yYay = 0.56; }
    else if (tur === 'companion') { taraf = 1; yMerkez = -0.45; yYay = 0.38; }
    else if (tur === 'daily') { taraf = 1; yMerkez = 0.05; yYay = 0.42; }
    else if (tur === 'receipts') { taraf = 1; yMerkez = 0.54; yYay = 0.32; }
    else { taraf = (hash % 2 === 0) ? -1 : 1; yMerkez = 0.25; yYay = 0.55; }
    // Tek kategori baskınsa iki yarımküreyi dengeli doldur.
    if (solSayi === 0 || sagSayi === 0) { taraf = (hash % 2 === 0) ? -1 : 1; yMerkez = 0; yYay = 0.78; }
    const u1 = ((hash & 0xffff) / 65535);
    const u2 = (((hash >>> 16) & 0xffff) / 65535);
    let ax = 0.16 + u1 * 0.66;
    let ny = Math.max(-0.82, Math.min(0.82, yMerkez + (u2 - 0.5) * 2 * yYay));
    if (!cokgendeMi(ax, ny, BEYIN_IC)) {
      const p = enYakinNokta(ax, ny, BEYIN_IC);
      ax = p[0]; ny = p[1];
    }
    return { taraf: taraf, ax: ax, ny: ny };
  }

  function grafSimule(veri, mod) {
    const genislik = Math.max(320, $('graf-tuval').clientWidth);
    const yukseklik = Math.max(240, $('graf-tuval').clientHeight);
    const m = beyinMetrik(genislik, yukseklik);
    let solAday = 0, sagAday = 0;
    veri.dugumler.forEach(function (n) {
      if (n.tur === 'knowledge') { solAday += 1; }
      else if (n.tur === 'companion' || n.tur === 'daily' || n.tur === 'receipts') { sagAday += 1; }
      else { solAday += 1; sagAday += 1; }
    });
    const dugumler = veri.dugumler.map(function (n) {
      const h = metinHash(n.id);
      const hedef = beyinHedef(n.tur, h, solAday, sagAday);
      let x, y;
      if (mod === 'beyin') {
        x = m.cx + hedef.ax * hedef.taraf * m.rx;
        y = m.cy + hedef.ny * m.ry;
      } else {
        const aci = (h % 3600) / 3600 * Math.PI * 2;
        const yaricap = Math.min(genislik, yukseklik) * (0.16 + ((h >>> 12) % 1000) / 1000 * 0.24);
        x = genislik / 2 + Math.cos(aci) * yaricap;
        y = yukseklik / 2 + Math.sin(aci) * yaricap;
      }
      return { veri: n, x: x, y: y, vx: 0, vy: 0, derece: 0, taraf: hedef.taraf,
        hedefX: m.cx + hedef.ax * hedef.taraf * m.rx, hedefY: m.cy + hedef.ny * m.ry };
    });
    const indeks = {};
    dugumler.forEach(function (d) { indeks[d.veri.id] = d; });
    const kenarlar = veri.kenarlar.map(function (e) { return { a: indeks[e.kaynak], b: indeks[e.hedef] }; })
      .filter(function (e) { return e.a && e.b; });
    const komsu = {};
    kenarlar.forEach(function (e) {
      e.a.derece += 1; e.b.derece += 1;
      (komsu[e.a.veri.id] = komsu[e.a.veri.id] || new Set()).add(e.b.veri.id);
      (komsu[e.b.veri.id] = komsu[e.b.veri.id] || new Set()).add(e.a.veri.id);
    });
    return { dugumler: dugumler, kenarlar: kenarlar, komsu: komsu, olcek: 1, panX: 0, panY: 0,
      secili: null, seciliTur: null, uzerinde: null, genislik: genislik, yukseklik: yukseklik, sabit: null, kare: 0,
      mod: mod, metrik: m, ham: veri };
  }

  function grafFizik(durum) {
    const d = durum.dugumler;
    const beyin = durum.mod === 'beyin';
    const itme = beyin ? 1750 : 4600;
    const hedefMesafe = beyin ? 76 : 165;
    for (let i = 0; i < d.length; i += 1) {
      for (let j = i + 1; j < d.length; j += 1) {
        let dx = d[j].x - d[i].x, dy = d[j].y - d[i].y;
        let uzak = Math.sqrt(dx * dx + dy * dy) || 0.01;
        if (uzak > (beyin ? 260 : 900)) { continue; }
        const kuvvet = Math.min(18, itme / (uzak * uzak));
        dx /= uzak; dy /= uzak;
        d[i].vx -= dx * kuvvet; d[i].vy -= dy * kuvvet;
        d[j].vx += dx * kuvvet; d[j].vy += dy * kuvvet;
      }
    }
    durum.kenarlar.forEach(function (e) {
      let dx = e.b.x - e.a.x, dy = e.b.y - e.a.y;
      const uzak = Math.sqrt(dx * dx + dy * dy) || 0.01;
      const k = beyin ? (e.a.taraf === e.b.taraf ? 0.012 : 0.004) : 0.014;
      const kuvvet = (uzak - hedefMesafe) * k;
      dx /= uzak; dy /= uzak;
      e.a.vx += dx * kuvvet; e.a.vy += dy * kuvvet;
      e.b.vx -= dx * kuvvet; e.b.vy -= dy * kuvvet;
    });
    const cx = durum.genislik / 2, cy = durum.yukseklik / 2;
    d.forEach(function (n) {
      if (durum.sabit === n) { n.vx = 0; n.vy = 0; return; }
      if (beyin) {
        n.vx += (n.hedefX - n.x) * 0.008;
        n.vy += (n.hedefY - n.y) * 0.008;
        n.vx *= 0.80; n.vy *= 0.80;
        n.x += n.vx; n.y += n.vy;
        beyinSinirla(n, durum.metrik);
      } else {
        n.vx += (cx - n.x) * 0.0012; n.vy += (cy - n.y) * 0.0012;
        n.vx *= 0.86; n.vy *= 0.86;
        n.x += n.vx; n.y += n.vy;
      }
    });
  }

  function kapaliEgri(ctx, noktalar) {
    const n = noktalar.length;
    const son = noktalar[n - 1], ilk = noktalar[0];
    ctx.beginPath();
    ctx.moveTo((son[0] + ilk[0]) / 2, (son[1] + ilk[1]) / 2);
    for (let i = 0; i < n; i += 1) {
      const p = noktalar[i], q = noktalar[(i + 1) % n];
      ctx.quadraticCurveTo(p[0], p[1], (p[0] + q[0]) / 2, (p[1] + q[1]) / 2);
    }
    ctx.closePath();
  }

  function beyinArkaPlanCiz(ctx, durum) {
    const m = durum.metrik;
    const olcek = durum.olcek;
    // Simetrik dış devre izleri
    ctx.save();
    ctx.strokeStyle = 'rgba(56, 178, 255, 0.18)';
    ctx.fillStyle = 'rgba(86, 214, 255, 0.34)';
    ctx.lineWidth = 1.2 / olcek;
    [-1, 1].forEach(function (taraf) {
      BEYIN_DEVRE.forEach(function (yol) {
        ctx.beginPath();
        yol.forEach(function (p, idx) {
          const x = m.cx + p[0] * taraf * m.rx, y = m.cy + p[1] * m.ry;
          if (idx === 0) { ctx.moveTo(x, y); } else { ctx.lineTo(x, y); }
        });
        ctx.stroke();
        const uc = yol[yol.length - 1];
        const ux = m.cx + uc[0] * taraf * m.rx, uy = m.cy + uc[1] * m.ry;
        ctx.beginPath();
        ctx.arc(ux, uy, 3.2 / olcek, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(ux, uy, 7.5 / olcek, 0, Math.PI * 2);
        ctx.stroke();
      });
    });
    // İki yarımküre silüeti (iç çizgisiz, kenar derinlik gölgeli)
    [-1, 1].forEach(function (taraf) {
      const pts = BEYIN_SAG.map(function (p) { return [m.cx + p[0] * taraf * m.rx, m.cy + p[1] * m.ry]; });
      const grad = ctx.createRadialGradient(m.cx + 0.38 * taraf * m.rx, m.cy - 0.08 * m.ry, m.rx * 0.08,
        m.cx + 0.38 * taraf * m.rx, m.cy, m.ry * 1.04);
      grad.addColorStop(0, 'rgba(32, 134, 232, 0.16)');
      grad.addColorStop(0.68, 'rgba(18, 92, 198, 0.22)');
      grad.addColorStop(1, 'rgba(56, 206, 255, 0.32)');
      ctx.save();
      kapaliEgri(ctx, pts);
      ctx.fillStyle = grad;
      ctx.fill();
      ctx.shadowColor = 'rgba(56, 214, 255, 0.75)';
      ctx.shadowBlur = 24;
      ctx.strokeStyle = 'rgba(116, 232, 255, 0.85)';
      ctx.lineWidth = 2.2 / olcek;
      ctx.stroke();
      ctx.restore();
      // Kenar içi yumuşak derinlik halkası (iç alanı boş bırakır)
      ctx.save();
      kapaliEgri(ctx, pts);
      ctx.clip();
      kapaliEgri(ctx, pts);
      ctx.strokeStyle = 'rgba(84, 214, 255, 0.14)';
      ctx.lineWidth = 14 / olcek;
      ctx.stroke();
      ctx.restore();
    });
    ctx.restore();
  }

  function grafCiz(durum, ctx, dpr) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, durum.genislik, durum.yukseklik);
    ctx.save();
    ctx.translate(durum.panX, durum.panY);
    ctx.scale(durum.olcek, durum.olcek);
    if (durum.mod === 'beyin') { beyinArkaPlanCiz(ctx, durum); }
    const odak = durum.uzerinde || durum.secili;
    const turOdak = !odak ? durum.seciliTur : null;
    const komsular = odak ? (durum.komsu[odak] || new Set()) : null;
    durum.kenarlar.forEach(function (e) {
      const vurgulu = odak
        ? (e.a.veri.id === odak || e.b.veri.id === odak)
        : (turOdak && (grafKategori(e.a.veri.tur) === turOdak || grafKategori(e.b.veri.tur) === turOdak));
      const soluk = (odak || turOdak) && !vurgulu;
      ctx.strokeStyle = vurgulu
        ? 'rgba(249, 215, 28, 0.82)'
        : (soluk ? 'rgba(110, 175, 230, 0.10)' : (durum.mod === 'beyin' ? 'rgba(110, 210, 255, 0.30)' : 'rgba(139,148,158,.35)'));
      ctx.lineWidth = (vurgulu ? 1.8 : 1) / durum.olcek;
      ctx.beginPath();
      ctx.moveTo(e.a.x, e.a.y);
      if (durum.mod === 'beyin') {
        const mx = (e.a.x + e.b.x) / 2, my = (e.a.y + e.b.y) / 2;
        const dx = e.b.x - e.a.x, dy = e.b.y - e.a.y;
        ctx.quadraticCurveTo(mx - dy * 0.10, my + dx * 0.10, e.b.x, e.b.y);
      } else {
        ctx.lineTo(e.b.x, e.b.y);
      }
      ctx.stroke();
    });
    durum.dugumler.forEach(function (n) {
      const secili = durum.secili === n.veri.id;
      const uzerinde = durum.uzerinde === n.veri.id;
      const turSecili = turOdak && grafKategori(n.veri.tur) === turOdak;
      const ilgili = odak
        ? (secili || uzerinde || (komsular && komsular.has(n.veri.id)))
        : (!turOdak || turSecili);
      const r = (Math.min(10, 5.2 + Math.sqrt(n.derece) * 1.4) + (secili ? 2.5 : (uzerinde || turSecili ? 1.8 : 0))) / durum.olcek;
      const renk = grafRenk(n.veri.tur);
      ctx.save();
      ctx.globalAlpha = ilgili ? 1 : 0.20;
      if (durum.mod === 'beyin' && ilgili) {
        ctx.shadowColor = renk;
        ctx.shadowBlur = (secili || uzerinde || turSecili) ? 16 : 9;
      }
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = renk;
      ctx.fill();
      if (secili || uzerinde || turSecili) {
        ctx.lineWidth = 2 / durum.olcek;
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();
      }
      ctx.restore();
    });
    if (durum.olcek > 0.5) {
      ctx.font = (11 / durum.olcek) + 'px ui-monospace, Menlo, monospace';
      ctx.textAlign = 'center';
      durum.dugumler.forEach(function (n) {
        const secili = durum.secili === n.veri.id;
        const uzerinde = durum.uzerinde === n.veri.id;
        const turSecili = turOdak && grafKategori(n.veri.tur) === turOdak;
        const ilgili = odak
          ? (secili || uzerinde || (komsular && komsular.has(n.veri.id)))
          : (!turOdak || turSecili);
        if (!ilgili) { return; }
        const etiket = n.veri.baslik.length > 22 ? n.veri.baslik.slice(0, 21) + '…' : n.veri.baslik;
        ctx.fillStyle = (secili || uzerinde || turSecili) ? '#f0f6fc' : (durum.mod === 'beyin' ? '#b8d4ee' : '#8b949e');
        ctx.fillText(etiket, n.x, n.y + 19 / durum.olcek);
      });
    }
    ctx.restore();
  }

  function grafBul(durum, olay) {
    const rect = $('graf-tuval').getBoundingClientRect();
    const x = (olay.clientX - rect.left - durum.panX) / durum.olcek;
    const y = (olay.clientY - rect.top - durum.panY) / durum.olcek;
    let en = null, mesafe = 15 / durum.olcek;
    durum.dugumler.forEach(function (n) {
      const d = Math.sqrt((n.x - x) * (n.x - x) + (n.y - y) * (n.y - y));
      if (d < mesafe) { mesafe = d; en = n; }
    });
    return en;
  }

  let grafIcerikIstek = 0;
  async function grafIcerik(yol) {
    const kutu = $('graf-icerik');
    const istek = ++grafIcerikIstek;
    kutu.textContent = 'Yükleniyor…';
    try {
      const not = await api('/api/not?yol=' + encodeURIComponent(yol));
      if (istek !== grafIcerikIstek) { return; }
      mdCiz(kutu, (not.metin || '') + (not.kisaltildi ? '\n\n*… (not kısaltıldı)*' : ''));
    } catch (error) {
      if (istek === grafIcerikIstek) { bosalt(kutu).append(el('p', { class: 'bos', text: error.message })); }
    }
  }

  function grafFiltreGuncelle() {
    const aktif = aktifGraf ? aktifGraf.seciliTur : null;
    document.querySelectorAll('#graf-lejant .graf-filtre').forEach(function (btn) {
      const secili = btn.dataset.tur === aktif;
      btn.classList.toggle('secili', secili);
      btn.setAttribute('aria-pressed', secili ? 'true' : 'false');
    });
  }

  function grafSec(durum, n) {
    durum.secili = n ? n.veri.id : null;
    const kutu = $('graf-secim');
    if (!n) {
      kutu.hidden = true;
      $('graf-icerik').textContent = 'Bir nota tıklayın…';
      return;
    }
    kutu.hidden = false;
    kutu.replaceChildren(
      el('div', { class: 'etiket', text: grafEtiket(n.veri.tur) }),
      el('h2', { text: n.veri.baslik }),
      el('p', { class: 'ust-bilgi', text: n.veri.id })
    );
    grafIcerik(n.veri.id);
  }

  function grafDongu(tuval, durum, ctx, dpr) {
    const ciz = function () {
      if (aktifGraf !== durum || !tuval.isConnected) { return; }
      if ($('gorunum-graf').hidden) { requestAnimationFrame(ciz); return; }
      if (durum.kare < 260) { grafFizik(durum); durum.kare += 1; }
      grafCiz(durum, ctx, dpr);
      requestAnimationFrame(ciz);
    };
    requestAnimationFrame(ciz);
  }

  function grafEtkilesim(tuval) {
    if (grafDinleyiciKuruldu) { return; }
    grafDinleyiciKuruldu = true;
    let basla = null;
    tuval.addEventListener('pointerdown', function (olay) {
      if (!aktifGraf) { return; }
      tuval.setPointerCapture(olay.pointerId);
      basla = { x: olay.clientX, y: olay.clientY, panX: aktifGraf.panX, panY: aktifGraf.panY,
        dugum: grafBul(aktifGraf, olay), tasindi: false };
      if (basla.dugum) { aktifGraf.sabit = basla.dugum; }
    });
    tuval.addEventListener('pointermove', function (olay) {
      if (!aktifGraf) { return; }
      if (!basla) {
        const hedef = grafBul(aktifGraf, olay);
        aktifGraf.uzerinde = hedef ? hedef.veri.id : null;
        tuval.style.cursor = hedef ? 'pointer' : 'grab';
        return;
      }
      const dx = olay.clientX - basla.x, dy = olay.clientY - basla.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) { basla.tasindi = true; }
      if (basla.dugum) {
        const rect = tuval.getBoundingClientRect();
        basla.dugum.x = (olay.clientX - rect.left - aktifGraf.panX) / aktifGraf.olcek;
        basla.dugum.y = (olay.clientY - rect.top - aktifGraf.panY) / aktifGraf.olcek;
        if (aktifGraf.mod === 'beyin') { beyinSinirla(basla.dugum, aktifGraf.metrik); }
        basla.dugum.vx = 0; basla.dugum.vy = 0;
      } else {
        aktifGraf.panX = basla.panX + dx;
        aktifGraf.panY = basla.panY + dy;
      }
    });
    tuval.addEventListener('pointerleave', function () {
      if (aktifGraf && !basla) { aktifGraf.uzerinde = null; }
    });
    const bitir = function () {
      if (aktifGraf && basla && !basla.tasindi) {
        if (basla.dugum) { grafSec(aktifGraf, basla.dugum); }
        else { aktifGraf.seciliTur = null; grafFiltreGuncelle(); grafSec(aktifGraf, null); }
      }
      basla = null;
      if (aktifGraf) { aktifGraf.sabit = null; }
    };
    tuval.addEventListener('pointerup', bitir);
    tuval.addEventListener('pointercancel', bitir);
    tuval.addEventListener('wheel', function (olay) {
      if (!aktifGraf) { return; }
      olay.preventDefault();
      const rect = tuval.getBoundingClientRect();
      const mx = olay.clientX - rect.left, my = olay.clientY - rect.top;
      const faktor = olay.deltaY < 0 ? 1.12 : 1 / 1.12;
      const yeni = Math.min(3, Math.max(0.25, aktifGraf.olcek * faktor));
      aktifGraf.panX = mx - (mx - aktifGraf.panX) * (yeni / aktifGraf.olcek);
      aktifGraf.panY = my - (my - aktifGraf.panY) * (yeni / aktifGraf.olcek);
      aktifGraf.olcek = yeni;
    }, { passive: false });
  }

  function grafBaslat(veri) {
    const tuval = $('graf-tuval');
    const kutu = tuval.parentElement;
    if (kutu) { kutu.classList.toggle('beyin', grafMod === 'beyin'); }
    $('graf-mod').textContent = grafMod === 'beyin' ? 'Mod: Beyin' : 'Mod: Serbest';
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const rect = tuval.getBoundingClientRect();
    tuval.width = Math.max(1, Math.round(rect.width * dpr));
    tuval.height = Math.max(1, Math.round(rect.height * dpr));
    const ctx = tuval.getContext('2d');
    const durum = grafSimule(veri, grafMod);
    aktifGraf = durum;
    grafFiltreGuncelle();
    grafEtkilesim(tuval);
    grafDongu(tuval, durum, ctx, dpr);
  }

  async function graf() {
    const notu = $('graf-notu');
    notu.textContent = 'Yükleniyor…';
    try {
      const veri = await api('/api/graf');
      grafBaslat(veri);
      notu.textContent = veri.dugumler.length + ' not · ' + veri.kenarlar.length + ' bağlantı';
    } catch (error) {
      notu.textContent = error.message;
    }
  }

  // --- güncelleme -------------------------------------------------------
  const GUNCELLEME = {
    available: ['Yeni sürüm mevcut', 'uyari'],
    up_to_date: ['Güncel', 'iyi'],
    noop: ['Zaten güncel', 'iyi'],
    ahead: ['Geliştirme sürümü', 'iyi'],
    updated: ['Güncellendi', 'iyi'],
    recovery_required: ['Kurtarma gerekiyor', 'kotu'],
    disabled: ['Otomatik bildirim kapalı', ''],
    unknown: ['Henüz kontrol edilmedi', '']
  };
  let sonGuncellemeKontrol = null;
  function guncellemeKaynakDegisti() {
    const yerel = $('guncelleme-kaynak').value === 'yerel';
    $('guncelleme-paket-alan').hidden = !yerel;
    $('guncelleme-uygula').disabled = true;
    sonGuncellemeKontrol = null;
  }
  async function guncelleme() {
    const ozet = bosalt($('guncelleme-ozet'));
    $('guncelleme-uygula').disabled = true;
    sonGuncellemeKontrol = null;
    try {
      const veri = await api('/api/guncelleme');
      const bilgi = GUNCELLEME[veri.durum] || [veri.durum || 'Bilinmiyor', ''];
      ozet.append(
        kart('Mevcut sürüm', veri.mevcut ? 'v' + veri.mevcut : '?', el('span', { class: 'rozet', text: 'Kurulu kasa' })),
        kart('Durum', bilgi[0], el('span', { class: 'rozet ' + bilgi[1], text: veri.hedef ? 'Son: v' + veri.hedef : (veri.durum || 'bekliyor') })),
        kart('Veri güvenliği', 'Korunur', el('span', { class: 'rozet iyi', text: 'Notlar ve ayarlar değişmez' }))
      );
      if (veri.yarim_islem) {
        $('guncelleme-sonuc').textContent = 'Tamamlanmamış bir güncelleme işlemi var. Terminalde serobeyinn.py recover çalıştır.';
      } else if (veri.kontrol_zamani) {
        $('guncelleme-sonuc').textContent = 'Son kontrol: ' + zaman(veri.kontrol_zamani) + (veri.hedef ? ' · Son sürüm: v' + veri.hedef : '');
      } else {
        $('guncelleme-sonuc').textContent = 'Kaynak seçip Kontrol Et düğmesine bas.';
      }
      if (SALT_OKUNUR) {
        $('guncelleme-kontrol').disabled = true;
        $('guncelleme-uygula').disabled = true;
      }
    } catch (error) {
      $('guncelleme-sonuc').textContent = error.message;
    }
  }
  async function guncellemeKontrolEt() {
    const dugme = $('guncelleme-kontrol');
    const kaynak = $('guncelleme-kaynak').value;
    const paket = $('guncelleme-paket').value.trim();
    if (kaynak === 'yerel' && !paket) {
      bildir('Yerel .zip paket yolunu gir.', true);
      return;
    }
    dugme.disabled = true;
    $('guncelleme-uygula').disabled = true;
    $('guncelleme-sonuc').textContent = 'Kontrol ediliyor…';
    try {
      const res = await api('/api/guncelleme/kontrol', { kaynak: kaynak, paket: paket });
      sonGuncellemeKontrol = { kaynak: kaynak, paket: paket, sonuc: res };
      const bilgi = GUNCELLEME[res.durum] || [res.durum || 'Bilinmiyor', ''];
      if (res.durum === 'available') {
        $('guncelleme-sonuc').textContent = 'Yeni sürüm hazır: v' + res.mevcut + ' -> v' + res.hedef + ' (' + kaynak + '). Onaylayarak güncelleyebilirsin.';
        $('guncelleme-uygula').disabled = SALT_OKUNUR;
        bildir('Yeni sürüm bulundu: v' + res.hedef);
      } else {
        $('guncelleme-sonuc').textContent = bilgi[0] + ' (mevcut: v' + (res.mevcut || '?') + (res.hedef ? ', kaynak: v' + res.hedef : '') + ').';
        bildir(bilgi[0]);
      }
    } catch (error) {
      $('guncelleme-sonuc').textContent = 'Hata: ' + error.message;
      bildir('Kontrol başarısız: ' + error.message, true);
    }
    dugme.disabled = SALT_OKUNUR;
  }
  async function guncellemeUygula() {
    if (!sonGuncellemeKontrol || sonGuncellemeKontrol.sonuc.durum !== 'available') { return; }
    const hedef = sonGuncellemeKontrol.sonuc.hedef || 'yeni sürüm';
    if (!window.confirm('v' + hedef + ' sürümüne güncellenecek. Önce otomatik yedek alınır, hata olursa geri alınabilir ve kullanıcı notlarına dokunulmaz. Devam edilsin mi?')) {
      return;
    }
    const dugme = $('guncelleme-uygula');
    dugme.disabled = true;
    $('guncelleme-sonuc').textContent = 'Yedekleniyor, doğrulanıyor ve güncelleniyor…';
    try {
      const res = await api('/api/guncelleme/uygula', {
        kaynak: sonGuncellemeKontrol.kaynak,
        paket: sonGuncellemeKontrol.paket,
        onay: true
      });
      $('guncelleme-sonuc').textContent = 'Güncelleme tamamlandı: v' + res.surum + '. Yeni sürümün açılması için SeroBeyinn Web.command ile yeniden başlat.';
      bildir('Güncellendi: v' + res.surum);
    } catch (error) {
      $('guncelleme-sonuc').textContent = 'Güncellenemedi: ' + error.message;
      bildir('Güncellenemedi: ' + error.message, true);
      dugme.disabled = SALT_OKUNUR;
    }
  }

  // --- gezinme ------------------------------------------------------------
  const YUKLE = { kokpit: kokpit, gorevler: gorevler, graf: graf, 'gozden-gecir': gozgecir, arama: null, makbuzlar: makbuzlar, hafiza: hafiza, guncelleme: guncelleme, yardim: null };
  function goster() {
    let ad = window.location.hash.replace('#', '');
    if (!(ad in YUKLE)) { ad = 'kokpit'; }
    if (ad !== 'gozden-gecir') {
      sonGozdenYukleme += 1;
      sonGozdenOnizleme += 1;
    }
    document.querySelectorAll('.gorunum').forEach(function (g) { g.hidden = g.id !== 'gorunum-' + ad; });
    document.querySelectorAll('.yan nav a').forEach(function (a) { a.classList.toggle('secili', a.dataset.gorunum === ad); });
    if (YUKLE[ad]) { YUKLE[ad]().catch(function (error) { bildir(error.message, true); }); }
  }
  async function esitle() {
    const dugme = $('esitle'); dugme.disabled = true;
    try {
      const sonuc = await api('/api/esitle', {});
      bildir('Eşitleme ' + (ESITLEME[sonuc.durum] || sonuc.durum) + ' (' + (sonuc.dizinlenen ?? 0) + ' kaynak, ' +
        sonuc.cakisma + ' çakışma)', sonuc.durum === 'conflict');
      goster();
    } catch (error) { bildir('Eşitlenemedi: ' + error.message, true); }
    dugme.disabled = SALT_OKUNUR;
  }
  async function kapat() {
    if (!window.confirm('Web sunucusu kapatılsın mı?')) { return; }
    try { await api('/api/kapat', {}); } catch (error) { bildir(error.message, true); return; }
    document.body.append(el('div', { class: 'kapandi', text: 'Sunucu kapandı. Yeniden açmak için: serobeyinn.py web ac' }));
  }
  let sonEtkinlik = 0;
  function etkinlik() {
    const simdi = Date.now();
    if (simdi - sonEtkinlik < 60000) { return; }
    sonEtkinlik = simdi;
    api('/api/etkinlik', {}).catch(function () {});
  }

  function baslikUygula(yeni) {
    const metin = (yeni && String(yeni).trim()) || 'SeroBeyinn Web';
    $('marka-baslik').textContent = metin;
    document.title = metin;
  }
  function markaDuzenleAc() {
    if (SALT_OKUNUR) { return; }
    $('marka-satir').hidden = true;
    $('marka-form').hidden = false;
    const girdi = $('marka-girdi');
    girdi.value = $('marka-baslik').textContent;
    girdi.focus();
    girdi.select();
  }
  function markaDuzenleKapat() {
    $('marka-form').hidden = true;
    $('marka-satir').hidden = false;
  }
  async function markaKaydet(event) {
    event.preventDefault();
    const dugme = $('marka-form').querySelector('button[type="submit"]');
    dugme.disabled = true;
    try {
      const sonuc = await api('/api/ayarlar', { baslik: $('marka-girdi').value });
      baslikUygula(sonuc.baslik);
      markaDuzenleKapat();
      bildir('Başlık güncellendi: ' + sonuc.baslik);
    } catch (error) { bildir('Başlık kaydedilemedi: ' + error.message, true); }
    dugme.disabled = false;
  }

  document.addEventListener('DOMContentLoaded', function () {
    $('mod-rozeti').textContent = SALT_OKUNUR ? 'Salt okunur' : 'Yazma açık';
    $('mod-rozeti').classList.add(SALT_OKUNUR ? 'iyi' : 'uyari');
    $('esitle').disabled = SALT_OKUNUR;
    $('sikistir').disabled = SALT_OKUNUR;
    $('yeni-gorev').hidden = SALT_OKUNUR;
    $('marka-duzenle').hidden = SALT_OKUNUR;
    $('marka-duzenle').addEventListener('click', markaDuzenleAc);
    $('marka-baslik').addEventListener('dblclick', markaDuzenleAc);
    $('marka-iptal').addEventListener('click', markaDuzenleKapat);
    $('marka-form').addEventListener('submit', markaKaydet);
    $('marka-girdi').addEventListener('keydown', function (e) { if (e.key === 'Escape') { markaDuzenleKapat(); } });
    $('kokpit-hizli-gorev').hidden = SALT_OKUNUR;
    $('esitle').addEventListener('click', esitle);
    $('kapat').addEventListener('click', kapat);
    $('sikistir').addEventListener('click', sikistir);
    $('yeni-gorev').addEventListener('submit', gorevOlustur);
    $('kokpit-hizli-gorev').addEventListener('submit', kokpitHizliGorev);
    $('kokpit-arama').addEventListener('submit', kokpitAramaGit);
    $('kokpit-yenile').addEventListener('click', kokpit);
    const DEV_QR = {
      wa: [0x1fc437f, 0x1048b41, 0x175245d, 0x174935d, 0x174935d, 0x1047641, 0x1fd557f, 0x12a00, 0x1df1cc4, 0x191b4c1,
        0xed7467, 0x12ada02, 0x13f7e6b, 0x9964c9, 0x135c4a7, 0xe139d2, 0x146cff8, 0x14f1b, 0x1fdd35b, 0x1056f1b,
        0x175edf8, 0x174843c, 0x1750711, 0x1057b5a, 0x1fd8fe3],
      mail: [0x1fcee7f, 0x1047f41, 0x175305d, 0x174665d, 0x174ee5d, 0x104ea41, 0x1fd557f, 0x1df00, 0x1df79c4, 0x1888d4f,
        0x345d7f, 0x11ae8c0, 0x15e62c1, 0x29d9c7, 0x1670467, 0x923960, 0x1645bfa, 0x19713, 0x1fd1757, 0x1053d11,
        0x17559f2, 0x1741b14, 0x1755639, 0x1055fba, 0x1fdfbcb]
    };
    function devQrCiz(tur) {
      const tuval = $('dev-qr');
      const ctx = tuval.getContext('2d');
      const satirlar = DEV_QR[tur] || DEV_QR.wa;
      const n = satirlar.length, pad = 2, hucre = 4;
      tuval.width = (n + pad * 2) * hucre;
      tuval.height = (n + pad * 2) * hucre;
      ctx.fillStyle = '#0a0a0a';
      ctx.fillRect(0, 0, tuval.width, tuval.height);
      ctx.fillStyle = '#00ff41';
      satirlar.forEach(function (satir, r) {
        for (let c = 0; c < n; c += 1) {
          if ((satir >>> (n - 1 - c)) & 1) { ctx.fillRect((c + pad) * hucre, (r + pad) * hucre, hucre, hucre); }
        }
      });
      $('dev-qr-etiket').textContent = tur === 'mail' ? 'E-posta QR' : 'WhatsApp QR';
      document.querySelectorAll('.dev-qr-tab').forEach(function (b) { b.classList.toggle('secili', b.dataset.qr === tur); });
    }
    $('gelistirici-ac').addEventListener('click', function () {
      const modal = $('gelistirici-modal');
      modal.querySelectorAll('.dev-dolgu').forEach(function (b) { b.style.width = '0%'; });
      modal.showModal();
      devQrCiz('wa');
      setTimeout(function () {
        modal.querySelectorAll('.dev-dolgu').forEach(function (b) { b.style.width = (b.dataset.pct || 0) + '%'; });
      }, 120);
    });
    document.querySelectorAll('.dev-qr-tab').forEach(function (b) {
      b.addEventListener('click', function () { devQrCiz(b.dataset.qr); });
    });
    $('gelistirici-kapat').addEventListener('click', function () { $('gelistirici-modal').close(); });
    $('gelistirici-modal').addEventListener('click', function (e) {
      if (e.target === $('gelistirici-modal')) { $('gelistirici-modal').close(); }
    });
    document.querySelectorAll('#gelistirici-modal [data-kopyala]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const deger = btn.dataset.kopyala;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(deger).then(function () { bildir('Kopyalandı: ' + deger); })
            .catch(function () { bildir(deger); });
        } else { bildir(deger); }
      });
    });
    $('gozden-yenile').addEventListener('click', gozgecir);
    $('arama-formu').addEventListener('submit', ara);
    $('arama-temizle').addEventListener('click', function () {
      $('arama-sorgu').value = '';
      $('arama-durum').textContent = '';
      bosalt($('arama-sonuclari')).append(el('li', { class: 'bos', text: 'En az 2 harf yazıp Ara düğmesine bas.' }));
      $('onizleme-baslik').textContent = 'Önizleme';
      $('onizleme-meta').textContent = '';
      $('onizleme').textContent = 'Bir sonuç seçin…';
      $('arama-sorgu').focus();
    });
    $('graf-yenile').addEventListener('click', graf);
    $('graf-mod').addEventListener('click', function () {
      grafMod = grafMod === 'beyin' ? 'serbest' : 'beyin';
      if (aktifGraf && aktifGraf.ham) { grafBaslat(aktifGraf.ham); } else { graf(); }
    });
    $('graf-ortala').addEventListener('click', function () {
      if (!aktifGraf) { return; }
      aktifGraf.olcek = 1; aktifGraf.panX = 0; aktifGraf.panY = 0;
    });
    document.querySelectorAll('#graf-lejant .graf-filtre').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!aktifGraf) { return; }
        const tur = btn.dataset.tur;
        aktifGraf.seciliTur = aktifGraf.seciliTur === tur ? null : tur;
        if (aktifGraf.seciliTur) { grafSec(aktifGraf, null); }
        grafFiltreGuncelle();
      });
    });
    $('proje-filtre').addEventListener('change', panoyuCiz);
    $('sorumlu-filtre').addEventListener('change', panoyuCiz);
    $('gorev-ara').addEventListener('input', panoyuCiz);
    $('gorev-kapali-goster').addEventListener('click', function () {
      gorevKapaliGoster = !gorevKapaliGoster;
      panoyuCiz();
    });
    $('gorev-detay-kapat').addEventListener('click', function () { $('gorev-detay').hidden = true; });
    $('makbuz-ara').addEventListener('input', makbuzListesiniCiz);
    $('makbuz-yenile').addEventListener('click', makbuzlar);
    $('hafiza-yenile').addEventListener('click', hafiza);
    $('guncelleme-kaynak').addEventListener('change', guncellemeKaynakDegisti);
    $('guncelleme-kontrol').addEventListener('click', guncellemeKontrolEt);
    $('guncelleme-uygula').addEventListener('click', guncellemeUygula);
    ['keydown', 'pointerdown', 'wheel'].forEach(function (name) { window.addEventListener(name, etkinlik, { passive: true }); });
    window.addEventListener('hashchange', goster);
    api('/api/durum').then(function (d) {
      if (d.baslik) { baslikUygula(d.baslik); }
      $('kasa-adi').textContent = d.kasa + (d.surum ? ' · v' + d.surum : '');
      $('bosta-notu').textContent = d.bosta_kapanma_dk + ' dakika kullanılmazsa kapanır.';
    }).catch(function () {});
    goster();
  });
})();
"""

_INDEX = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="serobeyinn-csrf" content="{csrf}">
<meta name="serobeyinn-salt-okunur" content="{read_only}">
<title>SeroBeyinn Web</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="/app.css">
<script src="/app.js" defer></script>
</head>
<body>
<div class="kabuk">
  <aside class="yan">
    <div class="marka"><span class="limon" aria-hidden="true">🍋</span><div class="marka-govde"><div id="marka-satir" class="marka-satir"><strong id="marka-baslik">SeroBeyinn Web</strong><button id="marka-duzenle" type="button" class="marka-duzenle" title="Başlığı düzenle" aria-label="Başlığı düzenle">✎</button></div><form id="marka-form" class="marka-form" hidden><input id="marka-girdi" type="text" maxlength="60" aria-label="Başlık" placeholder="SeroBeyinn Web"><button type="submit">Kaydet</button><button id="marka-iptal" type="button" class="ikincil">Vazgeç</button></form><small id="kasa-adi"></small></div></div>
    <nav aria-label="Bölümler">
      <a href="#kokpit" data-gorunum="kokpit">Kokpit</a>
      <a href="#gorevler" data-gorunum="gorevler">Görevler</a>
      <a href="#graf" data-gorunum="graf">Graf</a>
      <a href="#gozden-gecir" data-gorunum="gozden-gecir">Gözden geçir</a>
      <a href="#arama" data-gorunum="arama">Arama</a>
      <a href="#makbuzlar" data-gorunum="makbuzlar">İşlem Kayıtları (Receipts)</a>
      <a href="#hafiza" data-gorunum="hafiza">Hafıza</a>
      <a href="#guncelleme" data-gorunum="guncelleme">Güncelleme</a>
      <a href="#yardim" data-gorunum="yardim">Yardım</a>
    </nav>
    <div class="alt">
      <span id="mod-rozeti" class="rozet"></span>
      <button id="esitle" type="button">Eşitle</button>
      <button id="kapat" type="button" class="ikincil">Sunucuyu kapat</button>
      <small id="bosta-notu" class="aciklama"></small>
    </div>
  </aside>
  <main>
    <section id="gorunum-kokpit" class="gorunum">
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Kokpit</h1>
          <span id="kokpit-zaman" class="ust-bilgi"></span>
        </div>
        <div class="kokpit-ust-sag">
          <form id="kokpit-arama" class="kokpit-arama" autocomplete="off">
            <input id="kokpit-arama-sorgu" type="search" maxlength="200" placeholder="Kasada hızlı ara…" aria-label="Kasada hızlı ara">
            <button type="submit" class="ikincil">Ara</button>
          </form>
          <button id="kokpit-yenile" type="button" class="ikincil">Yenile</button>
          <a href="#yardim" class="dugme-bag">Yardım</a>
          <button id="gelistirici-ac" type="button" class="gelistirici-btn" title="Geliştirici Profil Kartını Görüntüle">&gt;_ BeNKaYS</button>
        </div>
      </div>
      <p class="aciklama">Sistem sağlığı, odak görevler, hafıza doluluğu ve son kayıtlar. Kartlara tıklayarak ilgili bölüme geçebilirsin.</p>
      <div id="kokpit-kartlar" class="izgara"></div>
      <div class="kokpit-ikili">
        <div class="kokpit-sutun">
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Odak görevler</h2>
              <a href="#gorevler">Tüm görevler</a>
            </div>
            <form id="kokpit-hizli-gorev" class="hizli-form" autocomplete="off">
              <input name="baslik" required maxlength="160" placeholder="Hızlı görev ekle (Enter)…" aria-label="Hızlı görev başlığı">
              <button type="submit">Ekle</button>
            </form>
            <ul id="kokpit-odak-gorevler" class="liste"></ul>
          </div>
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Dikkat bekleyenler</h2>
              <a href="#gozden-gecir">Gözden geçir</a>
            </div>
            <div id="kokpit-dikkat" class="dikkat-izgara"></div>
          </div>
        </div>
        <div class="kokpit-sutun">
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Hafıza durumu</h2>
              <a href="#hafiza">Hafızayı yönet</a>
            </div>
            <ul id="kokpit-hafiza-liste" class="liste"></ul>
            <div id="kokpit-hafiza-alt" class="hafiza-alt"></div>
          </div>
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Son kayıtlar</h2>
              <a href="#makbuzlar">Tüm kayıtlar</a>
            </div>
            <ul id="kokpit-makbuzlar" class="liste"></ul>
          </div>
        </div>
      </div>
    </section>
    <section id="gorunum-gorevler" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Görevler</h1>
          <div id="gorev-ozet" class="gorev-ozet-serit"></div>
        </div>
        <div class="kokpit-ust-sag">
          <button id="gorev-kapali-goster" type="button" class="ikincil">Kapalıları göster</button>
        </div>
      </div>
      <p class="aciklama">Kartları sütunlar arasında sürükleyip bırakabilir veya başlığına tıklayarak tam notu açabilirsin.</p>
      <form id="yeni-gorev" class="form" autocomplete="off">
        <label>Başlık<input name="baslik" required maxlength="160" placeholder="Ne yapılacak?"></label>
        <label>Sorumlu<input name="sorumlu" required maxlength="80" value="ben" placeholder="ör. ben"></label>
        <label>Proje<input name="proje" maxlength="80" list="proje-onerileri" placeholder="isteğe bağlı"></label>
        <label>Durum<select name="durum" id="yeni-durum"></select></label>
        <label class="genis">Açıklama<textarea name="aciklama" rows="2" maxlength="4000" placeholder="Kısa detay veya not…"></textarea></label>
        <div><button type="submit">Görev oluştur</button></div>
      </form>
      <datalist id="proje-onerileri"></datalist>
      <div class="gorev-arac">
        <input id="gorev-ara" type="search" maxlength="120" placeholder="Görevlerde ara…" aria-label="Görevlerde ara">
        <label>Proje <select id="proje-filtre"></select></label>
        <label>Sorumlu <select id="sorumlu-filtre"></select></label>
        <span id="gorev-notu" class="aciklama"></span>
      </div>
      <div id="gorev-detay" class="gorev-detay" hidden>
        <div class="bolum-baslik">
          <div>
            <h2 id="gorev-detay-baslik">Görev detayı</h2>
            <div id="gorev-detay-meta" class="ust-bilgi"></div>
          </div>
          <button id="gorev-detay-kapat" type="button" class="ikincil">Kapat</button>
        </div>
        <pre id="gorev-detay-metin" class="onizleme"></pre>
      </div>
      <div id="gorev-pano" class="pano"></div>
    </section>
    <section id="gorunum-gozden-gecir" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Gözden geçir</h1>
          <div id="gozden-ozet" class="gorev-ozet-serit"></div>
        </div>
        <div class="kokpit-ust-sag">
          <button id="gozden-yenile" type="button" class="ikincil">Yenile</button>
        </div>
      </div>
      <p class="aciklama">Unutulmuş işleri, biriken gelen kutusunu ve yarım kalan taslakları görmek için özet rapor. Bir öğeye tıklayınca sağda içeriği açılır.</p>
      <div class="ikili">
        <div class="gozden-sol">
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Gelen kutusu</h2>
              <span id="gozden-sayi-inbox" class="rozet">0</span>
            </div>
            <p class="sutun-aciklama">000-Inbox altında sınıflandırılmayı bekleyen notlar</p>
            <div id="gozden-inbox"></div>
          </div>
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Bayat konular</h2>
              <span id="gozden-sayi-konular" class="rozet">0</span>
            </div>
            <p class="sutun-aciklama">Threads içinde uzun süredir güncellenmeyen açık başlıklar</p>
            <ul id="gozden-konular" class="liste"></ul>
          </div>
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Bayat görevler</h2>
              <span id="gozden-sayi-gorevler" class="rozet">0</span>
            </div>
            <p class="sutun-aciklama">Açık kalıp uzun süredir hareket görmeyen görevler</p>
            <div id="gozden-gorevler"></div>
          </div>
          <div class="kokpit-bolum">
            <div class="bolum-baslik">
              <h2>Taslak notlar</h2>
              <span id="gozden-sayi-taslaklar" class="rozet">0</span>
            </div>
            <p class="sutun-aciklama">Henüz tamamlanmamış (taslak/draft) durumdaki notlar</p>
            <ul id="gozden-taslaklar" class="liste"></ul>
          </div>
        </div>
        <div class="gozden-sag">
          <div class="kokpit-bolum">
            <h2 id="gozden-onizleme-baslik">Önizleme</h2>
            <div id="gozden-onizleme" class="onizleme md-okuma"><p class="bos">Kayıt seçin…</p></div>
          </div>
        </div>
      </div>
    </section>
    <section id="gorunum-arama" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Arama</h1>
          <span id="arama-durum" class="rozet"></span>
        </div>
      </div>
      <p class="aciklama">Ajanların gördüğü dizinde arar: gizli, güvenilmeyen ve hassas klasördeki notlar sonuçlara girmez.</p>
      <div class="kokpit-bolum arama-panel">
        <form id="arama-formu" class="arama-kutu" autocomplete="off">
          <input id="arama-sorgu" type="search" maxlength="200" placeholder="Not, görev veya kavram ara…" aria-label="Arama">
          <button type="submit">Ara</button>
          <button id="arama-temizle" type="button" class="ikincil">Temizle</button>
        </form>
      </div>
      <div class="ikili">
        <div>
          <ul id="arama-sonuclari" class="liste">
            <li class="bos">En az 2 harf yazıp Ara düğmesine bas.</li>
          </ul>
        </div>
        <div class="gozden-sag">
          <div class="kokpit-bolum">
            <h2 id="onizleme-baslik">Önizleme</h2>
            <div id="onizleme-meta" class="ust-bilgi"></div>
            <div id="onizleme" class="onizleme md-okuma"><p class="bos">Bir sonuç seçin…</p></div>
          </div>
        </div>
      </div>
    </section>
    <section id="gorunum-makbuzlar" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>İşlem Kayıtları (Receipts)</h1>
          <span id="makbuz-sayac" class="rozet"></span>
        </div>
        <button id="makbuz-yenile" type="button" class="ikincil">Yenile</button>
      </div>
      <p id="makbuz-notu" class="aciklama"></p>
      <div id="makbuz-ozet" class="izgara"></div>
      <div class="arac-cubugu">
        <input id="makbuz-ara" type="search" maxlength="160" placeholder="Özet veya dosya yolunda filtrele…" aria-label="İşlem kayıtlarında ara">
      </div>
      <div id="makbuz-listesi"></div>
    </section>
    <section id="gorunum-hafiza" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Hafıza</h1>
          <span id="hafiza-notu" class="rozet"></span>
        </div>
        <button id="hafiza-yenile" type="button" class="ikincil">Yenile</button>
      </div>
      <details class="hafiza-rehber" open>
        <summary>Hafıza (Companion) nedir ve nasıl çalışır?</summary>
        <p>SeroBeyinn, yeni bir AI sohbeti açtığında seni, kurallarını ve önceki oturumda yarım kalan işleri hatırlamak için bu klasördeki çekirdek Markdown dosyalarını okur. Soldaki herhangi bir dosyaya tıklayarak AI ajanlarının hakkında ne gördüğünü sağ panelde okuyabilirsin.</p>
        <ul>
          <li><strong>Core.md:</strong> Kimlik, çalışma tarzın ve kalıcı temel bağlam.</li>
          <li><strong>Kurallar.md:</strong> Ajanların her oturumda uyması gereken kişisel kurallar.</li>
          <li><strong>Last-Session.md:</strong> Son oturumların özeti ve devir notları (karakter limitlidir).</li>
          <li><strong>Threads.md:</strong> Açık kalan konular ve devam eden iş takibi (karakter limitlidir).</li>
          <li><strong>Sıkıştır (companion-compact):</strong> Limit dolduğunda eski oturum/konu girdilerini hiçbir şeyi silmeden özel arşive taşır; böylece açılış bağlamı hızlı ve temiz kalır.</li>
        </ul>
      </details>
      <div id="hafiza-ozet" class="izgara"></div>
      <div class="ikili">
        <div>
          <div class="kokpit-bolum">
            <h2>Sınır takipli dosyalar</h2>
            <p class="sutun-aciklama">Oturum açılışında otomatik okunan ve boyut sınırı izlenen dosyalar</p>
            <ul id="hafiza-listesi" class="liste"></ul>
            <div class="hafiza-aksiyon">
              <button id="sikistir" type="button">Sıkıştır</button>
              <span id="hafiza-sikistir-not" class="aciklama"></span>
            </div>
          </div>
          <div class="kokpit-bolum">
            <h2>Çekirdek hafıza dosyaları</h2>
            <p class="sutun-aciklama">Tıklayarak sağ panelde okunabilir (salt okunur önizleme)</p>
            <ul id="hafiza-cekirdek" class="liste"></ul>
          </div>
        </div>
        <div class="gozden-sag">
          <div class="kokpit-bolum">
            <h2 id="hafiza-onizleme-baslik">Önizleme</h2>
            <div id="hafiza-onizleme-meta" class="ust-bilgi"></div>
            <div id="hafiza-onizleme" class="onizleme md-okuma"><p class="bos">Okumak için soldan bir hafıza dosyası seç…</p></div>
          </div>
        </div>
      </div>
    </section>
    <section id="gorunum-graf" class="gorunum" hidden>
      <h1>Graf</h1>
      <p class="aciklama">Vault'taki Markdown notları iki yarımküreli beyin haritasında dağılır. Bir düğüme tıklayınca sağda notun içeriği açılır; sürükleyerek gezin, tekerlekle yakınlaştır.</p>
      <div class="graf-ikili">
        <div>
          <div class="arac-cubugu">
            <button id="graf-yenile" type="button" class="ikincil">Yenile</button>
            <button id="graf-mod" type="button" class="ikincil">Mod: Beyin</button>
            <button id="graf-ortala" type="button" class="ikincil">Ortala</button>
            <span id="graf-notu" class="aciklama"></span>
            <span id="graf-lejant" class="graf-lejant" role="group" aria-label="Modül seçimi">
              <button type="button" class="graf-filtre" data-tur="knowledge" aria-pressed="false"><i class="n-knowledge"></i>Bilgi</button>
              <button type="button" class="graf-filtre" data-tur="daily" aria-pressed="false"><i class="n-daily"></i>Günlük</button>
              <button type="button" class="graf-filtre" data-tur="receipts" aria-pressed="false"><i class="n-receipts"></i>Kayıtlar</button>
              <button type="button" class="graf-filtre" data-tur="companion" aria-pressed="false"><i class="n-companion"></i>Hafıza</button>
              <button type="button" class="graf-filtre" data-tur="diger" aria-pressed="false"><i class="n-diger"></i>Diğer</button>
            </span>
          </div>
          <div class="graf-kutu"><canvas id="graf-tuval" aria-label="Not bağlantı grafiği"></canvas></div>
        </div>
        <aside class="graf-sag">
          <div id="graf-secim" class="kart" hidden></div>
          <div id="graf-icerik" class="onizleme md-okuma"><p class="bos">Bir nota tıklayın…</p></div>
        </aside>
      </div>
    </section>
    <section id="gorunum-guncelleme" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Güncelleme</h1>
          <span class="rozet">Yedekli ve onaylı</span>
        </div>
      </div>
      <p class="aciklama">SeroBeyinn sistem dosyalarını GitHub resmi sürümünden (BeNKaYS/SeroBeyinn) veya yerel .zip paketinden doğrulanmış biçimde günceller. Kullanıcı notları, görevler, veritabanı ve ayarlar güncellenmez; hata olursa serobeyinn.py rollback ile geri alınabilir.</p>
      <div id="guncelleme-ozet" class="izgara"></div>
      <div class="kokpit-bolum">
        <h2>Güncelleme Denetimi</h2>
        <div class="arac-cubugu">
          <label>Kaynak
            <select id="guncelleme-kaynak">
              <option value="github">GitHub (Resmi Release · BeNKaYS/SeroBeyinn)</option>
              <option value="yerel">Yerel paket (.zip)</option>
            </select>
          </label>
          <label id="guncelleme-paket-alan" hidden>Paket yolu
            <input id="guncelleme-paket" type="text" maxlength="500" placeholder="/yol/serobeyinn-v3-X.Y.Z.zip">
          </label>
          <button id="guncelleme-kontrol" type="button">Kontrol Et</button>
          <button id="guncelleme-uygula" type="button" disabled>Güncelle</button>
        </div>
        <p id="guncelleme-sonuc" class="aciklama"></p>
      </div>
    </section>
    <section id="gorunum-yardim" class="gorunum" hidden>
      <div class="kokpit-ust">
        <div class="kokpit-ust-sol">
          <h1>Yardım ve Kullanım Rehberi</h1>
          <span class="rozet iyi">Kasa + Skill + Web</span>
        </div>
        <a href="#kokpit" class="dugme-bag">Kokpite dön</a>
      </div>
      <p class="aciklama">SeroBeyinn hafıza sisteminin çalışma mantığı, sohbet tetikleyicileri, tüm menüler, alt özellikler ve günlük kullanımda işini kolaylaştıracak püf noktaları.</p>

      <h2>1. SeroBeyinn Nasıl Çalışır?</h2>
      <div class="yardim-izgara">
        <div class="yardim-kart">
          <h3>Tek Kaynak: Yerel Markdown Kasa</h3>
          <p>Tüm notların, görevlerin ve AI hafızan bilgisayarındaki düz Markdown dosyalarında tutulur (Obsidian ile de açabilirsin). Bulut, abonelik veya harici hesap yoktur.</p>
          <ul>
            <li><strong>Eşitleme (<code>sync</code>):</strong> Dosyalar yerel SQLite dizinine indekslenir; AI ajanları ve bu web paneli o dizini okur.</li>
            <li><strong>Güvenli yazma:</strong> Web paneli doğrudan dosya ezmez; CLI komutları, kilitler ve sır süzgeci üzerinden yazar.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Skill ve Hook Mekanizması</h3>
          <p>Antigravity, Claude Code, Codex, OpenCode ve Kiro yeni sohbet açtığında hook dosyası üzerinden çekirdek hafızanı otomatik okur.</p>
          <ul>
            <li><strong>Açılışta:</strong> <code>Core.md</code>, <code>Kurallar.md</code>, <code>Last-Session.md</code> ve <code>Threads.md</code> bağlama girer.</li>
            <li><strong>Kapanışta:</strong> Biten işler ve dokunulan kaynaklar işlem kaydı (receipt) olarak izlenir.</li>
          </ul>
        </div>
      </div>

      <h2>2. Hafıza Nasıl Tetiklenir? (Sohbette Kullanacağın İfadeler)</h2>
      <table class="yardim-tablo">
        <thead>
          <tr><th>Sohbette Ne Dersin?</th><th>Ne Olur?</th><th>Etkilenen Dosya</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>merhaba</code> · <code>selam</code> · <code>nasılsın</code></td>
            <td>Açık projede sorumlusu <code>@ajan</code> olan görevleri kontrol eder; "Bu projede şu görevim vardı, devam edeyim mi?" diye sorar (onaysız başlamaz).</td>
            <td><code>tasks/*.md</code></td>
          </tr>
          <tr>
            <td><code>oturumu kasaya yaz</code></td>
            <td>Oturumda yapılanları, alınan kararları, yarım kalan işleri ve yeni öğrenimleri kalıcı hafızaya işler.</td>
            <td><code>Last-Session.md</code>, <code>Threads.md</code>, <code>Journal.md</code></td>
          </tr>
          <tr>
            <td><code>bunu Journal'a ekle</code> · <code>öğrendiklerimizi yaz</code></td>
            <td>Çalışırken ortaya çıkan teknik gözlem, tercih veya açık soruyu çalışma günlüğüne ekler.</td>
            <td><code>Journal.md</code></td>
          </tr>
          <tr>
            <td><code>bir daha ... yapma</code> · <code>önce sor</code></td>
            <td>Kişisel çalışma kuralını tarihli biçimde kalıcı kurallara yazar; sonraki tüm sohbetlerde uygulanır.</td>
            <td><code>Kurallar.md</code></td>
          </tr>
          <tr>
            <td><code>hatırla ...</code> · <code>kasada ara ...</code></td>
            <td>Önceki kararları, proje notlarını ve ilgili kayıtları dizinden bulup bağlama getirir.</td>
            <td>Tüm görünür dizin</td>
          </tr>
          <tr>
            <td><code>görev ekle ...</code> · <code>proje durumu</code></td>
            <td>Yeni görev açar veya projedeki aktif/engellenmiş görevlerle son durumu özetler.</td>
            <td><code>tasks/*.md</code></td>
          </tr>
        </tbody>
      </table>

      <h2>3. Menüler ve Alt Özellikler</h2>
      <div class="yardim-izgara">
        <div class="yardim-kart">
          <h3>Kokpit <a href="#kokpit">Aç</a></h3>
          <p>Sistemin genel kontrol ekranı. Özet kartlara tıklayarak ilgili bölüme tek tıkla geçebilirsin.</p>
          <ul>
            <li><strong>Üst çubuk:</strong> Kasada hızlı arama kutusu, <code>Yenile</code> ve bu <code>Yardım</code> düğmesi.</li>
            <li><strong>Özet kartları:</strong> Doktor sağlığı, açık görev sayısı, hafıza doluluğu, bekleyen/bayat öğeler.</li>
            <li><strong>Odak görevler:</strong> Hızlı görev ekleme satırı (Enter ile ekler) ve acil/aktif görev listesi.</li>
            <li><strong>Sağ sütun:</strong> Hafıza doluluk özeti ve son işlem kayıtları.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Görevler <a href="#gorevler">Aç</a></h3>
          <p><code>tasks/</code> klasöründeki görevleri 6 sütunlu Kanban panosunda yönetir.</p>
          <ul>
            <li><strong>Sütunlar:</strong> Gelen, Aktif, Bekliyor, Engellendi, Bitti, İptal.</li>
            <li><strong>Yeni görev formu:</strong> Başlık, Sorumlu (<code>ben</code>, <code>ajan</code>, <code>claude</code> vb.), Proje, Durum ve Açıklama.</li>
            <li><strong>Filtreler:</strong> Proje seçici, Sorumlu filtresi, metin araması ve <code>Kapalıları göster/gizle</code>.</li>
            <li><strong>Kart aksiyonları:</strong> Açılır listeden anında durum değiştirme ve kart detay önizleme.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Graf <a href="#graf">Aç</a></h3>
          <p>Kasandaki eşitlenmiş notları ve aralarındaki <code>[[wiki]]</code> / Markdown bağlantılarını iki yarımküreli beyin haritasında gösterir.</p>
          <ul>
            <li><strong>Mod: Beyin / Serbest:</strong> Beyin haritası ile serbest ağ görünümü arasında geçiş yapar.</li>
            <li><strong>Modül filtreleri:</strong> <code>Bilgi</code>, <code>Günlük</code>, <code>Kayıtlar</code>, <code>Hafıza</code>, <code>Diğer</code> düğmelerine tıklayınca ilgili düğümler vurgulanır.</li>
            <li><strong>Etkileşim:</strong> Sürükleyerek gez, tekerlekle yakınlaştır, <code>Ortala</code> ile sıfırla; düğüme tıklayınca sağda Markdown önizleme açılır.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Gözden geçir <a href="#gozden-gecir">Aç</a></h3>
          <p>Unutulan veya biriken işleri yakalamak için salt okunur triage ekranı.</p>
          <ul>
            <li><strong>Gelen kutusu:</strong> <code>000-Inbox</code> klasör bazında öğe sayıları ve en eski not yaşı.</li>
            <li><strong>Bayat konular ve görevler:</strong> Uzun süredir hareket görmeyen başlıklar.</li>
            <li><strong>Taslak notlar:</strong> <code>taslak / draft / proposed</code> durumundaki notlar.</li>
            <li><strong>Sağ önizleme:</strong> Seçilen kaydı okunabilir Markdown formatında açar.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Arama <a href="#arama">Aç</a></h3>
          <p>AI ajanlarının kullandığı dizinde en az 2 harfle hızlı tam metin araması yapar.</p>
          <ul>
            <li><strong>Vurgulama:</strong> Eşleşen kelimeler sonuç özetinde öne çıkarılır.</li>
            <li><strong>Markdown okuyucu:</strong> Sonuca tıklayınca sağ panelde ham kod yerine başlık, tablo ve listeli temiz görünüm açılır.</li>
            <li><strong>Temizle:</strong> Aramayı ve önizlemeyi tek tıkla sıfırlar.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>İşlem Kayıtları (Receipts) <a href="#makbuzlar">Aç</a></h3>
          <p>Son 14 günde AI ajanlarının kasada hangi dosyalara dokunduğunu ve ne yaptığını denetleme ekranı.</p>
          <ul>
            <li><strong>Özet kartları:</strong> Toplam kayıt, dokunulan farklı dosya sayısı, son kayıt zamanı, saklanan gizli kaynak sayısı.</li>
            <li><strong>Gün gruplu akış:</strong> Bugün, Dün ve tarih başlıkları altında saat + özet + dosya yolu etiketleri.</li>
            <li><strong>Filtre:</strong> Özet metninde veya dosya yolunda anlık süzme.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Hafıza <a href="#hafiza">Aç</a></h3>
          <p>AI'ın oturumlar arası taşıdığı Companion dosyalarını inceleme ve bakım ekranı.</p>
          <ul>
            <li><strong>Sınır takipli dosyalar:</strong> <code>Last-Session.md</code> ve <code>Threads.md</code> için renkli doluluk çubukları (yeşil / sarı / kırmızı).</li>
            <li><strong>Çekirdek dosyalar:</strong> <code>Core.md</code>, <code>Kurallar.md</code> ve <code>Journal.md</code>; tıklayınca sağda okunabilir.</li>
            <li><strong>Sıkıştır:</strong> Limit dolduğunda eski girdileri silmeden arşive taşır (<code>companion-compact</code>).</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Sol Panel ve Başlık Araçları</h3>
          <p>Tüm sayfalarda sabit kalan kenar çubuğu kontrolleri.</p>
          <ul>
            <li><strong>Özel başlık:</strong> Sol üstteki başlığa çift tıkla veya <code>✎</code> ile kendi adını yaz (kalıcı kaydedilir).</li>
            <li><strong>Eşitle:</strong> Yeni/değişen notları dizine işler (<code>serobeyinn.py sync</code>).</li>
            <li><strong>Mod rozeti ve kapatma:</strong> <code>Yazma açık / Salt okunur</code> durumu, <code>Sunucuyu kapat</code> (boşta 30 dk sonra otomatik kapanır).</li>
          </ul>
        </div>
      </div>

      <h2>4. Püf Noktaları ve Güvenlik</h2>
      <div class="yardim-izgara">
        <div class="yardim-kart">
          <h3>Ajan Görev Akışı (@ajan)</h3>
          <ul>
            <li>Kendi yapacağın işlere <code>ben</code>, AI'a vereceğin işlere <code>ajan</code> (veya <code>claude</code>, <code>codex</code>, <code>antigravity</code>) yaz.</li>
            <li>Proje adını klasör adıyla aynı tut (ör. <code>SeroBeyinn</code>); yeni sohbette <code>merhaba</code> dediğinde ajan önce o projedeki görevini hatırlatır.</li>
            <li>Yeni görev veya not ekledikten sonra dışarıdan dosya değiştirdiysen mutlaka <strong>Eşitle</strong>'ye bas.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Gizlilik ve Güvenlik Kalkanı</h3>
          <ul>
            <li><strong>Özel notlar sızmaz:</strong> <code>visibility: private</code> notlar ve <code>Kasa / Şifre / Finans / Müşteri</code> klasörleri web arayüzüne ve ajan dizinine hiç girmez.</li>
            <li><strong>Parola kuralı:</strong> Şifreleri düz metin notlarda değil parola yöneticisinde tut.</li>
            <li><strong>Yalnız yerel ağ:</strong> Sunucu sadece <code>127.0.0.1</code> dinler; dış internete veya CDN'e tek istek gitmez.</li>
          </ul>
        </div>
        <div class="yardim-kart">
          <h3>Bakım, Çakışma ve Kısayol</h3>
          <ul>
            <li><strong>Sıkıştırma veri silmez:</strong> Eski oturum kayıtları arşive aynen taşınır, geri okunabilir.</li>
            <li><strong>Revizyon koruması:</strong> Aynı görev hem Obsidian hem Web'den değişirse çakışma uyarısı verir, veri ezilmez.</li>
            <li><strong>Salt okunur mod:</strong> Aynı bilgisayarda başka yerel sunucular çalışırken <code>serobeyinn.py web ac --read-only</code> ile açabilirsin.</li>
            <li><strong>Kısayol:</strong> Masaüstündeki <code>SeroBeyinn Web.command</code> güncel web kodunu kasaya otomatik aktarır ve sunucuyu temiz başlatır.</li>
          </ul>
        </div>
      </div>
    </section>
  </main>
</div>
<div id="bildirim" aria-live="polite"></div>
<dialog id="gelistirici-modal" class="gelistirici-modal" aria-labelledby="dev-baslik">
  <div class="dev-card">
    <div class="dev-ust">
      <div class="dev-noktalar">
        <span class="dev-nokta k" aria-hidden="true"></span>
        <span class="dev-nokta s" aria-hidden="true"></span>
        <span class="dev-nokta y" aria-hidden="true"></span>
        <span>~/BeNKaYS/profile.sh - bash</span>
      </div>
      <button id="gelistirici-kapat" type="button" class="dev-kapat" title="Kapat" aria-label="Kapat">×</button>
    </div>
    <div class="dev-govde">
      <div class="dev-komut"><span>root@benkays</span>:~$ ./whoami.sh</div>
      <div id="dev-baslik" class="dev-ad">SERCAN ÖZDEMİR</div>
      <div class="dev-mahlas">BeNKaYS</div>
      <div class="dev-unvan">Bilişim Teknolojileri Öğretmeni · Makine Öğrenmesi · C++</div>
      <hr class="dev-divider" data-label="// HAKKIMDA">
      <p class="dev-metin">Eğitim ve yazılımı birleştiren, özellikle <strong>C++</strong>, <strong>algoritmalar</strong> ve <strong>Makine Öğrenmesi</strong> üzerine projeler geliştiren bir yazılım öğretmeniyim.<br>Karmaşık sistemleri sade ve anlaşılır hale getirmek temel prensibimdir.</p>
      <hr class="dev-divider" data-label="// BECERİLER &amp; TEKNOLOJİ">
      <div class="dev-ikili">
        <div>
          <div class="dev-beceri"><div class="dev-beceri-ust"><span>Makine Öğrenmesi</span><span>80%</span></div><div class="dev-cubuk"><div class="dev-dolgu" data-pct="80"></div></div></div>
          <div class="dev-beceri"><div class="dev-beceri-ust"><span>C++ &amp; OOP</span><span>95%</span></div><div class="dev-cubuk"><div class="dev-dolgu" data-pct="95"></div></div></div>
          <div class="dev-beceri"><div class="dev-beceri-ust"><span>Algoritma Tasarımı</span><span>85%</span></div><div class="dev-cubuk"><div class="dev-dolgu" data-pct="85"></div></div></div>
          <div class="dev-beceri"><div class="dev-beceri-ust"><span>Eğitim Odaklı Dev</span><span>95%</span></div><div class="dev-cubuk"><div class="dev-dolgu" data-pct="95"></div></div></div>
          <div class="dev-beceri"><div class="dev-beceri-ust"><span>Python</span><span>70%</span></div><div class="dev-cubuk"><div class="dev-dolgu" data-pct="70"></div></div></div>
          <div class="dev-rozetler">
            <span class="dev-rozet">C++</span><span class="dev-rozet">Python</span><span class="dev-rozet">OpenCV</span>
            <span class="dev-rozet">Git</span><span class="dev-rozet">Linux</span><span class="dev-rozet">VSCode</span><span class="dev-rozet">ML</span>
          </div>
        </div>
        <div>
          <div class="dev-qr-alan">
            <div class="dev-qr-sekmeler">
              <button type="button" class="dev-qr-tab secili" data-qr="wa">WhatsApp</button>
              <button type="button" class="dev-qr-tab" data-qr="mail">E-posta</button>
            </div>
            <canvas id="dev-qr" width="116" height="116" aria-label="İletişim QR kodu"></canvas>
            <div id="dev-qr-etiket" class="dev-qr-etiket">WhatsApp QR</div>
          </div>
          <div class="dev-iletisim">
            <a class="dev-bag" href="mailto:sercanozdemir@yandex.com"><span>📧</span><span>sercanozdemir@yandex.com</span><small>--mail</small></a>
            <button type="button" class="dev-bag" data-kopyala="0506 885 85 85"><span>💬</span><span>WhatsApp · 0506 885 85 85</span><small>--chat</small></button>
            <button type="button" class="dev-bag" data-kopyala="github.com/BeNKaYS"><span>🐙</span><span>github.com/BeNKaYS</span><small>--github</small></button>
          </div>
        </div>
      </div>
      <div class="dev-alt">
        <span class="dev-alinti">Gündüz sınıf, gece terminal.</span>
        <span class="dev-sayac">[ BeNKaYS · yerel ]</span>
      </div>
    </div>
  </div>
</dialog>
</body>
</html>
"""

_UNLOCK = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SeroBeyinn Web: oturum</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="/app.css">
</head>
<body>
<div class="kilit"><div class="kart">
  <div class="marka"><span class="limon" aria-hidden="true">🍋</span><strong>SeroBeyinn Web</strong></div>
  <p>{message}</p>
  <form method="get" action="/">
    <input type="password" name="token" required autocomplete="off" aria-label="Oturum belirteci" placeholder="Oturum belirteci">
    <button type="submit">Aç</button>
  </form>
</div></div>
</body>
</html>
"""


def index_page(csrf, read_only):
    return _INDEX.format(csrf=html.escape(csrf, quote=True), read_only='1' if read_only else '0')


def unlock_page(failed):
    message = ('Belirteç geçersiz ya da bu sunucu yeniden başladı. ' if failed else '') + \
        'Oturum açmak için terminalde serobeyinn.py web ac çalıştır ya da yazdırdığı adresteki belirteci gir.'
    return _UNLOCK.format(message=html.escape(message))
