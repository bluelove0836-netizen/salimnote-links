# Salimnote Reels Rules

This file is the gate for Salimnote reels. Read it before generating or publishing any reel.

## Channel Role

- Account: `@sa.lim_note`
- Rail: home, housekeeping, living, Today의집 affiliate
- Core feeling: natural home-use review, not a product detail page
- Default: silent-first video with on-screen text and caption

## Non-Negotiables

1. The reel must feel like a real-use review.

   Use natural usage scenes, routine moments, before/after context, and lived-in home framing. Do not make a static discount ranking video.

2. Product facts are support, not the story.

   Price, discount, coupon, and campaign language can explain urgency, but the reel must first answer: "Why would this be useful in my home?"

3. Use one main product or one coherent use case.

   A multi-product reel is allowed only when all products support one routine, such as bathroom reset, pantry cleanup, table refresh, laundry corner, or entryway cleanup.

4. Link guidance must be natural.

   Use wording like:

   - `프로필 링크에 같이 정리해둘게요`
   - `기획전 링크에서 한 번에 볼 수 있어요`
   - `저장해두고 필요할 때 확인해보세요`

   Avoid making the whole video a link announcement.

5. Affiliate disclosure is mandatory.

   Caption must include:

   `※ 제휴/큐레이터 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다.`

6. Do not invent specs.

   Only use facts from product page metadata, official title, synced price/promo text, or verified detail page content. If a fact is uncertain, omit it.

7. Do not overclaim.

   Avoid words like "무조건", "완벽", "역대급" unless the official source says it. Prefer soft review language: `편한 편`, `보기 좋았어요`, `손이 자주 갈 타입`, `확인해볼 만해요`.

## Reel Structure

Target length: 18-28 seconds.

Scene 1: Hook, 0-3s

- Real home problem or desire
- No product-detail-page framing
- Example: `식탁은 멀쩡한데 분위기만 애매할 때`

Scene 2: Real Use, 3-8s

- Show the product in a believable home moment
- Use close-up or hand interaction when possible

Scene 3: Difference, 8-14s

- Explain one or two practical differentiators
- Examples: wipe-clean, reversible color, custom cut, narrow-space storage, washable, easier routine

Scene 4: Why Now, 14-20s

- Mention campaign, coupon, price, or limited timing only as urgency
- Keep it tied to use: `어차피 바꿀 거면 행사할 때 보는 게 낫죠`

Scene 5: CTA, final 3-5s

- Save and profile-link cue
- No hard-sell language

## Visual Rules

- Use lifestyle or realistic use scenes first.
- Product page images can be used as reference or insert, but not as the whole style.
- Avoid pure text cards unless they are intercut with real-use visuals.
- Keep text short: 1-2 lines per scene.
- Use large readable Korean text and enough safe margins for Reels UI.
- Prefer warm, clean, lightly lived-in Korean home visuals.

## Script Template

```json
{
  "hook": "집에서 겪는 구체적인 불편",
  "product_role": "이 제품이 해결하는 한 가지 역할",
  "usage_scenes": [
    "실사용 장면 1",
    "실사용 장면 2",
    "차별점 장면",
    "지금 살 이유 장면",
    "CTA 장면"
  ],
  "overlay_text": [
    "짧은 훅",
    "실사용 한 줄",
    "차별점 한 줄",
    "행사/쿠폰 한 줄",
    "프로필 링크 유도"
  ],
  "caption": "6-8줄 해요체 본문",
  "first_comment": "프로필 링크/기획전 안내",
  "hashtags": ["12개"]
}
```

## Candidate Selection

For an exhibition-based reel:

1. Filter from `live-products.json`.
2. Prefer household categories over food-only or unrelated items.
3. Rank by a mix of:

   - high discount or coupon
   - strong home-use scene potential
   - clear practical difference
   - available curator/exhibition link

4. Choose one primary product when possible.
5. If using several products, group them by one routine instead of ranking them.

## Rejection Checklist

Reject and remake the reel if:

- It is mostly a discount list.
- It looks like product-detail-page screenshots stitched together.
- It has no natural use scene.
- It introduces unverified claims.
- It drives the link before giving a reason to care.
- It mixes unrelated categories without a single household routine.
