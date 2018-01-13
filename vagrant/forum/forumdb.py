# "Database code" for the DB Forum.

import psycopg2
import datetime
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  pg = psycopg2.connect(dbname="forum")
  c = pg.cursor()
  query = "select content, time from posts order by time desc;"
  c.execute(query)
  return c.fetchall()
  pg.close()
  # return reversed(POSTS)

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  pg = psycopg2.connect(dbname="forum")
  c = pg.cursor()
  # Using a query parameter instead of string concatenation
  cleaned = bleach.clean(content)
  c.execute("insert into posts values (%s)", (cleaned,))
  pg.commit()
  pg.close()
  # POSTS.append((content, datetime.datetime.now()))
