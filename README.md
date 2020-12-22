# Simply Gym Scraping for capacity

## Introduction
This simple tool scrapes the capacity figures (i.e. the number of people in there) from the front page of their website.

This is to determine the quietest time to go.

## Code
Two simple scripts, one gets the data from the endpoint, parses it for the capacity % figure.
and writes it to a csv file along with the time.

The other script uses pandas to create a dataframe from the csv data, the pyplot is called to create a graph.

## AWS
As this tool needs to run 24/7 it will be run on AWS.

The plot tool will be run on data provided by a call to an endpoint that will return the csv data.

## Further enhancements
The endpoint csv data will be read by a D3 graph and available in a browser.
