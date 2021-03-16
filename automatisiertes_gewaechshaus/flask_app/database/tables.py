import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  database="AGdb",
  user="root",
  password="AGdb"

)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE satellites (id int NOT NULL AUTO_INCREMENT  PRIMARY KEY, name varchar(20), ip_addr varchar(36))")
mycursor.execute("CREATE TABLE programms (id int NOT NULL AUTO_INCREMENT PRIMARY KEY , name varchar(20), date_created timestamp)")
mycursor.execute('''CREATE TABLE satellite_programm (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_satellite int, id_programm int, FOREIGN KEY (id_satellite)
REFERENCES satellites(id), FOREIGN KEY (id_programm) REFERENCES programms(id))''')
mycursor.execute('''CREATE TABLE sensordata (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_satellite_programm int, date date, time time, temperature float(3),
brightness int(4), airhumidity float(3), soilhumidity float(3), FOREIGN KEY (id_satellite_programm) REFERENCES satellite_programm(id))''')
mycursor.execute("CREATE TABLE parameters (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(20), unit varchar(5))")
mycursor.execute("CREATE TABLE programm_parameter (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_programm int, id_parameter int, value  varchar(4))")
