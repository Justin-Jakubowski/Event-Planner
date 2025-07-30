# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session, json
from jinja2  import TemplateNotFound

from datetime import timedelta, datetime

# App modules
from app import app, dbConn, cursor
# from app.models import Profiles

# App main route + generic routing

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/eventScheduling')
def eventScheduling():
    if 'email' not in session:
        return render_template('loginPage.html')

    return render_template('createEvent.html')

@app.route('/viewInvitations')
def viewInvitations():
    if 'email' not in session:
        return render_template('loginPage.html')
    
    email = session.get('email')

    populatesql = '''
        SELECT es.esid, CONCAT(er.ename, ' #', es.esid) AS eventDesc
        FROM guestinvitations gi
        JOIN eventschedule es ON gi.esid = es.esid
        JOIN eventrecord er ON es.eid = er.eid
        WHERE gi.email = %s;
    '''
    cursor.execute(populatesql, email)
    eventInvites = cursor.fetchall()
    
    return render_template('guestHome.html', eventInvites=eventInvites)

@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html')

@app.route('/createAccountSubmit', methods=['POST', 'GET'])
def accountCreated():
    error = False

    #get user input values
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    upassword = request.form.get('upassword')
    number = request.form.get('number')
    gender = request.form.get('gender')
    dob = request.form.get('dob')


    if not fname:
        error = True
        flash('Please provide a first name')

    if not lname:
        error = True
        flash('Please provide a last name')

    if not email:
        error = True
        flash('Please provide an email')

    if not upassword:
        error = True
        flash('Please provide a password')

    if not dob:
        error = True
        flash('Please provide a date of birth')

    if error:
        return render_template('createAccount.html', fiName = fname, laName = lname, elMail = email, dateofb = dob )

     #update the database
    sql = 'SELECT count(*) AS countmatch FROM userprofile WHERE email=%s' 
    cursor.execute(sql, email)
    result = cursor.fetchone()
    if result['countmatch'] == 1:
        flash('This email is already in use.')
        error = True
    else:
        #the product id does not exist we should add as new
        sql = "INSERT INTO userprofile(email, firstname, lastname, upassword, phone, dateofbirth, gender, timeofcreation) VALUES(%s, %s, %s, %s, %s, %s, %s, NOW())"
        cursor.execute(sql, [email, fname, lname, upassword, number, dob, gender])
        dbConn.commit() #make the database changes permanent


    return render_template('loginPage.html')

@app.route('/login')
def login():
    return render_template('loginPage.html')

@app.route('/loginSubmit', methods=['POST', 'GET'])
def loginSubmit():
    error = False

    email = request.form.get('email')
    upassword = request.form.get('password')

    sql = 'SELECT count(*) AS countmatch FROM userprofile WHERE email=%s AND upassword=%s' 
    cursor.execute(sql, [email, upassword])
    result = cursor.fetchone()
    if result['countmatch'] == 0:
        flash('The email or password are not correct.')
        error = True

    if error:
        return render_template('loginPage.html', elMail = email)
    
    session['email'] = email
    session['upassword'] = upassword
    
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('upassword', None)
    return render_template('home.html')

@app.route('/profile')
def profile():
    if 'email' not in session:
        return render_template('loginPage.html')

    sql = 'SELECT * FROM userprofile WHERE email=%s'
    cursor.execute(sql, session.get('email'))
    result = cursor.fetchone()

    return render_template('userSetting.html', user = result)

