# -*- coding: utf-8 -*-
"""生成したデッキHTML（スライド本体）を機械検査する納品ゲート。

使い方(カレントディレクトリはどこでもよい):
    python3 scripts/verify_deck.py デッキ.html [--json OUT] [--keep]

役割分担（重要）:
- 本スクリプト  … **デッキ本体**を見る。スライド寸法・分量超過・ページ番号・
                   フッター・箇条書き記号・配色。
- ../diagram-parts-html/scripts/verify_html.py
                … **図解パーツ(dgs-scope)** と、文書全体の記入例残り
                   （未置換 `{{…}}` ／ 数値でない rowspan ／ テンプレのガイド文）を見る。
  図解を含むデッキは両方を通す。片方だけでは穴が残る。

なぜスクリプトか（このワークフローの通底課題）:
  デッキは `.slide{overflow:hidden}` と `.page-body{overflow:hidden}` の上に建っている。
  **収まらない内容は警告なく切り落とされる。** エラーもスクロールバーも崩れた見た目も出ない。
  表の最終行が消えたデッキは、消えたことを除けば完璧に見える。
  「ブラウザで見てスクロールバーが出ないこと」という目視チェックは、
  `.slide` の scrollHeight が何を詰め込んでも clientHeight と一致するため**常に真**で、
  空チェックだった。`.page-body` 側なら scrollHeight > clientHeight で正しく検出できる。

検査項目:
  A スライド寸法      … 全 `.slide` が 1280×720 か
  B 分量超過(切り捨て) … overflow:hidden の要素で scrollHeight > clientHeight でないか
  C ページ番号        … `P.<n>` が重複・逆行・欠番なく並んでいるか／枚数と整合するか
  D フッター左        … footer-left が全スライドで同一か
  E 箇条書き記号      … `―` 以外の記号が箇条書きの先頭に混ざっていないか
  F 配色             … design_system.md と template_base.html に無い色を使っていないか

  B・E は描画しないと分からないので headless Chrome を使う。
  図解パーツ(`.dgs-scope`)の内側は本スクリプトの対象外（verify_html.py の担当）。
"""
import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SLIDE_W, SLIDE_H = 1280, 720
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# 箇条書きの先頭に来ていたら不良とする記号。
# `―` は .block-body li::before が CSS で描くので、本文に書くと二重になる。
BAD_BULLETS = '・•‣▪◦●○∙*＊-‐‑‒–—―ー→▶'

PROBE_JS = r"""
(function(){
  function txt(el){ return el ? (el.textContent || '').trim() : null; }
  function inDiagram(el){ return !!el.closest('.dgs-scope'); }
  function run(){
    var slides = document.querySelectorAll('.slide');
    var out = [];
    for (var i=0;i<slides.length;i++){
      var s = slides[i], r = s.getBoundingClientRect();
      var clip = [];
      var all = s.querySelectorAll('*');
      for (var j=-1;j<all.length;j++){
        var el = (j < 0) ? s : all[j];
        if (j >= 0 && inDiagram(el)) continue;
        var cs = getComputedStyle(el);
        var oy = cs.overflowY, ox = cs.overflowX;
        var dy = el.scrollHeight - el.clientHeight;
        var dx = el.scrollWidth - el.clientWidth;
        if ((oy === 'hidden' || oy === 'clip') && dy > 1)
          clip.push({sel: sel(el), axis: 'y', over: dy,
                     h: el.clientHeight, need: el.scrollHeight});
        if ((ox === 'hidden' || ox === 'clip') && dx > 1)
          clip.push({sel: sel(el), axis: 'x', over: dx,
                     h: el.clientWidth, need: el.scrollWidth});
      }
      var bad = [];
      var items = s.querySelectorAll('li, .block-body p');
      for (var k=0;k<items.length;k++){
        if (inDiagram(items[k])) continue;
        var t = (items[k].textContent || '').replace(/^\s+/, '');
        if (t && BAD.indexOf(t.charAt(0)) >= 0)
          bad.push({sel: sel(items[k]), text: t.slice(0, 26)});
      }
      out.push({
        i: i + 1,
        w: Math.round(r.width), h: Math.round(r.height),
        clip: clip,
        footerLeft: txt(s.querySelector('.page-footer .left')),
        footerRight: txt(s.querySelector('.page-footer .right')),
        kind: s.querySelector('.slide-cover') ? 'cover'
             : (s.querySelector('.page-header') ? 'page' : 'other'),
        bad: bad
      });
    }
    var sink = document.getElementById('dgs-deck-probe');
    sink.setAttribute('data-json', btoa(unescape(encodeURIComponent(JSON.stringify(out)))));
    sink.setAttribute('data-done', '1');
  }
  function sel(el){
    var c = el.getAttribute && el.getAttribute('class');
    return el.tagName.toLowerCase() + (c ? '.' + c.trim().split(/\s+/).join('.') : '');
  }
  var BAD = "__BAD__";
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(run).catch(run);
  } else {
    window.addEventListener('load', run);
  }
})();
"""


