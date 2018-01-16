#!/home/benlove/projects/FSND-Virtual-Machine/venv/bin/python3

# Database code for log analysis project

import datetime as dt
import psycopg2


def main():
    popular_articles()
    popular_authors()
    high_errors()
    output_result()


# Most popular three articles of all time?
def popular_articles():
    pg = psycopg2.connect(dbname="news")
    c = pg.cursor()
    query = "select title, count(*) as views from articles as t1 join log as t2 on position(t1.slug in t2.path)<>0 where t2.status = '200 OK' group by title order by views desc limit 3;"
    c.execute(query)
    result = c.fetchall()
    for item in result:
        print("\"{}\" -- {} views".format(item[0], item[1]))
    # print(result)
    c.close()
    pg.close()
    return result

# Most popular authors of all time, sorted by article views?
def popular_authors():
    pg = psycopg2.connect(dbname="news")
    c = pg.cursor()
    base_query = "(select slug, name from articles join authors on articles.author = authors.id)"
    query = "select name, count(*) as views from {} as t1 join log as t2 on position(t1.slug in t2.path)<>0 where t2.status = '200 OK' group by name order by views desc;".format(base_query)
    c.execute(query)
    result = c.fetchall()
    for item in result:
        print("{: <25} {: >6} views".format(*item))
    # print(result)
    c.close()
    pg.close()
    return result

# On which days did more than 1% of requests lead to errors?
def high_errors():
    pg = psycopg2.connect(dbname="news")
    c = pg.cursor()
    table_1 = "(select date_trunc('day', log.time) \"day\", count(*) as successes from log where status = '200 OK' group by 1 order by 1)"
    table_2 = "(select date_trunc('day', log.time) \"day\", count(*) as errors from log where status != '200 OK' group by 1 order by 1)"
    query = "select ok.day, (1.0*errors/successes) as percent from {} as ok join {} as err on ok.day = err.day where (1.0*errors/successes)>0.01;".format(table_1, table_2)
    c.execute(query)
    result = c.fetchall()
    for item in result:
        d = item[0]
        d.strftime("%b %d, %Y")
        percent = round((item[1] * 100), 1)
        print("{: <15} {}%".format(d.strftime('%b %d, %Y'), percent))
    c.close()
    pg.close()
    return result

# Log success/error counts
def output_result():
    pass
# with open("output.txt", "a") as text_file:
#     text_file.write("Successes: {} ".format(successes))
#     text_file.write("Errors: {}\n".format(errors))


if __name__ == '__main__':
    main()
