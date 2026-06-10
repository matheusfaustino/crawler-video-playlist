import scrapy
import re
import json
from onepace.items import Season, ViewerData, Episode

REGEX_JSON_EPISODES = r'window\.viewer_data = (.*)'
DOWNLOAD_URL = r'https://pixeldrain.net/api/file/{}?download'    

class OnePace(scrapy.Spider):
    name = 'onepace'
    start_urls = ["https://onepace.net/en/watch"]
    
    def parse(self, response):
        
        for season in response.css(r'.\*\:last\:min-h-lvh > li'):
            item = Season(
                title = season.css('h2 a::text').get(),
                url = season.css('ul li:first-child ul li:last-child a::attr(href)').get()
            )
            
            yield scrapy.Request(
                item.url,
                callback=self.parse_season,
                cb_kwargs={"season": item}
            )
            
            
    def parse_season(self, response, season):
        json_epi = re.search(REGEX_JSON_EPISODES, response.text)
        if not json_epi:
            self.logger.warning(f'No JSON epi found: {response.url}')
            return
        
        # remove the semi-colon
        episodes_json = json.loads(json_epi.group(1).strip()[:-1])
        episodes = ViewerData.from_dict(episodes_json)
        
        
        for epi in episodes.api_response.files:
            #  	https://pixeldrain.net/u/cbjgKSRu
            #  	https://pixeldrain.net/api/file/cbjgKSRu?download
            video_id = epi.detail_href.split('/')[2]
            video_url = DOWNLOAD_URL.format(video_id)
            
            video = Episode(
                name = epi.name,
                url = video_url 
            )
            
            yield video
        