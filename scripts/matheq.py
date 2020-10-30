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
    dist = math.sqrt( (x2-x1)**2 + (y2-y1)**2  )
    return dist