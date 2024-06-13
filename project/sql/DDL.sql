CREATE TABLE People (
  pname  TEXT PRIMARY KEY,
  birth  INT  NOT NULL CHECK (birth > 0),
  death  INT  CHECK (death > 0 AND death > birth)
);

CREATE TABLE Titles (
  tid      VARCHAR(10) PRIMARY KEY,
  tname    TEXT NOT NULL,
  syear    INT  NOT NULL CHECK (syear > 0),
  eyear    INT  CHECK (eyear >= syear),
  runtime  INT  NOT NULL CHECK (runtime > 0),
  rating   NUMERIC  CHECK (rating >= 0 and rating <= 10),
  votes    INT      CHECK (votes >= 0)
);

CREATE TABLE TvSeries (
  tid  VARCHAR(10) PRIMARY KEY
    REFERENCES Titles (tid)
);

CREATE TABLE Genres (
  tid    VARCHAR(10)  REFERENCES Titles (tid),
  genre  VARCHAR(200),
  PRIMARY KEY (tid, genre)
);

CREATE TABLE Episodes (
  tid     VARCHAR(10)  REFERENCES TvSeries (tid)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  season  INT CHECK (season > 0),
  epnum   INT CHECK (epnum > 0),
  epname  TEXT,
  PRIMARY KEY (tid, season, epnum)
);

CREATE TABLE Produces (
  tid    VARCHAR(10)  REFERENCES Titles (tid),
  pname  TEXT  REFERENCES People (pname),
  task   VARCHAR(100),
  PRIMARY KEY (tid, pname, task)
);

CREATE TABLE Characters (
  cname  TEXT  PRIMARY KEY
);

CREATE TABLE PlaysIn (
  pname  TEXT  REFERENCES People (pname),
  tid    VARCHAR(10)  REFERENCES Titles (tid),
  PRIMARY KEY (pname, tid)
);

CREATE TABLE PlaysAs (
  pname  TEXT,
  tid    VARCHAR(10),
  cname TEXT  REFERENCES Characters (cname),
  FOREIGN KEY (pname, tid) REFERENCES PlaysIn (pname, tid),
  PRIMARY KEY (pname, tid, cname)
);
