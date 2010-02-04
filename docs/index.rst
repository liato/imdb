:mod:`imdb` --- A simple interface to the Internet Movie Database
=================================================================

..  module:: imdb
    :synopsis: A simple interface to the Internet Movie Database.


Retrieve information about movies, tv shows, actors and more from the
`Internet Movie Database <http://www.imdb.com/>`_.

.. toctree::
   :maxdepth: 1

   changes
   todo

Installation and requirements
-----------------------------

Make sure you have a working Python installation (>= 2.5) and that
`lxml <http://codespeak.net/lxml/>`_ is installed. Download the latest version
of imdb from `GitHub <http://github.com/liato/imdb>`_ or clone it using git.::

    git clone git://github.com/liato/imdb.git
    cd imdb
    python setup.py install


Usage
-----

The imdb lib has a series of different classes that perform different tasks.

* :class:`Title` --- Query `IMDB <http://www.imdb.com/>`__ for information about a movie or tv show.
* :class:`Name` --- Query `IMDB <http://www.imdb.com/>`__ for information about an actor/director etc.
* :class:`TitleSearch` --- Search `IMDB <http://www.imdb.com/>`__ for a movie or tv show.
* :class:`NameSearch` --- Search `IMDB <http://www.imdb.com/>`__ for an actor/director etc.

.. * :class:`Character` --- Query `IMDB <http://www.imdb.com/>`__ for information about a movieor tv character.
.. * :class:`SearchCharacter` --- Search `IMDB <http://www.imdb.com/>`__ for a character.

A quick run of the following code::
    
    import imdb, datetime
    
    
    s = imdb.TitleSearch('The Matrix')
    print 'Found %d matching titles, displaying some info from the best matching result:' % len(s.results)
    t = imdb.Title(s.bestmatch)
    print '%s (%d) was directed by %s\n' % (t.title, t.year, ' and '.join(d[0] for d in t.directors))
    
    sn = NameSearch('Kate Beckinsale')
    print 'Found %d matching names, displaying some info from the best matching result:' % len(sn.results)
    n = imdb.Name(sn.bestmatch)
    print '%s is %d years old and was born in %s' % (n.name, (datetime.date.today()-n.birthdate).days/365, n.birthplace)


Results in the following output::
    
    Found 10 matching titles, displaying some info from the best matching result:
    The Matrix (1999) was directed by Andy Wachowski and Lana Wachowski
    
    Found 4 matching names, displaying some info from the best matching result:
    Kate Beckinsale is 36 years old and was born in Finsbury Park, London, England, UK


The Title class
~~~~~~~~~~~~~~~

