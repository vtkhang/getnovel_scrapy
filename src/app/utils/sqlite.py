import time
import logging
import sqlite3
from pathlib import Path

_logger = logging.getLogger(__name__)


class GetNovelDB:

    def __init__(self, dbp: Path):
        self.con = sqlite3.connect(dbp)
        self.cur = self.con.cursor()

    def insert(self, info):
        query = """
        INSERT INTO novel VALUES (?,?,?,?,?,?,?,?)
        """
        try:
            self.cur.execute(query, (
                info["url_uuid"],
                info["title"],
                info["author"],
                info["types"],
                info["url"],
                info["foreword"],
                info["location"],
                info["cover"]
            ))
            self.con.commit()
        except Exception as err:
            _logger.error("Error: %s" % (str(err)))

    def close(self):
        self.con.close()


def check5row(dbp: Path = None):
    if dbp is None:
        dbp = Path(input("> Input path of database: "))
    if not dbp.exists():
        print("> Database is not exists!")
    else:
        query = """
        SELECT title, url FROM novel LIMIT 5
        """
        try:
            con = sqlite3.connect(dbp)
            cur = con.cursor()
            rs = cur.execute(query)
            print(rs.fetchall())
        except Exception as err:
            print("Query: %s\nError: %s" % (query, str(err)))


def new_db(dbp: Path = None):
    if dbp is None:
        dbp = Path(input("> Input path of database: "))
    if dbp.exists():
        dbp.rename(dbp.with_name(f"{dbp.name}_{time.strftime('%Y_%m_%d-%H_%M_%S')}"))
        print("> Renamed existing database!")
    query = """
            CREATE TABLE novel (
                url_uuid TEXT PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                types TEXT NOT NULL,
                url TEXT NOT NULL,
                foreword TEXT NOT NULL,
                location TEXT NOT NULL,
                cover TEXT NOT NULL
            )
            """
    try:
        con = sqlite3.connect(dbp)
        cur = con.cursor()
        cur.execute(query)
    except Exception as err:
        print("> Query: %s\nError: %s" %(query, str(err)))
        return
    print(f"> Location of new database: {dbp}")


if __name__ == "__main__":
    c = ""
    while(c not in ("create", "check") ):
        c = input("> Chooose mode: [create] [check]")
    ap = Path.home() / "GetNovel"
    sqlitep = ap / "database"
    sqlitep.mkdir(parents=True, exist_ok=True)
    sqlitenp = sqlitep / "getnovel.db"
    if c == "create":
        new_db(sqlitenp)
    if c == "check":
        check5row(sqlitenp)
