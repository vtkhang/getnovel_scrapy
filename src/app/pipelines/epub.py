"""Clean crawled text."""

import logging
from distutils.dir_util import copy_tree
from importlib.resources import files
from pathlib import Path

import data
from scrapy import Item, Spider
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem

from app.items import Chapter, Info

_logger = logging.getLogger(__name__)


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(
    logging.Formatter(fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s"),
)
_logger.addHandler(ch)


class Epub:
    """Define App pipeline."""

    def __init__(self: "Epub", result_dir: Path) -> None:
        """Init data."""
        self.sp = result_dir
        self.epub = result_dir / "epub"

    @classmethod
    def from_crawler(cls: "Epub", crawler: Crawler) -> "Epub":
        """Get settings."""
        return cls(result_dir=crawler.settings.get("RESULT"))

    def open_spider(self: "Epub", spider: Spider) -> None:  # noqa: ARG002
        """Copy template."""
        template = files(data).joinpath("template")
        copy_tree(str(template), str(self.epub))

    def process_item(self: "Epub", item: Item, spider: Spider) -> Item:  # noqa: ARG002
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
        for k in item:
            if item.get(k) == "" or item.get(k) is None:
                msg = f"Field {k} is empty!"
                raise DropItem(msg)
        try:
            _logger.info(item["title"])
            if isinstance(item, Info):
                r.append(item["title"])
                r.append(item["author"])
                r.append(item["types"])
                r.append(item["url"])
                r.append("\n".join(fix_bad_newline(item["foreword"])))
                # (self.sp / "foreword.txt").write_text(
                #     data="\n".join(r),
                #     encoding="utf-8",
                # )
            elif isinstance(item, Chapter):
                r.append(item["title"])
                r.append("\n".join(fix_bad_newline(item["content"])))
                # (self.sp / f"{item['index']}.txt").write_text(
                #     data="\n".join(r),
                #     encoding="utf-8",
                # )
            else:
                msg = "Invalid item detected!"
                raise DropItem(msg)
        except KeyError as key:
            _logger.warning("Error url: %s", item.get("url"))
            msg = f"Field {key} is not exist!"
            raise DropItem(msg) from KeyError
        return item


def fix_bad_newline(lines: list[str]) -> list[str]:
    """Tidy the result.

    Filtered blank lines. Concatenate lines that
    likely to be in the same setence.

    Examples
    --------
    >>> fix_bad_newline(["A and", "b"])
    >>> ["A and b"]

    Parameters
    ----------
    lines : list[str]
        Input lines.

    Returns
    -------
    list[str]
        Fixed lines.
    """
    s_lines: list[str] = [line.strip() for line in lines if line.strip()]
    result: list[str] = []
    result.append(s_lines[0])
    for line in s_lines[1:]:
        last = result[-1][-1]
        first = line[0]
        if last == "," or last.islower() or first.islower():
            result[-1] += " " + line
        elif first in ".,:":
            result += line
        else:
            result.append(line)
    return result
