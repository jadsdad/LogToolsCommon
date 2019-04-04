import MySQLdb as mariadb
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

conn = mariadb.connect(db='catalogue', user='simon',passwd='phaedra74',use_unicode=True, charset='utf8', read_default_file='~/.my.cnf')
basedir = str(Path.home()) + "/Charts"

def add_chart_history(Y, Q, artistid, albumid, rank, score, tyr):
    sql = "INSERT INTO chart_history VALUES ({}, {}, {}, {}, {}, {}, {});".format(Y, Q, artistid, albumid, rank, score, tyr)
    execute_sql(sql)

def add_rolling_chart_history(chartdate, artistid, albumid, rank, score, chartrun):
    sql = "INSERT INTO chart_history_rolling VALUES ('{}', {}, {}, {}, {}, {});".format(chartdate, artistid, albumid, rank, score, chartrun)
    execute_sql(sql)

def total_albums():
    sql = "SELECT COUNT(albumid) FROM album where SourceID<>6;"
    results = get_results(sql)
    return results[0][0]

def total_artists():
    sql = "SELECT COUNT(artistid) FROM artist;"
    results = get_results(sql)
    return results[0][0]

def get_results(sql):
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    return results

def total_albums_played():
    sql = "SELECT SUM(played) FROM album where sourceid<>6;"
    results = get_results(sql)
    return results[0][0]

def total_time():
    sql = "SELECT SUM(tracklength) FROM tracklengths inner join album on tracklengths.albumid = album.albumid " \
          "where album.sourceid<>6;"
    results = get_results(sql)
    return results[0][0]

def total_excl_bonus():
    sql = "SELECT SUM(tracklength) FROM tracklengths inner join album on tracklengths.albumid = album.albumid " \
          "where album.sourceid<> 6 and BonusTrack = 0;"
    results = get_results(sql)
    return results[0][0]

def execute_sql(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def format_to_MS(seconds):
    if type(seconds) == Decimal:
        seconds = float(seconds)

    mytime = timedelta(seconds=seconds)
    return "{:2d}:{:02d}".format(int(mytime.seconds // 60), int(mytime.seconds % 60))


def shorten_by_word(text, length):
    if text is None:
        return None

    wordsplit = text.split(" ")
    output = ""
    for w in wordsplit:
        if len(output) + len(w) < length:
            if len(output) > 0:
                output += " "
            output += w
        else:
            return output
    return output