..  class:: Title(id, fullplot = False)

    Create a new a new :class:`Title` instance and retrieve the information for
    the movie with the given *id*.
 
    *id* should be a string containing a 7 character long numeric identifier or
    an integer between *0* and *9999999*.
    To retrieve information about `The Matrix
    <http://www.imdb.com/title/tt0133093/>`_ *id* could for example be any of
    the following:
    
    * ``'http://www.imdb.com/title/tt0133093/'``
    * ``'tle/tt0133093'``
    * ``133093``
    
    If *fullplot* is ``True`` an additional request will be made to retrieve the
    full plot summary.
    
    **Class methods:**

    ..  method:: update
    
        Refresh the information.
       
       
    **Class attributes and example values:**

    ..  attribute:: title
    
        String with movie/tv show title or or ``None`` if no title is found.::
        
            'The Matrix'
       
       
    ..  attribute:: year
    
        Integer with the production year or ``None`` if no year is found.::
        
            1999
       
       
    ..  attribute:: id
    
        String with the id of the title.::
        
            'tt0133093'
            
       
    ..  attribute:: ratings
    
        A :class:`decimal.Decimal`  with the user rating or ``None`` if no
        rating is found.::
        
            Decimal('8.7')
       
       
    ..  attribute:: votes
            
        Integer with number of votes or ``None`` if there are less than five
        votes.::
        
            353330
       
       
    ..  attribute:: top
            
        String with the movies Top 250/Bottom 100 position or ``None`` if no
        position is found.
        votes.::
        
            'Top 250: #25'
       
       
    ..  attribute:: directors
            
        A list of tuples containing the directors name and IMDB id.::
        
            [('Andy Wachowski', 'nm0905152'),
             ('Lana Wachowski', 'nm0905154')]
       
       
    ..  attribute:: writers
    
        A list of tuples containing the directors name, IMDB id and what they
        wrote.::
        
            [('Andy Wachowski', 'nm0905152', 'written by'),
             ('Lana Wachowski', 'nm0905154', 'written by')]


    ..  attribute:: release
    
        A tuple containing :class:`datetime.date` instance with the release
        date and a string with the country.::
            
            (datetime.date(1999, 3, 31), 'USA')


    ..  attribute:: genres
    
        List of genres.::
        
            ['Action', 'Adventure', 'Sci-Fi', 'Thriller']


    ..  attribute:: tagline
        
        String with the tagline or ``None`` if no taglinge is found.::
            
            'Free your mind'


    ..  attribute:: plot
        
        String with the plot summary or ``None`` if no plot summary is found.::
            
            'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against the controllers of it.'


    ..  attribute:: cast
        
        List of tuples, first value in every tuple is a tuple with the actors
        name and IMDB id and the second value in every tuple is a list of
        tuples containing the character name and IMDB id for all the actors
        characters.
        If an actor doesn't have any corresponding character listed the second
        value in the root tuple will be an empty list. If an actor or a
        character doesn't have an IMDB id ``None`` will be returned in its
        place.::
          
            [(('Keanu Reeves', 'nm0000206'), [('Neo', 'ch0000741')]),
            (('Laurence Fishburne', 'nm0000401'), [('Morpheus', 'ch0000746')]),
            (('Carrie-Anne Moss', 'nm0005251'), [('Trinity', 'ch0000744')]),
            (('Hugo Weaving', 'nm0915989'), [('Agent Smith', 'ch0000745')]),
            (('Gloria Foster', 'nm0287825'), [('Oracle', 'ch0000765')]),
            (('Joe Pantoliano', 'nm0001592'), [('Cypher', 'ch0000749')]),
            (('Marcus Chong', 'nm0159059'), [('Tank', 'ch0000761')]),
            (('Julian Arahanga', 'nm0032810'), [('Apoc', 'ch0000771')]),
            (('Matt Doran', 'nm0233391'), [('Mouse', 'ch0000766')]),
            (('Belinda McClory', 'nm0565883'), [('Switch', 'ch0000774')]),
            (('Anthony Ray Parker', 'nm0662562'), [('Dozer', 'ch0029765')]),
            (('Paul Goddard', 'nm0323822'), [('Agent Brown', 'ch0000769')]),
            (('Robert Taylor', 'nm0853079'), [('Agent Jones', 'ch0000781')]),
            (('David Aston', 'nm0040058'), [('Rhineheart', 'ch0000777')]),
            (('Marc Aden', 'nm0336802'), [('Choi', 'ch0030779')])]


    ..  attribute:: runtime
        
        String with the runtime or ``None`` if no runtime is found.::
            
            '136 min'


    ..  attribute:: languages
        
        List of languages used in the movie.::
            
            ['English'] 


    ..  attribute:: countries
        
        List of countries where the movie was recorded.::
            
            ['USA', 'Australia']


    ..  attribute:: posterurl
        
        String with the URL to the poster thumbnail or ``None`` if no poster
        is found.::
            
            'http://ia.media-imdb.com/images/M/MV5BMjEzNjg1NTg2NV5BMl5BanBnXkFtZTYwNjY3MzQ5._V1._SX100_SY140'


The Name class
~~~~~~~~~~~~~~

