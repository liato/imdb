#!/usr/bin/env python
import datetime
from decimal import Decimal
import re
import urllib2

from lxml.html import parse

__version__ = '0.1.0'

asciionly = re.compile(r'[^a-zA-Z]')
numonly = re.compile(r'[^0-9]')
findyear = re.compile(r' \(?(?P<year>\d{4})(?:/[IV]*)?\)')
findid = re.compile(r'(?P<id>(?:tt|nm|ch)\d{7})', re.I)
def getid(str):
    m = findid.search(str)
    if m:
        return m.group('id')
    return None
    
class InvalidIDException(Exception):
    def __str__(self):
        return repr(self.args[0])

class Title(object):
    def __init__(self, id, fullplot = False):
        self.data = None
        if id is None:
            raise ValueError('Invalid IMDB id. (%s)' % id)
        elif isinstance(id, SearchResult):
            self.id = id.id
            if id.data is not None:
                self.data = id.data
        else:
            if isinstance(id, int) and (0 <= id <= 9999999):
                id = '%7s' % id
            m = re.search(r'(?:tt)?(?P<id>\d{7})', id, re.I)
            if m:
                self.id = 'tt%s' % m.group('id')
            else:
                raise ValueError('Invalid IMDB id. (%s)' % id)

        self.title = None
        self.genres = []
        self.rating = None
        self.votes = None
        self.top = None
        self.directors = []
        self.plot = None
        self.fullplot = None
        self.tagline = None
        self.release = None
        self.runtime = None
        self.alsoknownas = []
        self.countries = []
        self.languages = []
        self.cast = []
        self.year = None
        self.usercomment = None
        self.posterurl = None
        self.fullplot = fullplot
        self.update()
    
    def __repr__(self):
        return "imdb.Title('%s'%s)" % (self.id, (', fullplot=True' if self.fullplot else ''))

    def _infodiv(self, title, find=None):
        try:
            if not find:
                for el in self.infodivs[title].cssselect('.tn15more'):
                    el.drop_tree()
                return self.infodivs[title].text_content().replace('\n', '').strip()
            else:
                return [x.text.replace('\n', '').strip() for x in self.infodivs[title].findall('.//%s' % find)]
                
        except:
            if not find:
                return None
            else:
                return []


    def update(self):
        if self.data:
            data = self.data
        else:
            try:
                data = urllib2.urlopen('http://www.imdb.com/title/%s/' % self.id)
            except urllib2.HTTPError, e:
                raise ValueError('Invalid IMDB id. (%s)' % self.id)
            data = parse(data).getroot()

        self.infodivs = {}
        for e in data.cssselect('#tn15content div.info'):
            title = e.find('h5')
            content = e.find('div')
            if title is not None and title.text is not None and content is not None:
                self.infodivs[asciionly.sub('', title.text).lower()] = content
        for old, new in (('writer', 'writers'), ('director', 'directors')):
            if old in self.infodivs:
                self.infodivs[new] = self.infodivs[old]

        try:
            self.title = data.find('head').find('title').text
        except AttributeError:
            self.title = 'Unknown title'

        year = re.search(r'\((?P<year>\d{4})\)$', self.title)
        if year:
            self.year = int(year.group('year'))
            self.title = re.sub(r'\s\(\d{4}\)$', '', self.title)
        
        if 'directors' in self.infodivs:
            self.directors = [(x.text, (x.get('href').split('/')[2] if x.get('href', None) else None)) for x in self.infodivs['directors'].findall('.//a')]
        
        if 'writers' in self.infodivs:
            self.writers = [(x.text, (x.get('href').split('/')[2] if x.get('href', None) else None), x.tail.split(')')[0].split('(')[-1]) for x in self.infodivs['writers'].findall('.//a') if x.get('class', '') != 'tn15more']

        if 'genre' in self.infodivs:
            self.genres = [x.text for x in self.infodivs['genre'].findall('.//a') if '/Sections' in x.attrib.get('href')]
        if 'alsoknownas' in self.infodivs:
            self.alsoknownas = [self.infodivs['alsoknownas'].text.strip()]
            self.alsoknownas.extend([x.tail.strip() for x in self.infodivs['alsoknownas'].findall('.//br') if (hasattr(x, 'tail') and not x.tail is None)])
        try:
            rating = data.get_element_by_id('tn15rating')
            if rating is not None:
                self.rating = Decimal(rating.cssselect('div .starbar-meta b')[0].text.replace('/10', ''))
                self.votes = int(numonly.sub('', rating.cssselect('div .starbar-meta a')[0].text))
                top = rating.cssselect('div .starbar-special a')
                if top:
                    self.top = top[0].text
        except (AttributeError, IndexError):
            self.rating = None
            self.votes = None
            self.top = None
        

        self.plot = self._infodiv('plot').strip(' |')
        self.tagline = self._infodiv('tagline')
        try:
            releasedate, releasecountry = self._infodiv('releasedate').split('(', 2)
            self.release = (datetime.date(*datetime.datetime.strptime(releasedate.strip(), '%d %B %Y').timetuple()[:3]), releasecountry.strip(' )'))
        except ValueError:
            pass
        self.usercomment = self._infodiv('usercomments')
        self.runtime = self._infodiv('runtime')
        self.countries = self._infodiv('country', find='a')
        self.languages = self._infodiv('language', find='a')
        self.cast = []
        for x in data.cssselect('table.cast tr'):
            characters = []
            character = x.cssselect('.char a') or x.cssselect('.char')
            if character:
                for c in character:
                    characterid = c.get('href', None)
                    characterid = getid(characterid)
                    charactername = c.text and ''.join(c.text.split('/')[0]).strip() or None
                    characters.append((charactername, characterid))

            name = x.cssselect('.nm a') or x.cssselect('.nm')
            if name:
                nameid = name[0].get('href', None)
                nameid = nameid.split('/')[2] if nameid else nameid
                name = name[0].text.strip()
                self.cast.append(((name, nameid), characters))
        
        try:
            self.posterurl = data.cssselect('div.photo img')[0].get('src')
            if 'title_addposter' in self.posterurl:
                self.posterurl = None
        except (TypeError, KeyError):
            self.posterurl = None

        if self.fullplot:
            try:
                data = urllib2.urlopen("http://www.imdb.com/title/%s/plotsummary" % self.id)
                data = parse(data).getroot()
                self.fullplot = data.cssselect('p.plotpar')[0].text.strip()
            except (urllib2.HTTPError, AttributeError, IndexError):
                pass
        del self.infodivs
        self.data = None

