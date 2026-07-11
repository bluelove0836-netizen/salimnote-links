# Reference Reel Template

Use this template when the user says: "제품만 갈아끼우면서 이런 릴스".

Reference links:

- `https://www.instagram.com/reel/DZvm4bAzMRT/?igsh=aGkyNHZubHl6dnZr`
- `https://www.instagram.com/reel/DYlOfRfST6v/?igsh=MTVrYjlzbnI1aXFyNw==`
- `https://www.instagram.com/reel/DYwHXRtyEYL/?igsh=MXh0ZmFjNjVjcjk0aA==`

Observed reference pattern:

- Vertical phone-shot product demo
- Product or hand appears immediately
- Big bold Korean subtitle at the top
- Fast problem-to-solution framing
- Ordinary home setting, not polished brand ad
- One product per reel
- Result-first hook before details
- No long intro, no logo intro, no discount ranking

## Production Formula

Target length: 12-20 seconds.

Scene 1: Result Hook, 0-2s

- Show the product already solving the problem.
- Subtitle format: `이거 하나로 OO가 쉬워졌어요`
- Product must appear in the first second.

Scene 2: Problem Close-Up, 2-5s

- Show the annoying before state.
- Subtitle format: `맨날 OO 때문에 귀찮았는데`
- Use imperfect, real home texture.

Scene 3: Use Motion, 5-10s

- Show the hand using, placing, wiping, pulling, spraying, folding, or plugging the product.
- Subtitle format: `그냥 이렇게 쓰면 끝`
- This is the most important shot.

Scene 4: Difference, 10-15s

- Show the key product difference in action.
- Subtitle format: `좋았던 건 OO`
- Use only verified product facts.

Scene 5: Save/Link Cue, 15-20s

- Show final tidy result.
- Subtitle format: `필요하면 저장해두세요`
- Caption and first comment carry the affiliate disclosure and profile-link guidance.

## Caption Formula

Use a natural review tone:

```text
[살림노트] OO 때문에 은근 신경 쓰였던 분들 많죠.

이건 실제로 써보는 장면 기준으로 보면
OO할 때 손이 자주 갈 타입이에요.

특히 OO가 좋고,
OO한 집이면 확인해볼 만해요.

제품/기획전 링크는 프로필에 같이 정리해둘게요.

※ 제휴/큐레이터 활동의 일환으로 일정액의 수수료를 제공받을 수 있습니다.
```

## Text Rules

- Max 2 subtitle lines per scene.
- Keep each line under roughly 14 Korean characters where possible.
- Use thick white text with black shadow or black stroke.
- Safe area: top text must not hit Instagram UI.
- Avoid tiny product specs on-screen.

## Shot Rules

- Use real or realistic home-use footage first.
- Product page images may be used only as reference, not as the final look.
- If the source product has no usable footage, generate or film realistic usage clips before rendering.
- Do not present a static card slideshow as the final reel.

## Product Swap Variables

```json
{
  "product_id": "",
  "product_name": "",
  "product_url": "",
  "curator_url": "",
  "price_text": "",
  "promo_text": "",
  "problem": "",
  "result_hook": "",
  "use_motion": "",
  "difference": "",
  "why_now": "",
  "cta_target": ""
}
```

## Rejection Gate

Reject the output if:

- the reel can be understood without seeing the product in use
- it is mostly text cards
- it opens with a sale/discount instead of a real-life result
- it shows unrelated products together
- it feels like a product-detail-page summary
- it lacks a real hand/product interaction shot
