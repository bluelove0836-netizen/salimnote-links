# OpenAI Efficiency Playbook

Sources reviewed:

- OpenAI Cookbook: `Prompt_Caching_201.ipynb`
- OpenAI Cookbook: `agents_sdk/session_memory.ipynb`
- OpenAI Cookbook: `gpt-5/gpt-5_prompting_guide.ipynb`
- OpenAI Python SDK response parameter docs for `previous_response_id`, `prompt_cache_key`, `prompt_cache_options`, `parallel_tool_calls`, `service_tier`, and `reasoning`

## Operating Rules

1. Keep stable instructions at the beginning.

   Long-lived rules, brand rules, format rules, tool schemas, and output schemas should stay byte-stable and consistently ordered. Product data, URLs, current price, campaign status, and user-request specifics go near the end.

2. Use small variables instead of rewriting prompts.

   For repeat production, keep one stable prompt template and pass only a compact product payload:

   - `product_name`
   - `product_url`
   - `curator_url`
   - `price_text`
   - `promo_text`
   - `usage_angle`
   - `proof_points`
   - `cta_target`

3. Prefer structured outputs.

   Reels, card news, captions, hashtags, and upload packages should be generated as JSON or a fixed markdown schema. This reduces retries and makes validation deterministic.

4. Choose reasoning effort by task.

   Use low or medium reasoning for routine caption variants, product filtering, title cleanup, and templated scene generation. Use higher reasoning only for strategy, new format design, legal-risk review, or source interpretation.

5. Measure and preserve cacheability.

   Prompt caching benefits repeated prefixes. Stable prefixes over 1024 tokens can reduce latency and input-token cost. Avoid timestamps, product-specific data, or changing notes in the prefix; put dynamic metadata in metadata or at the end.

6. Use `prompt_cache_key` for repeated workflows.

   For an API implementation, use stable cache keys such as:

   - `salimnote:reel-template:v1`
   - `salimnote:cardnews-template:v1`
   - `salimnote:caption-template:v1`

   Keep key granularity specific enough that unrelated workflows do not compete, but broad enough to reuse the same template.

7. Use Responses API state for multi-turn pipelines.

   When generating multi-step assets through the OpenAI API, prefer Responses API with `previous_response_id` so the model can reuse prior state instead of resending the whole chain every time.

8. Trim noisy context, summarize durable decisions.

   For long production threads, keep:

   - durable channel rules
   - selected product facts
   - approved visual direction
   - final links
   - generated asset paths

   Drop or summarize:

   - failed experiments
   - verbose scrape output
   - repeated tool logs
   - stale candidate lists

9. Keep tool surfaces narrow.

   Use only the tools needed for the step. In an API implementation, define the full stable tool list once, then restrict per request with tool choice or allowed tools rather than changing the tool schema.

10. Use batch or flex-style processing for low-urgency bulk work.

    Bulk caption variants, product scoring, and batch script generation do not need interactive latency. Save the expensive model calls for the creative decisions that actually matter.

## Salimnote Application

For Salimnote content generation, the efficient workflow is:

1. Refresh product facts from `live-products.json`.
2. Select candidates with code, not an LLM.
3. Send only 3-5 shortlisted products to the model.
4. Use one stable Salimnote reel prompt.
5. Ask for structured JSON with scenes, overlay text, caption, first comment, and link target.
6. Render locally with cached image/video assets.
7. Validate dimensions and duration with `ffprobe`.
8. Upload only after the output matches the Salimnote reel rules.

This keeps OpenAI calls focused on creative judgment instead of data cleaning.
