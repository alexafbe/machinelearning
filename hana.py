from bottle import get, post, request, run, redirect, route

import dbapi

import time

@get(‘/login’)

def login_form():

    return ”'<DIV ALIGN=’CENTER’><BR><BR><BR><BR>

                <H1>Python (Bottle) & SAP HANA</H1>

                <BR><TABLE BORDER=’1′ BORDERCOLOR=’BLUE’

                     BGCOLOR=’WHITE’>

                <FORM METHOD=’POST’>

                <TR><TD>Server</TD><TD>

                <INPUT TYPE=’TEXT’ NAME=’Server’></TD></TR>

                <TR><TD>Port</TD><TD>

                <INPUT TYPE=’TEXT’ NAME=’Port’></TD></TR>

                <TR><TD>User</TD><TD>

                <INPUT TYPE=’TEXT’ NAME=’User’></TD></TR>

                <TR><TD>Password</TD>

                <TD><INPUT TYPE=’PASSWORD’ NAME=’Passwd’></TD></TR>

                <TR><TD COLSPAN=’2′ ALIGN=’CENTER’>

                <INPUT TYPE=’SUBMIT’ value=’Log In’ NAME=’LOG_IN’>

                <INPUT TYPE=’RESET’ value=’Clear’></TD></TR>

                </FORM>

                <TABLE>

              </DIV>”’

@post(‘/login’)

def login_submit():

    global cur

    Server = request.forms.get(‘Server’)

    Port = request.forms.get(‘Port’)

    User = request.forms.get(‘User’)

    Passwd = request.forms.get(‘Passwd’)

    Port = int(Port)

    conn = dbapi.connect(Server, Port, User, Passwd)

    cur = conn.cursor()

    redirect(“/parameters”)

@get(‘/parameters’)

def choose_parameters():

    global cur

    query = “SELECT CARRID,CARRNAME FROM SFLIGHT.SCARR WHERE MANDT = 300”

    ret = cur.execute(query)

    ret = cur.fetchall()

    output = “‘<CENTER><FORM METHOD=’POST’>”

    output += “Carrier <SELECT NAME=’Carrid’>”

    for row in ret:

        carrid = str(row[0])

        carrname = str(row[1])

        output += “<OPTION VALUE=’%s’>%s</OPTION>” % (carrid, carrname)

    output += “</SELECT>”

    query = “SELECT DISTINCT CITYFROM FROM SFLIGHT.SPFLI WHERE MANDT = 300”

    ret = cur.execute(query)

    ret = cur.fetchall()

    output += “City From<SELECT NAME=’Cityfrom’>”

    for row in ret:

        cityfrom = str(row[0])

        output += “<OPTION VALUE=’%s’>%s</OPTION>” % (cityfrom, cityfrom)

    output += “</SELECT>”

    output += “<INPUT TYPE=’SUBMIT’ value=’Show Query’ NAME=’show_query’>”

    output += ” </FORM></CENTER>”

    return output

@post(‘/parameters’)

def show_query():

    counter = 0

    start = time.clock()

    carrid = request.forms.get(‘Carrid’)

    cityfrom = request.forms.get(‘Cityfrom’)

    query = ”’SELECT SBOOK.CARRID,SBOOK.CONNID,FLDATE,PASSNAME,CITYFROM,CITYTO

                FROM SFLIGHT.SBOOK INNER JOIN SFLIGHT.SPFLI

                ON SBOOK.CONNID = SPFLI.CONNID

                WHERE SBOOK.CARRID = ‘%s’ AND CITYFROM = ‘%s’

                AND PASSNAME <> ”

                AND SBOOK.MANDT = 300

                AND year(FLDATE) = 2012

                ORDER BY FLDATE DESC”’ % (carrid, cityfrom)

    ret = cur.execute(query)

    ret = cur.fetchall()

    output = “<DIV ALIGN=’CENTER’><TABLE BORDER=’1′>”

    output += “<TR BGCOLOR=’#B9C9FE’>”

    output += “<TH>Carrier</TH><TH>Connection</TH>”

    output += “<TH>Flight Date</TH><TH>Passenger Name</TH>”

    output += “<TH>City From</TH><TH>City To</TH>”

    output += “</TR>”

    for row in ret:

        counter += 1

        carrid = str(row[0])

        connid = str(row[1])

        fldate = str(row[2])

        passname = row[3].encode(‘utf-8’)

        cityfrom = row[4].encode(‘utf-8’)

        cityto = row[5].encode(‘utf-8’)

        output += “<TR BGCOLOR=’#E8EDFF’>”

        output += ”'<TD>%s</TD><TD>%s</TD>

                         <TD>%s</TD><TD>%s</TD>

                         <TD>%s</TD><TD>%s</TD>”’ % (carrid, connid, fldate, passname, cityfrom, cityto)

        output += “</TR>”

    output += “</TABLE>”

    end = time.clock()

    time_taken = end – start

    output += “<H1>%s records in %s seconds</H1></DIV>” % (counter, time_taken)

    return output

run(host=’localhost’, port=8080)