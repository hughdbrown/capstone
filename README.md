# Capstone project

![Build status](https://api.travis-ci.org/hughdbrown/capstone.png?branch=master)

## Back story

On 2015-03-24, [Germanwings flight 9525](https://en.wikipedia.org/wiki/Germanwings_Flight_9525) from Barcelona to Dusseldorf crashed in the French Alps,
killing all 150 aboard. Over the course of several days,
evidence emerged that indicated that the crash was caused intentionally by the copilot. 

The interest in the story was high from the start but the progress of the story (with the gradual revelation of the copilot's suicide)
captured the world's interest over several days. Breaking news on the story caused spikes in internet traffic over this period.

Examination of the global interest cannot be captured from a single website. Instead, data from bit.ly's url shortening service can serve as
a proxy for the global activity.

To examine global interest in this air crash, bit.ly provided three days of data (2015-03-25 to 2015-03-27
inclusive) with 10 minutes of traffic from each of the 72 hours.

## Data science questions

1. Data visualization
2. Topic modeling

## Data

Bit.ly has two major types of data:
* **encodes**: when a bit.ly user creates a shortened url, the action is recorded as an encode
* **decodes**: when a user opens a bit.ly shortened url in a browser, the shortened url and expanded long url are recorded as a decode

The data I worked with was exclusively decodes. 

### urlhist documents
9187392 JSON documents that are the entire collection of data from bit.ly. The documents look like this:
```
{
	"_id" : ObjectId("55f22000d18938208d9ab3d5"),
	"timezone" : "America/Argentina/Cordoba",
	"country" : "AR",
	"timestamp" : ISODate("2015-03-25T00:00:00Z"),
	"short_url" : "1GRjv1C"
}
```

### urls documents
6208615 JSON documents that summarize unique `short_url` links. The documents look like this:
```
{
	"_id" : ObjectId("55ef4220c430767caa20d3da"),
	"count" : 6500,
	"short_url" : "1i1KcE0",
	"long_url" : "http://w-tutorials.info/wp-content/",
	"text" : "<meta HTTP-EQUIV=\"REFRESH\" content=\"0; url=http://w-tutorials.info/\">"
}
```

* `count`: count of hits for URL over 72 hour sample
* `short_url`: bit.ly short url for the story
* `long_url`: the full URL that story expands to
* `text`: if the HTML was downloadable, then this field is present and contains the HTML for the story
* `exc`: if the HTML was not downloadable/was not downloaded, then this field is present and contains an explanation of why the `text` is missing

### germanwings documents
24482 JSON documents (1.98 GB) that have story on Germanwings crash. These are used for topic modeling.Documents in this collection have either:
"germanwings or air crash or copilot" in either the `long_url` or the `text`.

```
{
	"_id" : ObjectId("55ef4c90c430767ceea30100"),
	"count" : 2286,
	"short_url" : "1bwwkVd",
	"long_url" : "http://www.usatoday.com/story/news/world/2015/03/26/germanwings-plane-crash/70473800/",
	"exc" : "HTTPConnectionPool(host='www.usatoday.com', port=80): Read timed out. (read timeout=12)"
}
```

* `count`: count of hits for URL over 72 hour sample
* `short_url`: bit.ly short url for the story
* `long_url`: the full URL that story expands to
* `text`: if the HTML was downloadable, then this field is present and contains the HTML for the story
* `exc`: if the HTML was not downloadable/was not downloaded, then this field is present and contains an explanation of why the `text` is missing

## Technology
* AWS, EC2, S3
* mongo
* ipython

## Python libraries
* pymongo (for working with mongo)
* requests (for all web requests)
* simplejson (for all JSON)
* awscli (for working with AWS)
* docopt (for sane command line options)
* flask (for web servers and website)
* six (for python 2.7 and 3.x compatibility)
* scikit-learn (for topic modeling)
* BeautifulSoup (for cleaning up HTML)
* wordcloud (for creating word clouds)
* scipy (for linear algebra)
* pandas (for data science)
* numpy (for general numerics and linear algebra)
* nltk (for natural language)

## Visualization

## Topic modeling




Graphics
* world traffic vs. germanwings traffic
* US-IT-ES-DE traffic
* US-CA traffic

Topic modeling
* US topics by hour
    
* IT topics by hour
* DE topics by hour
* ES topics by hour
