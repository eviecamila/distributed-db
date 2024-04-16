echo "Usuario del host maestro"
read master_user
echo "IP del host esclavo (Ejemplo: 192.168.0.3)"
read master_host
echo "Contraseña de MYSQL"
read password

# Editar el archivo de configuración my.cnf
cat <<EOF >> /etc/my.cnf
[mysqld]
server-id=20
master-connect-retry=60
replicate-do-db=asterisk
skip_slave_start
read_only
EOF

systemctl restart mariadb
cd /tmp

query="mysql -u root -p$password asterisk -e "
$query"CHANGE MASTER TO MASTER_HOST='192.168.142.248',MASTER_USER='fulano',MASTER_PASSWORD='sesamo',MASTER_LOG_FILE='mysql-bin.000001',MASTER_LOG_POS=98;"
$query"START SLAVE;"
clear
echo "Tu servidor esclavo ha iniciado correctamente"