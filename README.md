# UglyFeed CDN

This repository acts as CDN for the [UglyFeed](https://github.com/fabriziosalmi/UglyFeed) project.

You can find RSS content which is automatically generated by GitHub actions and python scripts. I use some of these XML feeds as source test feeds while testing UglyFeed updates and experiments. 

I want to automate as much as possible then I preferred the GitHub action approach (can be ported to Gitea and similar tools so quick). In addition I wanted to separate such content and the UglyFeed application code. This because a brand new repo.

- [![Generate Daily RSS Feeds](https://github.com/fabriziosalmi/uglyfeed-cdn/actions/workflows/generate_daily_feeds.yml/badge.svg)](https://github.com/fabriziosalmi/uglyfeed-cdn/actions/workflows/generate_daily_feeds.yml) 
- [![Generate Daily Universe Feeds](https://github.com/fabriziosalmi/uglyfeed-cdn/actions/workflows/generate_universe_feeds.yml/badge.svg)](https://github.com/fabriziosalmi/uglyfeed-cdn/actions/workflows/generate_universe_feeds.yml)

## Source feeds
Here you can find feeds intended to be used as source feeds for testing, These valid XML feeds are automatically updated on a daily basis. You can process them with [UglyFeed](https://github.com/fabriziosalmi/UglyFeed) or any other RSS reader:

- [Happened today](https://github.com/fabriziosalmi/uglyfeed-cdn/blob/main/happened-today/README.md)
- [Universe](https://github.com/fabriziosalmi/uglyfeed-cdn/blob/main/universe/README.md)

> source content is retrieved by GitHub action using the `wikipedia` python package

_Please note that such content is intended just for testing the UglyFeed project and not as a consistent RSS feed to be read by end users._

## Processed feeds
Here you can find feeds intended to be evaluated as rewritten/generated by LLM feeds. These valid XML feeds are automatically updated on a daily basis. You can evaluate them with [UglyFeed](https://github.com/fabriziosalmi/UglyFeed) metrics scripts or any other tool out there. You can process them with UglyFeed or any other RSS reader.

> [!NOTE]
> Temporary stopped :)
> - [Daily feeds by llama3 via Groq API](https://github.com/fabriziosalmi/uglyfeed-cdn/blob/main/feeds/uglyfeeds.xml)


