#!/home/benlove/projects/FSND-Virtual-Machine/venv/bin/python3
"""Database code for log analysis project."""

import psycopg2


def main():
    """One function to rule them all."""
    output_result()


def get_query_results(database, query):
    """Helper function to make generic queries to a PostgreSQL database.
    Connect, query, return result, and close connection.
    Two parameters required:
    Database name (as a string),
    Query to be made.
    """
    pg = psycopg2.connect(dbname=database)
    c = pg.cursor()
    c.execute(query)
    result = c.fetchall()
    c.close()
    pg.close()
    return result


def popular_articles():
    """Most popular three articles of all time.
    Format result for easy reading.
    """
    query = """
        select title, views
            from
                (select path, count(*) as views from log
                group by path, status)
            as t2
            join articles
                on t2.path = concat('/article/', articles.slug)
            order by views desc
            limit 3;
        """
    result = get_query_results("news", query)
    articles = ""
    for item in result:
        articles += "\"{}\" -- {} views\n".format(item[0], item[1])
    return articles


def popular_authors():
    """Most popular authors of all time, sorted by article views.
    Format result for easy reading.
    """
    query = """
            select name, count(*) as views
                from
                (select slug, name
                    from 
                    articles join authors on
                    articles.author = authors.id)
                as t1
                join log as t2 on
                t2.path = concat('/article/', t1.slug)
            group by name
            order by views desc;
            """
    result = get_query_results("news", query)
    authors = ""
    for item in result:
        authors += "{: <25} {: >6} views\n".format(*item)
    return authors


def high_errors():
    """On which days did more than 1% of requests lead to errors?
    In one query, two tables are made:
    one with columns of (day, successes),
    the other with columns of (day, errors).
    They are joined into a table with (day, percent).
    Format result for easy reading.
    """
    table_1 = """(select date_trunc('day', log.time) \"day\",
                    count(*) as successes
                    from log
                        where status = '200 OK'
                        group by 1
                        order by 1)"""
    table_2 = """(select date_trunc('day', log.time) \"day\",
                    count(*) as errors
                    from log
                        where status != '200 OK'
                        group by 1
                        order by 1)"""
    query = "select ok.day, (1.0*errors/(errors + successes)) as percent\
             from {} as ok join {} as err\
             on ok.day = err.day \
             where (1.0*errors/(errors + successes))>0.01;"\
             .format(table_1, table_2)
    result = get_query_results("news", query)
    errors = ""
    for item in result:
        d = item[0]
        d.strftime("%b %d, %Y")
        percent = round((item[1] * 100), 3)
        errors += "{: <15} {}% errors".format(d.strftime('%b %d, %Y'), percent)
    return errors


def output_result():
    """Log results to file."""
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
