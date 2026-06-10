BOT_NAME = "onepace"
SPIDER_MODULES = ["onepace.spider"]
NEWSPIDER_MODULE = "onepace.spider"

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_EXPIRATION_SECS = 0  # never expire

# politeness
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 4

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

ITEM_PIPELINES = {
    "onepace.pipelines.M3UPipeline": 300,
}