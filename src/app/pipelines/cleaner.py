"""Clean crawled text."""

import logging

from scrapy import Item, Spider
from scrapy.exceptions import DropItem

from app.items import Chapter, Info

_logger = logging.getLogger(__name__)


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(
    logging.Formatter(fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s"),
)
_logger.addHandler(ch)


class Cleaner:
    """Define App pipeline."""

    def process_item(self: "Cleaner", item: Item, spider: Spider) -> Item:
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
        sp = spider.settings.get("RESULT")
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
                (sp / "foreword.txt").write_text(
                    data="\n".join(r),
                    encoding="utf-8",
                )
            elif isinstance(item, Chapter):
                r.append(item["title"])
                r.append("\n".join(fix_bad_newline(item["content"])))
                (sp / f"{item['index']}.txt").write_text(
                    data="\n".join(r),
                    encoding="utf-8",
                )
            else:
                msg = "Invalid item detected!"
                raise DropItem(msg)
        except KeyError as key:
            _logger.warning("Error url: %s", item.get("url", "Field url is not exist!"))
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
