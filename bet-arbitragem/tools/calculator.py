from __future__ import division
import math

"""
func alterando para decimal
"""
def fractionToDecimal(fractional_odds):
	return 1.+ eval(fractional_odds)

"""
Alterando US em decimal
"""

def USToDecimal(us_odds):
    if '+' in us_odds:
      return ((float(us_odds.replace('+','').replace('-','')))/100.) +1.
    else:
      return ((100./float(us_odds.replace('+','').replace('-','')))) +1.


"""
http://www.bettingtools.co.uk/back-lay-equivs
"""

def layToBack(layOdds):
	return (1./float(layOdds)-1.)+1.



"""
Calculadora de Arb (Back-Back). Descobre se existe um arb quando dadas as chances de dois eventos mutuamente exclusivos. Dá ROI para arb
"""

def BackBack(stake,underdog,favourite):
    underdog_amount = (float(stake)*float(favourite))/(float(underdog)+float(favourite))
    favourite_amount = (float(stake)*float(underdog))/(float(underdog)+float(favourite))
    profit = (float(stake)*float(underdog)*float(favourite))/(float(underdog)+float(favourite))-float(stake)
    return underdog_amount, favourite_amount,profit

"""
Calculadora de Arb (Lay-Back). Verifica se existe um arb tanto para apoiar e estabelecer um evento. Dá ROI.
"""
def LayBack(stake,layOdds,backOdds):
	return BackBack(stake,layToBack(layOdds),backOdds)

"""
Calculadora de Arb (Lay-Lay). Verifica se existe um arb para a colocação de 2 eventos mutuamente excludentes em diferentes intercâmbios
"""

def LayLay(stake,underdog,favourite):
	return BackBack(stake,layToBack(underdog),layToBack(favourite))

"""
Arb Calculator (3-way)
"""

"""
(asian handicap)
"""