class Name(object):
    def __init__(self, id):
        self.data = None
        if id is None:
            raise ValueError('Invalid IMDB id. (%s)' % id)
        elif isinstance(id, SearchResult):
            self.id = id.id
            if id.data is not None:
                self.data = id.data
        else:
            if isinstance(id, int) and (0 <= id <= 9999999):
                id = '%7s' % id
            m = re.search(r"(?:nm)?(?P<id>\d{7})", id, re.I)
            if m:
                self.id = 'nm%s' % m.group("id")
            else:
                raise ValueError("Invalid IMDB id. (%s)" % id)

        self.name = None
        self.birthdate = None
        self.birthplace = None
        self.deathdate = None
        self.deathdate = None
        self.biography = None
        self.trivia = None
        self.awards = None
        self.alternatenames = []
        self.filmography = []
        self.photourl = None
        self.update()

    def __repr__(self):
        return "imdb.Name('%s')" % self.id

    def _infodiv(self, title, find=None):
        try:
            if not find:
                for el in self.infodivs[title].cssselect('.tn15more'):
                    el.drop_tree()
                return self.infodivs[title].text_content().replace('\n', '').strip()
            else:
                return [x.text.replace('\n', '').strip() for x in self.infodivs[title].findall('.//%s' % find)]
                
        except:
            if not find:
                return None
            else:
                return []


    def update(self):
        if self.data:
            data = self.data
        else:
            try:
                data = urllib2.urlopen('http://www.imdb.com/name/%s/' % self.id)
            except urllib2.HTTPError:
                raise ValueError("Invalid IMDB id. (%s)" % self.id)
            data = parse(data).getroot()

        self.infodivs = {}
        for e in data.cssselect('#tn15content div.info'):
            title = e.find('h5')
            content = e.find('div')
            if title is not None and title.text is not None and content is not None:
                self.infodivs[asciionly.sub('', title.text).lower()] = content
        for old, new in (('writer', 'writers'), ('director', 'directors')):
            if old in self.infodivs:
                self.infodivs[new] = self.infodivs[old]

        try:
            self.name = data.find('head').find('title').text
        except AttributeError:
            self.name = 'Unknown name'
        
        if 'dateofbirth' in self.infodivs:
            birthattrs = self.infodivs['dateofbirth'].findall('.//a')
            if birthattrs:
                birthday = None
                birthyear = None
                for attr in birthattrs:
                    href = attr.get('href').lower()
                    attr.text = attr.text.strip()
                    if 'onthisday' in href:
                        birthday = attr.text
                    elif 'borninyear' in href:
                        birthyear = attr.text
                    elif 'bornwhere' in href:
                        self.birthplace = attr.text
                if birthday and birthyear:
                    try:
                        self.birthdate = datetime.date(*datetime.datetime.strptime('%s %s' % (birthday, birthyear), '%d %B %Y').timetuple()[:3])
                    except ValueError:
                        pass
                elif birthyear:
                    try:
                        self.birthdate = datetime.date(*datetime.datetime.strptime(birthyear, '%Y').timetuple()[:3])
                    except ValueError:
                        pass
            
        
        if 'dateofdeath' in self.infodivs:
            deathattrs = self.infodivs['dateofdeath'].findall('.//a')[:2]
            if deathattrs:
                for attr in deathattrs:
                    href = attr.get('href').lower()
                    attr.text = attr.text.strip()
                    if 'onthisday' in href:
                        deathday = attr.text
                    elif 'diedinyear' in href:
                        deathyear = attr.text
                        self.deatplace = attr.tail.strip(' ,\n')
                if deathday and deathyear:
                    try:
                        self.deathdate = datetime.date(*datetime.datetime.strptime('%s %s' % (deathday, deathyear), '%d %B %Y').timetuple()[:3])
                    except ValueError:
                        pass
                elif birthyear:
                    try:
                        self.deathdate = datetime.date(*datetime.datetime.strptime(deathyear, '%Y').timetuple()[:3])
                    except ValueError:
                        pass
                        
        self.biography = self._infodiv('minibiography')
        self.trivia = self._infodiv('trivia')
        self.awards = self._infodiv('awards')
        if self.awards:
            self.awards = re.sub(r'\s+', ' ', self.awards.strip())
        self.alternatenames = self._infodiv('alternatenames')
 
        try:
            self.photourl =  data.cssselect('div.photo img')[0].get('src')
            if "nophoto" in self.photourl:
                self.photourl = None
        except TypeError,KeyError:
            self.photourl = None

        
        try:
            data = urllib2.urlopen('http://www.imdb.com/name/%s/filmorate' % self.id)
            data = parse(data).getroot()
            self.filmography = [x.text for x in data.cssselect('.filmo li > a')]
        except urllib2.HTTPError:
            pass
        
        del self.infodivs
        self.data = None

