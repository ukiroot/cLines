import sqlite3
import pytest

@pytest.mark.preparation_resources
def test_init_db_with_resources():
    con = sqlite3.connect("/tmp/db.sqlite")
    cur = con.cursor()
    cur.executescript('''
CREATE TABLE IF NOT EXISTS euts (
    name text NOT NULL);
CREATE TABLE IF NOT EXISTS bridges (
    name text NOT NULL);
CREATE TABLE IF NOT EXISTS linuxchans (
    name text NOT NULL);

DELETE FROM euts;
DELETE FROM bridges;
DELETE FROM linuxchans;

INSERT INTO euts (name) VALUES ('EUT_1');
INSERT INTO euts (name) VALUES ('EUT_2');
INSERT INTO euts (name) VALUES ('EUT_3');
INSERT INTO euts (name) VALUES ('EUT_4');
INSERT INTO euts (name) VALUES ('EUT_5');
INSERT INTO euts (name) VALUES ('EUT_6');
INSERT INTO euts (name) VALUES ('EUT_7');
INSERT INTO euts (name) VALUES ('EUT_8');

INSERT INTO bridges (name) VALUES ('mighty_bridge_1');
INSERT INTO bridges (name) VALUES ('mighty_bridge_2');
INSERT INTO bridges (name) VALUES ('mighty_bridge_3');
INSERT INTO bridges (name) VALUES ('mighty_bridge_4');

INSERT INTO linuxchans (name) VALUES ('ursamajor');
INSERT INTO linuxchans (name) VALUES ('ursaminor');
INSERT INTO linuxchans (name) VALUES ('lupus');
INSERT INTO linuxchans (name) VALUES ('virgo');
INSERT INTO linuxchans (name) VALUES ('vulpecula');
INSERT INTO linuxchans (name) VALUES ('aquarius');
INSERT INTO linuxchans (name) VALUES ('aries');
INSERT INTO linuxchans (name) VALUES ('pisces');''')