@app.route('/editprofile' , methods=['POST', 'GET'])
def editProfile():
    error = False

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    oldpass = request.form.get('old')
    newpass = request.form.get('new')
    confirm = request.form.get('confNew')
    tel = request.form.get('phone')


    if not fname:
        error = True
        flash('Please provide a first name')

    if not lname:
        error = True
        flash('Please provide a last name')

    if not oldpass:
        error = True
        flash('Password is required to change information')

    if not newpass == confirm:
        error = True
        flash('New passwords do not match')

    sql = 'SELECT count(*) AS countmatch FROM userprofile WHERE email=%s AND upassword=%s' 
    cursor.execute(sql, [session.get('email'), oldpass])
    result = cursor.fetchone()
    if result['countmatch'] == 0:
        flash('The Password is not correct.')
        error = True

    if error:
        return render_template('userSetting.html')
    
    if not newpass:
        newpass == oldpass

    sql = 'SELECT count(*) AS countmatch FROM userprofile WHERE email=%s' 
    cursor.execute(sql, session.get('email'))
    result = cursor.fetchone()
    if result['countmatch'] == 1:
        # the product Id exists in the table, we should update it
        sql = "update userProfile set firstname=%s, lastname=%s, phone=%s, upassword=%s WHERE email=%s"
        cursor.execute(sql, [fname, lname, tel, newpass, session.get('email')])
        dbConn.commit() #make the database changes permanent
        session.pop('upassword', None)
        session['upassword'] = newpass
        flash('Settings succesfully updated')
        
    
    return redirect(url_for('profile'))

@app.route('/deleteProfile')
def deleteProfile():
    sql = 'DELETE FROM userprofile WHERE email=%s' 
    cursor.execute(sql, session.get('email'))
    dbConn.commit()
    session.pop('email', None)
    session.pop('upassword', None)
    return redirect(url_for('home'))

@app.route('/visualizeUsers')
def visualizeUsers():
    sql = 'SELECT DATE(timeofcreation) AS label, COUNT(*) AS value FROM userprofile GROUP BY DATE(timeofcreation);'
    cursor.execute(sql)
    result = cursor.fetchall()
    result = json.dumps(result)
    return render_template('visualizeMeetings.html', chartData = result)

@app.route('/eventSchedulingSubmit', methods=['GET', 'POST'])
def eventSchedulingSubmit():
    email = session.get('email')
    event_name = request.form.get('event_name')
    event_location = request.form.get('event_location')
    zoom_link = request.form.get('zoom_link')
    additional_notes = request.form.get('additional_notes')
    
    cursor.execute("INSERT INTO eventrecord (organizeremail, ename, elocation, zoom, notes, timeofcreation) VALUES (%s, %s, %s, %s, %s, NOW())",
                        (email, event_name, event_location, zoom_link, additional_notes))
    dbConn.commit()
    
    return redirect(url_for('eventOverview'))

@app.route('/eventOverview')
def eventOverview():
    if 'email' not in session:
        return render_template('loginPage.html')
    
    email = session.get('email')
    
    cursor.execute("SELECT * FROM eventrecord WHERE organizeremail=%s", email)  
    event_records = cursor.fetchall()
    return render_template('eventOverview.html', events=event_records)

@app.route('/modifyEvent', methods=['GET', 'POST'])
def modifyEvent():
    if 'email' not in session:
        return render_template('loginPage.html')
    
    eid = request.form.get('eid')
    sql = "SELECT * FROM eventrecord WHERE eid = %s" 
    cursor.execute(sql, eid)
    result = cursor.fetchone()
    return render_template('modifyEvent.html', event = result)

@app.route('/modifyEventSubmit', methods=['GET', 'POST'])
def modifyEventSubmit():
    if 'email' not in session:
        return render_template('loginPage.html')

    event_name = request.form.get('ename')
    event_location = request.form.get('elocation')
    zoom_link = request.form.get('zoom')
    additional_notes = request.form.get('notes')
    final_date = request.form.get('efinaldate')
    eid = request.form.get('eid')

    cursor.execute(
            "UPDATE eventrecord SET ename = %s, elocation = %s, zoom = %s, notes = %s, efinaldate = %s WHERE eid = %s",
            (event_name, event_location, zoom_link, additional_notes, final_date, eid)
        )
    dbConn.commit()

    print("updated")
    return redirect(url_for('eventOverview'))

@app.route('/addGuest', methods=['GET', 'POST'])
def addGuest():   
    if 'email' not in session:
        return render_template('loginPage.html')

    eid = request.form.get('eid')
    sql = "SELECT * FROM eventrecord WHERE eid = %s" 
    cursor.execute(sql, eid)
    result = cursor.fetchone()
    return render_template('addGuest.html', event = result)

