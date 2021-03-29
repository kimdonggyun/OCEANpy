# calculation for any oceanographic formula
import math

def Cel_to_Kel (Cel):
    # convert Celsius to Kelvin
    Kel = Cel + 273.15
    return Kel

def Kel_to_Cel (Kel):
    # convert Kelvin to Celsius
    Cel = Kel - 273.15
    return Cel

def to_pot_temp ():
    # convert temperature to potential temperature
    pass

def calDist (x1, y1, x2, y2):
    # calculate the distance between to point
    dist = math.sqrt( (x2-x1)**2 + (y2-y1)**2  )
    return dist

def calOxyconsume (DW, Temp):
    # calculate oxygen consumption rate
    # DW: dry weight of individual taxa
    # Temperature
    oxycon = math.e**(-0.399 + 0.801*math.log(DW) + 0.069*math.log(Temp))
    return oxycon

def calOxycomsume2Carbon ():
    
    return carbon
    
    