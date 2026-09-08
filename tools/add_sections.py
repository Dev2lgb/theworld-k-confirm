# -*- coding: utf-8 -*-
"""원본 문서에 빠져 있던 내용을 같은 서식으로 덧붙인다.

transform.py 가 입력 요소로 바꾸기 전에 끼워 넣으므로, 여기 쓰는 마크업은
원본 문서와 똑같은 형식이어야 한다. 체크박스·서술칸·표 빈칸은 자동으로
입력 요소가 되고, 글자 크기와 여백도 build.py 에서 함께 조정된다.
"""

# ── 원본에서 쓰는 서식 조각 ──
TD  = ('text-align:left;font-weight:400;padding:7px 10px;'
       'border-bottom:1px solid oklch(0.87 0.008 60);'
       'border-right:1px solid oklch(0.87 0.008 60);vertical-align:top;')
TD_LAST = ('text-align:left;font-weight:400;padding:7px 10px;'
           'border-bottom:1px solid oklch(0.87 0.008 60);vertical-align:top;height:26px')
SERIF = "font-family:'Nanum Myeongjo',serif;"
BOX = ('break-inside:avoid;margin:13px 0 15px;padding:12px 16px 11px;'
       'background:oklch(0.973 0.010 55);border-left:2px solid oklch(0.45 0.10 35)')
DOT = ('<span style="flex:none;width:4px;height:4px;background:oklch(0.45 0.10 35);'
       'border-radius:50%;transform:translateY(-3px)"></span>')
CBOX = ('<span style="flex:none;display:inline-block;width:12px;height:12px;'
        'border:1px solid oklch(0.63 0.012 60);border-radius:1px;'
        'transform:translateY(2px)"></span>')


def p(text):
    return f'<p style="margin:0 0 9px;">{text}</p>\n'


def sub(text):
    return (f'<div style="{SERIF}font-weight:700;font-size:10.8pt;'
            f'color:oklch(0.26 0.008 60);margin:16px 0 7px">{text}</div>\n')


def bullets(items):
    rows = ''.join(
        f'<div style="display:flex;gap:10px;align-items:baseline">{DOT}'
        f'<span>{x}</span></div>' for x in items)
    return ('<div style="display:flex;flex-direction:column;gap:6px;'
            f'margin:10px 0 13px;break-inside:avoid">{rows}</div>\n')


def think(paras):
    inner = ''.join(f'<p style="margin:0 0 6px">{x}</p>' for x in paras)
    return (f'<div style="{BOX}"><div style="{SERIF}font-weight:700;font-size:9pt;'
            'letter-spacing:0.06em;color:oklch(0.45 0.10 35);margin-bottom:6px">저희 생각</div>'
            f'<div style="font-size:10.1pt">{inner}</div></div>\n')


def options(items):
    rows = ''.join(
        '<div style="display:flex;flex-wrap:wrap;gap:5px 20px;align-items:baseline">'
        '<span style="display:inline-flex;align-items:baseline;gap:7px">'
        f'{CBOX}<span>{x}</span></span></div>' for x in items)
    return ('<div style="display:flex;flex-direction:column;gap:6px;margin:12px 0 14px;'
            f'break-inside:avoid;padding-left:2px">{rows}</div>\n')


def writein(lines=3):
    rule = '<div style="border-bottom:1px solid oklch(0.87 0.008 60);height:27px"></div>'
    return ('<div style="break-inside:avoid;margin:12px 0 20px">'
            '<div style="font-size:9pt;letter-spacing:0.02em;color:oklch(0.50 0.012 60);'
            'margin-bottom:8px">적어 주실 내용</div>' + rule * lines + '</div>\n')


def table_row(no, name, use):
    return (f'<sc-raw-tr><sc-raw-td style="{TD}">{no}</sc-raw-td>'
            f'<sc-raw-td style="{TD}">{name}</sc-raw-td>'
            f'<sc-raw-td style="{TD}">{use}</sc-raw-td>'
            f'<sc-raw-td style="{TD_LAST}"></sc-raw-td></sc-raw-tr>')


def add_sections(body):
    """10장에 종목 안내 문구 항목을 넣는다."""

    # 1) 자료 목록 표에 한 줄 추가
    anchor = '홈페이지 하단과 각종 서류에 넣습니다</sc-raw-td>'
    at = body.find(anchor)
    assert at != -1, '자료 목록 표의 마지막 줄을 찾지 못했습니다'
    end = body.find('</sc-raw-tr>', at) + len('</sc-raw-tr>')
    body = body[:end] + table_row(
        14,
        '종목 안내 문구 (종목마다 어떤 자격인지, 누가 듣는지, 무엇을 배우는지)',
        '신청 전에 보시는 종목 안내 화면과 신청 화면에 넣습니다') + body[end:]

    # 2) 덧붙이는 말씀 끝에 설명 추가
    a2 = body.find('<p style="margin:0 0 9px;">13. 기관 정보')
    assert a2 != -1, '13. 기관 정보 문단을 찾지 못했습니다'
    e2 = body.find('</p>', a2) + 4

    block = (
        p('<b>14. 종목 안내 문구</b> 주신 문서에는 종목 이름과 번호만 있습니다. '
          'K-산업문화교육기술자격이 어떤 자격인지, K-직장적응자격은 무엇인지에 대한 설명이 없습니다.')
        + p('신청하시는 분은 이 설명을 읽고 어느 종목을 고를지 정하십니다. '
            '설명이 없으면 신청 화면에 종목 이름만 놓이게 되고, 처음 오신 분은 '
            '무엇을 신청하는지 모르는 채 수강료를 넣으시게 됩니다.')
        + think([
            '종목마다 아래 내용을 한두 문단씩 적어 주시면, 저희가 안내 화면을 만들어 드리겠습니다. '
            '문장을 다듬는 일은 저희가 하겠으니, 내용만 알려 주셔도 됩니다.',
            '2-7에서 말씀드린 대로 나중에 종목을 새로 만드실 수 있게 하는데, 그때도 '
            '아래 내용을 넣는 칸을 함께 두겠습니다.',
        ])
        + sub('종목마다 알려 주실 내용')
        + bullets([
            '어떤 자격인지 한 줄 설명',
            '누가 들으면 좋은지 (대상)',
            '무엇을 배우는지 (수업 내용)',
            '수업 시간과 방식 (15시간, 주말 이틀)',
            '이 자격을 따면 무엇을 할 수 있는지',
            '수강료와 자격증 발급수수료',
            '시험 방법과 합격 기준',
        ])
        + options([
            '동의 — 종목마다 위 내용을 정리해서 드리겠습니다',
            '변경 — 저희(개발사)가 초안을 만들어 드리면 고쳐 주시겠습니다',
            '변경 — 기타',
        ])
        + writein()
    )
    return body[:e2] + '\n' + block + body[e2:]
