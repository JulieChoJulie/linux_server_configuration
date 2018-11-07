# Linux Server Configuration
I took a baseline installation of a Linux server and prepare it to host my web applications. I secured your server from a number of attack vectors, install and configure a database server, and deploy one of my existing web applications onto it.

ip address: 18.233.226.44<br />
ssh port: 2200<br />
url: http://18.233.226.44.xip.io/recipes/<br />


## What I learned
* I learned how to access, secure, and perform the initial configuration of a bare-bones Linux server. 
* I learned how to install and configure a web and database server and actually host a web application.


## A List of Third-Party Resources 
* Amazon AWS EC2
* Google Cloud API (for OAuth authentication)
* Scrapy Crawler


## Summary of Softwares
* flask
* sqlalchemy
* apache2
* postgresql
* virtuallenv
* pip
* python

## Instructions

#### Launch a ubuntu instance of Amazon EC2
- Create an account or Sign in on Amazon AWS website.
- Launch a ubuntu instance of Amazon EC2 and create a new key pair and download it on your local machine.
- Set inbound rules for port 2200, 123, and 80.

#### Secure your server
- After log into the server, update the packages
```
$ sudo apt-get update
$ sudo apt-get upgrade
```

- Change the SSH port from 22 to 2200. Make sure to configure the EC2 firewall to allow it.
```
$ sudo nano /etc/ssh/sshd_config 
	* Change 22 -> 2200 and uncomment it. 
$ sudo service ssh restart	
```
	* Change 22 -> 2200 and uncomment it. 

- Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).
```
$sudo ufw status
$sudo ufw default deny incoming
$sudo ufw default allow outgoing

$sudo ufw allow 2200/tcp  
$sudo ufw allow 123/tcp
$sudo ufw allow 80/tcp
$sudo ufw enable
$sudo ufw status
```

#### Give the user **grader** access
- Create a new user account named **grader**.
`$ sudo adduser grader`
- Give grader the permission to sudo.
`$ sudo nano /etc/sudoers.d/grader`
	* and write like this below: 
		=> grader ALL=(ALL) NOPASSWD:ALL
- Create an SSH key pair for grader using the ssh-keygen tool.
	* On your local machine, 
	`$ ssh-keygen`
	* Open the public key and copy it.
	`$ cat .ssh/linuxProject.pub`
	* Go back to your server,
	```
	$ su - grader
	$ mkdir .ssh
	$ touch .ssh/authorized_keys
	$ nano .ssh/authorized_keys
	$ chmod 700 .ssh
	$ chmod 644 .ssh/authorized_keys
 	$ sudo nano /etc/ssh/sshd_config
	-> change from PasswordAuthentication yes to PasswordAuthentication no
	$ sudo service ssh restart
	```

#### Prepare to deploy your project.
- Configure the local timezone to UTC.  
`sudo timedatectl set-timezone UTC`

- Install packages we need for this project
```
$ sudo apt-get install python-pip
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
$ sudo pip install flask
```

- Install and configure PostgreSQL.
```
$ sudo apt-get install postgresql

$ sudo -u postgres psql

=> CREATE ROLE grader WITH LOGIN PASSWORD 'whguswn';
=> CREATE DATABASE catalog;
=> \q
```

#### Deploy the Item Catalog project
- Locate google API client secrets JSON file in /var/www/html/flaskapp directory.
```
$mkdir ~/flaskapp
$sudo ln -sT ~/flaskapp /var/www/html/flaskapp 
$ scp -P 2200 -i /Users/Hyeonjoo/.ssh/linuxProject -r ./client_secrets.json grader@ec2-18-233-226-44.compute-1.amazonaws.com:~/
$ sudo mv client_secrets.json ~/flaskapp/
```
- Clone and setup your Item Catalog project from the Github repository.
```
$ git clone https://github.com/JulieChoJulie/linux_server_configuration.git
$ cd ~/linux_server_configuration
$ sudo mv * ~/flaskapp
$ sudo chmod 777 flaskapp
$ mv ~/flaskapp/webserver.py ~/flaskapp/flaskapp.py
```


- Change database management systems from SQLite to postgreSQL in python files.
```
Add
import psycopg2
and Change to 
engine = create_engine('postgresql://grader:whguswn@localhost/catelog')
in database_setup.py, webserver.py, and addMenu.py
```

- Set up virtualenv and get requirements.txt file.
```
$ pip install pipreqs
> export PATH=$PATH:~/.local/bin is in your ~/.bashrc file.
$ source ~/.bashrc

$ cd ~/
$ pipreqs flaskapp/

$ sudo pip install virtualenv
$ cd ~/flaskapp
$ virtualenv -p python venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ pip install --upgrade oauth2client 
$ pip install psycopg2-binary
$ deactivate
```

- Create .msgi file and paste the content below.  
`$ sudo nano ~/flaskapp/flaskapp.msgi`
Content:
```
	import sys
	sys.path.insert(0, '/var/www/html/flaskapp')
	#activate_this is for activate the packages for virtual environment
	activate_this = '/var/www/html/flaskapp/venv/bin/activate_this.py'
	execfile(activate_this, dict(__file__=activate_this))
	from flaskapp import app as application
```	
- Create a configuration file for hosting our web application.
`$ sudo nano /etc/apache2/sites-available/flaskapp.conf`
Paste the content below.
```
	<VirtualHost *:80>
	  ServerName ubuntu
	  ServerAlias 18.233.226.44
	  ServerAdmin local@local
	  WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi
	  <Directory /var/www/html/flaskapp/>
	      Order allow,deny
	      Allow from all
	  </Directory>
	 Alias /static /var/www/html/flaskapp/static
	  <Directory /var/www/html/flaskapp/static/>
	      Order allow,deny
	      Allow from all
	  </Directory>
	  ErrorLog ${APACHE_LOG_DIR}/error.log
	  CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
```
- Enable our virtual host for our web application  
`sudo a2ensite flaskapp`
- Restart apache.  
`sudo apache2ctl restart`


## Acknowldgement
	Udacity - Full Stack Web Developer NanoDegree Program
	Icons made by Freepik from www.flaticon.com 
    Icon made by Those Icons from www.flaticon.com 
    Icon made by Smashicons from www.flaticon.com 
    https://www.webtunix.com/blog/run-flask-app-on-AWS-EC2


