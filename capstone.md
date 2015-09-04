# Bit.ly

## Background

[Bit.ly](https://bitly.com/) is well-known as an internet company that provides services as a url-shortening SAAS: users
take long urls that they have for content and submit them to Bit.ly, which assigns them
shorter, more easily typed urls from their website url-space.

Everyday, users take long URLs and shorten them to more manageable lengths to be copied and embedded
in email or otherwise passed to people they know. In a sense, bit.ly's store of web server activity is a
proxy for aggregate internet activity.

On 2015-03-24, a [Germanwings flight from Barcelona to Dusseldorf](https://en.wikipedia.org/wiki/Germanwings_Flight_9525)
crashed in the French Alps, killing all aboard.
This crashed captured the attention of internet users as details emerged that showed that the crash was a
deliberate suicide by the co-pilot.

## Capstone question

The capstone project proposed explores the internet activity that followed this disaster:

1. traffic segmented by location
* The story is expected to have differing levels of interest by location.

2. traffic segmented by time
* The story is expected to have differing levels of interest by time. In particular, as new information
is discovered and confirmed by investigators, the story is expected to have a resurgence of interest.

3. traffic identified by topic
* Topic modeling will identify different topics in the URLs, and these will have differing levels of interest.

In general, the capstone project addresses how data science tools can be applied to discover the
characteristics of the rapid emergence of a story of interest on the internet.

## Data source

Bit.ly data is divided broadly into two types: links submitted for shortening and shortened links
subsequently clicked on by users. The latter is considered to have more potential for business use because
actual people are consuming the data and have browser and location information.

The primary difficulty with this project is the size of the data involved. Bit.ly decode logs
are about 6 GB per hour of elapsed time. Getting three days of data would be about 500 GB of data uncompressed,
far too large to manage in full. Instead, the data capture will involve downsampling to the top ten minutes of each
hour for the 72 hours from 2015-03-25 to 2015-03-27 inclusive.

## Data techniques

In addition to downsampling to a more manageable size, the initial actions on the data will involve
identifying data links relevant to Germanwings disaster and working on those alone. Out of the 350K unique links that
appear in a 10 minute segment, Probably no more than 2000 will be relevant even at peak concentration on the
story.

## Data science tools

1. python
1.1 sklearn for machine learning
1.2 boto for AWS
1.3 flask/bootstrap for web development
2. AWS/S3


## Project collateral

The deliverables for this project will be at least one of these things:

1. a website that explains the project and shows results
2. a stack of slides for presenting the project to an audience
3. an infographic that summarizes the data and findings

## Plan of action

1. Download data
1.1 Copy from S3 storage to local machine
1.2 Backup data in bit.ly S3 storage to personal S3 storage
2. Summarize data
2.1 Calculate the top short URLs by hits in each 10 minute data set
2.2 Aggregate the top short URLs into a single ranking over 72 hours
3. Download the HTML of the URLs identified as top Germanwings stories
4. Store the HTML for processing in a database
5. Apply analysis to database
5.1 Analyze by location/timezone
5.2 Analyze by time
5.3 Apply topic modeling to determine top topics over time/location
6. Produce project collateral
6.1 Create flask/bootstrap website
6.2 Create slide deck for presentation
6.3 Create infographic

## Publishing

The project will be published in two ways:

1. a website that has the finished product
2. a [github repo](https://github.com/hughdbrown/capstone) that contains all the code and script used for the project (but not the data)
