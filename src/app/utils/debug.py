from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        'bachngocsach',
        u='https://bachngocsach.com.vn/reader/ai-tong-mat-quoc',
        start=4,
        stop=9
    )
    process.start() # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
