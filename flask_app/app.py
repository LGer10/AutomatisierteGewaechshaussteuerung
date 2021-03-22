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
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, name FROM satellites')
        satellite_list = cur.fetchall()

        cur.execute('SELECT id, name FROM programms')
        programm_list = cur.fetchall()

        cur.execute(
            'SELECT distinct id, date from sensordata where date >= curdate() - interval 7 day')
        date_span = cur.fetchall()
        cur.close()

    if request.method == 'POST' and request.form['loadButton'] == 'Laden':
        satellite_name = request.form['satellite_name']
        programme_name = request.form['programm_name']
        date_span = request.form['date_span']
        cur = mysql.connection.cursor()

        cur.execute('''SELECT date, time FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)" and id_programm in (select id from programms where name = "(%s)")))''', date_span, satellite_name, programm_name)
        date_span = cur.fetchall()
        dates_list = []
        for index in range(len(date_span)):
            dates_list.append(date_span[index][0])

        cur.execute('''SELECT temperature FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)" and id_programm in (select id from programms where name = "(%s))))''', date_span, satellite_name, programm_name)
        temperature = cur.fetchall()
        temperature_list = []
        for index in range(len(temperature)):
            temperature_list.append(temperature[index][0])

        cur.execute('''SELECT brightness FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)" and id_programm in (select id from programms where name = "(%s))))''', date_span, satellite_name, programm_name)
        brightness = cur.fetchall()
        brightness_list = []
        for index in range(len(brightness)):
            brightness_list.append(brightness[index][0])

        cur.execute('''SELECT airhumidity FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)" and id_programm in (select id from programms where name = "(%s))))''', date_span, satellite_name, programm_name)
        airhumidity = cur.fetchall()
        airhumidity_list = []
        for index in range(len(airhumidity)):
            airhumidity_list.append(airhumidity[index][0])

        cur.execute('''SELECT soilhumidity FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)" and id_programm in (select id from programms where name = "(%s))))''', date_span, satellite_name, programm_name)
        soilhumidity = cur.fetchall()
        soilhumidity_list = []
        for index in range(len(soilhumidity)):
            soilhumidity_list.append(soilhumidity[index][0])

        cur.close()

        return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span, temperature_list=temperature_list, dates_list=dates_list, brightness_list=brightness_list, airhumidity_list=airhumidity_list, solihumidity_list=soilhumidity_list)

    return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_span=date_span)


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
    id_list = [10, 20, 30, 40, 50]

    id_date = ["10.03.2021", "11.03.2021",
               "12.03.2021", "13.03.2021", "15.03.2020"]
    return render_template('test.html', title='Test', max=100, id_list=id_list, id_date=id_date)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
