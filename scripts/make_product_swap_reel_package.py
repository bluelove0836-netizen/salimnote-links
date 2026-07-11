#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LIVE_PRODUCTS = ROOT / "live-products.json"
CURATOR_LINKS = ROOT / "curator-links.json"
OUT_ROOT = ROOT / "reels" / "product-swap"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    normalized = re.sub(r"[^0-9A-Za-z가-힣]+", "-", text).strip("-")
    return normalized[:48] or "product"


def short_name(name: str) -> str:
    cleaned = re.sub(r"\[[^\]]+\]", "", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    for token in (" 테이블보", " 테이블 매트", " 모음전", " 외 "):
        if token in cleaned:
            cleaned = cleaned.split(token, 1)[0].strip()
    if len(cleaned) <= 32:
        return cleaned
    return cleaned[:32].rstrip() + "..."


def prompt_subject(name: str) -> str:
    if re.search(r"식탁보|테이블보|테이블 매트|식탁", name):
        return "a beige waterproof leather tablecloth on a wooden dining table"
    if re.search(r"발매트|규조토|욕실", name):
        return "a washable semicircle diatomite bath mat in front of a bathroom door"
    if re.search(r"트롤리", name):
        return "a slim rolling storage trolley in a Korean kitchen"
    if re.search(r"선반|랙", name):
        return "a metal storage shelf organizing pantry items on a balcony"
    if re.search(r"청소기", name):
        return "a cordless vacuum cleaner being used on a small apartment floor"
    if re.search(r"휴지통", name):
        return "a clean automatic trash bin in a kitchen corner"
    return "the household product being used naturally at home"


def infer_angle(name: str) -> dict[str, str]:
    if re.search(r"식탁보|테이블보|테이블 매트|식탁", name):
        return {
            "problem": "식탁은 멀쩡한데 상판 생활감이 안 가려지는 상황",
            "result_hook": "식탁 분위기 이걸로 바로 바뀌었어요",
            "use_motion": "손으로 식탁보를 펼치고 모서리를 맞추는 장면",
            "difference": "물자국은 닦아내고 양면 컬러로 분위기를 바꾸는 장면",
            "why_now": "식탁 리폼 고민 중이면 행사할 때 확인해볼 만한 타이밍",
        }
    if re.search(r"발매트|규조토|욕실", name):
        return {
            "problem": "욕실 앞 발매트가 금방 축축해지고 보기 싫어지는 상황",
            "result_hook": "욕실 앞 분위기 이걸로 정리됐어요",
            "use_motion": "샤워 후 발을 디디고 매트가 놓인 욕실 앞을 보여주는 장면",
            "difference": "빨아쓰는 소재와 반원형 오브제 느낌을 보여주는 장면",
            "why_now": "욕실 분위기 바꾸려던 분들이 확인해볼 만한 타이밍",
        }
    if re.search(r"트롤리|선반|랙|수납|정리함", name):
        return {
            "problem": "주방이나 베란다 물건이 바닥에 자꾸 쌓이는 상황",
            "result_hook": "바닥에 쌓이던 물건이 한 번에 정리됐어요",
            "use_motion": "자주 쓰는 물건을 선반이나 트롤리에 올려 정리하는 장면",
            "difference": "좁은 틈새나 팬트리에 맞춰 수납되는 장면",
            "why_now": "정리 시작하려던 분들이 행사할 때 보기 좋은 타이밍",
        }
    if re.search(r"청소기|먼지|휴지통", name):
        return {
            "problem": "바닥 먼지나 생활 쓰레기가 자꾸 신경 쓰이는 상황",
            "result_hook": "집안일 시간이 조금 줄어든 느낌이에요",
            "use_motion": "손으로 제품을 들고 바닥이나 생활 공간을 정리하는 장면",
            "difference": "귀찮은 동작을 줄여주는 사용 흐름을 보여주는 장면",
            "why_now": "청소 루틴 바꾸려던 분들이 쿠폰 있을 때 확인할 타이밍",
        }
    return {
        "problem": "집에서 자주 겪는 작은 불편을 해결하고 싶은 상황",
        "result_hook": "이거 하나로 집안일이 조금 편해졌어요",
        "use_motion": "손으로 제품을 꺼내 실제 생활 공간에서 사용하는 장면",
        "difference": "제품의 핵심 차별점을 가까운 장면으로 보여주는 컷",
        "why_now": "필요했던 제품이라면 행사할 때 확인해볼 만한 타이밍",
    }


def build_video_prompts(product: dict[str, Any], angle: dict[str, str]) -> list[dict[str, str]]:
    name = short_name(product["currentName"])
    subject = prompt_subject(product["currentName"])
    base_style = (
        "vertical smartphone video, Korean apartment home, realistic handheld footage, "
        "natural indoor light, ordinary lived-in home, no logo, no watermark, no text in image"
    )
    return [
        {
            "scene": "result_hook",
            "duration": "0-2s",
            "overlay": "이거 하나로\n일이 줄었어요",
            "prompt": f"{base_style}, show {subject} already improving the home scene, close product and hand interaction, result-first demo",
        },
        {
            "scene": "problem",
            "duration": "2-5s",
            "overlay": "맨날 이게\n거슬렸는데",
            "prompt": f"{base_style}, before shot of {angle['problem']}, close-up of the annoying everyday problem, slightly imperfect real home texture",
        },
        {
            "scene": "use_motion",
            "duration": "5-10s",
            "overlay": "그냥 이렇게\n쓰면 끝",
            "prompt": f"{base_style}, {subject}, clear hand movement, {angle['use_motion']}, product visible, practical demonstration",
        },
        {
            "scene": "difference",
            "duration": "10-15s",
            "overlay": "좋았던 건\n이 부분",
            "prompt": f"{base_style}, {angle['difference']}, close-up proof shot, slow handheld motion, product feature shown naturally",
        },
        {
            "scene": "cta",
            "duration": "15-20s",
            "overlay": "필요하면\n저장해두세요",
            "prompt": f"{base_style}, final tidy home result after using {subject}, calm satisfying after shot, product still visible but not salesy",
        },
    ]


def build_caption(product: dict[str, Any], angle: dict[str, str], link_target: str) -> str:
    name = short_name(product["currentName"])
    promo_line = ""
    if product.get("priceText") and product.get("promoText"):
        promo_line = f"\n판매처 표기 기준으로는 지금 {product['promoText']}라 확인해볼 만해요.\n"

    return (
        f"[살림노트] {angle['problem']} 있죠.\n\n"
        f"{name}는 실제로 쓰는 장면으로 보면\n"
        f"{angle['use_motion']} 흐름이라 손이 가는 타입이에요.\n"
        f"{promo_line}\n"
        f"{angle['difference']} 점도 보기 좋았고,\n"
        f"{angle['why_now']}이에요.\n\n"
        f"{link_target}는 프로필 링크에 같이 정리해둘게요.\n\n"
        "※ 제휴/큐레이터 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_id")
    parser.add_argument("--cta-target", default="제품/기획전 링크")
    args = parser.parse_args()

    live = load_json(LIVE_PRODUCTS)
    curator_links = {str(item["id"]): item for item in load_json(CURATOR_LINKS)}
    product = next((item for item in live["items"] if str(item["id"]) == str(args.product_id)), None)
    if not product:
        raise SystemExit(f"Product not found: {args.product_id}")

    linked = curator_links.get(str(product["id"]))
    if linked:
        product["curatorUrl"] = linked["curatorUrl"]
        product["hasCuratorLink"] = True

    angle = infer_angle(product["currentName"])
    prompts = build_video_prompts(product, angle)
    link = product.get("curatorUrl") or product.get("url")
    package = {
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "template": "reference-product-swap-v1",
        "product": {
            "id": product["id"],
            "name": product["currentName"],
            "url": product["url"],
            "link": link,
            "priceText": product.get("priceText", ""),
            "promoText": product.get("promoText", ""),
            "imageUrl": product.get("imageUrl", ""),
        },
        "angle": angle,
        "videoPrompts": prompts,
        "caption": build_caption(product, angle, args.cta_target),
        "firstComment": f"{args.cta_target}는 프로필 링크에서 확인할 수 있어요 :)\n\n{link}",
        "hashtags": [
            "살림노트",
            "살림템추천",
            "오늘의집추천",
            "생활용품추천",
            "주방살림",
            "정리수납",
            "집꾸미기",
            "살림꿀템",
            "신혼살림",
            "원룸살림",
            "인테리어소품",
            "제휴링크",
        ],
    }

    out_dir = OUT_ROOT / f"{product['id']}-{slugify(product['currentName'])}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "package.json").write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# {package['product']['name']} 릴스 패키지",
        "",
        "## 구조",
        "",
        "- 템플릿: reference-product-swap-v1",
        "- 형식: 실사용 데모형 릴스",
        "- 길이: 12-20초",
        "- 링크: " + package["product"]["link"],
        "",
        "## 장면별 생성 프롬프트",
        "",
    ]
    for idx, item in enumerate(prompts, start=1):
        lines.extend([
            f"### {idx}. {item['scene']} ({item['duration']})",
            "",
            f"- 자막: `{item['overlay']}`",
            f"- 프롬프트: {item['prompt']}",
            "",
        ])
    lines.extend([
        "## 본문",
        "",
        package["caption"],
        "",
        "## 첫 댓글",
        "",
        package["firstComment"],
        "",
        "## 해시태그",
        "",
        " ".join("#" + tag for tag in package["hashtags"]),
        "",
    ])
    (out_dir / "reel-package.md").write_text("\n".join(lines), encoding="utf-8")
    print(out_dir)


if __name__ == "__main__":
    main()
