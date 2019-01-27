.. Finance Scraper documentation master file, created by
   sphinx-quickstart on Sat Jan 26 20:43:21 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Finance Scraper's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   quickstart


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

General Information
-------------------
First of all: if you have already read the **README** of this project you can
simply skip this section (or read it, I really don't care that much).

Alright. Now I want to express how happy I am, that you have found your way to
this project and decided to even check out the doumentation in case you 
actually want to use it. All of this started as a small side project in order
to provide some API for another project I started working on. After some long
searches I found that a completely free API that can handle all the ticker
symbols that yahoo finance can handle was generally not available. This is why
I chose to further pursue this small side project of mine and *here we are!*


**When to use Finance Scraper?**

Before I tell you when not to use this API of course I want to get you hooked
on my project. This is why I'm going to give you a couple of great points on
why you should use Finance Scraper for your next project!

1. This API is maintained to stay up-to-date with the changes in its own data
sources APIs. Over the last couple of years a lot of Python based finance data
sources went dead due to both yahoo and google discontinuing their own APIs.
This project is maintained to stay current to prevent your project from dying
just because its underlying data source stopped working.

2. Other than a lot of the currently available finance data APIs this project
seeks to provide data from not only one specific market, but cut through the
same variety of international markets that websites like yahoo finance cover.

3. It's *unlimited* and *free!* Don't we all like free stuff? Well, the
commercially backed finance data sources sure don't, so they typically limit 
your usage of their API to a fixed amount of requests per minute, hour or day 
if you don't want to pay for it. This is not the case for this project. You 
just get it and it's all yours to use.


**When not to use Finance Scraper?**

Of course it would be delusional to belive that this project is the perfect
solution to any finance data fetching related issue. This is why I also want
to tell you under which circumstances you should probably keep on looking for
a soultion that better suits your needs.

* You need to get your data very fast.
* You only require financial data from one specific market.
* You expect to send out a few requests a minute, hour or even day.

In all of those cases you are probably going to be able to find a commercially
backed and maintained API that suits your needs better than this project. Due
to this API currently making full HTTP requests to its data sources there are
faster solutions on the market. It is especially easy to find APIs that only
cover a single market, especially if you are looking at the American stock
market. They can be way more specified and may even employ multiple servers
simply caching the current data to all supported tickers which will be 
beneficial to the user in the end. Last but not least, if you are only planning
on sending out very few requests there probably is an API that offers a free
plan next to its paid plans that covers your needs.

However, all of that said I still would be happy if you decide to use this
project for your own work, as this is what it is made for and the more people
it helps, the more people can give feedback and the better this API can be!