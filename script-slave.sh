echo "IP del host esclavo (Ejemplo: 192.168.0.3)"
read master_host
echo "Contraseña de MYSQL"
read password
echo "Nombre del archivo, ejemplo: mysql-bin.000001"
read filename
echo "Posicion, ejemplo: 32"
read pos

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
$query"CHANGE MASTER TO MASTER_HOST='$master_host',MASTER_USER='root',MASTER_PASSWORD='$master_password',MASTER_LOG_FILE='$filename',MASTER_LOG_POS=$pos;"
$query"START SLAVE;"
clear
echo "Tu servidor esclavo ha iniciado correctamente"