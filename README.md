# Finance Scaper
This project aims to provide an up-to-date data scraper for yahoo finance as a simple stock data API.

## The purpose & why to use Finance Scraper
There are a lot of APIs allowing you to pull stock/market data available for python. 
[Pandas Data Reader](https://pandas-datareader.readthedocs.io/en/latest/), 
[googlefinance](https://pypi.org/project/googlefinance/),
[IEXTrading](https://iextrading.com/developer/docs/#getting-started) are a just a few
of the massive amounts of data sources you could use for your application. 

So **why use the FinanceScraper API**? Well, there are a few issues with a lot of the
APIs readily available online:
1. A lot of the APIs are out of date. Both Yahoo and Google have stepped back from
providing APIs for finance data during the last couple of years and a lot of the
existing project - especially on GitHub - were created before that happened and never
maintained properly afterwards.
2. Those data sources that do work properly, often only provide access to a few
select markets, most of the time the American stock market. This obviously might
restrict your application, especially if you are planning to cater to an international
audience.
3. Another issue with commercially maintained APIs often comes with the usage. The free
access usually harshly restricts usage by limiting the quotes per minute or per day.
If you ever plan to provide your app to the general public, or just a couple of
friends, this could put you in a difficult situation of choosing between a free plan
or a generally usable program.

However, there are a couple of things other APIs can do better than this one. This is
why I do want to also tell you when **not** to use this API:
* You only need data from a **single market**. There are probably a bunch of APIs 
specializing in data from the market you are looking at. Take a look at those before 
jumping into FinanceScraper.
* You want to write a little application for your **personal use only**. In this case
the free plans of commercially available APIs are probably enough for you. Maybe take
a look at [WorldTradingData](https://www.worldtradingdata.com/).
* You need a lot of data very fast and have no means of parallelizing. In this case
you will probably want to use one of the well established APIs, as this project is
doing full HTML requests to ensure the most recent quotes possible. If you however
have a lot of rapid requests on the same data you may want to check out this
projects data caching/buffering capabilities.

## Project setup

If you simply want to use the API, I recommend using the latest stable version 
which can be acquired by running `` pip install FinanceScraper ``. For the API's
usage take a look at the documentation. (I swear it will come soon, this is still
in it's very beginning)

If you are looking to contribute to this project please go ahead! You're going to have
to fork the project and do your work in your own repository. If you are seeing anything
that could/should be improved please put in an issue and I will assign you if you want
to solve it yourself. In order to get your progress into this main project you just have
to put in a pull request for a branch up-to-date with the current master.

## ToDo
Now I also want to tell you about what I am planning to add to this project for the
next major, minor and micro versions.

### Micro
* [ ] add tests for the existing functionality
* [x] write a useful README
* [ ] write a simple documentation for the current functionality

### Minor
* [ ] write the documentation more in depth
* [ ] make the documentation interactive
* [ ] add more example code to show the intended usage

### Major
* look into performance improvements
* as this will be 1.x.x should be well documented and very usable