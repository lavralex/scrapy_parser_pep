import csv
import datetime as dt
from collections import Counter

from .settings import (
    BASE_DIR, ENCODING,
    RESULT_DIR,
    DATETIME_FORMAT,
    STATUSES_FILE_NAME,
    FILE_FORMAT,
)


class PepParsePipeline:

    def open_spider(self, spider):
        self.statuses_summary = Counter()

    def process_item(self, item, spider):
        self.statuses_summary[item['status']] += 1
        return item

    def close_spider(self, spider):
        creation_date = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'{STATUSES_FILE_NAME}_{creation_date}.{FILE_FORMAT}'
        with open(
            BASE_DIR / RESULT_DIR / file_name,
            'w',
            encoding=ENCODING
        ) as file:
            writer = csv.writer(
                file,
                dialect='unix',
                quoting=csv.QUOTE_NONE,
                escapechar='|'
            )
            writer.writerows(
                (
                    ('status', 'Count'),
                    *self.statuses_summary.items(),
                    ('Total', sum(self.statuses_summary.values()))
                )
            )
