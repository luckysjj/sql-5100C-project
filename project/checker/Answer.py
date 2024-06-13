"""
EASY
  - 2  points each
  - 12 points total
"""

ans01 = ''' 
SELECT DISTINCT pname AS name, (2023 - birth) AS age
FROM People
WHERE death IS NULL;
'''

ans02 = '''
SELECT DISTINCT pname AS name
FROM People
WHERE pname LIKE '% % %';
'''

ans03 = '''
SELECT DISTINCT epname AS episode
FROM Episodes
WHERE epname LIKE 'Singapore %' 
   OR epname LIKE '% Singapore %'
   OR epname LIKE '% Singapore' 
   OR epname = 'Singapore';
'''

ans04 = '''
SELECT DISTINCT cname AS character, pname AS name
FROM PlaysAs
WHERE POSITION(' ' IN cname) = 0;
'''

ans05 = '''
SELECT DISTINCT tname AS title, syear
FROM Titles
WHERE syear >= 1960 AND tid NOT IN (SELECT tid FROM TvSeries)
ORDER BY syear;
'''

ans06 = '''
SELECT DISTINCT  tname AS title, runtime, syear
FROM Titles
WHERE rating >= 7.5 AND votes >= 10000
AND tid NOT IN (SELECT tid FROM TvSeries)
ORDER BY tname, runtime DESC, syear DESC;
'''




"""
MEDIUM
  - 4  points each
  - 20 points total
"""

ans07 = '''
SELECT p.pname AS director, t.tname AS title
FROM People p
JOIN Produces pr ON p.pname = pr.pname
JOIN Titles t ON pr.tid = t.tid
JOIN Genres g ON t.tid = g.tid
WHERE pr.task = 'director' AND g.genre = 'Drama';
'''

ans08 = '''
SELECT People.pname AS name, birth, death
FROM People
WHERE pname NOT IN (SELECT pname FROM PlaysIn);
'''

ans09 = '''
SELECT
  People.pname AS name,
  COUNT(DISTINCT Titles.tid) AS count,
  MIN(Titles.syear) AS earliest,
  MAX(Titles.runtime) AS longest
FROM
  People 
JOIN
  PlaysIn  ON People.pname = PlaysIn.pname
JOIN
  Titles  ON PlaysIn.tid = Titles.tid
WHERE
  People.pname NOT IN (
    SELECT pname
    FROM Produces
    WHERE pname NOT IN (
      SELECT pname
      FROM PlaysIn
    )
  )
GROUP BY
  People.pname
HAVING
  COUNT(DISTINCT Titles.tid) > 0
ORDER BY
  name;
'''

ans10 = '''
WITH DietrichFilms AS (
  SELECT COUNT(DISTINCT PlaysIn.tid) AS DietrichFilmCount
  FROM PlaysIn
  INNER JOIN People ON PlaysIn.pname = People.pname
  WHERE People.pname = 'Marlene Dietrich'
),

ActorFilms AS (
  SELECT People.pname, COUNT(DISTINCT Titles.tid) AS Count
  FROM PlaysIn
  INNER JOIN Titles ON PlaysIn.tid = Titles.tid
  INNER JOIN People ON PlaysIn.pname = People.pname
  WHERE Titles.syear >= 1950
  GROUP BY People.pname
)

SELECT ActorFilms.pname AS name, ActorFilms.Count
FROM ActorFilms, DietrichFilms
WHERE ActorFilms.Count >= DietrichFilms.DietrichFilmCount;
'''

ans11 = '''
SELECT DISTINCT p1.pname AS name, pa1.cname AS character
FROM PlaysAs pa1
JOIN PlaysAs pa2 ON pa1.tid = pa2.tid AND pa1.pname = pa2.pname AND pa1.cname <> pa2.cname
JOIN People p1 ON pa1.pname = p1.pname
ORDER BY p1.pname, pa1.cname;
'''




"""
HARD
  - 7  points each
  - 28 points total
"""

ans12 = '''
SELECT DISTINCT Titles.tname AS title, 
       Episodes.season, 
       Episodes.epnum AS episode, 
       Episodes.epname AS name
FROM Titles
JOIN Episodes ON Titles.tid = Episodes.tid
JOIN TvSeries ON Titles.tid = TvSeries.tid
WHERE Titles.eyear IS NOT NULL
ORDER BY Titles.tname ASC, Episodes.season DESC, Episodes.epnum ASC;
'''



ans13 = '''
WITH GenreCounts AS (
    SELECT g.genre, COUNT(*) AS count
    FROM Genres g
    INNER JOIN Titles t ON g.tid = t.tid
    GROUP BY g.genre
    HAVING COUNT(*) >= 5
),
DistinctCounts AS (
    SELECT count
    FROM GenreCounts
    GROUP BY count
    ORDER BY count ASC
    LIMIT 3
)
SELECT gc.genre, gc.count
FROM GenreCounts gc
WHERE gc.count IN (SELECT count FROM DistinctCounts)
ORDER BY gc.count DESC, gc.genre ASC;
'''

ans14 = '''
WITH dean_genres AS (
    SELECT g.genre
    FROM PlaysIn pi
    JOIN Titles t ON pi.tid = t.tid
    JOIN Genres g ON t.tid = g.tid
    WHERE pi.pname = 'James Dean'
    GROUP BY g.genre
), actors_matching_dean AS (
    SELECT pi.pname
    FROM PlaysIn pi
    JOIN Titles t ON pi.tid = t.tid
    JOIN Genres g ON t.tid = g.tid
    WHERE g.genre IN (SELECT genre FROM dean_genres)
    GROUP BY pi.pname
    HAVING COUNT(DISTINCT g.genre) >= (SELECT COUNT(*) FROM dean_genres)
    AND pi.pname <> 'James Dean'
), actors_expanded_genres AS (
    SELECT pi.pname, g.genre
    FROM PlaysIn pi
    JOIN Titles t ON pi.tid = t.tid
    JOIN Genres g ON t.tid = g.tid
    WHERE pi.pname IN (SELECT pname FROM actors_matching_dean)
    GROUP BY pi.pname, g.genre
)
SELECT ae.pname AS name, ae.genre
FROM actors_expanded_genres ae
ORDER BY ae.pname, ae.genre;
'''
ans15 = '''
WITH GenreCounts AS (
    SELECT syear, genre, COUNT(*) as count
    FROM Titles
    JOIN Genres USING(tid)
    WHERE syear >= 1960
    GROUP BY syear, genre
),
MaxCounts AS (
    SELECT syear, MAX(count) as maxcount
    FROM GenreCounts
    GROUP BY syear
),
PopularGenres AS (
    SELECT GenreCounts.syear, GenreCounts.genre
    FROM GenreCounts
    JOIN MaxCounts ON GenreCounts.syear = MaxCounts.syear AND GenreCounts.count = MaxCounts.maxcount
),
YearRange AS (
    SELECT generate_series(MIN(syear), MAX(syear)) as year
    FROM Titles
    WHERE syear >= 1960
),
FinalOutput AS (
    SELECT YearRange.year, PopularGenres.genre
    FROM YearRange
    LEFT JOIN PopularGenres ON YearRange.year = PopularGenres.syear
)
SELECT * FROM FinalOutput
ORDER BY year;
'''



ans = [
  ans01, ans02, ans03, ans04, ans05,
  ans06, ans07, ans08, ans09, ans10,
  ans11, ans12, ans13, ans14, ans15,
]


