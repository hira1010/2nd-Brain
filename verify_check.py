import os

d = 'c:/Users/hirak/Desktop/2nd-Brain/18_レミ投資漫画/マンガノ/01_長編_希望の投資/01_ストーリー'
out = 'c:/Users/hirak/Desktop/2nd-Brain/verify_result.txt'
ep5 = sorted([f for f in os.listdir(d) if f.endswith('.md') and '.5_' in f])
themes = ['未来年表','複利','ドルコスト平均法','逆張り','長期投資','分散投資','配当貴族','FIRE']

with open(out, 'w', encoding='utf-8') as o:
    o.write(f'EPxx.5 files: {len(ep5)}\n')
    for f in ep5:
        o.write(f'  {f}\n')
    o.write('\n')

    for f in ep5:
        fp = os.path.join(d, f)
        with open(fp, 'r', encoding='utf-8-sig', errors='replace') as fh:
            c = fh.read()
        o.write(f'--- {f} ---\n')
        o.write(f'  KW: {"OK" if "キーワード枠" in c else "NG"}\n')
        o.write(f'  YT: {"OK" if "優斗の成長" in c else "NG"}\n')
        o.write(f'  TN: {"OK" if "田中の対比" in c else "NG"}\n')
        found = [t for t in themes if t in c]
        o.write(f'  TH: {found}\n')
        o.write(f'  RM: {"OK" if "レミの解説" in c else "NG"}\n\n')