..  class:: Name(id)

    Create a new a new :class:`Name` instance and retrieve the information for
    the person with the given *id*.
 
    *id* should be a string containing a 7 character long numeric identifier or
    an integer between *0* and *9999999*.
    To retrieve information about `Kate Beckinsale
    <http://www.imdb.com/name/nm0000295/>`_ *id* could for example be any of
    the following:
    
    * ``'http://www.imdb.com/name/nm0000295/'``
    * ``'m/name/nm0000295'``
    * ``295``
    
    **Class methods:**

    ..  method:: update
    
        Refresh the information.
       
       
    **Class attributes and example values:**

    ..  attribute:: name
    
        String with persons name or ``None`` if no name is found.::
        
            'Kate Beckinsale'
       
       
    ..  attribute:: id
    
        String with the persons IMDB id.::
        
            'nm0000295'
       
       
    ..  attribute:: birthdate
    
        A :class:`datetime.date` instance with the persons birth date or ``None`` if no birth date is found.::
        
            datetime.date(1973, 7, 26)
       
       
    ..  attribute:: birthplace
    
        String with the persons place of birth or ``None`` if no birth place is found.::
        
            'Finsbury Park, London, England, UK'
            
       
    ..  attribute:: deathdate
    
        A :class:`datetime.date` instance with the persons death date or ``None`` if no death date is found.::
        
            None
       
       
    ..  attribute:: deathplace
    
        String with the persons place of death or ``None`` if no death place is found.::
        
            None
            
       
    ..  attribute:: biography
    
        String with a mini biography or ``None`` if no biography is found.::
        
            'Kate Beckinsale was born on 26 July 1973 in England, and has resided in...'
       
       
    ..  attribute:: trivia
            
        String with short bit of trivia about the person.::
        
            'Has a daughter, Lily Mo Sheen (b. 31 January 1999), with Welsh actor...'
       
       
    ..  attribute:: awards
            
        String with number of award wins/nominations or ``None`` if no info is
        found.::
        
            '2 wins & 15 nominations'
       
       
    ..  attribute:: photourl
            
        String with the URL to the photo thumbnail or ``None`` if no photo is
        found.
        
            'http://ia.media-imdb.com/images/M/MV5BMTY4Mzk2NjM2NV5BMl5BanBnXkFtZTYwODc2MDI2._V1._SX100_SY137_.jpg'
            
       
    ..  attribute:: filmography
    
        A list of the persons movies.::
        
            ['The Aviator',
             'Nothing But the Truth',
             'Much Ado About Nothing',
             "Everybody's Fine",
             'Emma',
             'Cold Comfort Farm',
             'Snow Angels',
             'One Against the Wind',
             'Underworld',
             'Click',
             'Underworld: Evolution',
             'Serendipity',
             'Laurel Canyon',
             'Shooting Fish',
             'Vacancy',
             'Brokedown Palace',
             'Haunted',
             'The Last Days of Disco',
             'Winged Creatures',
             'The Golden Bowl',
             'Prince of Jutland',
             'Uncovered',
             'Alice Through the Looking Glass',
             'Van Helsing',
             'Pearl Harbor',
             'Whiteout',
             'Tiptoes',
             'Ladies & Gentlemen: The Best of George Michael',
             'Van Helsing: Behind the Screams',
             'Van Helsing: The Man and the Monsters',
             'The 66th Annual Golden Globe Awards',
             'The World of Van Helsing',
             'Scream Awards 2006',
             'Live from the Red Carpet: The 2006 Golden Globe Awards',
             "A Life Without Limits: The Making of 'The Aviator'",
             'The 63rd Annual Golden Globe Awards',
             '2002 MTV Movie Awards',
             'VH1 Big in 05',
             '2006 MTV Movie Awards',
             '8th Annual Screen Actors Guild Awards',
             "Journey to the Screen: The Making of 'Pearl Harbor'",
             '52 Most Irresistible Women',
             'Emma',
             'The Last Days of Disco',
             'On the Set: Serendipity']


The TitleSearch class
~~~~~~~~~~~~~~~~~~~~~

