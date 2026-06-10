# Crawler Video Playlist

A [Scrapy](https://scrapy.org/) crawler that turns a streaming web page into a playable `.m3u8` playlist.

The included spider targets [**One Pace**](https://onepace.net/en/watch): it walks every season on the watch page, extracts each episode's video file (hosted on [Pixeldrain](https://pixeldrain.com/)), and writes out a single `onepace.m3u8` playlist you can open in any player that supports M3U (VLC, mpv, etc.).

## How it works

1. **`parse`** — loads the [watch page](https://onepace.net/en/watch) and yields a request for each season's episode list.
2. **`parse_season`** — pulls the `window.viewer_data` JSON embedded in each season page, parses it into typed dataclasses ([`onepace/items.py`](onepace/items.py)), and yields one `Episode` per video file. Each Pixeldrain detail link (`/u/<id>`) is rewritten to a direct download URL (`/api/file/<id>?download`).
3. **`M3UPipeline`** ([`onepace/pipelines.py`](onepace/pipelines.py)) — collects every episode, sorts by the first number found in the filename, and writes the final `#EXTM3U` playlist to `onepace.m3u8`.

## Requirements

- Python **≥ 3.13** (see [`.python-version`](.python-version))
- [`uv`](https://docs.astral.sh/uv/) for dependency management (a `uv.lock` is committed)

## Setup

```bash
uv sync
```

This creates a `.venv` and installs Scrapy as pinned in [`uv.lock`](uv.lock).

## Usage

Run the spider from the project root:

```bash
uv run scrapy crawl onepace
```

When it finishes, the playlist is written to [`onepace.m3u8`](onepace.m3u8). Open it in your player of choice:

```bash
vlc onepace.m3u8
```

## Configuration

Crawl behavior lives in [`onepace/settings.py`](onepace/settings.py):

- **HTTP caching** is enabled and never expires (`HTTPCACHE_ENABLED`), so re-runs hit the local cache instead of the site. Delete the `.scrapy/` directory to force a fresh crawl.
- **Politeness** — AutoThrottle is on with a 1-second download delay and a cap of 4 concurrent requests per domain.

## Project layout

```
onepace/
├── items.py                 # Season / Episode + typed viewer_data dataclasses
├── pipelines.py             # M3UPipeline — builds and writes the .m3u8
├── settings.py              # Scrapy settings (cache, throttling, pipeline)
└── spider/
    └── onepace_spider.py    # The OnePace spider
scrapy.cfg                   # Scrapy project config
onepace.m3u8                 # Generated playlist (git-ignored)
```

> **Note:** `*.m3u8` and the `.scrapy/` cache are git-ignored — the playlist is a build artifact, not source.

## Disclaimer

This tool is for personal and educational use. Respect [onepace.net](https://onepace.net/)'s terms of service and the politeness settings when crawling.

---

> _This README was generated with the help of AI._