def render(path, keep=False):
    """デッキの複製に計測スクリプトを差し込んで描画する。

    複製を元ファイルと同じディレクトリに置くのは、相対パスの参照
    (画像・分割CSSなど)を壊さないため。
    """
    src = open(path, encoding='utf-8').read()
    probe = PROBE_JS.replace('__BAD__', BAD_BULLETS)
    inject = f'<div id="dgs-deck-probe"></div>\n<script>{probe}</script>\n'
    if '</body>' in src:
        doc = src.replace('</body>', inject + '</body>', 1)
    else:
        doc = src + inject
    tmp = os.path.join(os.path.dirname(os.path.abspath(path)),
                       '.verify_deck_tmp.html')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(doc)

    def cleanup():
        if keep:
            print(f'   (計測用HTML: {tmp})')
        elif os.path.exists(tmp):
            os.remove(tmp)

    if not os.path.exists(CHROME):
        cleanup()
        sys.exit(f'NG: Google Chrome が見つからない: {CHROME}')
    proc = subprocess.run(
        [CHROME, '--headless', '--disable-gpu', '--no-sandbox',
         '--hide-scrollbars', '--force-device-scale-factor=1',
         '--window-size=1400,1000', '--virtual-time-budget=20000',
         '--dump-dom', f'file://{tmp}'],
        capture_output=True, text=True, timeout=300)
    m = re.search(r'<div id="dgs-deck-probe"([^>]*)>', proc.stdout)
    if not m or 'data-done="1"' not in m.group(1):
        cleanup()
        sys.exit('NG: 描画による計測ができなかった。HTMLが壊れている可能性がある。\n'
                 + (proc.stderr or '')[:600])
    data = json.loads(base64.b64decode(
        re.search(r'data-json="([^"]*)"', m.group(1)).group(1)).decode('utf-8'))
    cleanup()
    return data


def norm_hex(h):
    h = h.lower().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return '#' + h[:6]