@app.route('/addGuestSubmit', methods=['POST'])
def addGuestSubmit():
    email = request.form.get('email')
    gender = request.form.get('gender')
    age = request.form.get('age')
    eid = request.form.get('eid')

    cursor.execute("INSERT INTO eventguest (eid, email, gender, age) VALUES (%s, %s, %s, %s)", (eid, email, gender, age))
    dbConn.commit()

    # Redirect to the event overview page after successfully adding the guest
    return redirect(url_for('eventOverview'))

@app.route('/genderVisualization', methods=['POST', 'GET'])
def genderVisualization():
    eid = request.form.get('eid') 

    sql = "SELECT gender AS label, COUNT(*) AS value FROM eventguest WHERE eid = %s GROUP BY gender;"
    cursor.execute(sql, (eid,))
    result = cursor.fetchall()
    result = json.dumps(result)
    print(result)

    return render_template("genderVisualization.html", chartData = result)

def loadSchedule(eid):
    sql = """
        SELECT 
            es.esid, 
            es.startdate, 
            es.enddate, 
            es.responsedeadline,
            COUNT(DISTINCT sr.email) AS responsecount,
            (SELECT COUNT(*) FROM guestinvitations gi WHERE gi.esid = es.esid) AS totalresponses
        FROM
            eventschedule es
        LEFT JOIN 
            scheduleresponse sr ON es.esid = sr.esid
        LEFT JOIN
            guestinvitations gi ON es.esid = gi.esid
        WHERE 
            es.eid = %s
        GROUP BY 
            es.esid, es.startdate, es.enddate, es.responsedeadline
        ORDER BY 
            es.esid;
    """
    cursor.execute(sql, eid)
    result = cursor.fetchall()

    return result

@app.route('/manageTasks', methods=['POST', 'GET'])
def manageTasks():
    eid = request.form.get('eid')

    titlesql = "SELECT ename FROM eventrecord WHERE eid=%s;"
    cursor.execute(titlesql, eid)
    ename = cursor.fetchone()
    
    result = loadSchedule(eid)

    return render_template('managescheduling.html', eid=eid, ename=ename['ename'], tableData=result)

@app.route('/createTask/<int:eid>')
def createTask(eid):
    titlesql = "SELECT ename FROM eventrecord WHERE eid=%s;"
    cursor.execute(titlesql, eid)
    ename = cursor.fetchone()
    return render_template('createtask.html', eid=eid, ename=ename['ename'])

@app.route('/createTaskConfirm', methods=['POST', 'GET'])
def createTaskConfirm():
    eid = request.args.get('eid', type=int)
    
    titlesql = "SELECT ename FROM eventrecord WHERE eid=%s;"
    cursor.execute(titlesql, eid)
    ename = cursor.fetchone()

    startdate = request.form.get("startDate")
    enddate = request.form.get("endDate")
    responsedeadline = request.form.get("deadline")
    notes = request.form.get("notes")

    createsql="INSERT INTO eventschedule (eid, startdate, enddate, responsedeadline, tasknotes) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(createsql, (eid, startdate, enddate, responsedeadline or None, notes or None))
    dbConn.commit()

    invitesql="INSERT INTO guestinvitations (email, esid) SELECT eg.email, es.esid FROM eventschedule es JOIN eventguest eg ON es.eid = eg.eid WHERE es.esid = LAST_INSERT_ID();"
    cursor.execute(invitesql)
    dbConn.commit()

    result = loadSchedule(eid)

    return render_template('managescheduling.html', eid=eid, ename=ename['ename'], tableData=result)

@app.route('/modifyTask')
def modifyTask():
    esid = request.args.get('esid', type=int)
    
    populatesql = "SELECT er.ename, es.startdate, es.enddate, es.responsedeadline, es.tasknotes FROM eventschedule es JOIN eventrecord er ON es.eid = er.eid WHERE es.esid = %s;"
    cursor.execute(populatesql, esid)
    taskData = cursor.fetchone()

    return render_template('modifytask.html', esid=esid, ename=taskData['ename'], startdate=taskData['startdate'], enddate=taskData['enddate'], deadline=taskData['responsedeadline'], notes=taskData['tasknotes'])

