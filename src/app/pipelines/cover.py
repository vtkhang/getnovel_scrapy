"""Download novel's cover."""

from contextlib import suppress
from pathlib import Path
from shutil import copy

from itemadapter import ItemAdapter
from scrapy import Item
from scrapy.pipelines.images import ImagesPipeline


class CoverImage(ImagesPipeline):
    """Define Image Pipeline."""

    def item_completed(
        self: "CoverImage",
        results: list,
        item: Item,
        info: ImagesPipeline.SpiderInfo,
    ) -> Item:
        """Overide default item_completed method."""
        with suppress(KeyError):
            img_store = Path(info.spider.settings["IMAGES_STORE"])
            sp = Path(info.spider.settings["RESULT"])
            for ok, x in results:
                if ok:
                    copy(img_store / x["path"], sp / "cover.jpg")
            ItemAdapter(item)[self.images_result_field] = [x for ok, x in results if ok]
        return item
