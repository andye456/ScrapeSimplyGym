import urllib.request as ur
import json
import logging, time
from logging.handlers import TimedRotatingFileHandler

# Logger to handle rotating log files
logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler("data.csv", when="midnight", interval=1, backupCount=7)
formatter = logging.Formatter('%(asctime)s, %(message)s','%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


while True:
    # Get the simply gym endpoint data, I think 10775 is Cheltenham
    page_text = ur.urlopen("https://simplygym.co.uk/wp-json/visualizer/v1/action/10775/csv/").read().decode("utf-8-sig").replace("\ufeff","")
    page_json = json.loads(page_text)
    csv = page_json['data']['csv']
    # Get the capacity data
    capacity = ascii(csv).split(",")[3].split("\\n")[0]
    logger.info(capacity)
    time.sleep(300)

