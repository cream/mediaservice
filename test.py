from mediaservice import modelbase

modelbase.setup()

from mediaservice.audio import crawler

crawler.crawl('/home/jonas/music')