class SearchResult(object):
    def __init__(self, name, id, data=None, **kwargs):
        self.name = name
        self.id = id
        self.data = data
        self.kwargs = kwargs
        
    def __repr__(self):
        return repr('<%s%s [%s]>' % (self.name, (' %s' % self.kwargs.get('extras', None) if self.kwargs.get('extras', None) else ''), self.id))

    __str__ = __repr__        


class TitleSearch(object):
    def __init__(self, query):
        self._query = query
        self.query = query
        self.query_year = None
        self.results = []
        self.bestmatch = None
        self.search()

    def __repr__(self):
        return "imdb.TitleSearch(%r)" % self._query
        
    def search(self, query=None):
        self.query = query or self.query
        self._query = query or self._query
        m = re.search(r'(?P<title>.+?)(?: \(?(?P<year>\d{4})(?:/[IV]*)?\)?)?$', self.query, re.I)
        if m.group('year'):
            self.query = m.group('title').strip()
            self.query_year = m.group('year').strip()

        try:
            data = urllib2.urlopen('http://www.imdb.com/find?s=tt&q=%s' % urllib2.quote(self.query.encode('latin-1')))
        except urllib2.HTTPError, e:
            raise ValueError('Unable to connect to IMDB.')
            
        if "/find?s=" not in data.url: # We've been redirected to the first result
            url = data.url
            data = parse(data).getroot()
            try:
                title = data.find('head').find('title').text
            except AttributeError:
                pass
            else:
                year = findyear.search(title)
                if year:
                    year = year.group('year')
                self.results.append(SearchResult(title, getid(url), data=data, year=year))
                self.bestmatch = self.results[0]
            
            
        else:
            data = parse(data).getroot()
            results = data.cssselect('td[valign="top"]')
           
            for t in results:
                i = None
                if len(t) >= 1 and t[0].tag == 'a' and t[0].text and t[0].tail:
                    i = 0
                elif len(t) >= 3 and t[2].tag == 'a' and t[2].text and t[2].tail:
                    i = 2
                if not i is None:
                    year = findyear.search(t[i].tail)
                    if year:
                        year = year.group('year')
                    self.results.append(SearchResult(t[i].text.strip(), getid(t[i].attrib['href']), extras=t[i].tail.strip(), year=year))

            if self.results:
                if self.query_year:
                    for r in self.results:
                        if r.name.lower() == self.query.lower() and self.query_year == r.year:
                            self.bestmatch = r
                            break

                    if not self.bestmatch:
                        for r in self.results:
                            if r.name.lower() == ('the %s' % self.query.lower()) and self.query_year == r.year:
                                self.bestmatch = r
                                break

                    if not self.bestmatch:
                        for r in self.results:
                            if r.name.lower() == ('"%s"' % self.query.lower()) and self.query_year == r.year:
                                self.bestmatch = r
                                break
                
                if not self.bestmatch:
                    for r in self.results:
                        if r.name.lower() == self.query.lower():
                            self.bestmatch = r
                            break

                if not self.bestmatch:
                    for r in self.results:
                        if r.name.lower() == ('the %s' % self.query.lower()):
                            self.bestmatch = r
                            break

                if not self.bestmatch:
                    for r in self.results:
                        if r.name.lower() == ('"%s"' % self.query.lower()):
                            self.bestmatch = r
                            break
                        
                if not self.bestmatch:
                    self.bestmatch = self.results[0]
                    