@app.route('/modifyTaskConfirm', methods=['POST', 'GET'])
def modifyTaskConfirm():
    esid = request.args.get('esid', type=int)
    
    titlesql = "SELECT es.eid, er.ename FROM eventschedule es JOIN eventrecord er ON es.eid = er.eid WHERE es.esid = %s;"
    cursor.execute(titlesql, esid)
    einfo = cursor.fetchone()

    responsedeadline = request.form.get("deadline")
    notes = request.form.get("notes")

    updatesql = "UPDATE eventschedule SET responsedeadline = %s, tasknotes = %s WHERE esid = %s;"
    cursor.execute(updatesql, (responsedeadline or None, notes or None, esid))
    dbConn.commit()
    
    result = loadSchedule(einfo['eid'])

    return render_template('managescheduling.html', eid=einfo['eid'], ename=einfo['ename'], tableData=result)

@app.route('/deleteTask', methods=['POST', 'GET'])
def deleteTask():
    esid = request.args.get('esid', type=int)
    
    titlesql = "SELECT es.eid, er.ename FROM eventschedule es JOIN eventrecord er ON es.eid = er.eid WHERE es.esid = %s;"
    cursor.execute(titlesql, esid)
    einfo = cursor.fetchone()

    deletesql="DELETE FROM eventschedule WHERE esid=%s;"
    cursor.execute(deletesql, esid)
    dbConn.commit()

    deleteinvitesql = "DELETE FROM guestinvitations WHERE esid=%s;"
    cursor.execute(deleteinvitesql, esid)
    dbConn.commit()

    result = loadSchedule(einfo['eid'])

    return render_template('managescheduling.html', eid=einfo['eid'], ename=einfo['ename'], tableData=result)

@app.route('/viewDetails')
def viewDetails():
    esid = request.args.get('esid', type=int)

    titlesql="SELECT er.ename FROM eventschedule es JOIN eventrecord er ON es.eid = er.eid WHERE es.esid=%s;"
    cursor.execute(titlesql, esid)
    ename = cursor.fetchone()

    startenddatesql = "SELECT startdate, enddate FROM eventschedule WHERE esid = %s;"
    cursor.execute(startenddatesql, esid)
    daterange = cursor.fetchone()

    startdate = daterange['startdate']
    enddate = daterange['enddate']

    datelist = [startdate + timedelta(days=x) for x in range((enddate - startdate).days + 1)]

    guestemailsql = "SELECT email FROM guestinvitations WHERE esid = %s;"
    cursor.execute(guestemailsql, esid)
    guestemaillist = [row['email'] for row in cursor.fetchall()]

    availabilitysql = "SELECT email, datechoice, availability FROM scheduleresponse WHERE esid=%s AND datechoice BETWEEN %s AND %s;"
    cursor.execute(availabilitysql, (esid, startdate, enddate))
    availabilitylist = cursor.fetchall()

    tableData = {}
    for guestemail in guestemaillist:
        guestdata = {}

        for date in datelist:
            datestr = date.strftime("%m/%d/%y")
            
            availabilityentry = next((entry for entry in availabilitylist if entry['email'] == guestemail and entry['datechoice'] == date), None)
            availability = availabilityentry['availability'] if availabilityentry else ''
            
            guestdata[datestr] = availability
        
        tableData[guestemail] = guestdata
    
    totalcountsql = """
        SELECT
            datechoice,
            COUNT(CASE WHEN availability = 'Y' THEN 1 END) AS ycount,
            COUNT(CASE WHEN availability = 'M' THEN 1 END) AS mcount,
            COUNT(CASE WHEN availability = 'N' THEN 1 END) AS ncount
        FROM scheduleresponse
        WHERE esid = %s
        GROUP BY datechoice;
    """
    cursor.execute(totalcountsql, esid)
    totalcount = cursor.fetchall()

    ycount_values = [entry['ycount'] for entry in totalcount]
    mcount_values = [entry['mcount'] for entry in totalcount]
    ncount_values = [entry['ncount'] for entry in totalcount]

    fusionchartsdata = {
        "chart": {
            "subcaption": "Scheduling Task #" + str(esid),
            "xaxisname": "Dates",
            "yaxisname": "Availability",
            "formatnumberscale": "1",
            "plottooltext": "<b>$dataValue</b> people said <b>$seriesName</b> for $label",
            "theme": "gammel",
            "drawcrossline": "1"
        },
        "categories": [
            {
                "category": [{"label": date.strftime("%m/%d/%y")} for date in datelist]
            }
        ],
        "dataset": [
            {
                "seriesname": "Yes",
                "data": [{"value": str(count)} for count in ycount_values],
                "color": "00BB00"
            },
            {
                "seriesname": "Maybe",
                "data": [{"value": str(count)} for count in mcount_values],
                "color": "FFA500"
            },
            {
                "seriesname": "No",
                "data": [{"value": str(count)} for count in ncount_values],
                "color": "FF0000"
            }
        ]
    }

    return render_template('taskdetails.html', esid=esid, ename=ename['ename'], datelist=datelist, guestemaillist=guestemaillist, tabledata=tableData, totalcount=totalcount, fusionchartsdata=fusionchartsdata)

