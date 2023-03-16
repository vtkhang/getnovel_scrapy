"""Define your item pipelines here

   Don't forget to add your pipeline to the ITEM_PIPELINES setting
   See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

   useful for handling different item types with a single interface
"""

import uuid
import logging
from pathlib import Path

from scrapy.exceptions import DropItem

from app.items import Info, Chapter
from app.utils.sqlite import GetNovelDB

_logger = logging.getLogger(__name__)


class AppPipeline:
    """Define sqlite pipeline"""

    def open_spider(self, spider):
        """Initialize attributes."""
        self.sp = Path(spider.settings["RESULT"])
        self.url_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, spider.start_urls[0]))
        self.sp: Path = self.sp / spider.name / self.url_uuid
        self.sp.mkdir(exist_ok=True, parents=True)
        self.db = GetNovelDB(Path(spider.settings["SQLITE_DATABASE"]))
    
    def close_spider(self, spider):
        """End process."""
        self.db.close()

    def process_item(self, item, spider):
        """Store items to files.

        Parameters
        ----------
        item : Item
            Input item.
        spider : Spider
            The spider that scraped input item.

        Returns
        -------
        Item
            Return item for another pipelines.

        Raises
        ------
        DropItem
            If item contains empty fields.
        DropItem
            If any field is not exists.
        DropItem
            Invalid item detected.
        """
        r = []
        for k in item.keys():
            if item.get(k) == "" or item.get(k) is None:
                raise DropItem(f"Field {k} is empty!")
        try:
            if isinstance(item, Info):
                img = Path(spider.settings["IMAGES_STORE"]) / item["images"][0]["path"]
                r.append(item["title"])
                r.append(item["author"])
                r.append(item["types"])
                r.append(item["url"])
                r.append(item["foreword"])
                (self.sp / "cover.jpg").write_bytes(img.read_bytes())
                (self.sp / "foreword.txt").write_text(data="\n".join(r), encoding="utf-8")
                #SQLite
                info = dict(item)
                info["url_uuid"] = self.url_uuid
                info["location"] = str(self.sp)
                info["cover"] = str(img)
                self.db.insert(info)
            elif isinstance(item, Chapter):
                r.append(item["title"])
                r.append(item["content"])
                (self.sp / f"{item['id']}.txt").write_text(data="\n".join(r), encoding="utf-8")
            else:
                raise DropItem("Invalid item detected!")
        except KeyError as key:
            _logger.warning(f"Error url: {item.get('url', 'Field url is not exist!')}")
            raise DropItem(f"Field {key} is not exist!")
        return item