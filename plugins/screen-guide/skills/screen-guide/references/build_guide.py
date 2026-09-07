#!/usr/bin/env python3
"""ゾーン切り出し＋base64埋め込みで、1ファイル完結のガイドHTMLを作る。

使い方:
  python build_guide.py plan.json out.html

plan.json の形:
{
  "title": "リベシティ ホーム画面の見方",
  "lead": "2026-09-07 に Chrome（ログイン済み）で確認。赤い番号を押すと解説へ飛びます。",
  "zones": [
    {"label": "画面A-1 固定要素", "src": "C:/Users/.../screenshot-1.jpg",
     "crop": [0, 0, 1568, 60], "scale": 2, "items": [1, 2, 4]},
    ...
  ],
  "items": {
    "1": {"where": "最上段バー、中央左", "what": "検索欄 ＝ サイト内検索の入口", "how": "..."},
    ...
  },
  "order": "③ → ⑨ → ⑩ ...",
  "unverified": "②メニューの中身 ..."
}
crop は [left, top, right, bottom]（そのスクショのピクセル）。省略で全体。scale は表示倍率（1〜3）。
"""
import sys, json, base64, io, html
from pathlib import Path
from PIL import Image

CSS = """
:root{--panel:#fff;--fg:#333;--muted:#7a8291;--line:#dfe3ea;--mark:#ff4d5e}
*{box-sizing:border-box}body{margin:0;background:#e8ebf0;color:var(--fg);font:14px/1.6 -apple-system,"Segoe UI","Hiragino Sans","Noto Sans JP",sans-serif}
.wrap{max-width:1100px;margin:20px auto;padding:0 14px}h1{font-size:19px;margin:0 0 4px}.lead{color:var(--muted);margin:0 0 16px;font-size:13px}
h2.sc{font-size:15px;margin:26px 0 8px}.shot{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff}.shot img{display:block;width:100%;height:auto}
.item{display:grid;grid-template-columns:32px 1fr;gap:10px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:11px 13px;margin:8px 0;scroll-margin-top:12px}
.item:target{outline:2px solid var(--mark)}.item .n{width:24px;height:24px;border-radius:50%;background:var(--mark);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:13px}
.item h3{margin:0 0 3px;font-size:14px}.item p{margin:0;font-size:13px}.item .where{font-size:11px;color:var(--muted);margin-bottom:3px}.foot{color:var(--muted);font-size:12px;margin-top:12px}
"""

def img_data(src, crop, scale):
    im = Image.open(src).convert("RGB")
    if crop: im = im.crop(tuple(crop))
    if scale and scale != 1: im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def main(plan_path, out_path):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    e = html.escape
    parts = [f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(plan["title"])}</title><style>{CSS}</style></head><body><div class="wrap">',
             f'<h1>{e(plan["title"])}</h1><p class="lead">{e(plan.get("lead",""))}</p>']
    items = plan["items"]
    for z in plan["zones"]:
        parts.append(f'<h2 class="sc">{e(z["label"])}</h2><div class="shot"><img src="{img_data(z["src"], z.get("crop"), z.get("scale",1))}" alt="{e(z["label"])}"></div>')
        for n in z["items"]:
            it = items[str(n)]
            parts.append(f'<div class="item" id="p{n}"><div class="n">{n}</div><div><div class="where">{e(it["where"])}</div><h3>{e(it["what"])}</h3><p>{e(it["how"])}</p></div></div>')
    if plan.get("order"): parts.append(f'<p class="foot">読む順番の目安：{e(plan["order"])}</p>')
    parts.append(f'<p class="foot">未確認点：{e(plan.get("unverified","なし"))}</p>')
    parts.append('</div></body></html>')
    Path(out_path).write_text("".join(parts), encoding="utf-8")
    print(f"wrote {out_path} ({Path(out_path).stat().st_size//1024} KB)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
