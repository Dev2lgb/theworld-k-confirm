# -*- coding: utf-8 -*-
import json, os, sys
S = sys.argv[1]
OUT = sys.argv[2]
body = open(os.path.join(S,'body.html'), encoding='utf-8').read()

PAPER = '<p style="margin:0 0 9px;">□ 안에 ∨ 표시를 하시거나, 동그라미를 쳐 주시면 됩니다. 전화로 말씀해 주셔도 됩니다.</p>'
WEB = ('<p style="margin:0 0 9px;">네모 칸을 눌러 표시하시고, 빈칸에는 바로 적으시면 됩니다. '
       '적으신 내용은 이 브라우저에 자동으로 저장되니, 중간에 창을 닫으셨다가 이어서 하셔도 됩니다.</p>'
       '<p style="margin:0 0 9px;">다 적으신 뒤 화면 위쪽 <b>답변 파일 저장</b>을 누르시면 답변이 파일 하나로 '
       '내려받아집니다. 그 파일을 메일이나 메신저로 보내 주십시오. 전화로 말씀해 주셔도 됩니다.</p>')
assert PAPER in body, '안내문을 찾지 못했습니다'
body = body.replace(PAPER, WEB)
fields = json.load(open(os.path.join(S,'fields.json'), encoding='utf-8'))

ACCENT = 'oklch(0.45 0.10 35)'
INK    = 'oklch(0.26 0.008 60)'

head = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>K-자격 수강신청 관리 시스템 확인 요청서</title>
<meta name="description" content="사단법인 더월드 — K-자격 수강신청 관리 전산시스템 구축 확인 요청서">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Nanum+Myeongjo:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%238a3f2b'/%3E%3Cpath d='M9 16.5l4.5 4.5L23 11.5' stroke='%23fff' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<style>
:root{
  --accent: oklch(0.45 0.10 35);
  --accent-soft: oklch(0.973 0.010 55);
  --ink: oklch(0.26 0.008 60);
  --muted: oklch(0.50 0.012 60);
  --line: oklch(0.87 0.008 60);
  --paper: #fdfcfa;
  --bg: oklch(0.955 0.008 60);
  --ok: oklch(0.52 0.11 155);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'IBM Plex Sans KR',-apple-system,BlinkMacSystemFont,'Malgun Gothic',sans-serif;
  font-size:10.4pt;line-height:1.72;letter-spacing:-0.01em}

/* ── 상단 바 ── */
.bar{position:sticky;top:0;z-index:50;background:rgba(253,252,250,.94);
  backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--line)}
