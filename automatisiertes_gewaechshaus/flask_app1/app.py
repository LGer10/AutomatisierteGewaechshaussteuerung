from flask_mysqldb import MySQL

from flask import Flask, session, render_template, request,make_response,redirect,flash, Markup
from flask import Flask
app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AGdb'
app.config['MYSQL_DB'] = 'AGdb'


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
                        cur.execute('insert into programm (id, name, date_created) values (%s, %s, current_timestamp())', [id_p, name_p])
                        mysql.connection.commit()
                        return render_template('admin.html')


@app.route('/dashboard')
def dashboard():
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, name FROM satellites')
        list = cur.fetchall()
        cur.execute('SELECT id, name FROM programms')
        listP = cur.fetchall()
        cur.execute('SELECT distinct id, date from sensordata where date > curdate() - interval 7 day')
        listD = cur.fetchall()

        cur = mysql.connection.cursor()
        cur.execute('SELECT temperature FROM sensordata where id_satellite = 1 and id_programm = 1')
        list = cur.fetchall()
        id_list = []
        for index in range(len(list)):
                id_list.append(list[index][0])

        cur.execute('SELECT date from sensordata where id_satellite = 1 and id_programm = 1')
        date= cur.fetchall()
        id_date = []
        for index in range(len(date)):
                id_date.append(date[index][0])
        cur.close()
        return render_template('dashboard.html', list=list, listP=listP, listD=listD, id_list=id_list, id_date=id_date)




@app.route('/test')
def test():
        id_list = [10, 20, 30, 40, 50]

        id_date = ["10.03.2021", "11.03.2021","12.03.2021", "13.03.2021", "15.03.2020"]
        return render_template('test.html', title='Test', max=100, id_list=id_list, id_date=id_date)


if __name__ == '__main__':
        app.run(host= "0.0.0.0", debug=True)

