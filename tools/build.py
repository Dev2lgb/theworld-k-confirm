# -*- coding: utf-8 -*-
"""본문(body.html) + 틀(head/tail) -> 배포용 index.html"""
import json, os, re, sys

S   = sys.argv[1]                       # 작업 디렉터리
OUT = sys.argv[2]                       # 출력 파일
HERE = os.path.dirname(os.path.abspath(__file__))

body   = open(os.path.join(S, 'body.html'), encoding='utf-8').read()
fields = json.load(open(os.path.join(S, 'fields.json'), encoding='utf-8'))
head   = open(os.path.join(HERE, 'head.html'), encoding='utf-8').read()
tail   = open(os.path.join(HERE, 'tail.html'), encoding='utf-8').read()

# 종이 서식용 안내문을 웹 안내문으로 교체
PAPER = ('<p style="margin:0 0 9px;">\u25a1 \uc548\uc5d0 \u2228 \ud45c\uc2dc\ub97c \ud558\uc2dc\uac70\ub098, '
         '\ub3d9\uadf8\ub77c\ubbf8\ub97c \uccd0 \uc8fc\uc2dc\uba74 \ub429\ub2c8\ub2e4. '
         '\uc804\ud654\ub85c \ub9d0\uc500\ud574 \uc8fc\uc154\ub3c4 \ub429\ub2c8\ub2e4.</p>')
WEB = ('<p style="margin:0 0 9px;">네모 칸을 눌러 표시하시고, 빈칸에는 바로 적으시면 됩니다. '
       '적으시는 대로 자동으로 저장되니, 중간에 창을 닫으셨다가 이어서 하셔도 됩니다.</p>'
       '<p style="margin:0 0 9px;">다 적으신 뒤 따로 보내실 것은 없습니다. 저희가 화면에서 바로 확인합니다. '
       '전화로 말씀해 주셔도 됩니다.</p>')
assert PAPER in body, '안내문을 찾지 못했습니다'
body = body.replace(PAPER, WEB)

# ── 본문 인라인 스타일: 폰트 교체 + 크기 1.2배 ──
SCALE = 1.2

def _n(v, unit):
    x = round(float(v) * SCALE, 2)
    x = int(x) if x == int(x) else x
    return f'{x}{unit}'

# 명조/IBM 지정을 공통 폰트 변수로
body = body.replace("font-family:'Nanum Myeongjo',serif", 'font-family:var(--ff)')
body = body.replace("font-family:'IBM Plex Sans KR',sans-serif", 'font-family:var(--ff)')

# 글자 크기(pt)
body = re.sub(r'font-size:([\d.]+)pt', lambda m: 'font-size:' + _n(m.group(1), 'pt'), body)

# 여백(margin/padding/gap)의 px 값
def _spacing(m):
    prop, val = m.group(1), m.group(2)
    return prop + ':' + re.sub(r'([\d.]+)px', lambda k: _n(k.group(1), 'px'), val)
body = re.sub(r'(margin[a-z-]*|padding[a-z-]*|gap):([^;"]*)', _spacing, body)

# 표 빈 칸 높이
body = re.sub(r'height:26px', 'height:' + _n('26', 'px'), body)

slim = [{k: f[k] for k in ('id','ch','chTitle','q','qTitle','type','label')} for f in fields]
tail = tail.replace('__FIELDS__', json.dumps(slim, ensure_ascii=False, separators=(',', ':')))

open(OUT, 'w', encoding='utf-8').write(head + body + tail)
print('생성:', OUT, f'{os.path.getsize(OUT):,} bytes')
