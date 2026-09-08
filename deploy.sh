#!/usr/bin/env bash
# Vercel 배포 — npx vercel login 을 마친 뒤 실행
set -e
npx --yes vercel@latest link --yes --project theworld-k-confirm
npx --yes vercel@latest blob store add answers || echo "Blob 저장소가 이미 있으면 넘어갑니다"
npx --yes vercel@latest env pull .env.local || true
npx --yes vercel@latest deploy --prod --yes