.bar-in{max-width:860px;margin:0 auto;padding:9px 20px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.brand{font-family:'Nanum Myeongjo',serif;font-weight:800;font-size:11.5pt;letter-spacing:-.02em;
  margin-right:auto;display:flex;align-items:center;gap:9px;min-width:0}
.brand b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dot{flex:none;width:8px;height:8px;border-radius:50%;background:var(--accent)}
.prog{display:flex;align-items:center;gap:9px;font-size:9pt;color:var(--muted);white-space:nowrap}
.track{width:110px;height:5px;border-radius:3px;background:var(--line);overflow:hidden}
.fill{height:100%;width:0;background:var(--accent);transition:width .35s ease}
.btn{font:inherit;font-size:9pt;font-weight:500;padding:6px 13px;border-radius:6px;
  border:1px solid var(--line);background:#fff;color:var(--ink);cursor:pointer;white-space:nowrap;
  transition:background .15s,border-color .15s}
.btn:hover{background:var(--accent-soft);border-color:var(--accent)}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn.primary:hover{filter:brightness(1.08)}
.saved{font-size:8.5pt;color:var(--ok);opacity:0;transition:opacity .3s;white-space:nowrap}
.saved.on{opacity:1}

/* ── 장 이동 ── */
.nav{max-width:860px;margin:0 auto;padding:0 20px 9px;display:flex;gap:6px;overflow-x:auto;
  scrollbar-width:thin}
.nav a{flex:none;font-size:8.5pt;text-decoration:none;color:var(--muted);padding:4px 10px;
  border:1px solid var(--line);border-radius:20px;background:#fff;transition:.15s}
.nav a:hover{border-color:var(--accent);color:var(--accent)}
.nav a.done{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);font-weight:500}
.nav a i{font-style:normal;opacity:.65;font-size:7.8pt;margin-left:4px}

/* ── 종이 ── */
.page{max-width:860px;margin:22px auto 60px;background:var(--paper);padding:46px 52px 60px;
  border:1px solid var(--line);border-radius:3px;box-shadow:0 1px 3px rgba(80,50,35,.06)}

/* ── 작성자 ── */
.who{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px 18px;
  margin:0 0 30px;padding:16px 18px;background:var(--accent-soft);
  border-left:2px solid var(--accent);border-radius:0 3px 3px 0}
.who label{display:block;font-size:8.6pt;letter-spacing:.02em;color:var(--accent);
  font-weight:600;margin-bottom:5px}
.who input{width:100%;font:inherit;font-size:10pt;padding:6px 9px;border:1px solid var(--line);
  border-radius:4px;background:#fff;color:var(--ink)}
.who input:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:transparent}

/* ── 선택지 ── */
.opt{display:inline-flex;align-items:flex-start;gap:9px;cursor:pointer;padding:3px 7px 3px 4px;
  margin:-3px 0 -3px -4px;border-radius:5px;transition:background .13s;-webkit-tap-highlight-color:transparent}
.opt:hover{background:var(--accent-soft)}
.opt input{flex:none;appearance:none;-webkit-appearance:none;margin:0;width:15px;height:15px;
  border:1.5px solid oklch(0.63 0.012 60);border-radius:3px;background:#fff;cursor:pointer;
  position:relative;transform:translateY(3px);transition:.13s}
.opt input:hover{border-color:var(--accent)}
.opt input:checked{background:var(--accent);border-color:var(--accent)}
.opt input:checked::after{content:'';position:absolute;left:4.4px;top:1.4px;width:4px;height:8px;
  border:solid #fff;border-width:0 2px 2px 0;transform:rotate(43deg)}
.opt input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.opt input:checked~.opt-t{font-weight:600;color:var(--accent)}
.opt-t{transition:.13s}

/* ── 서술 입력 ── */
.wi{break-inside:avoid;margin:12px 0 22px}
.wi-l{display:block;font-size:9pt;letter-spacing:.02em;color:var(--muted);margin-bottom:7px}
.f-ta{width:100%;font:inherit;font-size:10.1pt;line-height:1.7;padding:10px 12px;
  border:1px solid var(--line);border-radius:5px;background:#fff;color:var(--ink);
  resize:vertical;min-height:62px;transition:border-color .15s,box-shadow .15s}
.f-ta::placeholder{color:oklch(0.72 0.008 60)}
.f-ta:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px oklch(0.45 0.10 35/.11)}
.f-ta.has{background:var(--accent-soft);border-color:oklch(0.75 0.04 40)}

h2,h3{scroll-margin-top:112px}

/* ── 표 ── */
.tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0 18px}
.tbl-wrap sc-raw-table{margin:0;min-width:420px}
sc-raw-table{display:table;width:100%;border-collapse:collapse;margin:14px 0 18px;font-size:9.6pt}
sc-raw-thead{display:table-header-group}
sc-raw-tbody{display:table-row-group}
sc-raw-tr{display:table-row}
sc-raw-th,sc-raw-td{display:table-cell}
.td-in{padding:0!important}
.f-in{width:100%;font:inherit;font-size:9.6pt;padding:7px 10px;border:0;background:transparent;
  color:var(--ink);border-radius:0}