class NameSearch(object):
    def __init__(self, query):
        self.query = query
        self.results = []
        self.bestmatch = None
        self.search()
        
    def __repr__(self):
        return "imdb.NameSearch(%r)" % self.query
        
    def search(self, query=None):
        self.query = query or self.query
        try:
            data = urllib2.urlopen('http://www.imdb.com/find?s=nm&q=%s' % urllib2.quote(self.query.encode('latin-1')))
        except urllib2.HTTPError, e:
            raise ValueError('Unable to connect to IMDB.')
            
        if "/find?s=" not in data.url: # We've been redirected to the first result
            url = data.url
            data = parse(data).getroot()
            try:
                title = data.find('head').find('title').text
            except AttributeError:
                pass
            else:
                self.results.append(SearchResult(title, getid(url), data=data))
                self.bestmatch = self.results[0]
            
            
        else:
            data = parse(data).getroot()
            results = data.cssselect('td[valign="top"]')
           
            for t in results:
                i = None
                if len(t) >= 1 and t[0].tag == 'a' and t[0].text and t[0].tail:
                    i = 0
                elif len(t) >= 3 and t[2].tag == 'a' and t[2].text and t[2].tail:
                    i = 2
                if not i is None:
                    self.results.append(SearchResult(t[i].text.strip(), getid(t[i].attrib['href']), t[i].tail.strip()))

            if self.results:
                self.bestmatch = self.results[0]                    
            
if __name__ == "__main__":
    from pprint import pprint
    pprint(Title(TitleSearch('matrix').bestmatch).__dict__)
    pprint(Name(NameSearch('kate beckinsale').bestmatch).__dict__)