@app.route('/availability/<int:esid>')
def availability(esid):
    email = session.get('email')

    titlesql="SELECT er.ename FROM eventschedule es JOIN eventrecord er ON es.eid = er.eid WHERE es.esid=%s;"
    cursor.execute(titlesql, esid)
    ename = cursor.fetchone()

    startenddatesql = "SELECT startdate, enddate FROM eventschedule WHERE esid = %s;"
    cursor.execute(startenddatesql, esid)
    daterange = cursor.fetchone()

    startdate = daterange['startdate']
    enddate = daterange['enddate']

    datelist = [startdate + timedelta(days=x) for x in range((enddate - startdate).days + 1)]


    return render_template('availability.html', esid=esid, email=email, datelist=datelist, ename=ename['ename'])

@app.route('/availabilityconfirmed', methods=['POST', 'GET'])
def availabilityconfirmed():
    esid = request.args.get('esid')  
    email = session.get('email')

    availability_data = []

    startenddatesql = "SELECT startdate, enddate FROM eventschedule WHERE esid = %s;"
    cursor.execute(startenddatesql, esid)
    daterange = cursor.fetchone()

    startdate = daterange['startdate']
    enddate = daterange['enddate']

    datelist = [startdate + timedelta(days=x) for x in range((enddate - startdate).days + 1)]

    for date in datelist:
        date_str = date.strftime('%Y-%m-%d')
        availability = request.form.get(f'selectOption_{date_str}')
        comment = request.form.get(f'selectComment_{date_str}')

        availability_data.append((esid, email, date, availability, comment or None))

    createsql = "INSERT INTO scheduleresponse (esid, email, datechoice, availability, comments) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(createsql, availability_data)
    dbConn.commit()

    populatesql = '''
        SELECT es.esid, CONCAT(er.ename, ' #', es.esid) AS eventDesc
        FROM guestinvitations gi
        JOIN eventschedule es ON gi.esid = es.esid
        JOIN eventrecord er ON es.eid = er.eid
        WHERE gi.email = %s;
    '''
    cursor.execute(populatesql, email)
    eventInvites = cursor.fetchall()

    return render_template('guestHome.html', esid=esid, eventInvites=eventInvites)
    

@app.route('/modify/<int:esid>>')
def modify(esid):
    email = session.get('email')

    titlesql="SELECT er.ename FROM eventschedule es JOIN eventrecord er ON es.eid = er.eid WHERE es.esid=%s;"
    cursor.execute(titlesql, esid)
    ename = cursor.fetchone()

    startenddatesql = "SELECT startdate, enddate FROM eventschedule WHERE esid = %s;"
    cursor.execute(startenddatesql, esid)
    daterange = cursor.fetchone()

    startdate = daterange['startdate']
    enddate = daterange['enddate']

    datelist = [startdate + timedelta(days=x) for x in range((enddate - startdate).days + 1)]

    availability_data = []
    for date in datelist:
        availability_sql = "SELECT availability FROM scheduleresponse WHERE esid = %s AND email = %s AND datechoice = %s;"
        cursor.execute(availability_sql, (esid, email, date))
        existing_availability = cursor.fetchone()

        availability_data.append((date, existing_availability['availability']))

    return render_template('modify.html', esid=esid, email=email, ename=ename['ename'], availability_data=availability_data)

