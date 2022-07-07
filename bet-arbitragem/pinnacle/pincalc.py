def ConvertUS(americanOdds): # CONVERTENDO ODDS US EM DECIMAL
    if americanOdds >= 0:
        decimalOdds = "{:10.3f}".format(americanOdds / 100 +1)
    else:
        decimalOdds = "{:10.3f}".format(100 / (americanOdds * -1) + 1)
    return float(decimalOdds)

