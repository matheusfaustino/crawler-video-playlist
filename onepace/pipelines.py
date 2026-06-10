import re
from pathlib import Path
from onepace.items import Episode

class M3UPipeline:
    def open_spider(self, spider):
        self.lines = []

    def process_item(self, item: Episode, spider):
        title = item.name
        url = item.url
        
        self.lines.append({
            'line': f"#EXTINF:-1,{title}\n{url}", 'title': title
        })
        
        return item

    def close_spider(self, spider):
        self.lines.sort(key=self._sort_key)
        
        items = ["#EXTM3U"]
        for d in self.lines:
            items.append(d['line'])
        
        (Path(__file__).parent.parent / 'onepace.m3u8').write_text(
            '\n'.join(items) + '\n',
            encoding='utf-8'
        )
        
    @staticmethod
    def _sort_key(item):
        # pull the first number out of the filename
        nums = re.findall(r"\d+", item["title"])
        
        return int(nums[0]) if nums else 0