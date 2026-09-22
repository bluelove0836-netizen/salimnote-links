#!/usr/bin/env python3
"""Add cloud-reviewed, published Salimnote reels to the product link page."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
IG_ROOT = Path(os.environ.get("SALIMNOTE_IG_ROOT", "/Users/sso/orca/projects/인스타그램"))
QUEUE = IG_ROOT / "data/reels-queue.json"
MANUAL = ROOT / "manual-products.json"

# Curated mapping keeps duplicate Instagram revisions on one product card.
PRODUCTS = {
    "coupang-tnine-lint-remover-tn3000": {
        "id": "coupang-tnine-lint-remover-tn3000",
        "name": "티나인 보풀제거기 TN-3000",
        "promoText": "같은 니트의 양쪽을 비교한 제조사 시연. 옷감별 사용 방법은 제품 설명서에서 확인하세요.",
        "category": "cleaning",
        "frame_second": 3.7,
    },
    "coupang-1662710143": {
        "id": "coupang-sothing-zero-shoe-dryer",
        "name": "소싱 제로 신발 건조기 DSHJ-S-1904",
        "promoText": "운동화 안쪽에 넣어 쓰는 제조사 시연. 신발 소재별 사용 가능 여부와 시간은 설명서에서 확인하세요.",
        "category": "living",
        "frame_second": 4.2,
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def eligible(row: dict) -> tuple[dict, Path] | None:
    spec = PRODUCTS.get(row.get("productId"))
    review = row.get("qualityReview") or {}
    if not spec or row.get("status") != "published" or not row.get("publishedAt"):
        return None
    if review.get("status") != "passed" or not (review.get("verdict") or {}).get("passed"):
        return None
    if review.get("engine") not in {"codex", "claude", "gemini"} or not row.get("link"):
        return None
    asset = review.get("asset") or ""
    if not asset.startswith(f"reviewed-{row['id']}-") or not asset.endswith(".mp4"):
        return None
    video = IG_ROOT / ".cache/reels" / row["id"] / asset
    if not video.is_file() or sha256(video) != review.get("videoSha256"):
        return None
    return spec, video


def sync() -> int:
    rows = json.loads(QUEUE.read_text())["items"]
    selected = {}
    for row in rows:
        candidate = eligible(row)
        if candidate:
            spec, video = candidate
            key = spec["id"]
            if key not in selected or row["publishedAt"] > selected[key][0]["publishedAt"]:
                selected[key] = (row, spec, video)
    data = json.loads(MANUAL.read_text())
    items = data["items"]
    existing = {item["id"]: item for item in items}
    changed = 0
    for key, (row, spec, video) in selected.items():
        old = existing.get(key, {})
        thumb = ROOT / "assets" / f"{key}-thumbnail.jpg"
        video_hash = sha256(video)
        if (old.get("sourceVideoSha256") != video_hash
                or old.get("thumbnailFrameSecond") != spec["frame_second"]
                or not thumb.is_file()):
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error", "-ss", str(spec["frame_second"]),
                "-i", str(video), "-frames:v", "1", "-vf", "scale=480:-1", str(thumb),
            ], check=True, timeout=30)
        affiliate_source = spec.get("affiliateSource", old.get("source", "coupang"))
        affiliate_url = spec.get("affiliateUrl") or (old.get("url") if affiliate_source == "naver_connect" else row["link"])
        if affiliate_source == "naver_connect" and not spec.get("affiliateChannelVerified"):
            raise ValueError(f"Naver Connect channel ownership is not verified for {key}")
        if affiliate_source == "naver_connect" and not affiliate_url:
            raise ValueError(f"Missing verified Naver Connect link for {key}")
        updated = dict(old, id=key, url=affiliate_url, curatorUrl=affiliate_url,
                       hasCuratorLink=True, name=spec["name"], currentName=spec["name"],
                       promoText=spec["promoText"], category=spec["category"],
                       imageUrl=f"./assets/{thumb.name}", imageSha256=sha256(thumb),
                       imageSourceUrl=(row.get("sourceUrls") or [""])[0],
                       imageLicense="살림노트가 편집·검수한 제조사 시연 영상 프레임",
                       source=affiliate_source, linkNote="살림노트 영상 속 제품",
                       instagramPosted=True, postType="reel", publishedAt=row["publishedAt"],
                       sourceVideoSha256=video_hash,
                       thumbnailFrameSecond=spec["frame_second"], correctionPending=False)
        if updated != old:
            if old:
                old.clear()
                old.update(updated)
            else:
                items.append(updated)
            changed += 1
    if changed:
        MANUAL.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"eligible_products": len(selected), "changed_products": changed}, ensure_ascii=False))
    return changed


if __name__ == "__main__":
    sync()
