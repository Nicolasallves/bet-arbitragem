from tools import calculator as calc
from tools import sqlitecommands as sq
from sbr import sbrscraper as sbr
from betfair import bfairapi as b
from betfair import userinfo
from betfair import bfairtools as btools
from pandas import DataFrame
from pinnacle import pinnaclexml as pin
from datetime import date

"""
## Conexão no Tor 
import socket
import socks
 
def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9150, True)
    socket.socket = socks.socksocket
    print("Conectado ao Tor!")
"""

# Conexão sql
con = sq.conn



def writeSBR():
  todays_date = str(date.today()).replace('-','')
  soup, time_ml = sbr.soup_url('ML', todays_date)
  df = sbr.parse_and_write_data(soup,todays_date,time_ml) # Getting dataframe of SBR odds
  df.to_sql('tennis',con,schema=None,if_exists='replace',index=True,index_label=True,chunksize=None,dtype=None) # Writing dataframe to master.db -- tennis.


# atualiza odds
def writePinnacle():
  fullListing = pin.UpdateFeed()[0]
  for event in fullListing:
    try:
      playerOne = pin.sortType(event,'Tennis','Match')[0].lower().replace("'","")
      playerOneOdds = pin.sortType(event,'Tennis','Match')[2]
      playerTwo = pin.sortType(event,'Tennis','Match')[3].lower().replace("'","")
      playerTwoOdds = pin.sortType(event,'Tennis','Match')[5]
      print playerOne, playerOneOdds, playerTwo, playerTwoOdds
      #sq.dynamic_data_entry('Pinnacle',playerOne)
      sq.update(playerOne,'Pinnacle',playerOneOdds)
      sq.update(playerTwo,'Pinnacle',playerTwoOdds)
    except TypeError:
      pass
    except Exception as e: 
      print "Erro ao escrever o Pinnacle: " + e
  con.commit()

# add nomes da betfair

# att odds betfair
def writeBetfair():
  market_catalogue = b.getMarketCatalogue('2')  
  playerOne = []
  playerTwo = []
  backOddsOne = []
  backOddsTwo = []
  for i in range(len(market_catalogue)):
    playerOne.append(bt.bfairRenamer(market_catalogue[i]['runners'][0]['runnerName']))
    playerTwo.append(bt.bfairRenamer(market_catalogue[i]['runners'][1]['runnerName']))
    backOddsOne.append(bt.playerOdds(market_catalogue[i]['marketId'],0,'Back'))
    backOddsTwo.append(bt.playerOdds(market_catalogue[i]['marketId'],1,'Back'))
  
  for i in range(len(playerOne)-1):
    try:
      sq.dynamic_data_entry('player',playerOne[i])
      sq.dynamic_data_entry('player',playerTwo[i])
    except UnicodeError:
      pass
  sq.conn.commit()

  for i in range(len(playerOne)):
    try:
      sq.update(playerOne[i],'betfairBack',backOddsOne[i])
      sq.update(playerTwo[i],'betfairBack',backOddsTwo[i])
    except IndexError:
      print "erro de index"
      pass
  competitors = {playerOne[i]:playerTwo[i] for i in range(len(playerOne))}  
  return competitors




# interagindo com o bd (dicionario)
def lookForArbs(competitors):
  for playerOne in competitors:
    try:
      if calc.BackBack(100,max(sq.read_from_db(playerOne[i])[0][1:]), max(sq.read_from_db(competitors[playerOne[i]])[0][1:]))[2]>0:
        print "Nós teremos " + str(calc.BackBack(100,max(sq.read_from_db(playerOne[i])[0][1:]), max(sq.read_from_db(competitors[playerOne[i]])[0][1:]))[2]) + "% ROI if we bet " + str(calc.BackBack(100,max(sq.read_from_db(playerOne[i])[0][1:]), max(sq.read_from_db(competitors[playerOne[i]])[0][1:]))[0]) + "% on " + str(playerOne[i]) + " at " + str(max(sq.read_from_db(playerOne[i])[0][1:])) + " and " + str(calc.BackBack(100,max(sq.read_from_db(playerOne[i])[0][1:]), max(sq.read_from_db(competitors[playerOne[i]])[0][1:]))[1]) + "% on " + str(competitors[playerOne[i]]) + " at " + str( max(sq.read_from_db(competitors[playerOne[i]])[0][1:]))
      else:
        pass
    except IndexError:
      pass
  



def main():
  writeSBR()
  writePinnacle()
  competitors = writeBetfair()
  lookForArbs(competitors)

while __name__ == "__main__":
  main()

