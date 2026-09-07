// 実画面に赤枠＋番号バッジを注入する（Claude in Chrome の javascript_tool で実行）
// 使い方：window.sgMark({5:[82,95,381,250], ...}, {1:[486,4,560,38], ...}) → ページ座標／固定要素
//        window.sgClear() で全部消す。固定要素だけ消すなら window.sgClear('fixed')
window.sgClear = (kind) => document.querySelectorAll(kind ? '.sg-mark.sg-'+kind : '.sg-mark').forEach(e => e.remove());
window.sgMark = (page = {}, fixed = {}) => {
  const SIZE = 44, PAD = 6;
  const add = (n, [x, y, w, h], isFixed) => {
    const f = document.createElement('div');
    f.className = 'sg-mark sg-' + (isFixed ? 'fixed' : 'page');
    f.style.cssText = `position:${isFixed ? 'fixed' : 'absolute'};left:${x}px;top:${y}px;width:${w}px;height:${h}px;` +
      'border:3px solid #ff4d5e;border-radius:6px;box-sizing:border-box;pointer-events:none;z-index:2147483000;';
    const b = document.createElement('div');
    b.textContent = n;
    // 枠の内側左上に置く。枠が画面端・固定ヘッダーに接していても欠けない
    b.style.cssText = `position:absolute;left:${PAD}px;top:${PAD}px;width:${SIZE}px;height:${SIZE}px;border-radius:50%;` +
      `background:#ff4d5e;color:#fff;font:700 22px/${SIZE}px sans-serif;text-align:center;` +
      'box-shadow:0 0 0 3px #fff,0 2px 6px rgba(0,0,0,.4);';
    f.appendChild(b);
    document.body.appendChild(f);
  };
  for (const k in page) add(k, page[k], false);
  for (const k in fixed) add(k, fixed[k], true);
  return document.querySelectorAll('.sg-mark').length;
};
// 要素の座標を取る補助：見出しテキストから、それを含む section の [x,y,w,h]（ページ座標）
window.sgBox = (txt, tag = 'h1,h2,h3,h4') => {
  const h = [...document.querySelectorAll(tag)].find(e => e.innerText.trim().startsWith(txt));
  if (!h) return null;
  let p = h;
  while (p.parentElement && p.parentElement.tagName !== 'MAIN' && p.parentElement.getBoundingClientRect().height < 900) {
    p = p.parentElement; if (p.tagName === 'SECTION') break;
  }
  const r = p.getBoundingClientRect();
  return [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)];
};
'sg loaded';
