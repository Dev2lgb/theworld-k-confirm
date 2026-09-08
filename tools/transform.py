# -*- coding: utf-8 -*-
"""K-자격 확인요청서: 정적 문서 -> 입력 가능한 웹 폼 변환기"""
import re, os, sys, json, html as htmlmod

S = sys.argv[1]
src = open(os.path.join(S, 'template.html'), encoding='utf-8').read()

# ── 본문만 추출 (폰트 @font-face 652개 제거, 구글폰트 CDN으로 대체) ──
m = re.search(r'<doc-page[^>]*>(.*)</doc-page>', src, re.S)
body = m.group(1)

# ── 이번 회차에서 빼는 문항 ──
# 번호만 적으면 그 문항 블록(제목·저희 생각·선택지·서술칸)이 통째로 빠지고,
# 같은 장의 뒷 문항 번호가 앞으로 당겨집니다. 되살리려면 목록에서 지우십시오.
DROP = {'1-1'}

def drop_questions(html, drop):
    """빼기로 한 문항 블록을 제거하고 같은 장의 번호를 다시 매긴다."""
    if not drop:
        return html
    H3 = re.compile(r'<h3[^>]*>')
    CH = re.compile(r'<div style="break-before:page;')
    NUM = re.compile(r'(<span style="color:oklch\(0\.45 0\.10 35\);margin-right:9px">)([\d\-]+)\.(</span>)')

    removed = []
    while True:
        cut = None
        for m in H3.finditer(html):
            head = html[m.start():m.start() + 400]
            nm = NUM.search(head)
            if nm and nm.group(2) in drop and nm.group(2) not in removed:
                nxt = H3.search(html, m.end())
                ch  = CH.search(html, m.end())
                ends = [x.start() for x in (nxt, ch) if x]
                cut = (m.start(), min(ends) if ends else len(html), nm.group(2))
                break
        if not cut:
            break
        removed.append(cut[2])
        html = html[:cut[0]] + html[cut[1]:]

    # 빠진 장의 번호를 다시 매긴다
    chapters = {n.split('-')[0] for n in removed}
    seq = {}
    def renum(m):
        ch = m.group(2).split('-')[0]
        if ch not in chapters:
            return m.group(0)
        seq[ch] = seq.get(ch, 0) + 1
        return f'{m.group(1)}{ch}-{seq[ch]}.{m.group(3)}'
    html = NUM.sub(renum, html)
    print('  뺀 문항:', ', '.join(removed) or '없음')
    return html

body = drop_questions(body, DROP)

fields = []          # {id, ch, q, type, label}
cur_ch = {'no': '', 'title': ''}
cur_q  = {'no': '', 'title': ''}
counters = {}

def next_id(kind):
    base = cur_q['no'] or (cur_ch['no'] + '-머리말') or '서문'
    key = f'{base}:{kind}'
    counters[key] = counters.get(key, 0) + 1
    return f'{base}_{kind}{counters[key]}'

def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

# ── 1) 장/문항 제목에 앵커와 추적 마커 삽입 ──
def on_h2(mo):
    inner = strip_tags(mo.group(2))
    cur_ch['title'] = inner
    return f'{mo.group(1)} id="ch-{cur_ch["no"]}" data-ch="{cur_ch["no"]}"{mo.group(3)}'

out = []
pos = 0
# 장 번호는 h2 앞의 "N장" 배지에서 읽는다
badge_re = re.compile(r'letter-spacing:0\.22em[^"]*">(\d+)장</div>')
h2_re    = re.compile(r'(<h2)([^>]*>)(.*?)(</h2>)', re.S)
h3_re    = re.compile(r'(<h3)([^>]*>)(.*?)(</h3>)', re.S)