.f-in:focus{outline:none;background:#fff;box-shadow:inset 0 0 0 2px var(--accent)}
.f-in.has{background:var(--accent-soft);font-weight:500}
.f-in::placeholder{color:oklch(0.78 0.008 60);font-size:8.8pt}
.td-in{background:repeating-linear-gradient(-45deg,transparent,transparent 6px,oklch(0.45 0.10 35/.045) 6px,oklch(0.45 0.10 35/.045) 12px)}
.td-in:has(.f-in.has){background:none}

/* ── 하단 ── */
.end{max-width:860px;margin:0 auto 70px;padding:26px 30px;background:var(--paper);
  border:1px solid var(--line);border-radius:3px;text-align:center}
.end h4{font-family:'Nanum Myeongjo',serif;font-size:13pt;font-weight:800;margin:0 0 8px}
.end p{color:var(--muted);font-size:9.5pt;margin:0 0 18px;line-height:1.7}
.end-btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.end .btn{font-size:10pt;padding:10px 22px}

/* ── 모바일 ── */
@media (max-width:760px){
  body{font-size:10.8pt}
  .page{margin:14px 0 40px;padding:26px 20px 44px;border-left:0;border-right:0;border-radius:0}
  .end{margin:0 12px 44px;padding:22px 18px}
  .bar-in{padding:7px 14px;gap:8px}
  .brand{font-size:10pt;flex:1 1 auto;min-width:0}
  .brand b{font-size:9.6pt}
  .prog{order:3;flex:1 1 100%;gap:7px;font-size:8.2pt;margin-top:-2px}
  .track{flex:1 1 auto;width:auto}
  .btn{padding:5px 10px;font-size:8.4pt}
  .btn .long{display:none}
  .saved{order:4;font-size:8pt}
  .nav{padding:0 14px 7px}
  .nav a{font-size:8pt;padding:3px 9px}
  h2,h3{scroll-margin-top:146px}
  sc-raw-table{font-size:8.8pt}
  .f-in{font-size:8.8pt;padding:6px}
  sc-raw-th,sc-raw-td{padding:6px 7px!important}
}

/* ── 인쇄 ── */
@media print{
  @page{size:A4;margin:16mm}
  body{background:#fff;font-size:10pt}
  .bar,.nav,.end,.no-print{display:none!important}
  .page{max-width:none;margin:0;padding:0;border:0;box-shadow:none;background:#fff}
  .opt input{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .f-ta,.f-in{border-color:#ccc}
  .who{background:#f7f4f1;-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>
</head>
<body>
<div class="bar no-print">
  <div class="bar-in">
    <div class="brand"><span class="dot"></span><b>K-자격 확인 요청서</b></div>
    <div class="prog"><div class="track"><div class="fill" id="fill"></div></div><span id="ptext">0 / 0</span></div>
    <span class="saved" id="saved">자동 저장됨</span>
    <button class="btn" id="btn-load">불러<span class="long">오기</span></button>
    <button class="btn" id="btn-print">인쇄</button>
    <button class="btn primary" id="btn-save"><span class="long">답변 파일 </span>저장</button>
  </div>
  <div class="nav" id="nav"></div>
</div>

<div class="page">
<div class="who no-print">
  <div><label for="_name">작성하신 분 성함</label><input id="_name" type="text" placeholder="예: 홍길동"></div>
  <div><label for="_org">소속 · 직위</label><input id="_org" type="text" placeholder="예: 사단법인 더월드 사무국장"></div>
  <div><label for="_tel">연락처</label><input id="_tel" type="text" placeholder="예: 010-0000-0000"></div>
</div>
'''

tail_tpl = '''
</div>

<div class="end no-print">
  <h4>다 적으셨으면</h4>
  <p>아래 <b>답변 파일 저장</b>을 누르시면 답변이 파일 하나로 내려받아집니다.<br>
     그 파일을 메일이나 메신저로 보내 주시면 됩니다.<br>
     작성하신 내용은 이 브라우저에 자동으로 저장되니, 중간에 닫으셨다가 이어서 하셔도 됩니다.</p>
  <div class="end-btns">
    <button class="btn" onclick="window.print()">인쇄 / PDF로 저장</button>
    <button class="btn primary" onclick="saveFile()">답변 파일 저장</button>
  </div>
</div>

<input type="file" id="filein" accept=".json,application/json" hidden>

<script>
const FIELDS = __FIELDS__;
const KEY = 'kjagyeok-confirm-v1';
const META = ['_name','_org','_tel'];
const byQ = {};
FIELDS.forEach(f => { (byQ[f.q] = byQ[f.q] || []).push(f); });

/* ── 상태 읽고 쓰기 ── */
function collect(){
  const d = { meta:{}, answers:{}, savedAt:new Date().toISOString() };
  META.forEach(k => { const e=document.getElementById(k); if(e) d.meta[k]=e.value; });
  FIELDS.forEach(f => {
    const e = document.getElementById(f.id); if(!e) return;
    const v = f.type==='check' ? e.checked : e.value;
    if (v === true || (typeof v==='string' && v.trim())) d.answers[f.id] = v;
  });
  return d;
}
function apply(d){
  if(!d) return;
  META.forEach(k => { const e=document.getElementById(k); if(e && d.meta && d.meta[k]!=null) e.value=d.meta[k]; });
  FIELDS.forEach(f => {
    const e = document.getElementById(f.id); if(!e) return;
    const v = d.answers ? d.answers[f.id] : undefined;
    if (f.type==='check') e.checked = v===true;
    else e.value = (typeof v==='string') ? v : '';
  });
  refresh();
}

/* ── 자동 저장 ── */
let t = null;
const savedEl = document.getElementById('saved');
function autosave(){
  clearTimeout(t);
  t = setTimeout(() => {
    try { localStorage.setItem(KEY, JSON.stringify(collect())); } catch(e){}
    savedEl.classList.add('on');
    setTimeout(()=>savedEl.classList.remove('on'), 1600);
  }, 420);
}

/* ── 진행률 ── */
function answered(q){
  return byQ[q].some(f => {
    const e = document.getElementById(f.id); if(!e) return false;
    return f.type==='check' ? e.checked : e.value.trim() !== '';
  });
}
function refresh(){
  const qs = Object.keys(byQ);
  const n = qs.filter(answered).length;
  document.getElementById('fill').style.width = (qs.length ? n/qs.length*100 : 0) + '%';
  document.getElementById('ptext').textContent = n + ' / ' + qs.length + ' 문항';
  document.querySelectorAll('[data-nav]').forEach(a => {
    const ch = a.dataset.nav;
    const cqs = qs.filter(q => byQ[q][0].ch === ch);
    const cn = cqs.filter(answered).length;
    a.querySelector('i').textContent = cn + '/' + cqs.length;
    a.classList.toggle('done', cn > 0 && cn === cqs.length);
  });
  FIELDS.forEach(f => {
    if (f.type==='check') return;
    const e = document.getElementById(f.id); if(e) e.classList.toggle('has', e.value.trim()!=='');
  });
}

/* ── 장 이동 ── */
(function(){
  const nav = document.getElementById('nav');
  const seen = [];
  FIELDS.forEach(f => { if (f.ch && !seen.includes(f.ch)) seen.push(f.ch); });
  seen.forEach(ch => {
    const a = document.createElement('a');
    a.href = '#ch-' + ch; a.dataset.nav = ch;
    a.innerHTML = ch + '장 <i></i>';
    nav.appendChild(a);
  });
})();

/* ── 파일 저장 / 불러오기 ── */
function summaryText(d){
  const L = ['K-자격 수강신청 관리 시스템 확인 요청서 — 답변',
             '작성: ' + (d.meta._name||'') + ' ' + (d.meta._org||'') + ' ' + (d.meta._tel||''),
             '저장: ' + new Date(d.savedAt).toLocaleString('ko-KR'), ''];
  let ch = null, q = null;
  FIELDS.forEach(f => {
    const v = d.answers[f.id]; if (v===undefined) return;
    if (f.ch !== ch){ ch = f.ch; L.push('', '── ' + ch + '장 ' + f.chTitle + ' ──'); q=null; }
    if (f.q !== q){ q = f.q; L.push('', '[' + f.q + '] ' + f.qTitle); }
    L.push(f.type==='check' ? '  ☑ ' + f.label : '  ▸ ' + String(v).replace(/\\n/g,'\\n    '));
  });
  return L.join('\\n');
}
function saveFile(){
  const d = collect();
  d.summary = summaryText(d);
  d.document = 'K-자격 수강신청 관리 시스템 확인 요청서';
  const who = (d.meta._name||'답변').replace(/[^가-힣A-Za-z0-9]/g,'') || '답변';
  const dt = new Date();
  const stamp = dt.getFullYear() + String(dt.getMonth()+1).padStart(2,'0') + String(dt.getDate()).padStart(2,'0');
  const blob = new Blob([JSON.stringify(d, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'K자격_확인요청서_' + who + '_' + stamp + '.json';
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 1200);
}
document.getElementById('btn-save').addEventListener('click', saveFile);
document.getElementById('btn-print').addEventListener('click', ()=>window.print());
document.getElementById('btn-load').addEventListener('click', ()=>document.getElementById('filein').click());
document.getElementById('filein').addEventListener('change', function(){
  const f = this.files[0]; if(!f) return;
  const r = new FileReader();
  r.onload = () => {
    try { apply(JSON.parse(r.result)); autosave(); alert('불러왔습니다.'); }
    catch(e){ alert('파일을 읽지 못했습니다. 저장한 json 파일이 맞는지 확인해 주십시오.'); }
  };
  r.readAsText(f); this.value = '';
});

/* ── 표 가로 스크롤 래핑 · 입력칸 안내 ── */
(function(){
  document.querySelectorAll('sc-raw-table').forEach(t => {
    const w = document.createElement('div'); w.className = 'tbl-wrap';
    t.parentNode.insertBefore(w, t); w.appendChild(t);
    const heads = [...t.querySelectorAll('sc-raw-thead sc-raw-th')].map(h => h.textContent.trim());
    t.querySelectorAll('sc-raw-tbody sc-raw-tr').forEach(tr => {
      [...tr.children].forEach((td, i) => {
        const inp = td.querySelector('.f-in');
        if (inp && heads[i]) inp.placeholder = heads[i];
      });
    });
  });
})();

/* ── 초기화 ── */
document.addEventListener('input', e => { if(e.target.matches('.f-ta,.f-in,.who input')){ refresh(); autosave(); }});
document.addEventListener('change', e => { if(e.target.matches('.f-cb')){ refresh(); autosave(); }});
try { const raw = localStorage.getItem(KEY); if(raw) apply(JSON.parse(raw)); } catch(e){}
refresh();
window.addEventListener('beforeunload', () => { try{ localStorage.setItem(KEY, JSON.stringify(collect())); }catch(e){} });
</script>
</body>
</html>
'''

slim = [{'id':f['id'],'ch':f['ch'],'chTitle':f['chTitle'],'q':f['q'],
         'qTitle':f['qTitle'],'type':f['type'],'label':f['label']} for f in fields]
tail = tail_tpl.replace('__FIELDS__', json.dumps(slim, ensure_ascii=False, separators=(',',':')))

open(OUT,'w',encoding='utf-8').write(head + body + tail)
print("생성:", OUT, f"{os.path.getsize(OUT):,} bytes")
