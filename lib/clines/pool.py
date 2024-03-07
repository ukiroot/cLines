import sys, os
import sqlite3
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))

con = sqlite3.connect(os.path.join(os.path.expanduser("~"), ".db.sqlite"))
cur = con.cursor()

def get_bridges(qantity):
    list = []
    for i in range(qantity):
        list.append(get_resources_from_db('bridges'))
    return list


def get_euts(qantity):
    list = []
    for i in range(qantity):
        list.append(get_resources_from_db('euts'))
    return list


def get_linuxchans(qantity):
    list = []
    for i in range(qantity):
        list.append(get_resources_from_db('linuxchans'))
    return list


def get_resources_from_db(table_name):
    cur.execute("BEGIN EXCLUSIVE;").fetchone()
    resource = cur.execute("SELECT name FROM {} LIMIT 1;".format(table_name)).fetchone()[0]
    cur.execute("DELETE from {} WHERE name='{}';".format(table_name, resource)).fetchone()
    cur.execute("COMMIT;").fetchone()
    return resource


def release_euts(euts):
    release_resources_in_db('euts', euts)


def release_bridges(bridges):
    release_resources_in_db('bridges', bridges)


def release_linuxchans(linuxchans):
    release_resources_in_db('linuxchans', linuxchans)


def release_resources_in_db(table_name, resourses):
    for resource in resourses:
       cur.execute("BEGIN EXCLUSIVE;").fetchone()
       cur.execute("INSERT INTO {} (name) VALUES ('{}')".format(table_name, resource)).fetchone()
       cur.execute("COMMIT;").fetchone()
