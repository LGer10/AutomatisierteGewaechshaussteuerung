#!/usr/bin/python3

# automatisiertes gewächshaus | main-script flask_app | version 0.1

# ibraries
from flask import Flask, session, render_template, request, make_response, redirect, flash, Markup, url_for
from flask_mysqldb import MySQL
import requests

# flask instance for app
app = Flask(__name__)

# MySQL instance for app
mysql = MySQL(app)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AGdb'
app.config['MYSQL_DB'] = 'AGdb'


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
    cur.execute(
        'SELECT id, date from sensordata where date >= (select  max(date) - 7) group by date')
    date_span = cur.fetchall()

    # By entering the dashboard via GET-request, data from the last day inserted into the MySQL database
    # and from the satellite with ID = 1 and programm with ID = 1 should automatically be displayed

    # SQL statement to select satellite and programm with ID = 1
    # cur-fetchone() generates a tupel of all data in one MySQL row, as only one satellite ad one programm is selected
    # the object can be called as [0] object of the tupel

    # start satellite
    cur.execute('SELECT name from satellites where id = 1')
    start_satellite = cur.fetchone()

    # start programm
    cur.execute('SELECT name from programms where id = 1')
    start_programm = cur.fetchone()

    # SQL statement to select the ideal value of the parameters from programm with ID = 1
    # This value is needed to dispaly the ideal value in the charts of the dashboard

    # ideal value temperature
    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
    (select id from parameters where name = 'Temperatur')''')
    start_temperature_value = cur.fetchone()

    # ideal value brighteness
    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Helligkeit')''')
    start_brightness_value = cur.fetchone()

    # ideal value airhumidity
    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Luftfeuchtigkeit')''')
    start_airhumidity_value = cur.fetchone()

    # ideal value soilhumidity
    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Bodenfeuchtigkeit')''')
    start_soilhumidity_value = cur.fetchone()

    # To only display datapoints from the last inserted day into MySQL database with satellite and programm ID = 1,
    # date and time are selected where date is the highest date available with satellite and programm ID = 1
    # and where satellite and programm ID = 1
    # cur-fetchall()) generates a tupel of all data in one or more MySQL rows, as date and time is selected
    # the objects of both rows can be called as [0][0] object of the tupel

    # date and time
    cur.execute('''SELECT date, time FROM sensordata where date = (SELECT max(date) FROM sensordata where id_satellite_programm in
        (SELECT id FROM satellite_programm where id_satellite = 1
        and id_programm = 1)) and id_satellite_programm in
        (SELECT id FROM satellite_programm where id_satellite = 1
        and id_programm = 1)''')
    start_dates = cur.fetchall()

    # temperature where date = startdate
    cur.execute('''SELECT temperature FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_temperature = cur.fetchall()

    # brightness where date = startdate
    cur.execute('''SELECT brightness FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_brightness = cur.fetchall()

    new_start_brightness = {}
    new_value = 0
    for value in start_brightness:
        new_value = new_value + value
        new_start_brightness = new_start_brightness + new_value

    # airhumidity where date = startdate
    cur.execute('''SELECT airhumidity FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_airhumidity = cur.fetchall()

    # soilhumidity where date = startdate
    cur.execute('''SELECT soilhumidity FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_soilhumidity = cur.fetchall()

    # close MySQL database cursor
    cur.close()

    # if POST-method from the load Button is requested
    # display data from selected values
    if request.method == 'POST' and request.form['loadButton'] == 'Laden':

        # request.form gets values selected in dropdown fields
        # dropdown shows names but values = ID
        satellite_id = request.form['satellite_id']
        programm_id = request.form['programm_id']
        selected_date_id = request.form['selected_date_id']

        # connection-cursor to MySQL database
        cur = mysql.connection.cursor()

        # SQL statement to display selected satellite in dropdown field
        cur.execute('SELECT name from satellites where id = (%s)',
                    [satellite_id])
        displayed_satellite = cur.fetchone()

        # SQL statement to display selected programm in dropdown field
        cur.execute('SELECT name from programms where id = (%s)',
                    [programm_id])
        displayed_programm = cur.fetchone()

        # SQL statement to select the ideal value of the parameters from selected programm id dropdown field
        # This value is needed to dispaly the ideal value in the charts of the dashboard

        # ideal value temperature
        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in
        (select id from parameters where name = 'Temperatur')''', [programm_id])
        temperature_value = cur.fetchone()

        # ideal value brightness
        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Helligkeit')''', [programm_id])
        brightness_value = cur.fetchone()

        # ideal value airhumidity
        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Luftfeuchtigkeit')''', [programm_id])
        airhumidity_value = cur.fetchone()

        # ideal value soilhumidity
        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Bodenfeuchtigkeit')''', [programm_id])
        soilhumidity_value = cur.fetchone()

        # SQL statement to select date and time from selected values in dropdown fields
        cur.execute('''SELECT date, time FROM sensordata where date >= (SELECT date FROM sensordata where id = (%s)) and id_satellite_programm in 
        (SELECT id FROM satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        dates = cur.fetchall()

        # SQL statement to select temperature from selected values in dropdown fields
        cur.execute('''SELECT temperature FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (SELECT id FROM satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        temperature = cur.fetchall()

        cur.execute('''SELECT distinct date FROM sensordata where date >= (SELECT date FROM sensordata where id = (%s)) and id_satellite_programm in 
        (SELECT id FROM satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        brightness_dates = cur.fetchall()

        brightness = {}
        for date in brightness_dates[0]:
            # SQL statement to select brightness from selected values in dropdown fields
            cur.execute('''SELECT brightness FROM sensordata where date = (%s) and id_satellite_programm in 
            (select id from satellite_programm where id_satellite = (%s) 
            and id_programm = (%s))''', [date, satellite_id, programm_id])
            _brightness = cur.fetchall()

            new_brightness = {}
            new_value = 0
            for value in _brightness:
                new_value = new_value + value
                new_brightness = new_brightness + new_value
            
            brightness = brightness + new_brightness

        # SQL statement to select airhumidity from selected values in dropdown fields
        cur.execute('''SELECT airhumidity FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        airhumidity = cur.fetchall()

        # SQL statement to select soilhumidity from selected values in dropdown fields
        cur.execute('''SELECT soilhumidity FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        soilhumidity = cur.fetchall()

        # close MySQL database cursor
        cur.close()

        # return dashboard-template with selected values in dropdown fields
        return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, displayed_satellite=displayed_satellite, displayed_programm=displayed_programm, temperature_value=temperature_value, brightness_value=brightness_value, airhumidity_value=airhumidity_value, soilhumidity_value=soilhumidity_value, dates=dates, temperature=temperature, brightness=brightness, airhumidity=airhumidity, soilhumidity=soilhumidity)

    # return start-dashboard-template with data from satellite and programm with ID = 1 and from last inserted date in MySQL DB where satellite and programm ID = 1
    return render_template('start_dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, start_satellite=start_satellite, start_programm=start_programm, start_temperature_value=start_temperature_value, start_brightness_value=start_brightness_value, start_airhumidity_value=start_airhumidity_value, start_soilhumidity_value=start_soilhumidity_value, start_dates=start_dates, start_temperature=start_temperature, new_start_brightness=new_start_brightness, start_airhumidity=start_airhumidity, start_soilhumidity=start_soilhumidity)


# admin
# both methods GET and POST are allowed
# default method is GET, if nothing else is declared
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # connection-cursor to MySQL database
    cur = mysql.connection.cursor()

    # SQL statement to fetch all available satellites in MySQL database orderd by ID
    # cur.fetchall() generates a tupel with all selected rows from MySQl database
    cur.execute('SELECT id, name FROM satellites')
    satellite_list = cur.fetchall()

    # SQL statement to fetch all available programms in MySQL database orderd by ID
    cur.execute('SELECT id, name FROM programms')
    programm_list = cur.fetchall()

    # close MySQL database cursor
    cur.close()

    # if POST-method from the 'Programm laden' button is requested
    if request.method == 'POST':
        if request.form['Button'] == 'Programm laden':
            # request.form gets seected values in dropdown fields
            satellite_id = request.form['satellite_id']
            programm_id = request.form['programm_id']

            # connection-cursor to MySQL database
            cur = mysql.connection.cursor()

            # set current_programm from selected satellite to value from selected programm in dropdown field
            cur.execute('UPDATE satellites set current_programm = (%s) where id = (%s)', [
                        programm_id, satellite_id])
            # commit updated table
            mysql.connection.commit()

            # get ip-adress from selected satellite in dropdown field
            cur.execute(
                'SELECT ip_addr from satellites WHERE id = (%s)', satellite_id)
            ip_addr = cur.fetchone()
            ip_addr = ip_addr[0]

            # select parameter values from selected programm
            cur.execute('''select pp.value from parameters p
			join programm_parameter pp on p.id = pp.id_parameter
			join programms pr on pr.id = pp.id_programm where pr.id = (%s)''', [programm_id])

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

        # if POST-method from the 'Satellit hinzufügen' button is requested
        if request.form['Button'] == 'Satellit hinzufügen':
            # request.form gets user input from input fields
            satellite_name = request.form['satellite_name']
            ip_addr = request.form['ip_addr']

            # connection-cursor to MySQL database
            cur = mysql.connection.cursor()

            # insert satellite-name and ip-adress from input fields into table satellites
            cur.execute('insert into satellites (name, ip_addr) values (%s, %s)', [
                        satellite_name, ip_addr])

            # select ID of added satellite
            cur.execute('select id from satellites where name = (%s)', [
                        satellite_name])
            satellite_id = cur.fetchone()

            # select ID of all programms
            cur.execute('SELECT id FROM programms')
            programm_id_list = cur.fetchall()

            # insert satellite-ID for every existing programm to generate the satellite-programm relations
            for programm_id in programm_id_list:
                cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [
                            satellite_id, programm_id])

            # commit insert statement
            mysql.connection.commit()

            # close MySQL database cursor
            cur.close()

            # redirect to admin route
            return redirect(url_for('admin'))

        # if POST-method from the 'Programm hinzufügen' button is requested
        if request.form['Button'] == 'Programm hinzufügen':
            # request.form gets user input from input fields
            programm_name = request.form['programm_name']
            temperature = request.form['temperature']
            brightness = request.form['brightness']
            airhumidity = request.form['airhumidity']
            soilhumidity = request.form['soilhumidity']

            # connection-cursor to MySQL database
            cur = mysql.connection.cursor()

            # insert programm name and date created into table programms
            cur.execute('insert into programms (name, date_created) values (%s, current_timestamp())', [
                        programm_name])

            # select inserted programm id
            cur.execute('select id from programms where name = (%s)', [
                        programm_name])
            programm_id = cur.fetchone()

            # select id of all satellites
            cur.execute('SELECT id FROM satellites')
            satellite_id_list = cur.fetchall()

            # insert programm-ID for every existing satellite to generate the satellite-programm relations
            for satellite_id in satellite_id_list:
                cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [
                            satellite_id, programm_id])

            # insert all parameters from user input in input fields
            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Temperatur"), %s)''', [programm_id, temperatur])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Helligkeit"), %s)''', [programm_id, helligkeit])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Luftfeuchtigkeit"), %s)''', [programm_id, luftfeuchtigkeit])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Bodenfeuchtigkeit"), %s)''', [programm_id, bodenfeuchtigkeit])

            # commit insert statement
            mysql.connection.commit()

            # close MySQL database cursor
            cur.close()

            # redirect to admin route
            return redirect(url_for('admin'))
    # return admin-template with satellites and programm lists
    return render_template('admin.html', satellite_list=satellite_list, programm_list=programm_list)


@app.route('/test')
def test():

    return render_template('test.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
