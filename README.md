[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Eizdy-ez/news-20-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Eizdy-ez/news-20-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# Friday 20 November 2026 — World News in One Image

Entry for the make.fun bounty
[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120)
($250, 50 places paid). The program writes one 1024×1024 PNG summing up
Friday 20 November 2026 to `/output/entry.png`.

## The image

An original editorial front page, drawn programmatically by `draw.py`
(Pillow, no photographs, no copied artwork, no network). The date is
front and centre, and six stories are each clear from their picture
and short label:

1. **Shenzhen — Three leaders, one table.** Trump, Xi and Putin meet
   and issue a joint peace pledge, their first three-way summit.
2. **Kyiv under fire.** Russia fires 400+ drones and 110 missiles at
   Ukraine; 8 killed. Two missiles land in Poland.
3. **The Hague — Genocide ruling.** The UN court (ICJ) finds Myanmar
   committed genocide against the Rohingya, a first against a state.
4. **The Gulf — Tanker ablaze.** A ship is struck in the Strait of
   Hormuz; fire aboard, no casualties. The US blockade holds; the
   exact cause is disputed.
5. **Antalya — Climate talks stall.** COP31 runs past its Friday
   deadline with no deal; the draft drops the fossil-fuel phase-out.
6. **Markets slide.** The S&P 500 falls 3.7% into correction as AI
   shares sell off around the world.

## Files

- `main.ts` — Node 22 entrypoint (standard library only). Copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
- `entry.png` — the image, 1024×1024 PNG, 106,453 bytes (under 1 MiB).
- `draw.py` — the script that draws `entry.png` from scratch.
  Re-running it reproduces the same image.
- `LICENSE` — MIT.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs write byte-identical output (verified: same sha256 both runs).
The program uses no network.
