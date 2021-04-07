#!/usr/bin/python3

# automatisiertes gewächshaus | main-script flask_app | version 0.1

# libraries
from flask import Flask, session, render_template, request, make_response, redirect, flash, url_for
from flask_mysqldb import MySQL
import requests

# flask instance for app and secret key for session
app = Flask(__name__)
app.secret_key = 'huelsenschlaepper'

# MySQL instance for app
mysql = MySQL(app)

# MySQL connection
try:
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'AGdb'
    app.config['MYSQL_DB'] = 'AGdb'

    print('MySQL Datenbank-Verbindung erfolgreich')
except:
    print('Datenbank-Verbindung konnte nicht hergestellt werden')


# home
@app.route('/')
def home():
    # default method is GET, if nothing else is declared
    # returns home-template
    return render_template('home.html')

# dashboard


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # both methods GET and POST are allowed
    # default method is GET, if nothing else is declared

    try:
        # connection-cursor to MySQL database
        cur = mysql.connection.cursor()

        # SQL statement to fetch all available satellites in MySQL database orderd by ID
        # cur.fetchall() generates a tupel with all selected rows from MySQl database
        cur.execute('SELECT id, name FROM satellites')
        satellite_list = cur.fetchall()

        # SQL statement to fetch all available programms in MySQL database orderd by ID
        cur.execute('SELECT id, name FROM programms')
        programm_list = cur.fetchall()

        # SQL statement to fetch dates of the last 7 days in MySQL database orderd by ID and group by date to only show distinct dates
        cur.execute('''SELECT id, date FROM sensordata WHERE date >
        (SELECT  max(date) - interval 7 day FROM sensordata) group by date''')
        date_span = cur.fetchall()

        # By entering the dashboard via GET-request, data from the last day inserted into the MySQL database
        # and from the satellite with ID = 1 and current loaded programm should automatically be displayed

        # SQL statement to select satellite with ID = 1 and current loaded programm
        # cur-fetchone() generates a tupel of all data in one MySQL row, as only one satellite ad one programm is selected
        # the object can be called as [0] object of the tupel

        # start satellite
        cur.execute('SELECT name FROM satellites WHERE id = 1')
        start_satellite = cur.fetchone()

        # start programm
        cur.execute('SELECT current_programm FROM satellites WHERE id = 1')
        c_programm = cur.fetchone()

        cur.execute('SELECT name FROM programms WHERE id = (%s)',
                    [c_programm[0]])
        start_programm = cur.fetchone()

        # SQL statement to select the ideal value of the parameters from programm with ID = 1
        # This value is needed to dispaly the ideal value in the charts of the dashboard

        # ideal value temperature
        cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
        (SELECT id FROM parameters WHERE name = 'Temperatur')''', [c_programm[0]])
        start_temperature_value = cur.fetchone()

        # ideal value brighteness
        cur.execute('''SELECT value from programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Helligkeit')''', [c_programm[0]])
        start_brightness_value = cur.fetchone()

        # ideal value airhumidity
        cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Luftfeuchtigkeit')''', [c_programm[0]])
        start_airhumidity_value = cur.fetchone()

        # ideal value soilhumidity
        cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Bodenfeuchtigkeit')''', [c_programm[0]])
        start_soilhumidity_value = cur.fetchone()

        # To only display datapoints from the last inserted day into MySQL database with satellite and programm ID = 1,
        # date and time are selected where date is the highest date available with satellite ID = 1 and programm id from current loaded programm
        # and where satellite ID = 1 and programm id from current loaded programm
        # cur-fetchall() generates a tupel of all data in one or more MySQL rows, as date and time is selected
        # the objects of both rows can be called as [0][0] object of the tupel

        # date and time
        cur.execute('''SELECT date, time FROM sensordata WHERE date = (SELECT max(date) FROM sensordata WHERE id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = 1
            AND id_programm = (%s))) AND id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = 1
            AND id_programm = (%s))''', [c_programm[0], c_programm[0]])
        start_dates = cur.fetchall()

        # temperature where date = startdate
        cur.execute('''SELECT temperature FROM sensordata WHERE date = (%s) AND id_satellite_programm in
        (SELECT id FROM satellite_programm WHERE id_satellite = 1
        AND id_programm = (%s))''', [start_dates[0][0], c_programm[0]])
        start_temperature = cur.fetchall()

        # brightness where date = startdate
        cur.execute('''SELECT brightness FROM sensordata WHERE date = (%s) AND id_satellite_programm in
        (SELECT id FROM satellite_programm WHERE id_satellite = 1
        AND id_programm = (%s))''', [start_dates[0][0], c_programm[0]])
        start_brightness = cur.fetchall()

        # brightness-values were added up where date = startdate to display the brightness hours for a day
        new_start_brightness = []
        new_value = 0
        for value in start_brightness:
            new_value = new_value + value[0]
            new_start_brightness.append(new_value)

        # airhumidity where date = startdate
        cur.execute('''SELECT airhumidity FROM sensordata WHERE date = (%s) AND id_satellite_programm in
        (SELECT id FROM satellite_programm WHERE id_satellite = 1
        AND id_programm = (%s))''', [start_dates[0][0], c_programm[0]])
        start_airhumidity = cur.fetchall()

        # soilhumidity where date = startdate
        cur.execute('''SELECT soilhumidity FROM sensordata WHERE date = (%s) AND id_satellite_programm in
        (SELECT id FROM satellite_programm WHERE id_satellite = 1
        AND id_programm = (%s))''', [start_dates[0][0], c_programm[0]])
        start_soilhumidity = cur.fetchall()

        # close MySQL database cursor
        cur.close()
    except:
        flash('Error')
        flash('Daten konnten nicht geladen werden - Seite erneut laden')
        return render_template('fail.html')

    # if POST-method from the load Button is requested
    # display data from selected values
    if request.method == 'POST' and request.form['loadButton'] == 'Laden':
        try:
            # request.form gets values selected in dropdown fields
            # dropdown shows names but values = ID
            satellite_id = request.form['satellite_id']
            programm_id = request.form['programm_id']
            selected_date_id = request.form['selected_date_id']

            # connection-cursor to MySQL database
            cur = mysql.connection.cursor()

            # SQL statement to display selected satellite in dropdown field
            cur.execute('SELECT name FROM satellites WHERE id = (%s)',
                        [satellite_id])
            displayed_satellite=cur.fetchone()

            # SQL statement to display selected programm in dropdown field
            cur.execute('SELECT name FROM programms WHERE id = (%s)',
                        [programm_id])
            displayed_programm=cur.fetchone()

            # SQL statement to select the ideal value of the parameters from selected programm id dropdown field
            # This value is needed to dispaly the ideal value in the charts of the dashboard

            # ideal value temperature
            cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Temperatur')''', [programm_id])
            temperature_value=cur.fetchone()

            # ideal value brightness
            cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Helligkeit')''', [programm_id])
            brightness_value=cur.fetchone()

            # ideal value airhumidity
            cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Luftfeuchtigkeit')''', [programm_id])
            airhumidity_value=cur.fetchone()

            # ideal value soilhumidity
            cur.execute('''SELECT value FROM programm_parameter WHERE id_programm = (%s) AND id_parameter in
            (SELECT id FROM parameters WHERE name = 'Bodenfeuchtigkeit')''', [programm_id])
            soilhumidity_value=cur.fetchone()

            # SQL statement to select date and time from selected values in dropdown fields
            cur.execute('''SELECT date, time FROM sensordata WHERE date >= (SELECT date FROM sensordata WHERE id = (%s)) AND id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = (%s)
            AND id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
            dates=cur.fetchall()

            # SQL statement to select temperature from selected values in dropdown fields
            cur.execute('''SELECT temperature FROM sensordata WHERE date >= (SELECT date FROM sensordata WHERE
            id = (%s)) AND id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = (%s)
            AND id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
            temperature=cur.fetchall()

            # select distinct dates for get brightness hours per day
            cur.execute('''SELECT distinct date FROM sensordata WHERE date >= (SELECT date FROM sensordata WHERE id = (%s)) AND id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = (%s)
            AND id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
            brightness_dates=cur.fetchall()

            # define list for brightness
            brightness=[]

            # for each date add up all brightess values to display brigthness hours per day
            for date in brightness_dates:
                # SQL statement to select brightness from selected values in dropdown fields
                cur.execute('''SELECT brightness FROM sensordata WHERE date = (%s) AND id_satellite_programm in
                (SELECT id FROM satellite_programm WHERE id_satellite = (%s)
                AND id_programm = (%s))''', [date, satellite_id, programm_id])
                _brightness=cur.fetchall()

                # for each value in brightness add up the new value and add new value to brightness list
                new_value=0
                for value in _brightness:
                    new_value=new_value + value[0]
                    brightness.append(new_value)

            # SQL statement to select airhumidity from selected values in dropdown fields
            cur.execute('''SELECT airhumidity FROM sensordata WHERE date >= (SELECT date FROM sensordata WHERE
            id = (%s)) AND id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = (%s)
            AND id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
            airhumidity=cur.fetchall()

            # SQL statement to select soilhumidity from selected values in dropdown fields
            cur.execute('''SELECT soilhumidity FROM sensordata WHERE date >= (SELECT date FROM sensordata WHERE
            id = (%s)) AND id_satellite_programm in
            (SELECT id FROM satellite_programm WHERE id_satellite = (%s)
            AND id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
            soilhumidity=cur.fetchall()

            # close MySQL database cursor
            cur.close()
        except:
            flash('Error')
            flash('Daten konnten nicht geladen werden - Seite und Daten erneut laden')
            return render_template('fail.html')

        # return dashboard-template with selected values in dropdown fields
        return render_template('dashboard.html', satellite_list = satellite_list, programm_list = programm_list, date_span = date_span, displayed_satellite = displayed_satellite, displayed_programm = displayed_programm, temperature_value = temperature_value, brightness_value = brightness_value, airhumidity_value = airhumidity_value, soilhumidity_value = soilhumidity_value, dates = dates, temperature = temperature, brightness = brightness, airhumidity = airhumidity, soilhumidity = soilhumidity)

    # return start-dashboard-template with data FROM satellite and programm with ID = 1 and from last inserted date in MySQL DB where satellite and programm ID = 1
    return render_template('start_dashboard.html', satellite_list = satellite_list, programm_list = programm_list, date_span = date_span, start_satellite = start_satellite, start_programm = start_programm, start_temperature_value = start_temperature_value, start_brightness_value = start_brightness_value, start_airhumidity_value = start_airhumidity_value, start_soilhumidity_value = start_soilhumidity_value, start_dates = start_dates, start_temperature = start_temperature, new_start_brightness = new_start_brightness, start_airhumidity = start_airhumidity, start_soilhumidity = start_soilhumidity)


# admin
# both methods GET and POST are allowed
# default method is GET, if nothing else is declared
@ app.route('/admin', methods = ['GET', 'POST'])
def admin():
    try:
        # connection-cursor to MySQL database
        cur=mysql.connection.cursor()

        # SQL statement to fetch all available satellites in MySQL database orderd by ID
        # cur.fetchall() generates a tupel with all selected rows from MySQl database
        cur.execute('SELECT id, name FROM satellites')
        satellite_list=cur.fetchall()

        # SQL statement to fetch all available programms in MySQL database orderd by ID
        cur.execute('SELECT id, name FROM programms')
        programm_list=cur.fetchall()

        # close MySQL database cursor
        cur.close()

        if 'user_name' in session:
            user_name=session['user_name']
            return render_template('admin.html', user_name = user_name, satellite_list = satellite_list, programm_list = programm_list)

    # exception if load data failed
    except:
        flash('Error')
        flash('Ein Fehler ist aufgetreten. Bitte Seite erneut laden.')
        return render_template('fail.html')

    # if POST-method from the 'Programm laden' button is requested
    if request.method == 'POST':
        if request.form['Button'] == 'Login':
            try:
                session['user_name']=request.form['user_name']
                user_name = request.form['user_name']
                password=request.form['password']

                cur=mysql.connection.cursor()

                cur.execute('SELECT name, password from users where name = (%s) and password = (%s)', [
                            user_name, password])
                credentials=cur.fetchall()
                user=credentials[0][0]
                pw=credentials[0][1]

                if user_name == user and password == pw:
                    return render_template('admin.html', password = password, user_name = user_name, satellite_list = satellite_list, programm_list = programm_list)

            except:
                flash('Login nicht erfolgreich')
                return render_template('fail.html')

        if request.form['Button'] == 'Logout':
            session.pop(user_name, None)
            return redirect(url_for('admin'))
                
        if request.form['Button'] == 'Programm laden':
            try:
                # request.form gets selected values in dropdown fields
                satellite_id=request.form['satellite_id']
                programm_id=request.form['programm_id']

                # connection-cursor to MySQL database
                cur=mysql.connection.cursor()

                # set current_programm from selected satellite to value from selected programm in dropdown field
                cur.execute('UPDATE satellites set current_programm = (%s) WHERE id = (%s)', [
                            programm_id, satellite_id])
                # commit updated table
                mysql.connection.commit()

                # get ip-adress from selected satellite in dropdown field
                cur.execute(
                    'SELECT ip_addr FROM satellites WHERE id = (%s)', [satellite_id])
                ip_addr = cur.fetchone()
                ip_addr = ip_addr[0]

                # select parameter values from selected programm
                cur.execute('''SELECT pp.value FROM parameters p
                join programm_parameter pp on p.id = pp.id_parameter
                join programms pr on pr.id = pp.id_programm WHERE pr.id = (%s)''', [programm_id])

                # declare parameters as variables
                programm_values = cur.fetchall()
                temperature_value = programm_values[0][0]
                brightness_value = programm_values[1][0]
                airhumidity_value = programm_values[2][0]
                soilhumidity_value = programm_values[3][0]

                # close MySQL database cursor
                cur.close()

                # post-request url to load programm
                url = f'''http://{ip_addr}:8081/post_data?temperature={temperature_value}&brightness={brightness_value}
                &air_humidity={airhumidity_value}&soil_humidity={soilhumidity_value}'''

                # send post request to url
                post = requests.post(url)

                # flash message by success
                flash('Programm erfolgreich geladen')
                return render_template('success.html')

            # exception if load programm failed
            except:
                flash('Error')
                flash('Ein Fehler ist aufgetreten - Programm erneut laden')
                return render_template('fail.html')


        # if POST-method from the 'Satellit hinzufügen' button is requested
        if request.form['Button'] == 'Satellit hinzufügen':
            try:
                # request.form gets user input from input fields
                satellite_name = request.form['satellite_name']
                ip_addr = request.form['ip_addr']

                # validation of user input
                if len(satellite_name) < 1 or len(ip_addr) < 8:
                    flash('Eingaben unvollständig oder ungültig')
                    return render_template('fail.html')

                else:
                    # connection-cursor to MySQL database
                    cur = mysql.connection.cursor()

                    # insert satellite-name and ip-adress FROM input fields into table satellites
                    cur.execute('insert into satellites (name, ip_addr) values (%s, %s)', [
                                satellite_name, ip_addr])

                    # select ID of added satellite
                    cur.execute('SELECT id FROM satellites WHERE name = (%s)', [
                                satellite_name])
                    satellite_id = cur.fetchone()

                    # select ID of all programms
                    cur.execute('SELECT id FROM programms')
                    programm_id_list = cur.fetchall()

                    # insert satellite-ID for every existing programm to generate the satellite-programm relations
                    for programm_id in programm_id_list:
                        cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [satellite_id, programm_id])

                    # commit insert statement
                    mysql.connection.commit()

                    # close MySQL database cursor
                    cur.close()

                    # flash message by success
                    flash('Satellit erfolgreich erstellt')
                    return render_template('success.html')
                    
            # exception if add satellite failed
            except:
                flash('Error')
                flash('Satellit konnte nicht erstellt werden - Satellit erneut erstellen')
                return render_template('fail.html')


        # if POST-method from the 'Programm hinzufügen' button is requested
        if request.form['Button'] == 'Programm hinzufügen':
            try:
                # request.form gets user input from input fields
                programm_name = request.form['programm_name']
                temperature = request.form['temperature']
                brightness = request.form['brightness']
                airhumidity = request.form['airhumidity']
                soilhumidity = request.form['soilhumidity']

                # validation of user input
                if len(programm_name) < 1 or len(temperature) < 1 or len(brightness) < 1 or len(airhumidity) < 1 or len(soilhumidity) < 1:
                    flash('Eingaben unvollständig oder ungültig')
                    return render_template('fail.html')
                
                else:
                    # connection-cursor to MySQL database
                    cur = mysql.connection.cursor()

                    # insert programm name and date created into table programms
                    cur.execute('insert into programms (name, date_created) values (%s, current_timestamp())', [
                                programm_name])

                    # select inserted programm id
                    cur.execute('SELECT id FROM programms WHERE name = (%s)', [
                                programm_name])
                    programm_id = cur.fetchone()

                    # select id of all satellites
                    cur.execute('SELECT id FROM satellites')
                    satellite_id_list = cur.fetchall()

                    # insert programm-ID for every existing satellite to generate the satellite-programm relations
                    for satellite_id in satellite_id_list:
                        cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [satellite_id, programm_id])

                    # insert all parameters from user input in input fields
                    cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                                VALUES (%s, (SELECT id FROM parameters WHERE name = "Temperatur"), %s)''', [programm_id, temperature])

                    cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                                VALUES (%s, (SELECT id FROM parameters WHERE name = "Helligkeit"), %s)''', [programm_id, brightness])

                    cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                                VALUES (%s, (SELECT id FROM parameters WHERE name = "Luftfeuchtigkeit"), %s)''', [programm_id, airhumidity])

                    cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                                VALUES (%s, (SELECT id FROM parameters WHERE name = "Bodenfeuchtigkeit"), %s)''', [programm_id, soilhumidity])

                    # commit insert statement
                    mysql.connection.commit()

                    # close MySQL database cursor
                    cur.close()

                    # flash message by success
                    flash('Programm erfolgreich erstellt')
                    return render_template('success.html')

            # exception if add programm failed
            except:
                flash('Error')
                flash('Programm konnte nicht erstellt werden - Programm erneut erstellen')
                return render_template('fail.html')

    # return admin-template with satellites and programm lists
    return render_template('admin_login.html')

# to run app as standalone instance
if __name__ == '__main__':
    # app is available for all users in LAN and debug mode is on
    app.run(host="0.0.0.0", debug=True)
