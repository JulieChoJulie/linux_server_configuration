# linux_server_configuration

chmod 400 /Users/hyeonjoo/Downloads/hj_linuxProject.pem
ssh -i ~/Downloads/hj_linuxProject.pem ubuntu@ec2-34-237-245-201.compute-1.amazonaws.com

sudo apt-get update
sudo apt-get upgrade

sudo nano /etc/ssh/sshd_config
change 22 - > 2200
uncomment

sudo service ssh restart

sudo timedatectl set-timezone UTC

sudo ufw status
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 2200/tcp  
sudo ufw allow 123/tcp
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status


sudo adduser grader

sudo nano /etc/sudoers.d/grader

grader ALL=(ALL) NOPASSWD:ALL


su - grader

(on local machine)
ssh-keygen
/Users/Hyeonjoo/.ssh/linuxProject
cat .ssh/linuxProject.pub

copy the contetn



mkdir .ssh
touch .ssh/authorized_keys
nano .ssh/authorized_keys

upload key pub on Amazon AWS


chmod 700 .ssh
chmod 644 .ssh/authorized_keys

sudo nano /etc/ssh/sshd_config
-> check if PasswordAuthentication no

sudo service ssh restart

ssh grader@ec2-34-238-165-67.compute-1.amazonaws.com -i ~/.ssh/linuxProject -p 2200



sudo apt-get install apache2

sudo apt-get install libapache2-mod-wsgi

sudo apt-get install postgresql

sudo -u postgres psql

=> CREATE ROLE grader WITH LOGIN PASSWORD 'whguswn';
=> CREATE DATABASE recipes;
=> \q

Change to 
engine = create_engine('postgresql://grader:whguswn@localhost/recipes')
in database_setup.py, webserver.py, and addMenu.py

sudo mkdir /var/www/recipes
sudo touch /var/www/recipes/client_secrets.json
sudo nano /var/www/recipes/client_secrets.json
=> place client_secrets.json


we also need to move app.secret_key outside of if name == 'main':



google colud platform
Authorised JavaScript origins
http://ec2-34-238-165-67.compute-1.amazonaws.com




scp -P 2200 -i /Users/Hyeonjoo/.ssh/linuxProject -r ./Project grader@ec2-34-238-165-67.compute-1.amazonaws.com:~/



sudo mv Part5-Project /var/www/recipes/

pip install pipreqs
> export PATH=$PATH:~/.local/bin is in your ~/.bashrc file.
source ~/.bashrc

pwd: /var/www/recipes
pipreqs Part5-Project/

confirm
cat Part5-Project/requirements.txt

cd Part5-Project/
pip install -r requirements.txt 




