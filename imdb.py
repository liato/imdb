import re
import urllib2

from lxml.html import parse

asciionly = re.compile(r'[^a-zA-Z]')

class InvalidIDException(Exception):
    def __str__(self):
        return repr(self.args[0])

class Title(object):
    def __init__(self, id, fullplot = False):
        if isinstance(id, int):
            id = str(id)
        m = re.search(r'(?:tt)?(?P<id>\d{7})', id, re.I)
        if m:
            self.id = m.group('id')
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


    def _infodiv(self, title, find=None):
        try:
            if not find:
                return self.infodivs[title].text.replace('\n', '').strip()
            else:
                return [x.text.replace('\n', '').strip() for x in self.infodivs[title].findall('.//%s' % find)]
                
        except:
            if not find:
                return None
            else:
                return []


    def update(self):
        try:
            data = urllib2.urlopen('http://www.imdb.com/title/tt%s/' % self.id)
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
            self.title = data.find('head').find('titles').text
        except AttributeError:
            self.title = 'Unknown title'

        year = re.search(r'\((?P<year>\d{4})\)$', self.title)
        if year:
            self.year = year.group('year')
            self.title = re.sub(r'\s\(\d{4}\)$', '', self.title)
        
        if 'directors' in self.infodivs:
            self.directors = [x.text for x in self.infodivs['directors'].findall('.//a')]
        
        if 'genre' in self.infodivs:
            self.genres = [x.text for x in self.infodivs['genre'].findall('.//a') if '/Sections' in x.attrib.get('href')]
        if 'alsoknownas' in self.infodivs:
            self.alsoknownas = [self.infodivs['alsoknownas'].text.strip()]
            self.alsoknownas.extend([x.tail.strip() for x in self.infodivs['alsoknownas'].findall('.//br') if (hasattr(x, 'tail') and not x.tail is None)])
        try:
            rating = data.get_element_by_id('tn15rating')
            if rating is not None:
                self.rating = rating.cssselect('div .starbar-meta b')[0].text
                self.votes = rating.cssselect('div .starbar-meta a')[0].text
                top = rating.cssselect('div .starbar-special a')
                if top:
                    self.top = top[0].text
        except (AttributeError, IndexError):
            self.rating = None
            self.votes = 'No votes'
            self.top = None
        

        self.plot = self._infodiv('plot')
        self.tagline = self._infodiv('tagline')
        self.release = self._infodiv('releasedate')
        self.usercomment = self._infodiv('usercomments')
        self.runtime = self._infodiv('runtime')
        self.countries = self._infodiv('country', find='a')
        self.languages = self._infodiv('language', find='a')
        self.cast = []
        for x in data.cssselect('table.cast tr'):
            character = x.cssselect('.char a') or x.cssselect('.char')
            if character:
                character = character[0].text and character[0].text.strip() or None

            name = x.cssselect('.nm a') or x.cssselect('.nm')
            if name:
                name = name[0].text.strip()
                self.cast.append((name, character))
        
        try:
            self.posterurl = data.cssselect('div.photo img')[0].get('src')
            if 'title_addposter' in self.posterurl:
                self.posterurl = None
        except (TypeError, KeyError):
            self.posterurl = None

        if self.fullplot:
            try:
                data = urllib2.urlopen("http://www.imdb.com/title/tt%s/plotsummary" % self.id)
                data = parse(data).getroot()
                self.fullplot = data.cssselect('p.plotpar')[0].text.strip()
            except (urllib2.HTTPError, AttributeError, IndexError):
                pass    

