import { put } from '@vercel/blob';

const MAX = 400 * 1024;              // 답변 한 건 최대 400KB
const ID = /^[a-z0-9]{6,40}$/;

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST 만 받습니다' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: '본문이 json 이 아닙니다' });

  const id = String(body.id || '').toLowerCase();
  if (!ID.test(id)) return res.status(400).json({ error: '문서 번호가 올바르지 않습니다' });

  const record = {
    id,
    meta: {
      _name: String(body.meta?._name ?? '').slice(0, 60),
      _org:  String(body.meta?._org  ?? '').slice(0, 80),
      _tel:  String(body.meta?._tel  ?? '').slice(0, 40),
    },
    answers: {},
    done: Number(body.done) || 0,
    total: Number(body.total) || 0,
    savedAt: new Date().toISOString(),
  };

  const src = body.answers && typeof body.answers === 'object' ? body.answers : {};
  for (const [k, v] of Object.entries(src)) {
    if (!/^[0-9A-Za-z가-힣\-_장]{1,60}$/.test(k)) continue;
    if (v === true) record.answers[k] = true;
    else if (typeof v === 'string' && v.trim()) record.answers[k] = v.slice(0, 4000);
  }

  const json = JSON.stringify(record);
  if (json.length > MAX) return res.status(413).json({ error: '내용이 너무 깁니다' });

  try {
    await put(`answers/${id}.json`, json, {
      access: 'public',
      contentType: 'application/json; charset=utf-8',
      addRandomSuffix: false,
      allowOverwrite: true,
      cacheControlMaxAge: 0,
    });
    return res.status(200).json({ ok: true, savedAt: record.savedAt });
  } catch (e) {
    return res.status(500).json({ error: '저장하지 못했습니다', detail: String(e?.message || e) });
  }
}
