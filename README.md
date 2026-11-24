# news-image-20261124-v1

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sanschiko3-dotcom/news-image-20261124-v1/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/sanschiko3-dotcom/news-image-20261124-v1/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124).

## What it is

A photo-led front page, **"THE WORLD TODAY — Tuesday, 24 November 2026"**, drawn with Pillow at build time (`render.py`) and shipped as `entry.png`. The entry program `main.py` (Python 3.13, standard library only) copies that image to `/output/entry.png` — no network, fully deterministic.

Four stories lead the page:

1. **LEAD** — Sea drone hits a Russian corvette off Benghazi, Libya.
2. **CLIMATE** — COP31 collapses: 90+ nations reject a draft with no "fossil fuels".
3. **SECURITY** — NATO: 25 airspace violations in 2026; debris falls in Poland, 20 Nov.
4. **MARKETS** — Huang back as NVIDIA CEO; Nasdaq +6.51%.

Plus an "Also today" strip: US–Iran (Treasury sanctions, Qatar mediates), Rohingya at the ICJ (14 states back the case), and the Nepal quake (magnitude 5.6).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB, byte-identical on every run
```

## License

MIT — see [LICENSE](LICENSE).