@app.route('/modifyConfirmed', methods=['POST', 'GET'])
def modifyConfirmed():
    esid = request.args.get('esid')  
    email = session.get('email')

    modified_availability_data = []

    startenddatesql = "SELECT startdate, enddate FROM eventschedule WHERE esid = %s;"
    cursor.execute(startenddatesql, esid)
    daterange = cursor.fetchone()

    startdate = daterange['startdate']
    enddate = daterange['enddate']

    datelist = [startdate + timedelta(days=x) for x in range((enddate - startdate).days + 1)]

    for date in datelist:
        date_str = date.strftime('%Y-%m-%d')
        modified_availability = request.form.get(f'selectOption_{date_str}')
        modified_comment = request.form.get(f'selectComment_{date_str}')

        modified_availability_data.append((esid, email, date, modified_availability, modified_comment or None))

        update_sql = "UPDATE scheduleresponse SET availability = %s, comments = %s WHERE esid = %s AND email = %s AND datechoice = %s;"
        cursor.execute(update_sql, (modified_availability, modified_comment, esid, email, date))

    dbConn.commit()

    populatesql = '''
        SELECT es.esid, CONCAT(er.ename, ' #', es.esid) AS eventDesc
        FROM guestinvitations gi
        JOIN eventschedule es ON gi.esid = es.esid
        JOIN eventrecord er ON es.eid = er.eid
        WHERE gi.email = %s;
    '''
    cursor.execute(populatesql, email)
    eventInvites = cursor.fetchall()
    

    return render_template('guestHome.html', esid=esid, eventInvites=eventInvites)

@app.route('/deleteResponse', methods=['POST', 'GET'])
def deleteResponse():
    esid = request.args.get('esid')
    email = session.get('email')

    deletesql = "DELETE FROM scheduleresponse WHERE esid=%s AND email=%s"
    cursor.execute(deletesql, (esid, email))
    dbConn.commit()

    populatesql = '''
        SELECT es.esid, CONCAT(er.ename, ' #', es.esid) AS eventDesc
        FROM guestinvitations gi
        JOIN eventschedule es ON gi.esid = es.esid
        JOIN eventrecord er ON es.eid = er.eid
        WHERE gi.email = %s;
    '''
    cursor.execute(populatesql, email)
    eventInvites = cursor.fetchall()

    return render_template('guestHome.html', esid=esid, eventInvites=eventInvites)

@app.route('/exploreresponses/<int:esid>')
def exploreresponses(esid):
    startenddatesql = "SELECT startdate, enddate FROM eventschedule WHERE esid = %s;"
    cursor.execute(startenddatesql, esid)
    daterange = cursor.fetchone()

    startdate = daterange['startdate']
    enddate = daterange['enddate']

    datelist = [startdate + timedelta(days=x) for x in range((enddate - startdate).days + 1)]

    return render_template('exploreresponses.html', datelist=datelist, esid=esid)

@app.route('/exploreresponsesConfirmed', methods=['POST', 'GET'])
def exploreresponsesConfirmed():
    esid = request.args.get('esid')  
    dateChoice_str= request.form.get('graphDate')
    dateChoice = datetime.strptime(dateChoice_str, '%Y-%m-%d')

    sql= "SELECT availability AS label, COUNT(*) AS value FROM scheduleresponse WHERE esid = %s AND dateChoice = %s GROUP BY availability;"
    cursor.execute(sql, (esid,dateChoice))
    result=cursor.fetchall()

    result = json.dumps(result)
    
    return render_template('graphResponses.html', chartData=result)