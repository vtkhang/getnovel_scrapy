"""Default settings."""

from pathlib import Path

BOT_NAME = "GetNovelScrapy"
h = (Path.home() / BOT_NAME).resolve()
r_dir = h / "result"
r_dir.mkdir(parents=True, exist_ok=True)
c_dir = h / "cache"
c_dir.mkdir(parents=True, exist_ok=True)
ROBOTSTXT_OBEY = True
SPIDER_MODULES = ["app.spiders"]
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
)
ITEM_PIPELINES = {"app.pipelines.FilePipeline": 1}
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
RESULT = r_dir
# AUTOTHROTTLE
AUTOTHROTTLE_ENABLED = True
# COOKIES
COOKIES_ENABLED = False
# FINGERPRINT
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# CACHE
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = c_dir
