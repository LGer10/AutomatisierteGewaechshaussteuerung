# automatisiertes gewächshaus | main-script flask_app | version 0.1

# Libraries
from flask import Flask, session, render_template, request, make_response, redirect, flash, Markup, url_for
from flask_mysqldb import MySQL

# Flask App Instanz erstellen
app = Flask(__name__)
# MySQL Instanz für die App erstellen
mysql = MySQL(app)

# MySQL Datenbank Verbindung herstellen
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AGdb'
app.config['MYSQL_DB'] = 'AGdb'

# Startseite
# ohne Methodendeklaration ist nur die default Methode 'GET' möglich


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()

    cur.execute('SELECT id, name FROM satellites')
    satellite_list = cur.fetchall()

    cur.execute('SELECT id, name FROM programms')
    programm_list = cur.fetchall()

    cur.execute(
        'SELECT id, date from sensordata where date >= (select  max(date) - 7) group by date')
    date_span = cur.fetchall()

    cur.execute('SELECT name from satellites where id = 1')
    start_s = cur.fetchone()
    start_satellite_array = []
    start_satellite_array.append(start_s[0])
    start_satellite = start_satellite_array[0]

    cur.execute('SELECT name from programms where id = 1')
    start_p = cur.fetchone()
    start_programm_array = []
    start_programm_array.append(start_p[0])
    start_programm = start_programm_array[0]

    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Temperatur')''')
    start_temperature_v = cur.fetchone()
    start_temperature_value_array = []
    start_temperature_value_array.append(start_temperature_v[0])
    start_temperature_value = start_temperature_value_array[0]

    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Helligkeit')''')
    start_brightness_v = cur.fetchone()
    start_brightness_value_array = []
    start_brightness_value_array.append(start_brightness_v[0])
    start_brightness_value = start_brightness_value_array[0]

    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Luftfeuchtigkeit')''')
    start_airhumidity_v = cur.fetchone()
    start_airhumidity_value_array = []
    start_airhumidity_value_array.append(start_airhumidity_v[0])
    start_airhumidity_value = start_airhumidity_value_array[0]

    cur.execute('''SELECT value from programm_parameter where id_programm = 1 and id_parameter in
        (select id from parameters where name = 'Bodenfeuchtigkeit')''')
    start_soilhumidity_v = cur.fetchone()
    start_soilhumidity_value_array = []
    start_soilhumidity_value_array.append(start_soilhumidity_v[0])
    start_soilhumidity_value = start_soilhumidity_value_array[0]

    cur.execute('''SELECT date FROM sensordata where date = (SELECT max(date) FROM sensordata where id_satellite_programm in
        (SELECT id FROM satellite_programm where id_satellite = 1
        and id_programm = 1))''')
    start_dates = cur.fetchall()
    start_dates_list = []
    start_date = start_dates_list[0]

    for index in range(len(start_dates)):
        start_dates_list.append(start_dates[index][0])

    cur.execute('''SELECT temperature FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_date])
    start_temperature = cur.fetchall()
    start_temperature_list = []
    for index in range(len(start_temperature)):
        start_temperature_list.append(start_temperature[index][0])

    cur.execute('''SELECT brightness FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_date])
    start_brightness = cur.fetchall()
    start_brightness_list = []
    for index in range(len(start_brightness)):
        bstart_rightness_list.append(start_brightness[index][0])

    cur.execute('''SELECT airhumidity FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_date])
    start_airhumidity = cur.fetchall()
    start_airhumidity_list = []
    for index in range(len(start_airhumidity)):
        start_airhumidity_list.append(start_airhumidity[index][0])

    cur.execute('''SELECT soilhimidity FROM sensordata where date = (%s) and id_satellite_programm in 
    (SELECT id FROM satellite_programm where id_satellite = 1 
    and id_programm = 1)''', [start_date])
    start_soilhumidity = cur.fetchall()
    start_soilhumidity_list = []
    for index in range(len(start_soilhumidity)):
        start_soilhumidity_list.append(start_soilhumidity[index][0])

    if request.method == 'POST' and request.form['loadButton'] == 'Laden':
        satellite_id = request.form['satellite_id']
        programm_id = request.form['programm_id']
        selected_date = request.form['selected_date']

        cur = mysql.connection.cursor()
        cur.execute('SELECT name from satellites where id = (%s)',
                    [satellite_id])
        displayed_s = cur.fetchone()
        displayed_satellite_array = []
        displayed_satellite_array.append(displayed_s[0])
        displayed_satellite = displayed_satellite_array[0]

        cur.execute('SELECT name from programms where id = (%s)',
                    [programm_id])
        displayed_p = cur.fetchone()
        displayed_programm_array = []
        displayed_programm_array.append(displayed_p[0])
        displayed_programm = displayed_programm_array[0]

        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Temperatur')''', [programm_id])
        temperature_v = cur.fetchone()
        temperature_value_array = []
        temperature_value_array.append(temperature_v[0])
        temperature_value = temperature_value_array[0]

        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Helligkeit')''', [programm_id])
        brightness_v = cur.fetchone()
        brightness_value_array = []
        brightness_value_array.append(brightness_v[0])
        brightness_value = brightness_value_array[0]

        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Luftfeuchtigkeit')''', [programm_id])
        airhumidity_v = cur.fetchone()
        airhumidity_value_array = []
        airhumidity_value_array.append(airhumidity_v[0])
        airhumidity_value = airhumidity_value_array[0]

        cur.execute('''SELECT value from programm_parameter where id_programm = (%s) and id_parameter in 
        (select id from parameters where name = 'Bodenfeuchtigkeit')''', [programm_id])
        soilhumidity_v = cur.fetchone()
        soilhumidity_value_array = []
        soilhumidity_value_array.append(soilhumidity_v[0])
        soilhumidity_value = soilhumidity_value_array[0]

        cur.execute('''SELECT date FROM sensordata where date >= (SELECT date FROM sensordata where id = (%s)) and id_satellite_programm in 
        (SELECT id FROM satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date, satellite_id, programm_id])
        dates = cur.fetchall()
        dates_list = []
        for index in range(len(dates)):
            dates_list.append(dates[index][0])

        cur.execute('''SELECT temperature FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (SELECT id FROM satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date, satellite_id, programm_id])
        temperature = cur.fetchall()
        temperature_list = []
        for index in range(len(temperature)):
            temperature_list.append(temperature[index][0])

        cur.execute('''SELECT brightness FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date, satellite_id, programm_id])
        brightness = cur.fetchall()
        brightness_list = []
        for index in range(len(brightness)):
            brightness_list.append(brightness[index][0])

        cur.execute('''SELECT airhumidity FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date, satellite_id, programm_id])
        airhumidity = cur.fetchall()
        airhumidity_list = []
        for index in range(len(airhumidity)):
            airhumidity_list.append(airhumidity[index][0])

        cur.execute('''SELECT soilhumidity FROM sensordata where date >= (SELECT date from sensordata WHERE 
        id = (%s)) and id_satellite_programm in 
        (select id from satellite_programm where id_satellite = (%s) 
        and id_programm = (%s))''', [selected_date, satellite_id, programm_id])
        soilhumidity = cur.fetchall()
        soilhumidity_list = []
        for index in range(len(soilhumidity)):
            soilhumidity_list.append(soilhumidity[index][0])

        cur.close()

        return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, temperature_list=temperature_list, dates_list=dates_list, brightness_list=brightness_list, airhumidity_list=airhumidity_list, soilhumidity_list=soilhumidity_list, displayed_satellite=displayed_satellite, displayed_programm=displayed_programm, temperature_value=temperature_value, brightness_value=brightness_value, airhumidity_value=airhumidity_value, soilhumidity_value=soilhumidity_value)

    return render_template('start_dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, start_satellite=start_satellite, start_programm=start_programm, start_dates_list=start_dates_list, start_temperature_value=start_temperature_value, start_brightness_value=start_brightness_value, start_airhumidity_value=start_airhumidity_value, start_soilhumidity_value=start_soilhumidity_value, start_temperature_list=start_temperature_list, start_brightness_list=start_brightness_list, start_airhumidity_list=start_airhumidity_list, start_soilhumidity_list=start_soilhumidity_list)


# Adminseite
# Methoden 'GET' und 'POST' in dieser Route erlaubt
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name FROM satellites')
    satellite_list = cur.fetchall()
    cur.execute('SELECT id, name FROM programms')
    programm_list = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        if request.form['Button'] == 'Programm laden':
            s_id = request.form['s_id']
            p_id = request.form['p_id']
            cur = mysql.connection.cursor()
            cur.execute('UPDATE satellites set current_programm = (%s) where id = (%s)', [
                        p_id, s_id])
            cur.execute('''select p.name, pp.value from parameters p
			join programm_parameter pp on p.id = pp.id_parameter
			join programms pr on pr.id = pp.id_programm where pr.id = (%s)''', [p_id])
            mysql.connection.commit()

            cur.close()

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