..  class:: TitleSearch(query)

    Create a new a new :class:`TitleSearch` instance and retrieve all search
    results matching *query*.
 
    The *query* should be a string or a unicode string if *query* contains
    non-ASCII characters.
    
   
    **Class methods:**

    ..  method:: search([query])
    
        Perform a new search using *query*. If *query* is ``None`` the previous
        query will be used.
       
       
    **Class attributes and example values:**

    ..  attribute:: results
    
        List of :class:`SearchResult` objects. Returned in the same order as
        presented on `IMDB <http://www.imdb.com/find?s=tt&q=matrix>`_.::
        
            ['<The Matrix (1999) [tt0133093]>',
             '<The Matrix Reloaded (2003) [tt0234215]>',
             '<The Matrix Revolutions (2003) [tt0242653]>',
             '<The Transformers: The Movie (1986) [tt0092106]>',
             '<"Matrix" (1993) [tt0106062]>',
             '<The Matrix Revisited (2001) (V) [tt0295432]>',
             '<Enter the Matrix (2003) (VG) [tt0277828]>',
             '<Armitage III: Poly Matrix (1997) (V) [tt0109151]>',
             '<Armitage: Dual Matrix (2002) (V) [tt0303678]>',
             '<"Threat Matrix" (2003) [tt0364888]>',
             '<Sex and the Matrix (2000) (TV) [tt0274085]>',
             '<The Matrix: Path of Neo (2005) (VG) [tt0451118]>',
             '<Avatar (2004) [tt0270841]>',
             u'<Buhera m\xe1trix (2007) [tt0970173]>',
             "<Making 'The Matrix' (1999) (TV) [tt0365467]>",
             '<The Matrix Online (2005) (VG) [tt0390244]>',
             '<Crash Course (2003) (V) [tt0437137]>',
             "<Making 'Enter the Matrix' (2003) (V) [tt0391319]>",
             "<Return to Source: Philosophy & 'The Matrix' (2004) (V) [tt0439783]>",
             '<The Matrix Recalibrated (2004) (V) [tt0410519]>',
             "<Decoded: The Making of 'The Matrix Reloaded' (2003) (TV) [tt1074193]>",
             '<Jiang shi zhuo yao (1988) [tt0095399]>',
             "<That 70's Matrix (2001) [tt0339779]>",
             '<The Matrix Defence (2003) (TV) [tt0389150]>',
             '<The Matrix: The Movie Special (1999) (TV) [tt0438231]>',
             '<V-World Matrix (1999) (V) [tt0211096]>',
             '<M.A.N.: Matrix Adjusted Normal (1992) [tt0333846]>',
             '<Matrix. Wrong Number (2006) (V) [tt1543488]>',
             u'<New York 360\xba Presents: The 2007 Matrix Awards (2007) (TV) [tt1025014]>',
             '<The Father (2010) [tt1392983]>',
             '<The Living Matrix (2009) [tt1499960]>']        


    ..  attribute:: bestmatch
    
        A :class:`SearchResult` object containing the result that imdb
        determined best matched your query or ``None`` if no results were
        returned::
        
            '<The Matrix (1999) [tt0133093]>'
            

The NameSearch class
~~~~~~~~~~~~~~~~~~~~

..  class:: NameSearch(query)

    Create a new a new :class:`NameSearch` instance and retrieve all search
    results matching *query*.
 
    The *query* should be a string or a unicode string if *query* contains
    non-ASCII characters.
    
   
    **Class methods:**

    ..  method:: search([query])
    
        Perform a new search using *query*. If *query* is ``None`` the previous
        query will be used.
       
       
    **Class attributes and example values:**

    ..  attribute:: results
    
        List of :class:`SearchResult` objects. Returned in the same order as
        presented on `IMDB <http://www.imdb.com/find?s=nm&q=james+cameron>`_.::
        
            ['<James Cameron [nm0000116]>',
             '<James Cameron [nm2953992]>',
             '<James Cameron [nm1706599]>',
             '<James Cameron [nm0131603]>',
             '<James Cameron [nm0131606]>',
             '<James Cameron [nm0131605]>',
             '<James Cameron [nm0131604]>',
             '<James Cameron [nm0131609]>',
             '<James Cameron [nm0131608]>',
             '<James Cameron [nm0131607]>',
             '<James Cameron [nm2779873]>',
             '<Jim Davidson [nm0203375]>',
             '<Cameron J. Mooney [nm2993669]>',
             '<James O. Cameron [nm1776289]>',
             '<Sean James Cameron [nm1676822]>',
             '<James Andrew Cameron [nm2363483]>',
             '<Cameron James [nm3681965]>',
             '<Cameron James [nm2592892]>',
             '<James Cameran [nm3434475]>',
             '<Jameka Cameron [nm2724259]>']


    ..  attribute:: bestmatch
    
        A :class:`SearchResult` object containing the best matching result or
        ``None`` if no results were returned.

        .. note::        

            This attribute is provided for consistency and always returns
            ``results[0]`` if ``results`` is not empty.
        
        ::
        
            '<James Cameron [nm0000116]>'


The SearchResult class
~~~~~~~~~~~~~~~~~~~~~~

..  class:: SearchResult(name, id, data=None, **kwargs)

    Create a new a new :class:`SearchResult` instance containing name and IMDB
    id.
 
       
    **Class attributes:**

    ..  attribute:: name
    
        String with the name of the search result.
        
    

    ..  attribute:: id
    
        String with the search results IMDB id.
        

    ..  attribute:: data
    
        To prevent downloading the same content twice this attribute holds a
        :class:`lxml.html` object when a search is redirected to the
        first match.


    ..  attribute:: kwargs
    
        A dict with all keyword arguments.


License
-------
::
    Copyright (c) 2010 liato
   
    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:
   
    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.
   
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

