import sqlite3
import time
import datetime


conn = sqlite3.connect('master.db')

c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS tennis(player TEXT, Pinnacle REAL, WillHill REAL, betThreeSixFive REAL, Bookmaker REAL, BetOnline REAL, TheGreekSportsbook REAL, JustBet REAL, SportsInteraction REAL, WagerWeb REAL, FiveDimes REAL)')



"""
Colunas:
player
betfairBack
betfairLay
williamhill
ladbrokes
"""

def dynamic_data_entry(column,entry):
	c.execute("INSERT INTO tennis(" + column + ") VALUES(?)",
				(str(entry),))
	conn.commit()


def update(player,column,entry):
	c.execute('SELECT * FROM tennis')
	c.execute("UPDATE tennis SET " + column + " = " + str(entry) + " WHERE player = '" + player + "'")
	conn.commit()

def read_from_db(player):
	c.execute("SELECT * FROM tennis WHERE player = '" + player + "'")
	return list(c.fetchall())

create_table()


