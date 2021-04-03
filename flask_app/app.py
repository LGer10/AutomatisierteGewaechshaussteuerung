# automatisiertes gewächshaus | main-script flask_app | version 0.1

# Libraries
from flask import Flask, session, render_template, request, make_response, redirect, flash, Markup, url_for
from flask_mysqldb import MySQL

# Flask instance for app
app = Flask(__name__)

# MySQL instance for app
mysql = MySQL(app)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AGdb'
app.config['MYSQL_DB'] = 'AGdb'


# Home


@app.route('/')
def home():
    # default method is GET, if nothing else is declared
    # returns home-template
    return render_template('home.html')

# Dashboard


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
    start_temperature = cur.fetchone()

    # brightness where date = startdate
    cur.execute('''SELECT brightness FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_brightness = cur.fetchone()

    # airhumidity where date = startdate
    cur.execute('''SELECT airhumidity FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_airhumidity = cur.fetchone()

    # soilhumidity where date = startdate
    cur.execute('''SELECT soilhumidity FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_dates[0][0]])
    start_soilhumidity = cur.fetchone()

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
        temperature = cur.fetchone()

        # SQL statement to select brightness from selected values in dropdown fields
        cur.execute('''SELECT brightness FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        brightness = cur.fetchone()

        # SQL statement to select airhumidity from selected values in dropdown fields
        cur.execute('''SELECT airhumidity FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        airhumidity = cur.fetchone()

        # SQL statement to select soilhumidity from selected values in dropdown fields
        cur.execute('''SELECT soilhumidity FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date_id, satellite_id, programm_id])
        soilhumidity = cur.fetchone()

        # close MySQL database cursor
        cur.close()

        # return dashboard-template with selected values in dropdown fields
        return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, displayed_satellite=displayed_satellite, displayed_programm=displayed_programm, temperature_value=temperature_value, brightness_value=brightness_value, airhumidity_value=airhumidity_value, soilhumidity_value=soilhumidity_value, dates=dates, temperature=temperature, brightness=brightness, airhumidity=airhumidity, soilhumidity=soilhumidity)

    # return start-dashboard-template with data from satellite and programm with ID = 1 and from last inserted date in MySQL DB where satellite and programm ID = 1
    return render_template('start_dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, start_satellite=start_satellite, start_programm=start_programm, start_temperature_value=start_temperature_value, start_brightness_value=start_brightness_value, start_airhumidity_value=start_airhumidity_value, start_soilhumidity_value=start_soilhumidity_value, start_dates=start_dates, start_temperature=start_temperature, start_brightness=start_brightness, start_airhumidity=start_airhumidity, start_soilhumidity=start_soilhumidity)


# Admin
# both methods GET and POST are allowed
# Default method is GET, if nothing else is declared
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
            programm_id = request.form['satellite_id']

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
			join programms pr on pr.id = pp.id_programm where pr.id = (%s)''', [p_id])

            # close MySQL database cursor
            cur.close()

            programm_values = cur.fetchone()
            temperature_value = programm_values[0]
            brightness_value = programm_values[1]
            airhumidity_value = programm_values[2]
            soilhumidity_value = programm_values[3]

            url = f'''http://"{ip_addr}:8081/post_data?temperature={temperature_value}&brightness={brightness_value}
            &air_humidity={airhumidity_value}& soil_humidity={soilhumidity_value}'''

            post = requests.post(url)

        if request.form['Button'] == 'Satellit hinzufügen':
            satellite_name = request.form['satellite_name']
            ip_addr = request.form['ip_addr']

            cur = mysql.connection.cursor()
            cur.execute('insert into satellites (name, ip_addr) values (%s, %s)', [
                        satellite_name, ip_addr])
            cur.execute('select id from satellites where name = (%s)', [
                        satellite_name])
            satellite_id = cur.fetchone()

            cur.execute('SELECT id FROM programms')
            programm_id_list = cur.fetchall()

            for programm_id in programm_id_list:
                cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [
                            satellite_id, programm_id])

            mysql.connection.commit()
            cur.close()

            return redirect(url_for('admin'))

        if request.form['Button'] == 'Programm hinzufügen':
            programm_name = request.form['programm_name']
            temperatur = request.form['temperatur']
            helligkeit = request.form['helligkeit']
            luftfeuchtigkeit = request.form['luftfeuchtigkeit']
            bodenfeuchtigkeit = request.form['bodenfeuchtigkeit']

            cur = mysql.connection.cursor()
            cur.execute('insert into programms (name, date_created) values (%s, current_timestamp())', [
                        programm_name])

            cur.execute('select id from programms where name = (%s)', [
                        programm_name])
            programm_id = cur.fetchone()

            cur.execute('SELECT id FROM satellites')
            satellite_id_list = cur.fetchall()

            for satellite_id in satellite_id_list:
                cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [
                            satellite_id, programm_id])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Temperatur"), %s)''', [programm_id, temperatur])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Helligkeit"), %s)''', [programm_id, helligkeit])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Luftfeuchtigkeit"), %s)''', [programm_id, luftfeuchtigkeit])

            cur.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
                        VALUES (%s, (select id from parameters where name = "Bodenfeuchtigkeit"), %s)''', [programm_id, bodenfeuchtigkeit])

            mysql.connection.commit()
            cur.close()

            return redirect(url_for('admin'))

    return render_template('admin.html', satellite_list=satellite_list, programm_list=programm_list)


@app.route('/test')
def test():

    return render_template('test.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
