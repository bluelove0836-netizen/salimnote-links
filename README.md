# salimnote-links

GitHub Pages source for the Salimnote Instagram bio link page.

## Data files

- `products.json`: exhibition product source list
- `curator-links.json`: curator links that are ready to expose
- `live-products.json`: synced product snapshot with current title, price, promo copy, and change detection

When a product gets a curator link, add the matching `id` and `curatorUrl` to `curator-links.json`.

## Refresh flow

- Run `python3 scripts/refresh_live_products.py` to sync current product title, price, and promo text from Ohouse product pages.
- GitHub Actions also refreshes `live-products.json` every 6 hours via `.github/workflows/refresh-live-products.yml`.
