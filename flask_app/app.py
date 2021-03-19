# automatisiertes gewächshaus | main-script flask_app | version 0.1

from flask import Flask, session, render_template, request,make_response,redirect,flash, Markup
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sml12345'
app.config['MYSQL_DB'] = 'AutoGewaechshaus'


@app.route('/')
def home():
        return render_template('home.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
        if request.method=='GET':
                cur= mysql.connection.cursor()
                cur.execute('SELECT id, name FROM satellites')
                list = cur.fetchall()
                cur.execute('SELECT id, name FROM programm')
                listP = cur.fetchall()
                return render_template('admin.html', list=list, listP=listP)

        if request.method=='POST':
                if request.form['addButton'] == 'Add Satellite':
                        id= request.form['id']
                        name= request.form['name']
                        ip_addr = request.form['ip_addr']
                        cur= mysql.connection.cursor()
                        cur.execute('insert into satellites (id, name, ip_addr) values (%s, %s, %s)', [id, name, ip_addr])
                        mysql.connection.commit()
                        return render_template('admin.html')

                if request.form['addButton'] == 'Add Programm':
                        id_p = request.form['id_p']
                        name_p= request.form['name_p']
                        temp= request.form['temp']
                        hell = request.form['hell']
                        l_feu = request.form['l_feu']
                        b_feu = request.form['b_feu']
                        cur= mysql.connection.cursor()
                        cur.execute('insert into programm (id, name, temp, brightness, airhumidity, soilhumidity) values (%s, %s, %s, %s, %s, %s)', [id_p, name_p, temp, hell, l_feu, b_feu])
                        mysql.connection.commit()
                        return render_template('admin.html')


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
        if request.method =='GET':
                cur = mysql.connection.cursor()
                cur.execute('SELECT id, name FROM satellites')
                satellite_list = cur.fetchall()

                cur.execute('SELECT id, name FROM programms')
                programm_list = cur.fetchall()

                cur.execute('SELECT distinct id, date from sensordata where date > curdate() - interval 7 day')
                date_list = cur.fetchall()

        if request.method =='GET' and request.form['AnzeigenButton'] == 'Anzeigen':
                satellite_name= request.args.get(['satellite_name'])
                programme_name= request.args.get(['programm_name'])
                date_span = request.args.get(['date_span'])
                cur = mysql.connection.cursor()
                cur.execute('''SELECT temperature FROM sensordata where date >= (%s) and id_satellite_programm in (select id from satellite_programm where id_satellite in 
                (select id from satellites where name = "(%s)") and id_programm in (select id from programms where name = "(%s))''',date_span, satellite_name, programm_name))
                temperature = cur.fetchall()
                temperature_list = []
                for index in range(len(temperature)):
                        temperature_list.append(temperature[index][0])

                cur.execute('SELECT date from sensordata where id_satellite = 1 and id_programm = 1')
                dates = cur.fetchall()
                dates_list = []
                for index in range(len(dates)):
                        dates_list.append(dates[index][0])

                cur.execute('SELECT brightness from sensordata where id_satellite = 1 and id_programm = 1')
                brightness = cur.fetchall()
                brightness_list = []
                for index in range(len(brightness)):
                        brightness_list.append(brightness[index][0])

                cur.execute('SELECT airhumidity from sensordata where id_satellite = 1 and id_programm = 1')
                airhumidity = cur.fetchall()
                airhumidity_list = []
                for index in range(len(airhumidity)):
                        airhumidity_list.append(airhumidity[index][0])

                cur.execute('SELECT soilhumidity from sensordata where id_satellite = 1 and id_programm = 1')
                soilhumidity = cur.fetchall()
                soilhumidity_list = []
                for index in range(len(soilhumidity)):
                        asoilhumidity_list.append(soilhumidity[index][0])

                cur.close()
                
                return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_list=date_list, temperature_list=temperature_list, dates_list=dates_list, brightness_list=brightness_list, airhumidity_list=airhumidity_list, solihumidity_list=soilhumidity_list)

        return render_template('dashboard.html', satellite_list=satellite_list, programm_list=programm_list, date_list=date_list)



@app.route('/test')
def test():
        id_list = [10, 20, 30, 40, 50]

        id_date = ["10.03.2021", "11.03.2021","12.03.2021", "13.03.2021", "15.03.2020"]
        return render_template('test.html', title='Test', max=100, id_list=id_list, id_date=id_date)


if __name__ == '__main__':
        app.run(host= "0.0.0.0", debug=True)

