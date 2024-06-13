import psycopg as pg

"""
NOTE: $ is part of terminal/cmd prompt
      and not part of command

Depending on how you install PostgreSQL,
  PG_HOME or PATH may not contain the path
  to pg_config.

If you encounter error when installing psycopg
  using the following command

$ pip install psycopg

  or

$ python3 -m pip install psycopg

  then you may need to add the following manually

1. Export PG_HOME
$ export PG_HOME=/Library/PostgreSQL/16

2. Export PATH
$ export PATH=$PATH:$PG_HOME/bin

3. Then install psycopg again
$ pip install psycopg

  or

$ python3 -m pip install psycopg

If you still encounter an error, you may
need to install additional binaries using

$ pip install "psycopg[binary,pool]"

  or

$ python3 -m pip install "psycopg[binary,pool]"
"""

class DB():
  def __init__(self, **configs):
    port = configs.get('port', 5432)
    host = f"'{configs.get('host', 'localhost' )}'"
    name = f"'{configs.get('name', 'postgres'  )}'"
    user = f"'{configs.get('user', 'postgres'  )}'"
    pswd = f"'{configs.get('pswd', 'adminadmin')}'"

    self.res = []
    try:
      self.conn = pg.connect(f'host={host} dbname={name} user={user} port={port} password={pswd}')
    except Exception as e:
      self.open = False
    else:
      self.open = True

  def __repr__(self):
    return self.conn.__repr__() if self.open else 'Connection Closed'

  def exec(self, command):
    if self.open:
      try:
        cur = self.conn.cursor()
        cur.execute(command)
      except pg.DatabaseError as e:
        self.conn.rollback()
        self.res.append(e)
      else:
        self.res.append(cur.statusmessage)
        self.conn.commit()
    return self

  def fetch(self, query, *args):
    if self.open:
      try:
        cur = self.conn.cursor()
        if len(args) == 0:
          cur.execute(query)
        else:
          cur.execute(query, args)
        res = cur.fetchall()
      except pg.DatabaseError as e:
        print(e)
        self.res.append(e)
      else:
        res = ([desc[0] for desc in cur.description], res)
        self.res.append(res)
    return self

  def close(self):
    self.conn.close()
    return self
