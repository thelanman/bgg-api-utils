# Booard Game Geek (BGG) API Utilities

Various utilities for fetching BGG Game entries via [their XML API](https://boardgamegeek.com/wiki/page/BGG_XML_API2). Also, includes a basic Game model and will eventually provide querying and data analytic functions for the massive dataset of +

## Dependencies
- Python 2.7+ Standard Library

## Setup
##### Start fresh
```sh
$ git clone this repo
```
##### Usage
```sh
>>> import api, utils
>>>
>>> # Fetch Games with ID 1 -> 200 and save to xml files at given path
>>> api.bulk_game_retriever(1, 200,  '/path/to/save/games/')
>>>
>>> # Load XML from file as Game
>>> xml = utils.load_xml_from_file('/path/to/save/games/bgg_game_000171.xml')
>>> game = api.Game(xml)
>>> print game
Game(Chess : 171)
```

## Thanks
[Board Game Geek] (https://boardgamegeek.com/)

## License
MIT
