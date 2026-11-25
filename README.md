# news-image-20261125 — The World in One Page

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/DavidQlla06/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/DavidQlla06/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun competition
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
sum up the world's news of Wednesday 25 November 2026 in one image.

## The image

A newspaper front page, drawn entirely in code (`generate.py`, Pillow):

- **Lead story:** Nvidia chief Jensen Huang apologises to staff and says he is in therapy, a day after the board voted him back in as CEO; shares jumped 31.5% on Monday.
- **World map** with 13 numbered pins: China's purge of Shanghai party chief Chen Jining, the Houthi strike on Riyadh's PIF Tower, Putin's retaliation warning, NATO early-warning jets for Poland, tankers mined in the Strait of Hormuz, the Gaza strike, North Korea's Swiss-office threat, the BJP–Akali reunion, India's Nepal package, the UK hosting the 2035 Women's World Cup, England's T20 win in Australia, and South Korea's minister resigning over an exam scandal.
- **12 briefs + a 6-item ticker** covering Huawei's trade-secret verdict, the chip-smuggling crackdown, Waymo's freeway pullback, Anthropic's slide below its IPO price, Bitcoin under $57,000, the Sensex drop, Priyansh Arya's 181, Sooryavanshi's 28-ball hundred, Babar Azam's ILT20 debut, Gukesh's title match, an asteroid eclipse, and Denmark's "ghetto" evictions ruling.

## How to run

```sh
python3 generate.py   # writes entry.png (1024x1024, deterministic)
python3 main.py       # same, then copies it to /output/entry.png
```

`generate.py` reads `stories.json` and draws the page with Pillow. `main.py` runs it and copies the PNG to `/output/entry.png`.
