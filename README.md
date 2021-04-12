# [![Build Status](https://github.com/jessicapaz/dealer-rater-scraper/actions/workflows/build.yml/badge.svg)](https://github.com/jessicapaz/dealer-rater-scraper/actions)

## How the project works

This app scrapes pages from a [dealer rater website](https://www.dealerrater.com) and returns the most positives reviews for a specific dealer.

The criteria used to choose the best reviews are:
- The latest reviews date.
- The best rated reviews.
---
## How to run the app

To run this app you need to pass some values via command line arguments, the options are:
Argument    |Description
---------   |-
`dealer`    |The dealer's slug 
`page_start`|The first page you want to scrape
`page_end`  |The final page you want to scrape
`limit`     |The number of reviews you want to display


That said, now you can build the docker image by running:

`docker build . -t dealer-rater`

And run:

`docker run --env-file=.env dealer-rater pipenv run python -m app.main --limit 3 --dealer "McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685" --page_start 1 --page_end 5`

---
## How to run the tests

You can run the tests by running:

`docker run dealer-rater make test`