def palette(paths):
    """design_system.md / template_base.html から許容色を集める。"""
    allowed = set()
    for p in paths:
        if os.path.exists(p):
            allowed |= {norm_hex(h) for h in
                        re.findall(r'#[0-9A-Fa-f]{3,8}\b', open(p, encoding='utf-8').read())}
    allowed |= {'#ffffff', '#000000'}
    return allowed


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('deck')
    ap.add_argument('--design', default=os.path.join(ROOT, 'references', 'design_system.md'))
    ap.add_argument('--template', default=os.path.join(ROOT, 'assets', 'template_base.html'))
    ap.add_argument('--json')
    ap.add_argument('--keep', action='store_true')
    args = ap.parse_args()

    if not os.path.exists(args.deck):
        sys.exit(f'NG: 検査対象が存在しない: {args.deck}')
    doc = open(args.deck, encoding='utf-8').read()

    err, warn = [], []
    slides = render(args.deck, keep=args.keep)
    if not slides:
        sys.exit(f'NG: {args.deck} に .slide が1枚も無い。デッキではない可能性がある。')

    # ---------- A. スライド寸法 ----------
    for s in slides:
        if (s['w'], s['h']) != (SLIDE_W, SLIDE_H):
            err.append(f"[寸法] スライド{s['i']}: {s['w']}×{s['h']}px "
                       f'（{SLIDE_W}×{SLIDE_H}px でない）')

    # ---------- B. 分量超過(無言の切り捨て) ----------
    for s in slides:
        for c in s['clip']:
            axis = '縦' if c['axis'] == 'y' else '横'
            err.append(f"[分量超過] スライド{s['i']}: {c['sel']} が{axis}に "
                       f"{c['over']}px はみ出し、**無言で切り落とされている**"
                       f"（枠 {c['h']}px / 必要 {c['need']}px）。"
                       '行数を減らすか、スライドを分割する。')

    # ---------- C. ページ番号 ----------
    nums = []
    for s in slides:
        fr = s['footerRight']
        if fr is None:
            if s['kind'] == 'page':
                err.append(f"[ページ番号] スライド{s['i']}: page-footer が無い"
                           '（表紙・章扉以外はページ番号を入れる）')
            continue
        m = re.fullmatch(r'P\.\s*(\d+)', fr)
        if not m:
            err.append(f"[ページ番号] スライド{s['i']}: フッター右が \"{fr}\" で "
                       '`P.<数字>` 形式でない')
            continue
        nums.append((s['i'], int(m.group(1))))
    if nums:
        seq = [n for _, n in nums]
        dup = sorted({n for n in seq if seq.count(n) > 1})
        if dup:
            err.append(f'[ページ番号] 重複している番号がある: {dup}')
        gaps = [(a, b) for (_, a), (_, b) in zip(nums, nums[1:]) if b != a + 1]
        if gaps:
            err.append(f'[ページ番号] 連番が飛ぶ／逆行している: '
                       + ' / '.join(f'P.{a} の次が P.{b}' for a, b in gaps))
        if len(nums) > len(slides):
            err.append(f'[ページ番号] 番号{len(nums)}個に対しスライドは{len(slides)}枚')

    # ---------- D. フッター左 ----------
    lefts = {s['footerLeft'] for s in slides if s['footerLeft'] is not None}
    if len(lefts) > 1:
        err.append('[フッター] footer-left がスライドによって違う: '
                   + ' / '.join(f'"{x}"' for x in sorted(lefts)))

    # ---------- E. 箇条書き記号 ----------
    for s in slides:
        for b in s['bad']:
            err.append(f"[箇条書き] スライド{s['i']}: 先頭に記号がある \"{b['text']}\"。"
                       '記号は CSS の `―` が描くので本文に書かない。')

    # ---------- F. 配色 ----------
    allowed = palette([args.design, args.template])
    tmpl_only = set()
    if os.path.exists(args.design) and os.path.exists(args.template):
        d = {norm_hex(h) for h in re.findall(r'#[0-9A-Fa-f]{3,8}\b',
                                             open(args.design, encoding='utf-8').read())}
        t = {norm_hex(h) for h in re.findall(r'#[0-9A-Fa-f]{3,8}\b',
                                             open(args.template, encoding='utf-8').read())}
        tmpl_only = t - d
    # 図解パーツは別標準なので配色検査から外す。除外するのは2種類:
    #  (1) inject_css.py が管理する dgs-css ブロックそのもの
    #  (2) 貼り付け先で `.dgs-scope{--color-primary:…}` を上書きするテーマ変更
    #      （図解のテーマは図解標準の管轄。その配色のコントラストは
    #        diagram-parts-html 側の inject_css.py --theme が検算する）
    # 行番号を保つため、消す代わりに同じ行数の改行へ置き換える。
    def blank(m):
        return '\n' * m.group(0).count('\n')

    scan = re.sub(r'/\* ==== dgs-css BEGIN ====.*?/\* ==== dgs-css END ==== \*/',
                  blank, doc, flags=re.S)
    scan = re.sub(r'[^{}]*\.dgs-scope[^{}]*\{[^{}]*\}', blank, scan)
    used = {}
    for m in re.finditer(r'#[0-9A-Fa-f]{3,8}\b', scan):
        used.setdefault(norm_hex(m.group(0)), set()).add(
            scan[:m.start()].count('\n') + 1)
    unknown = {c: sorted(v)[:4] for c, v in used.items() if c not in allowed}
    if unknown:
        err.append('[配色] design_system.md にも template_base.html にも無い色がある: '
                   + ' / '.join(f'{c}(行{",".join(map(str, ln))})'
                                for c, ln in sorted(unknown.items())))
    if tmpl_only:
        warn.append('template_base.html にあるが design_system.md に載っていない色: '
                    + ' '.join(sorted(tmpl_only))
                    + '（デッキ側では許容しているが、design_system.md に追記すべき）')

    # ---------- 結果 ----------
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump({'slides': slides, 'errors': err, 'warnings': warn},
                      f, ensure_ascii=False, indent=1)

    kinds = {}
    for s in slides:
        kinds[s['kind']] = kinds.get(s['kind'], 0) + 1
    print(f"対象: {args.deck}")
    print(f"  スライド {len(slides)}枚（"
          + ' / '.join(f'{k} {v}' for k, v in sorted(kinds.items()))
          + f"） ページ番号 {len(nums)}個"
          + (f"（P.{nums[0][1]}〜P.{nums[-1][1]}）" if nums else ''))

    if warn:
        print('WARN(不良ではないが要確認):')
        for w in warn:
            print(' ', w)
    if err:
        print('NG:')
        for e in err:
            print(' ', e)
        sys.exit(1)
    print(f'OK {args.deck}: 検査6項目すべて通過'
          '（図解パーツは ../diagram-parts-html/scripts/verify_html.py で別途検査する）'
          + (f' （WARN {len(warn)}件）' if warn else ''))


if __name__ == '__main__':
    main()
