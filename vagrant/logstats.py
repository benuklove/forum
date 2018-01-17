#!/home/benlove/projects/FSND-Virtual-Machine/venv/bin/python3

"""Database code for log analysis project."""

import psycopg2


def main():
    """One function to rule them all."""
    output_result()


def popular_articles():
    """Most popular three articles of all time.
    Connect, query, return result, and close connection.
    Format result for easy reading.
    """
    pg = psycopg2.connect(dbname="news")
    c = pg.cursor()
    query = "select title, count(*) as views from articles\
                as t1 join log as t2 on position(t1.slug in t2.path)<>0\
                 where t2.status = '200 OK'\
                  group by title order by views desc limit 3;"
    c.execute(query)
    result = c.fetchall()
    articles = ""
    for item in result:
        articles += "\"{}\" -- {} views\n".format(item[0], item[1])
    c.close()
    pg.close()
    return articles


def popular_authors():
    """Most popular authors of all time, sorted by article views.
    Connect, query, return result, and close connection.
    Format result for easy reading.
    """
    pg = psycopg2.connect(dbname="news")
    c = pg.cursor()
    base_query = "(select slug, name from articles join authors\
                     on articles.author = authors.id)"
    query = "select name, count(*) as views\
             from {} as t1 join log as t2 on position(t1.slug in t2.path)<>0\
              where t2.status = '200 OK' group by name order by views desc;"\
              .format(base_query)
    c.execute(query)
    result = c.fetchall()
    authors = ""
    for item in result:
        authors += "{: <25} {: >6} views\n".format(*item)
    c.close()
    pg.close()
    return authors


def high_errors():
    """On which days did more than 1% of requests lead to errors?
    Connect, query, return result, and close connection.
    In one query, two tables are made:
    one with columns of (day, successes),
    the other with columns of (day, errors).
    They are joined into a table with (day, percent).
    Format result for easy reading.
    """
    pg = psycopg2.connect(dbname="news")
    c = pg.cursor()
    table_1 = "(select date_trunc('day', log.time) \"day\",\
                 count(*) as successes from log where status = '200 OK'\
                  group by 1 order by 1)"
    table_2 = "(select date_trunc('day', log.time) \"day\",\
                 count(*) as errors from log where status != '200 OK'\
                  group by 1 order by 1)"
    query = "select ok.day, (1.0*errors/successes) as percent\
             from {} as ok join {} as err\
             on ok.day = err.day \
             where (1.0*errors/successes)>0.01;"\
             .format(table_1, table_2)
    c.execute(query)
    result = c.fetchall()
    errors = ""
    for item in result:
        d = item[0]
        d.strftime("%b %d, %Y")
        percent = round((item[1] * 100), 1)
        errors += "{: <15} {}% errors".format(d.strftime('%b %d, %Y'), percent)
    c.close()
    pg.close()
    return errors


def output_result():
    """Log results to file"""
    errors = high_errors()
    authors = popular_authors()
    articles = popular_articles()
    with open("output.txt", "a") as text_file:

        text_file.write("Top three most popular articles\n"
                        "--------------------------------------------------"
                        "\n{}\n\n"
                        .format(articles))

        text_file.write("Most popular authors of all time,"
                        " sorted by article views\n--------------------------"
                        "-------------------------------\n{}\n\n"
                        .format(authors))

        text_file.write("Days with errors greater than 1%\n"
                        "--------------------------------\n{}\n\n"
                        .format(errors))


if __name__ == '__main__':
    main()
