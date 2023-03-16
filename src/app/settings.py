import time
from pathlib import Path

ap = Path.home() / "GetNovel"
# Default image path for imagepipeline
imgp = ap / "images"
imgp.mkdir(parents=True, exist_ok=True)
# Result directory
result = ap / "crawled"
result.mkdir(parents=True, exist_ok=True)
# Log
lp = ap / "logs"
lp.mkdir(parents=True, exist_ok=True)
lnp = lp / f'{time.strftime("%Y_%m_%d-%H_%M_%S")}.log'
# Sqlite Database
sqlitep = ap / "database"
sqlitep.mkdir(parents=True, exist_ok=True)
sqlitenp = sqlitep / "getnovel.db"
# SCRAPY
BOT_NAME = r"GetNovel"
ROBOTSTXT_OBEY = True
SPIDER_MODULES = ["app.spiders"]
USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
COOKIES_DEBUG = True
# ITEM PIPELINES
ITEM_PIPELINES = {
    "app.pipelines.AppPipeline": 300,
    "scrapy.pipelines.images.ImagesPipeline": 200
}
IMAGES_STORE = str(imgp)
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# LOG SETTINGS
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_SHORT_NAMES = True
LOG_FILE = str(lnp)
LOG_FILE_APPEND = False
LOG_LEVEL = "INFO"
# AUTOTHROTTLE SETTINGS
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 6
DOWNLOAD_DELAY = 3
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
# SAVE PATH
RESULT = str(result)
#SQLITE DATABASE
SQLITE_DATABASE = str(sqlitenp)