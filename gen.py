import base64,html,json
R=[("robot","Web","Hackaday","Sesame","Dorian Todd","3Dプリントの小さな4脚ロボット。OLEDの顔で感情を表し、部品代は約60ドル。",["ESP32","MG90S×8","OLED"],"https://hackaday.com/2026/01/24/building-a-little-quadruped-robot/","sesame"),
("robot","Web","Hackaday","TongDou","solitary dev","真鍮ボディのオープンソース卓上ロボット。",["ESP32-S3","OLED","24GHzレーダー","IMU","ギアモーター"],"https://hackaday.com/2026/07/31/tiny-desktop-robot-has-radar/","tongdou"),
("robot","Web","Hackaday.io","BugBot","Jerome Graves","7cm角の振動駆動・全方向4脚ロボット。群ロボット教材として安価に設計。",["XIAO ESP32-S3 Sense","コアレスモーター","VL53L5CX","TinyML"],"https://hackaday.io/project/205769-bugbot-vibration-based-quadruped","bugbot"),
("robot","Web","Hackaday.io","NeuroMouse V2.0","Inky Ganbold, Yu Hong Chen","2026年AAMCで総合3位のマイクロマウス。",["ESP32-S3","N20","DRV8833","MPU-6500"],"https://hackaday.io/project/206865-neuromouse-v20-esp32-s3-micromouse-3rd-at-aamc","neuro"),
("robot","Web","Hackster","TN-24 V2.0","tech_nickk","OLEDの目で表情を出す歩行型の卓上ロボット。",["XIAO ESP32S3 Sense","マイクロサーボ×4","MPU6050","OLED"],"https://www.hackster.io/tech_nickk/tn-24-v2-0-cute-desktop-companion-robot-44a472","tn24"),
("robot","Web","Hackster","ESP32 4x4 RC Rover","Gokux","全部3Dプリントの4WDローバー。ブラウザのジョイスティックで操作。",["XIAO ESP32C3","DRV8833","N20×4","18650"],"https://www.hackster.io/Gokux/esp32-powered-4x4-rc-rover-fully-3d-printed-wi-fi-control-a7320d","rover"),
("robot","X","X","ダイアル・ナイツ","あるば～と（@albertlabo）","M5Stack Dialで動くクローラー型ロボットで、ドリルやカタナなどの装備を付け替えられる。",["M5Stack Dial","クローラー"],"https://x.com/albertlabo/status/2099740432649568580","dial"),
("robot","X","X","AtomDogを作ってみた","さすけ（@sasuke9410）","M5Stackのコンテスト入賞作の再現で、サーボ4個で歩き、猫の頭と尻尾が付いている。",["M5Stack","サーボ×4","3Dプリント"],"https://x.com/sasuke9410/status/2100234383693410689","atomdog"),
("robot","X","X","最小の努力で作った猫型ロボット","みっちさん（@mityomi722）","スタックチャンがベースで、アプリで動かせて肉球がプニプニ。",["M5Stack","スタックチャン"],"https://x.com/mityomi722/status/2086443485159387475","neko"),
("robot","X","X","Stack-Chan Minimal","A-Uta（@UtaAoya）","ATOMS3RとローカルAIの会話ロボットで、作り方を本に寄稿している。",["ATOMS3R","ローカルAI","スタックチャン"],"https://x.com/UtaAoya/status/2097089049026773462","minimal"),
("robot","X","X","Chibi Ram","harshit gupta（@harshit87218175）","ESP32-S3とカメラで周りを見て、クラウドのLLMで考え、音声とサーボで反応する対話ロボット。",["ESP32-S3","OV3660","PCA9685","LLM"],"https://x.com/harshit87218175/status/2109187654978084975","chibi"),
("robot","X","X","MeridianでSO-101を駆動","holypong（@automo_emo）","ESP32ベースのボードでロボットアームを動かし、PCのシミュレータと100Hzで同期。",["ESP32","Meridian","Feetech","SO-101","UDP"],"https://x.com/automo_emo/status/2101923813013549259","meridian"),
("art","Web","Prix Ars Electronica 2025","Organism + Excitable Chaos","Navid Navab, Garnet Willis","ロボット三重振り子のカオス運動で、1910年製パイプオルガンの気流をサーボとバルブで変える。ゴールデン・ニカ受賞。",["三重振り子","加速度センサー","サーボ","バルブ"],"https://www.navidnavab.com/organism-excitable-chaos",None),
("art","Web","Hochschuh & Donovan","Plasticity of Mirrors","Hochschuh & Donovan","直径68mmの光る2輪ロボット10台の群れが観客の手と関わり合う。",["自作PCB","ブラシレスモーター","IMU","RGB LED","ハンドトラッキング"],"https://hochschuh-donovan.com/portfolio/plasticity-of-mirrors/",None),
("art","Web","michaelzhou.studio","Wallaby Kinetic","Michael Zhou","多数のステッピングモーターをネットワークで協調させるキネティック作品。",["ESP32-S3","SAMD21","TMC2209","AS5600","RS485"],"https://michaelzhou.studio/creative-tech/wallaby-kinetic","wallaby"),
("art","Web","cargo.site","Pixel Chord","Muzi Marilyn Fang, Moira Zhang","ステッピングモーターをMIDIに対応させ、楽器として演奏させる。",["NEMA17","DRV8825","Arduino","Max"],"https://muzifang.cargo.site/pixel-chord","pixel"),
("art","Web","sam-janssen.com","Together","Sam Janssen","毎回違うパターンで回転し続けるCCTVカメラの作品。",["Arduino","ステッピングモーター","スリップリング","CCTV"],"https://www.sam-janssen.com/work-1/project-one-yrf7a-lc2jd-dgdlr-3kee8-gzph9","together"),
("art","Web","National Science and Media Museum","Circus","Nayan Kulkarni","観客を追うロボットカメラと固定カメラの映像を、家庭用テレビ上でリアルタイムに合成する。",["ロボットカメラ","映像フィードバック","TVモニター"],"https://www.scienceandmediamuseum.org.uk/about-us/press-office/national-science-and-media-museum-unveils-circus-nayan-kulkarni-brand-new",None),
("art","X","X（紹介：はむぞう @hamuzou）","機械仕掛けのススキ","ハルスギモト","藝祭2026の作品。モーターでススキの穂をなびかせるキネティックアートで、宮田亮平賞を受賞。",["モーター","キネティック"],"https://x.com/hamuzou/status/2096435031480918121","susuki"),
("art","X","X（@Behold3d）","Birds In Flight","Julia Daser + Pepi Ng","Arduinoで制御するモーター付きのらせんが、糸でつった鳥を群れのように上下させる。",["Arduino","モーター","スチールらせん","3Dプリント"],"https://x.com/Behold3d/status/2084580861513515044","birds"),
("art","X","X","舞台作品「模#2」","Kei Tsujimoto（@KeiTsujimoto）","ESP32で動くロボットと音響を組み合わせたダンス作品の制作記録。",["ESP32","ロボット","音響","ダンス"],"https://x.com/KeiTsujimoto/status/2104880082989039647","mo2")]
e=html.escape
def card(c,s,site,t,a,su,tags,u,k):
    img=f'<img src="data:image/jpeg;base64,{base64.b64encode(open(k+".jpg","rb").read()).decode()}" alt="{e(t)}">' if k else '<div class="ph">画像なし</div>'
    tg="".join(f"<span>{e(x)}</span>" for x in tags)
    return f'<article class="card" data-src="{s}">{img}<div class="b"><h3>{e(t)}</h3><p class="m">{e(a)} ・ 出典: {s}（{e(site)}）</p><p>{e(su)}</p><div class="tags">{tg}</div><a href="{e(u)}" target="_blank" rel="noopener noreferrer">元ページを開く →</a></div></article>'
