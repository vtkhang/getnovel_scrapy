"""Default settings."""

import time
from pathlib import Path

BOT_NAME = "GetNovelScrapy"
h = (Path.home() / BOT_NAME).resolve()
ROBOTSTXT_OBEY = True
SPIDER_MODULES = ["app.spiders"]
ITEM_PIPELINES = {
    "app.pipelines.Epub": 1,
    "app.pipelines.CoverImage": 2,
}
i_dir = h / "images"
i_dir.mkdir(parents=True, exist_ok=True)
IMAGES_STORE = i_dir
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
# RESULT
r_dir = h / "result"
r_dir.mkdir(parents=True, exist_ok=True)
RESULT = r_dir
# COOKIES
COOKIES_ENABLED = False
# FINGERPRINT
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# CACHE
c_dir = h / "cache"
c_dir.mkdir(parents=True, exist_ok=True)
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = c_dir
# LOGGING
l_dir = h / "logs"
l_dir.mkdir(parents=True, exist_ok=True)
LOG_FILE = l_dir / f'{time.strftime("%Y-%m-%d_%H-%M-%S")}.log'
LOG_LEVEL = "DEBUG"
