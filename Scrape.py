import urllib.request as ur
import json
import logging, time, os
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Logger to handle rotating log files
logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler("data.csv", when="midnight", interval=1, backupCount=7)
# for testing, rolls log every 15 seconds
# handler = TimedRotatingFileHandler("data.csv", when="s", interval=15, backupCount=7)
formatter = logging.Formatter('%(asctime)s,%(message)s','%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

def scrape():
    while True:
        # Get the simply gym endpoint data every 5 minutes, I think 10775 is Cheltenham
        page_text = ur.urlopen("https://simplygym.co.uk/wp-json/visualizer/v1/action/10775/csv/").read().decode("utf-8-sig").replace("\ufeff","")
        page_json = json.loads(page_text)
        csv = page_json['data']['csv']
        # Get the capacity data
        capacity = ascii(csv).split(",")[3].split("\\n")[0]
        print("Logging capacity")
        # Writes csv headings for the D3 graph to read if they are not already there
        with open("data.csv") as f:
            first_line = f.readline()
        if "time" not in first_line:
            f = open('data.csv', 'r+')
            lines = f.readlines()  # read old content
            f.seek(0)  # go back to the beginning of the file
            f.write("time,capacity\n")  # write new content at the beginning
            for line in lines:  # write old content after new
                f.write(line)
            f.close()
        logger.info(capacity)
        time.sleep(300)

# This is a web server so that the csv data can be provided on an endpoint for remote apps to use
class my_server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin : *")
        self.end_headers()
        csv_data = Path("data.csv").read_text()
        self.wfile.write(bytes(csv_data,encoding="utf-8"))

def server():
    hostname="0.0.0.0"
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
