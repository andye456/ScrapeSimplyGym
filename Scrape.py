import urllib.request as ur
import json
import logging, time
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Logger to handle rotating log files
logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler("data.csv", when="midnight", interval=1, backupCount=7)
formatter = logging.Formatter('%(asctime)s, %(message)s','%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

def scrape():
    while True:
        # Get the simply gym endpoint data, I think 10775 is Cheltenham every 5 minutes
        page_text = ur.urlopen("https://simplygym.co.uk/wp-json/visualizer/v1/action/10775/csv/").read().decode("utf-8-sig").replace("\ufeff","")
        page_json = json.loads(page_text)
        csv = page_json['data']['csv']
        # Get the capacity data
        capacity = ascii(csv).split(",")[3].split("\\n")[0]
        print("Logging capacity")
        logger.info(capacity)
        time.sleep(300)

# This is a web server so that the csv data can be provided on an endpoint for remote apps to use
class my_server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        csv_data = Path("data.csv").read_text()
        self.wfile.write(bytes(csv_data,encoding="utf-8"))

def server():
    hostname="localhost"
    server_port=32766
    webserver = HTTPServer((hostname, server_port), my_server)
    try:
        print("Server started")
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    x = Thread(target=scrape)
    y = Thread(target=server)
    x.start()
    y.start()