# 순차 스캔용 통합 정규식
token_re = re.compile(
    r'(?P<badge>letter-spacing:0\.22em[^"]*">(?P<chno>\d+)장</div>)'
    r'|(?P<h2><h2)(?P<h2attr>[^>]*>)(?P<h2in>.*?)</h2>'
    r'|(?P<h3><h3)(?P<h3attr>[^>]*>)(?P<h3in>.*?)</h3>'
    r'|(?P<opt><span style="display:inline-flex;align-items:baseline;gap:7px">)'
    r'|(?P<wi><div style="break-inside:avoid;margin:12px 0 20px"><div style="font-size:9pt;letter-spacing:0\.02em;color:oklch\(0\.50 0\.012 60\);margin-bottom:8px">적어 주실 내용</div>)'
    r'|(?P<td><sc-raw-td style="(?P<tdstyle>[^"]*height:26px)"></sc-raw-td>)'
    r'|(?P<bl><span style="display:inline-block;border-bottom:1px solid oklch\(0\.72 0\.01 60\);'
    r'min-width:54px;height:0\.9em;vertical-align:-2px"></span>)'
    r'|(?P<ln><span style="flex:1;border-bottom:1px solid oklch\(0\.87 0\.008 60\);height:1\.35em"></span>)',
    re.S)

BLANK_RE = re.compile(
    r'<span style="(?:display:inline-block;border-bottom:1px solid oklch\(0\.72 0\.01 60\)[^"]*'
    r'|flex:1;border-bottom:1px solid oklch\(0\.87 0\.008 60\);height:1\.35em)"></span>')


def blank_label(html, at):
    """빈칸에 이름을 붙인다. 표 안이면 '줄 이름 — 칸 문구', 밖이면 바로 앞 항목 이름."""
    td = html.rfind('<sc-raw-td', 0, at)
    if td != -1 and html.find('</sc-raw-td>', td, at) == -1:
        end = html.find('</sc-raw-td>', at)
        cell = strip_tags(BLANK_RE.sub(' ○ ', html[html.find('>', td) + 1:end]))
        first = ''
        tr = html.rfind('<sc-raw-tr', 0, td)
        if tr != -1:
            m = re.search(r'<sc-raw-td[^>]*>(.*?)</sc-raw-td>', html[tr:], re.S)
            if m:
                first = strip_tags(BLANK_RE.sub(' ○ ', m.group(1)))
        label = f'{first} — {cell}' if first and first != cell else cell
        return re.sub(r'\s+', ' ', label).strip()[:70]

    prev = html.rfind('</span>', 0, at)
    lab = ''
    if prev != -1:
        st = html.rfind('<span', 0, prev)
        if st != -1:
            lab = strip_tags(html[st:prev])
    return (re.sub(r'\s+', ' ', lab).strip() or '빈칸')[:70]


def close_span(s, start):
    """start는 여는 <span ...> 의 '<' 위치. 짝이 맞는 </span> 끝 인덱스 반환."""
    depth = 0
    i = start
    tag = re.compile(r'<(/?)span\b[^>]*>', re.I)
    while True:
        mo = tag.search(s, i)
        if not mo: return -1, -1
        if mo.group(1): 
            depth -= 1
            if depth == 0: return mo.start(), mo.end()
        else:
            depth += 1
        i = mo.end()

