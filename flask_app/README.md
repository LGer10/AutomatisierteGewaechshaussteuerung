# automatisiertes gewächshaus | flask_app | version 0.1

## Konfiguration Raspberry Pi Model 4 B

### Installation Betriebssystem

1. Raspberry Pi Imager Tool installieren
https://www.raspberrypi.org/software/
2. OS und SD-Card auswählen und write ausführen

### Einloggen und Passwort ändern

1. Raspi an externen Monitor,Tastatur und Maus anschliessen
2. Mit default Crendentials pi/raspberry anmelden - Achtung! Tastaturlayout standardmässig auf Englisch eingestellt 

Zum Ändern folgender Befehl ausführen:
```plaintext
sudo raspi-config
```
Danach im Configuration Tool unter "Localisation Options" das Tastatur-Layout auswählen

3. Passwort ändern 

Folgende Befehl ausführen:
```plaintext
passwd
```

Neues Passwort festlegen

### Einbinden in das WLAN
1. Im File "wpa_supplicant.conf" die WLAN Credentials und das Land in welchem sich 
das Gerät befindet eintragen
```plaintext
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

network={
    ssid="yourSSID"
    psk="yourPW"
}
```
2. Reboot des Raspi 


### SSH für Remote-Zugriff aktivieren

1. Configuration-Tool aufrufen
```plaintext
sudo raspi-config
```

2. Unter "Interface Option" kann SSH aktiviert werden

Für die Remote-Verbidnug herzustellen eignet sich das Tool "Putty"

### Flask installieren

1. Python installer "pip" installieren

```plaintext
sudo apt install python3-pip
```
Bei der Verwendung von python3 muss "pip3" verwendet werden

2. Flask installieren

```plaintext
sudo pip3 install flask
```
### MySQL Datenbank installieren

1. MySQL Server installieren
```plaintext
sudo apt install mariadb-server
```
MySQL wird als Dropin-Replacement von MariaDB ausgeführt
Die Kommandozeile funktioniert mit MySQL Syntax

2. Passwort festlegen

```plaintext
sudo mysql_secure_installation
```
Löst geführte installation aus

3. Flask-MySQLdb installieren
```plaintext
sudo pip3 install Flask-MySQLdb
```

4. MySQL connector installieren
```plaintext
pip3 install mysql-connector-python
```
### Git installieren

1. Git installieren

```plaintext
sudo apt install git
```



Dieser Ordner enthält das Main-Script der Flask App, die Datenbank-Files der MySQL DB und die HTML-Files des Web-GUI.