import urllib2
import xml.etree.ElementTree as ET

from utils import Throttle, get_xml_subelement


@Throttle(sleep=(1,4))
def get_xml_games_api(gid, path=None):
    url = 'https://www.boardgamegeek.com/xmlapi2/thing?type=boardgame&id=%s&stats=1'
    if type(gid) is not list:
        gid = [gid]
    try:
        response = urllib2.urlopen(url % ','.join(map(lambda x:str(x), gid)))
    except:
        raise
    html = response.read()
    xml_elem = ET.fromstring(html)
    xml_elems = []
    for x in xml_elem:
        xml_elems += [x]
        if path is not None:
            with open(path + 'bgg_game_%06d.xml' % int(x.attrib['id']), 'w') as f:
                f.write(ET.tostring(x).replace('\t', '').replace('\n\n', '\n'))
    return xml_elems


def bulk_game_retriever(start, stop, path=None):
    inc = min(99, stop - start)
    for s in range(start, stop, inc):
        print s
        get_xml_games_api(range(s, s + inc), path)


class Game(object):
    def __init__(self, xml_elem):
        self.id = int(xml_elem.attrib['id'])
        self.names_alt = get_xml_subelement(xml_elem, ".//name[@type='alternate']", 'value', True)
        self.name = get_xml_subelement(xml_elem, ".//name[@type='primary']", 'value')
        self.min_players = get_xml_subelement(xml_elem, 'minplayers', 'value', convert=int)
        self.max_players = get_xml_subelement(xml_elem, 'maxplayers', 'value', convert=int)
        self.min_age = get_xml_subelement(xml_elem, 'minage', 'value', convert=int)
        suggested_playerage = xml_elem.find(".//poll[@name='suggested_playerage']")
        self.suggested_playerage = {'totalvotes': int(suggested_playerage.attrib['totalvotes'])}
        weighted = 0
        totalvotes = self.suggested_playerage['totalvotes']
        for s in suggested_playerage[0] if totalvotes > 0 else []:
            self.suggested_playerage[s.attrib['value']] = int(s.attrib['numvotes'])
            weighted += (int(s.attrib['value']) if s.attrib['value'] != '21 and up' else 21) * int(s.attrib['numvotes'])
        self.avg_age = round(weighted / float(totalvotes)) if totalvotes > 0 else None
        self.min_playtime = get_xml_subelement(xml_elem, 'minplaytime', 'value', convert=int)
        self.max_playtime = get_xml_subelement(xml_elem, 'maxplaytime', 'value', convert=int)
        self.playingtime = get_xml_subelement(xml_elem, 'playingtime', 'value', convert=int)
        self.year_published = get_xml_subelement(xml_elem, 'yearpublished', 'value', convert=int)
        self.description = get_xml_subelement(xml_elem, 'description')
        self.categories = get_xml_subelement(xml_elem, ".//link[@type='boardgamecategory']", 'value', True)
        self.families = get_xml_subelement(xml_elem, ".//link[@type='boardgamefamily']", 'value', True)
        self.mechanics = get_xml_subelement(xml_elem, ".//link[@type='boardgamemechanic']", 'value', True)
        self.suggested_numplayers = {}
        suggested_numplayers = xml_elem.find(".//poll[@name='suggested_numplayers']")
        self.suggested_numplayers['totalvotes'] = int(suggested_numplayers.attrib.get('totalvotes', 0.0))
        if self.suggested_numplayers['totalvotes'] > 0:
            for results in suggested_numplayers:
                numplayers = results.attrib.get('numplayers')
                self.suggested_numplayers[numplayers] = {}
                for result in results:
                    self.suggested_numplayers[numplayers][result.attrib['value']] = int(result.attrib['numvotes'])
            self.calc_suggested_numplayers()
        self.ratings = {}
        ratings = xml_elem.find('statistics').find('ratings')
        self.ratings['usersrated'] = get_xml_subelement(ratings, 'usersrated', 'value', convert=int)
        self.ratings['average'] = get_xml_subelement(ratings, 'average', 'value', convert=float)
        self.ratings['bayesaverage'] = get_xml_subelement(ratings, 'bayesaverage', 'value', convert=float)
        self.ratings['stddev'] = get_xml_subelement(ratings, 'stddev', 'value', convert=float)
        self.ratings['median'] = get_xml_subelement(ratings, 'median', 'value', convert=float)
        self.ratings['owned'] = get_xml_subelement(ratings, 'owned', 'value', convert=int)
        self.ratings['trading'] = get_xml_subelement(ratings, 'trading', 'value', convert=int)
        self.ratings['wanting'] = get_xml_subelement(ratings, 'wanting', 'value', convert=int)
        self.ratings['wishing'] = get_xml_subelement(ratings, 'wishing', 'value', convert=int)
        self.ratings['numcomments'] = get_xml_subelement(ratings, 'numcomments', 'value', convert=int)
        self.ratings['numweights'] = get_xml_subelement(ratings, 'numweights', 'value', convert=int)
        self.ratings['averageweight'] = get_xml_subelement(ratings, 'averageweight', 'value', convert=float)
        ranks = ratings.find('ranks')
        self.ranks = get_xml_subelement(ranks, 'rank', ['bayesaverage', 'friendlyname', 'id', 'name', 'type', 'value'], True, quiet=True)
        self.rank = get_xml_subelement(ranks, ".//rank[@name='boardgame']", 'value', convert=int, quiet=True)

    def calc_suggested_numplayers(self):
        for s in ['Best', 'Recommended', 'Not Recommended']:
            self.suggested_numplayers[s] = max(self.suggested_numplayers.items(), key=lambda p: p[1][s] if p[0] not in ['totalvotes', 'Best', 'Recommended', 'Not Recommended'] else -10000)[0]

    def __repr__(self):
        return 'Game(%s : %s)' % (self.name, self.id)
