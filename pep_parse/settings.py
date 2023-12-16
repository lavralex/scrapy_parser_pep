from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

ENCODING = 'utf-8'

BOT_NAME = 'pep_parse'

STATUSES_FILE_NAME = 'status_summary'
PEP_FILE_NAME = 'pep'
FILE_FORMAT = 'csv'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

RESULT_DIR = 'results'

FEED_EXPORT_ENCODING = ENCODING

FEEDS = {
    f'{RESULT_DIR}/{PEP_FILE_NAME}_%(time)s.{FILE_FORMAT}': {
        'format': FILE_FORMAT,
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

DOMAIN = 'peps.python.org'

SPIDER_NAME = 'pep'
