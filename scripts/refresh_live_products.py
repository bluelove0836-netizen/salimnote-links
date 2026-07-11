#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "products.json"
CURATOR_PATH = ROOT / "curator-links.json"
LIVE_PATH = ROOT / "live-products.json"

TITLE_RE = re.compile(r'<meta property="og:title" content="([^"]+)"')
DESC_RE = re.compile(r'<meta property="og:description" content="([^"]+)"')
PRICE_RE = re.compile(r'<meta property="product:price:amount" content="([^"]+)"')
IMAGE_RE = re.compile(r'<meta property="og:image" content="([^"]+)"')

PROMO_KEYWORDS = (
    "브랜드위크",
    "쿠폰",
    "단하루",
    "특가",
    "사은품",
    "추가적립",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def money_text(amount: int | None) -> str:
    if amount is None:
        return ""
    return f"{amount:,}원"


def detect_campaign_badges(title: str, description: str) -> list[str]:
    source = f"{title} {description}"
    badges: list[str] = []
    for keyword in PROMO_KEYWORDS:
        if keyword in source and keyword not in badges:
            badges.append(keyword)
    return badges


def guess_category(name: str) -> str:
    if re.search(r"(식탁|식기|접시|파스타볼|그릇|테이블|에어프라이어|밥솥|주방|쿡웨어)", name):
        return "kitchen"
    if re.search(r"(트롤리|정리함|수납|행거|바구니|압축|박스|틈새|선반)", name):
        return "storage"
    if re.search(r"(청소기|세탁|세제|건조대|건조기|빨래|키친타월|휴지|화장지)", name):
        return "cleaning"
    return "living"


def parse_meta(html: str, pattern: re.Pattern[str]) -> str:
    match = pattern.search(html)
    if not match:
        return ""
    return unescape(match.group(1)).strip()


def fetch_product(product: dict[str, Any], curator_lookup: dict[str, dict[str, Any]]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [
                "curl",
                "-L",
                "-s",
                "--max-time",
                "20",
                product["url"],
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        html = result.stdout
        if not html:
            raise RuntimeError("empty response")
    except Exception as exc:
        return {
            "id": str(product["id"]),
            "url": product["url"],
            "name": product["name"],
            "currentName": product["name"],
            "currentPrice": None,
            "priceText": "",
            "promoText": "",
            "imageUrl": "",
            "category": guess_category(product["name"]),
            "campaignBadges": [],
            "isCampaign": False,
            "hasCuratorLink": str(product["id"]) in curator_lookup,
            "curatorUrl": curator_lookup.get(str(product["id"]), {}).get("curatorUrl", ""),
            "linkNote": curator_lookup.get(str(product["id"]), {}).get("note", ""),
            "syncError": str(exc),
        }

    current_name = parse_meta(html, TITLE_RE) or product["name"]
    promo_text = parse_meta(html, DESC_RE)
    price_raw = parse_meta(html, PRICE_RE)
    image_url = parse_meta(html, IMAGE_RE)
    price_amount = int(price_raw) if price_raw.isdigit() else None
    badges = detect_campaign_badges(current_name, promo_text)

    return {
        "id": str(product["id"]),
        "url": product["url"],
        "name": product["name"],
        "currentName": current_name,
        "currentPrice": price_amount,
        "priceText": money_text(price_amount),
        "promoText": promo_text,
        "imageUrl": image_url,
        "category": guess_category(current_name),
        "campaignBadges": badges,
        "isCampaign": bool(badges),
        "hasCuratorLink": str(product["id"]) in curator_lookup,
        "curatorUrl": curator_lookup.get(str(product["id"]), {}).get("curatorUrl", ""),
        "linkNote": curator_lookup.get(str(product["id"]), {}).get("note", ""),
        "syncError": "",
    }


def load_previous_items() -> dict[str, dict[str, Any]]:
    if not LIVE_PATH.exists():
        return {}
    data = load_json(LIVE_PATH)
    items = data.get("items", []) if isinstance(data, dict) else []
    return {str(item["id"]): item for item in items}


def main() -> None:
    products = load_json(PRODUCTS_PATH)
    curator_links = load_json(CURATOR_PATH)
    curator_lookup = {str(item["id"]): item for item in curator_links}
    previous_items = load_previous_items()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    items: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(fetch_product, product, curator_lookup)
            for product in products
        ]
        for future in as_completed(futures):
            items.append(future.result())

    items.sort(key=lambda item: int(item["id"]))

    changed_count = 0
    for item in items:
        previous = previous_items.get(item["id"])
        changed_fields: list[str] = []
        if previous:
            has_previous_live_data = any(
                previous.get(field) not in ("", None, [])
                for field in ("currentPrice", "promoText", "imageUrl")
            )
            for field in ("currentName", "currentPrice", "promoText"):
                if has_previous_live_data and previous.get(field) != item.get(field):
                    changed_fields.append(field)
        item["changedFields"] = changed_fields
        item["changeDetected"] = bool(changed_fields)
        item["syncedAt"] = now
        if changed_fields:
            changed_count += 1

    payload = {
        "meta": {
            "generatedAt": now,
            "sourceCount": len(products),
            "campaignCount": sum(1 for item in items if item["isCampaign"]),
            "curatorLinkedCount": sum(1 for item in items if item["hasCuratorLink"]),
            "changedCount": changed_count,
        },
        "items": items,
    }
    LIVE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
