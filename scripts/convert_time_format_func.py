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

if __name__ == "__main__":
    position = "79°01.884'N"
    print(stbposition_dms2dec_func(position))
    