class Name(object):
    def __init__(self, id):
        if isinstance(id, int):
            id = str(id)
        m = re.search(r"(?:nm)?(?P<id>\d{7})", id, re.I)
        if m:
            self.id = m.group("id")
        else:
            raise ValueError("Invalid IMDB id. (%s)" % id)

        self.name = None
        self.birthdate = None
        self.birthplace = None
        self.deathdate = None
        self.biography = None
        self.trivia = None
        self.awards = None
        self.altnames = []
        self.filmography = []
        self.photourl = None
        self.update()


    def _infodiv(self, title, find=None):
        try:
            if not find:
                return self.infodivs[title].text.replace('\n', '').strip()
            else:
                return [x.text.replace('\n', '').strip() for x in self.infodivs[title].findall('.//%s' % find)]
                
        except:
            if not find:
                return None
            else:
                return []


    def update(self):
        try:
            data = urllib2.urlopen('http://www.imdb.com/name/nm%s/' % self.id)
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
            
        self.birthdate = ' '.join(self._infodiv('dateofbirth', find='a')[:2])
        try:
            self.birthplace = self._infodiv('dateofbirth', find='a')[2]
        except IndexError:
            pass
        
        self.deathdate = ' '.join(self._infodiv('dateofdeath', find='a')[:2]) or None
        self.biography = self._infodiv('minibiography')
        self.trivia = self._infodiv('trivia')
        self.awards = self._infodiv('awards')
        if self.awards:
            self.awards = re.sub(r'\s+', ' ', self.awards.strip())
        self.altnames = self._infodiv('alternatenames')
 
        try:
            self.photourl =  data.cssselect('div.photo img')[0].get('src')
            if "nophoto" in self.photourl:
                self.photourl = None
        except TypeError,KeyError:
            self.photourl = None

        
        try:
            data = urllib2.urlopen('http://www.imdb.com/name/nm%s/filmorate' % self.id)
            data = parse(data).getroot()
            self.filmography = [x.text for x in data.cssselect('.filmo li > a')]
        except urllib2.HTTPError:
            pass



class Search(object):
    def __init__(self, string, name=False):
        self.searchstring = string
        self.result = None
        self.name = name
        self.update()

    def update(self, searchstring = None):
        if not searchstring:
            searchstring = self.searchstring
        else:
            self.searchstring = searchstring
       
        m = re.search(r"(?P<result>(?:nm|tt)\d{7})", searchstring, re.I)
        if m:
            self.result = m.group("result")
            return
        
        if self.name:
            regex = [r"<a href=\"\/name\/(nm\d{7})\/\"[^>]*>([^<]*?)</a>"]
            url = "http://www.imdb.com/find?s=nm&q=%s" % urllib2.quote(searchstring.encode('latin-1'))
        else:
            m = re.search(r"(?P<movie>.+?)(?: \(?(?P<year>\d{4})\)?)?$", searchstring, re.I)
            movie = m.group("movie").strip(" ")
            year = m.group("year")
            movie = re.escape(movie)
    
            regex = []
            if year:
               year = re.escape(year)
               regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+")</a> \("+year+"\)")
               regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+", The)</a> \("+year+"\)")
               regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>(\""+movie+"\")</a> \("+year+"\)")
               regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?"+movie+"[^<]*?)</a> \("+year+"\)")
               regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?)</a> \("+year+"\)")
            regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+")</a>")
            regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>("+movie+", The)</a>")
            regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>(\""+movie+"\")</a>")
            regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?"+movie+"[^<]*?)</a>")
            regex.append(r"<a href=\"\/title\/(tt\d{7})\/\"[^>]*>([^<]*?)</a>")
            url = "http://www.imdb.com/find?s=tt&q=%s" % urllib2.quote(m.group("movie").encode('latin-1'))
        
    
        url = urllib2.urlopen(url)
        if "/find?s=" not in url.url: # We've been redirected to the first result
            m = re.search(r"/(?:name|title)/(?P<result>(?:nm|tt)\d{7})", url.url, re.I)
            if m:
                self.result = m.group("result")
                return
            
        #data = _unescape(url.read())
        data = url.read()

        self.result = None
        for x in regex:
            m = re.search(x, data, re.IGNORECASE)
            if m:
                self.result = m.group(1)
                break
            
if __name__ == "__main__":
    from pprint import pprint
    t = Title("tt0499549")
    pprint(t.__dict__)
    
    n = Name("nm0000295")
    pprint(n.__dict__)