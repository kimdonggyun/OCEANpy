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
    # calculate oxygen consumption rate (µl O2 / (Ind*Hour) )
    # DW: dry weight of individual taxa (mg Dry C / Ind)
    # Temperature in Celsius 
    oxycon = math.e**(-0.399 + 0.801*math.log(DW) + 0.069*math.log(Temp))
    return oxycon

def calOxycomsume2Carbon (R, RQ):
    # calculate carbon ingestion and egestion rate (µg C / (ind*Day))
    # R : In situ respiration rate (µl O2 / (Ind*Day))
    # RQ : Respiration Quitient (Carb;1 Protein;0.97 Fat;0.73)
    # C : Carbon mass per Mole Volume (12g / 22.4L)
    # U : Average digestive efficiency
    # K : Gross growth efficiency
    
    C = 12/22.4
    U = 0.7
    K = 0.3
    
    carbon_ingestion = R*C*RQ*( 1/(U-K) )
    carbon_egestion = carbon_ingestion*0.3
    
    
    return carbon_ingestion, carbon_egestion
    
    