i = 0
res = []
while True:
    mo = token_re.search(body, i)
    if not mo:
        res.append(body[i:]); break
    res.append(body[i:mo.start()])

    if mo.group('badge'):
        cur_ch['no'] = mo.group('chno')
        res.append(mo.group('badge')); i = mo.end()

    elif mo.group('h2'):
        cur_ch['title'] = strip_tags(mo.group('h2in'))
        cur_q['no'] = ''
        res.append(f'<h2 id="ch-{cur_ch["no"]}"{mo.group("h2attr")}{mo.group("h3in") if False else mo.group("h2in")}</h2>')
        i = mo.end()

    elif mo.group('h3'):
        inner = mo.group('h3in')
        num = re.match(r'\s*<span[^>]*>([^<]*?)\.?</span>', inner)
        if num:
            cur_q['no'] = num.group(1).strip().rstrip('.')
        else:
            cur_q['no'] = f'{cur_ch["no"]}장-{strip_tags(inner)[:14]}'
        _t = strip_tags(inner)
        if num: _t = _t[len(strip_tags(num.group(0))):].strip()
        cur_q['title'] = _t
        anchor = re.sub(r'[^0-9A-Za-z가-힣\-]', '_', cur_q['no'])
        res.append(f'<h3 id="q-{anchor}" data-q="{htmlmod.escape(cur_q["no"])}"{mo.group("h3attr")}{inner}</h3>')
        i = mo.end()

    elif mo.group('opt'):
        s0 = mo.start('opt')
        ce, cend = close_span(body, s0)
        block = body[s0:cend]
        label = strip_tags(re.sub(r'^.*?border-radius:1px;transform:translateY\(2px\)"></span>', '', block, flags=re.S))
        fid = next_id('선택')
        fields.append({'id': fid, 'ch': cur_ch['no'], 'chTitle': cur_ch['title'],
                       'q': cur_q['no'], 'qTitle': cur_q['title'], 'type': 'check', 'label': label})
        res.append(f'<label class="opt"><input type="checkbox" class="f-cb" id="{fid}">'
                   f'<span class="opt-t">{label}</span></label>')
        i = cend

    elif mo.group('wi'):
        # 컨테이너 끝까지: 밑줄 div들 + 닫는 </div>
        j = mo.end()
        n = 0
        while True:
            mm = re.match(r'<div style="border-bottom:1px solid oklch\(0\.87 0\.008 60\);height:27px"></div>', body[j:])
            if not mm: break
            n += 1; j += mm.end()
        assert body[j:j+6] == '</div>', body[j:j+40]
        j += 6
        fid = next_id('서술')
        fields.append({'id': fid, 'ch': cur_ch['no'], 'chTitle': cur_ch['title'],
                       'q': cur_q['no'], 'qTitle': cur_q['title'], 'type': 'text', 'label': '적어 주실 내용'})
        res.append(f'<div class="wi"><label class="wi-l" for="{fid}">적어 주실 내용</label>'
                   f'<textarea class="f-ta" id="{fid}" rows="{max(2,n)}" '
                   f'placeholder="자유롭게 적어 주십시오"></textarea></div>')
        i = j

    elif mo.group('bl'):
        fid = next_id('빈칸')
        fields.append({'id': fid, 'ch': cur_ch['no'], 'chTitle': cur_ch['title'],
                       'q': cur_q['no'], 'qTitle': cur_q['title'], 'type': 'blank',
                       'label': blank_label(body, mo.start('bl'))})
        res.append(f'<input type="text" class="f-bl" id="{fid}" inputmode="numeric" '
                   f'aria-label="{htmlmod.escape(cur_q["no"])} 빈칸">')
        i = mo.end()

    elif mo.group('ln'):
        fid = next_id('줄')
        fields.append({'id': fid, 'ch': cur_ch['no'], 'chTitle': cur_ch['title'],
                       'q': cur_q['no'], 'qTitle': cur_q['title'], 'type': 'line',
                       'label': blank_label(body, mo.start('ln'))})
        res.append(f'<input type="text" class="f-ln" id="{fid}" '
                   f'placeholder="성함 · 직위 · 연락처">')
        i = mo.end()

    elif mo.group('td'):
        fid = next_id('표')
        fields.append({'id': fid, 'ch': cur_ch['no'], 'chTitle': cur_ch['title'],
                       'q': cur_q['no'], 'qTitle': cur_q['title'], 'type': 'cell', 'label': '표 입력칸'})
        res.append(f'<sc-raw-td style="{mo.group("tdstyle")}" class="td-in">'
                   f'<input type="text" class="f-in" id="{fid}"></sc-raw-td>')
        i = mo.end()

body2 = ''.join(res)

open(os.path.join(S, 'body.html'), 'w', encoding='utf-8').write(body2)
open(os.path.join(S, 'fields.json'), 'w', encoding='utf-8').write(json.dumps(fields, ensure_ascii=False, indent=1))

from collections import Counter
print("변환 완료")
print("  필드 수:", len(fields), Counter(f['type'] for f in fields).most_common())
print("  본문 크기:", f"{len(body2):,} bytes")
print("  남은 정적 체크박스:", body2.count('border-radius:1px;transform:translateY(2px)'))
print("  남은 밑줄:", body2.count('height:27px'))
print("  남은 빈 셀:", len(re.findall(r'<sc-raw-td style="[^"]*height:26px"></sc-raw-td>', body2)))
print("  남은 인라인 빈칸:", len(re.findall(r'border-bottom:1px solid oklch\(0\.72 0\.01 60\)', body2))
      + len(re.findall(r'flex:1;border-bottom:1px solid oklch\(0\.87 0\.008 60\);height:1\.35em', body2)))
chs = sorted({f['ch'] for f in fields}, key=lambda x:(len(x),x))
print("  장:", chs)
