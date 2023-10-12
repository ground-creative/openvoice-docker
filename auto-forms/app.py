import scrapy, csv, getopt, sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pathlib import Path
import random
import string

CAMPAIGN = 'default'
MODE = 'collect-data'
SESSION = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

options, remainder = getopt.getopt(sys.argv[1:], 'c:m:', ['campaign=', 'mode=',])

for opt, arg in options:
    if opt in ('-c', '--campaign'):
        CAMPAIGN = arg
    elif opt in ('-m', '--mode'):
        MODE = arg

domains = []
with open(str(Path.cwd()) +'/domains/' + CAMPAIGN + '/list.txt', 'r') as fd:
	reader = csv.reader(fd)
	for row in reader: 
		domains.append(row[0])

#print(domains)




print("GOOOOOOOOOOOO")

settings = get_project_settings()
#settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'

process = CrawlerProcess(settings)
process.crawl('spider', start_urls=domains, campaign = CAMPAIGN, mode = MODE, session = SESSION)
process.start()