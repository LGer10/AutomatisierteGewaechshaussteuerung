# automatisiertes gewächshaus | main-script flask_app | version 0.1

#Libraries
from flask import Flask, session, render_template, request,make_response,redirect,flash, Markup
from flask_mysqldb import MySQL

#Flask App Instanz erstellen
app = Flask(__name__)
#MySQL Instanz für die App erstellen
mysql = MySQL(app)

#MySQL Datenbank Verbindung herstellen
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AGdb'
app.config['MYSQL_DB'] = 'AGdb'

#Startseite
#ohne Methodendeklaration ist nur die default Methode 'GET' möglich
@app.route('/')
def home():
        return render_template('home.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
        if request.method =='GET':
                cur = mysql.connection.cursor()
                cur.execute('SELECT id, name FROM satellites')
                satellite_list = cur.fetchall()

                cur.execute('SELECT id, name FROM programms')
                programm_list = cur.fetchall()

                cur.execute('SELECT distinct id, date from sensordata where date >= curdate() - interval 7 day')
                date_list = cur.fetchall()

        if request.method == 'POST'and request.form['loadButton'] == 'Laden':
                satellite_name= request.form['satellite_name']
                programme_name= request.form['programm_name']
                date_span = request.form['date_span']
                
                cur.execute('''SELECT date, time FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)" and id_programm in (select id from programms where name = "(%s)")))''', date_span, satellite_name, programm_name)
                dates = cur.fetchall()
                dates_list = []
                for index in range(len(dates)):
                        dates_list.append(dates[index][0])
                
                cur = mysql.connection.cursor()
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
                        
                return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_list=date_list, temperature_list=temperature_list, dates_list=dates_list, brightness_list=brightness_list, airhumidity_list=airhumidity_list, solihumidity_list=soilhumidity_list)

        return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_list=date_list)               


#Adminseite
#Methoden 'GET' und 'POST' in dieser Route erlaubt
@app.route('/admin', methods=['GET','POST'])
def admin():
	if request.method == 'GET':
                cur= mysql.connection.cursor()
                cur.execute('SELECT id, name FROM satellites')
                satellite_list = cur.fetchall()
                cur.execute('SELECT id, name FROM programms')
                programm_list = cur.fetchall()
        
                return render_template('admin.html', satellite_list=satellite_list, programm_list=programm_list)

        if request.method =='POST':
                if request.form['Button'] == 'Programm laden':
                        satellite_name= request.form['satellite_name']
                        programme_name= request.form['programm_name']
                        cur= mysql.connection.cursor()
                        cur.execute('''select p.name, pp.value from parameters p
                        join programm_parameter pp on p.id = pp.id_parameter
                        join programms pr on pr.id = pp.id_programm where pr.name = (%s)''', [programme_name])
                   
                if request.form['Button'] == 'Satellit hinzufügen':
                        satellite_name = request.form['satellite_name']
                        ip_addr = request.form['ip_addr']
                        cur= mysql.connection.cursor()
                        cur.execute('insert into satellites (name, ip_addr) values (%s, %s)', [satellite_name, ip_addr])
                        mysql.connection.commit()
                        satellite_id = cur.execute('select id from satellites where name = (%s)', satellite_name)
                        
                        
                        cur.execute('SELECT name FROM programms')
                        programm_list = cur.fetchall()

                        for programm in programm_list:
                                programm_id = cur.execute('select id from programms where name = (%s)', [programm])

                                cur.execute('insert into satellite_programm (id_satellite, id_programm) VALUES (%s, %s)', [satellite_id, programm_id])
                                mysql.connection.commit()
                                

                if request.form['Button'] == 'Programm hinzufügen':
                        programm_name= request.form['programm_name']
                        temperatur= request.form['temperatur']
                        helligkeit = request.form['helligkeit']
                        luftfeuchtigkeit = request.form['luftfeuchtigkeit']
                        bodenfeuchtigkeit = request.form['bodenfeuchtigkeit']
                        cur= mysql.connection.cursor()
                        cur.execute('insert into programms (name, temperature, brightness, airhumidity, soilhumidity) values (%s, %s, %s, %s, %s)', [programm_name, temperatur, helligkeit, luftfeuchtigkeit, bodenfeuchtigkeit])
                        mysql.connection.commit()

        return render_template('admin.html')


@app.route('/test')
def test():
        id_list = [10, 20, 30, 40, 50]

        id_date = ["10.03.2021", "11.03.2021","12.03.2021", "13.03.2021", "15.03.2020"]
        return render_template('test.html', title='Test', max=100, id_list=id_list, id_date=id_date)


if __name__ == '__main__':
        app.run(host= "0.0.0.0", debug=True)