sec=lambda cat,h:f'<section data-cat="{cat}"><h2>{h}</h2><div class="grid">'+"".join(card(*r) for r in R if r[0]==cat)+'</div></section>'
n=lambda s:sum(1 for r in R if s=="all" or r[1]==s)
doc=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小型ロボット＆インスタレーション作品ギャラリー</title><style>
body{{font-family:system-ui,"Noto Sans CJK JP",sans-serif;margin:0;padding:24px;background:#f7f7f8;color:#111}}h1{{margin:0 0 4px}}.sum{{color:#555;margin:0 0 16px}}
.f button{{border:1px solid #ccc;background:#fff;border-radius:999px;padding:6px 14px;margin:0 6px 6px 0;cursor:pointer;font-size:14px}}.f button.on{{background:#111;color:#fff;border-color:#111}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}.card{{background:#fff;border:1px solid #e3e3e6;border-radius:12px;overflow:hidden;display:flex;flex-direction:column}}
.card img,.ph{{width:100%;aspect-ratio:5/3;object-fit:cover;display:block}}.ph{{background:#ddd;color:#666;display:flex;align-items:center;justify-content:center;font-weight:600}}
.b{{padding:12px 14px 14px}}h3{{margin:0 0 4px;font-size:17px}}.m{{color:#666;font-size:13px;margin:0 0 6px}}.b p{{font-size:14px;line-height:1.5;margin:0 0 8px}}
.tags span{{display:inline-block;border:1px solid #ddd;border-radius:999px;padding:1px 8px;font-size:12px;color:#444;margin:0 4px 4px 0}}a{{color:#1a5fd0;font-size:14px}}.hide{{display:none}}
</style></head><body><h1>小型ロボット＆インスタレーション作品ギャラリー</h1><p class="sum">小型マイコンを使ったロボット作品と、モーターやディスプレイを使ったインスタレーション{n("all")}件。出典（Web/X）で絞り込めます。</p>
<div class="f"><button class="on" data-f="all">すべて ({n("all")})</button><button data-f="Web">Web ({n("Web")})</button><button data-f="X">X ({n("X")})</button></div>
{sec("robot","小型ロボット・マイコン作品")}{sec("art","インスタレーション・アート")}
<script>document.querySelectorAll('.f button').forEach(b=>b.onclick=()=>{{const f=b.dataset.f;document.querySelectorAll('.f button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('.card').forEach(c=>c.classList.toggle('hide',f!=='all'&&c.dataset.src!==f));document.querySelectorAll('section').forEach(s=>s.classList.toggle('hide',!s.querySelector('.card:not(.hide)')))}})</script></body></html>'''
open('gallery.html','w').write(doc)
