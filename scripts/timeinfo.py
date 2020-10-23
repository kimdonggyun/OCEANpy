# anuthing about time 
import ephem
from timezonefinder import TimezoneFinder
import math
import datetime

def stbposition_dms2dec_func(dms):
    #convert position format from staionbook's (Degree,time or Dgree,time,second) to decimal
    dms_split = dms.split(' ')
    cardinal_points = dms_split[-1]
    ## Get Degree ##
    for i in dms_split:
        if i != '':
            degree = i
            break
    try:
        degree = int(degree)
    except:
        degree = int(degree[:-1])
    ## Get minute and second ##
    m_s = dms_split[-2]
    if "'" in m_s:
        if "," in m_s:
            minute = m_s[:-1].replace(',', '.')
            second = 0
        elif "." in m_s:
            minute = m_s[:-1]
            second = 0
    else:
        if "," in m_s:
            minute = m_s.replace(',', '.')
            second = 0
        elif "." in m_s:
            minute = m_s
            second = 0

    if cardinal_points == 'N' or cardinal_points == 'E':
        return (1)*(int(degree) + float(minute)/60 + float(second)/3600)
    elif cardinal_points == 'S' or cardinal_points == 'W':
        return (-1)*(int(degree) + float(minute)/60 + float(second)/3600)


    
def metaheader_dms2dec_func(dms):
    #convert position format of (Degree,time or Dgree,time,second) to decimal
    dms ='{:f}'.format(dms)
    dms_split = str(dms).split('.')

    ## Get Degree ##
    degree = int(dms_split[0])
    ## Get minute and second ##
    minute = dms_split[-1]
    deg_minute =(int(minute[0:4].ljust(4, '0'))/60)/100

    if degree >= 0:
        return (int(abs(degree)) + deg_minute)
    elif degree < 0:
        return (-1)*(int(abs(degree)) + deg_minute)

    
def dec2dm_func(dms):
    #convert decimal format to dd.mmmmm format
    dms ='{:f}'.format(dms)
    dms_split = str(dms).split('.')
    
    ## Get Degree ##
    degree = int(dms_split[0])
    ## Get minute and second ##
    minute = dms_split[-1]
    dec_minute =(int(minute[0:4].ljust(4, '0'))*60)/1000000

    if degree >= 0:
        return (int(abs(degree)) + dec_minute)
    elif degree < 0:
        return (-1)*(int(abs(degree)) + dec_minute)



import pytz
def local_to_utc (latitude, longitude, datetime):
    # lat and lon = float or int, datetime = datetime object
    # convert local time to utc time
    tf = TimezoneFinder()
    local = tf.timezone_at(lat=latitude, lng=longitude) # retunrn timezone as string eg. 'US/Eastern'
    local_zone = pytz.timezone(local) # convert timezone string to timezone type
    local_dt = local_zone.localize(datetime) # convert local date time to local timezone format
    utc_dt = local_dt.astimezone(pytz.utc) # convert local timezone format to utc timezone
    utc = utc_dt.strftime('%Y-%m-%d %H:%M:%S') # convert utc timezone to string with certain format
    return utc

from dateutil import tz
def utc_to_local (latitude, longitude, datetime):
    # lat and lon = float or int, datetime = datetime object
    # convert utc time to local time
    tf = TimezoneFinder()
    local = tf.timezone_at(lat=latitude, lng=longitude) # retunrn timezone as string eg. 'US/Eastern'
    local_zone = pytz.timezone(local) # convert timezone string to timezone type
    
    utc_zone = tz.gettz('UTC') # set UTC time zone
    utc_dt = datetime.replace(tzinfo=utc_zone) # tell this is UTC time
    local_dt = utc_dt.astimezone(local_zone)
    local_dt = local_dt.strftime('%Y-%m-%d %H:%M:%S')
    return local_dt


def day_night(latitude, longitude, dt):
    # lat and lon = string, datetime = datetime object
    # return day, night, dawn and dusk info, based on given lat, lon and time
    o = ephem.Observer()
    o.lat = str(latitude)
    o.lon = str(longitude)
    o.date = local_to_utc(37, 126, dt) # string format

    s = ephem.Sun()
    s.compute(o)
    
    local_time = dt
    sun_altitude = float(s.alt) # radian

    try:
        next_sunset_local = datetime.datetime.strptime( utc_to_local(latitude, longitude, o.next_setting(ephem.Sun()).datetime() ), '%Y-%m-%d %H:%M:%S')

    except ephem.AlwaysUpError as e:
        if str(e) == 'ephem.AlwaysUpError': # incase polar day
            return 'day'
    except ephem.NeverUpError as e:
        if str(e) == 'ephem.NeverUpError': # incase polar night
            return 'night'

    if sun_altitude > 0:
        return 'day'
    elif (sun_altitude > -0.261799) and (next_sunset_local.date() == dt.date()): # 0.261799 is around 15 degrees
        return 'dawn'
    elif (sun_altitude > -0.261799) and (next_sunset_local.date() > dt.date()):
        return 'dusk'
    else:
        return 'night'
