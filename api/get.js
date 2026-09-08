import { list } from '@vercel/blob';

const ID = /^[a-z0-9]{6,40}$/;

export default async function handler(req, res) {
  const id = String(req.query?.id || '').toLowerCase();
  if (!ID.test(id)) return res.status(400).json({ error: '문서 번호가 올바르지 않습니다' });
  try {
    const { blobs } = await list({ prefix: `answers/${id}.json`, limit: 1 });
    const hit = blobs.find(b => b.pathname === `answers/${id}.json`);
    if (!hit) { res.setHeader('Cache-Control', 'no-store');
                return res.status(200).json({ empty: true }); }
    const r = await fetch(hit.url, { cache: 'no-store' });
    if (!r.ok) throw new Error('blob ' + r.status);
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json(await r.json());
  } catch (e) {
    return res.status(500).json({ error: '불러오지 못했습니다', detail: String(e?.message || e) });
  }
}
