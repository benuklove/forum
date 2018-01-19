"The Backend"
=====================

Logs Analysis Project
---------------------------------------------------------------------------

### This project sets up a mock PostgreSQL database for a fictional news website. The provided Python script uses the psycopg2 library to query the database and produce a report that answers the following three questions:

1.  What are the most popular three articles of all time?
2.  Who are the most popular article authors of all time?
3.  On which days did more than 1% of requests lead to errors?

#### Relevant Files

[Database Tables](https://github.com/benuklove/forum/blob/master/vagrant/news_tables.png) - from newsdata.sql (not included, but can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip))
- authors
  - columns: (primary - id), name, bio
- articles
  - columns: (primary - id), (foreign author to authors.id), title, slug, lead, body, time
- log
  - columns: (primary - id), ip, method, status, time, path

Python script to query the database, return results as text file
- [logstats.py](https://github.com/benuklove/forum/blob/master/vagrant/logstats.py)

Resulting text file with query output
- [output.txt](https://github.com/benuklove/forum/blob/master/vagrant/output.txt)

#### Requirements

The only non-standard library you will need is psycopg.

This project runs on Python.  It will not run on "legacy Python".

#### How to run

From the terminal, in the same directory as newsdata.sql, and after loading the data with `psql -d news -f newsdata.sql`, type python logstats.py.

The file `output.txt` will be created with the relevant query answers.
