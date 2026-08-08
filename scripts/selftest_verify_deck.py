# -*- coding: utf-8 -*-
"""verify_deck.py の各検査が「壊れた入力を実際に止める」ことを確認する自己テスト。

使い方:
    python3 scripts/selftest_verify_deck.py [正常なデッキ.html]

    引数を省略した場合の既定: ../../サンプル/demo-次世代POSシステム刷新プロジェクト.html

なぜ必要か:
- 検査は**両方向**で確かめないと意味がない。
  「壊れた入力が止まること」と「正常な入力が通ること」の両方。
  実際に、検査していないものを「検査する」と書いてしまう事故が起きている。
  検査を1つ足したら、ここに壊し方を1つ足す。

やること:
  正常なデッキを1箇所ずつ壊した複製を作り、verify_deck.py が
  exit 1 になり、かつ該当タグ（[分量超過] など）を出すことを確認する。
  最後に、元の正常なデッキが exit 0 で通ることを確認する。
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LAB = os.path.dirname(os.path.dirname(ROOT))
VERIFY = os.path.join(HERE, 'verify_deck.py')
DEFAULT_DECK = os.path.join(LAB, 'サンプル', 'demo-次世代POSシステム刷新プロジェクト.html')


def mut_overflow(s):
    """表の行を大量に増やし、page-body から無言で切り落とされる状態を作る。"""
    m = re.search(r'(<tr>(?:(?!</tr>).)*?</tr>)\s*</tbody>', s, re.S)
    return s[:m.end(1)] + m.group(1) * 14 + s[m.end(1):]


def mut_pagenum(s):
    """ページ番号を1つ飛ばす。"""
    return s.replace('class="right">P.7<', 'class="right">P.9<', 1)


def mut_footer(s):
    """2枚目のフッター左を別の文字列にする。"""
    i = s.find('class="left"')
    j = s.find('class="left"', i + 1)
    k = s.find('>', j) + 1
    return s[:k] + '別プロジェクト' + s[s.find('<', k):]


def mut_bullet(s):
    """デッキ本体の箇条書き先頭に `・` を書く（CSSの `―` と二重になる）。"""
    m = re.search(r'<div class="block-body">\s*<ul>\s*<li>', s)
    return s[:m.end()] + '・' + s[m.end():]


def mut_color(s):
    """design_system.md に無い色を足す。"""
    return s.replace('</style>', '  .invented { color: #FF00AA; }\n</style>', 1)


def mut_size(s):
    """スライドの高さを 720px から変える。"""
    return s.replace('</style>', '  .slide { height: 700px; }\n</style>', 1)


CASES = [
    ('分量超過', mut_overflow, '[分量超過]'),
    ('ページ番号', mut_pagenum, '[ページ番号]'),
    ('フッター', mut_footer, '[フッター]'),
    ('箇条書き', mut_bullet, '[箇条書き]'),
    ('配色', mut_color, '[配色]'),
    ('寸法', mut_size, '[寸法]'),
]


def main():
    deck = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DECK
    if not os.path.exists(deck):
        sys.exit(f'NG: 検査に使う正常なデッキが無い: {deck}\n'
                 '    正常に通ることが分かっているデッキを引数で渡す。')
    src = open(deck, encoding='utf-8').read()
    outdir = os.path.dirname(os.path.abspath(deck))
    ok = True

    for name, fn, tag in CASES:
        path = os.path.join(outdir, f'.selftest_{name}.html')
        try:
            broken = fn(src)
        except Exception as e:  # 壊し方が対象デッキの構造に合っていない
            print(f'FAIL  {name:<6} 壊した複製を作れない（{e}）。'
                  'このデッキには該当構造が無い可能性がある。')
            ok = False
            continue
        if broken == src:
            print(f'FAIL  {name:<6} 壊した複製が元と同一。壊し方が効いていない。')
            ok = False
            continue
        open(path, 'w', encoding='utf-8').write(broken)
        r = subprocess.run([sys.executable, VERIFY, path], capture_output=True, text=True)
        os.remove(path)
        hit = tag in r.stdout
        good = r.returncode == 1 and hit
        print(f'{"PASS" if good else "FAIL"}  {name:<6} exit={r.returncode} '
              f'{tag}を検出={hit}')
        if not good:
            print('      ' + r.stdout.strip().replace('\n', '\n      ')[:500])
            ok = False

    r = subprocess.run([sys.executable, VERIFY, deck], capture_output=True, text=True)
    good = r.returncode == 0
    print(f'{"PASS" if good else "FAIL"}  正常系  exit={r.returncode}'
          + ('' if good else '  ← 誤検知。正常なデッキを止めている。'))
    if not good:
        print('      ' + r.stdout.strip().replace('\n', '\n      ')[:800])

    if ok and good:
        print(f'\nOK selftest: 検査{len(CASES)}項目すべてが壊れた入力を止め、'
              '正常な入力を通した')
        return
    sys.exit(1)


if __name__ == '__main__':
    main()
