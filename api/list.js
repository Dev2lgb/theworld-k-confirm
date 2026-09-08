import { list } from '@vercel/blob';

export default async function handler(req, res) {
  try {
    const { blobs } = await list({ prefix: 'answers/', limit: 200 });
    const rows = await Promise.all(blobs.map(async b => {
      const id = b.pathname.replace(/^answers\//, '').replace(/\.json$/, '');
      try {
        const r = await fetch(b.url, { cache: 'no-store' });
        const d = await r.json();
        return { id, meta: d.meta || {}, done: d.done || 0, total: d.total || 0,
                 savedAt: d.savedAt || b.uploadedAt, size: b.size };
      } catch {
        return { id, meta: {}, done: 0, total: 0, savedAt: b.uploadedAt, size: b.size };
      }
    }));
    rows.sort((a, b) => String(b.savedAt).localeCompare(String(a.savedAt)));
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ rows });
  } catch (e) {
    return res.status(500).json({ error: '목록을 읽지 못했습니다', detail: String(e?.message || e) });
  }
}
