echo "IP del host esclavo (Ejemplo: 192.168.0.3)"
read master_host
echo "Contraseña de MYSQL"
read password
echo "Nombre del archivo, ejemplo: mysql-bin.000001"
read filename
echo "Posicion, ejemplo: 32"
read pos

# Editar el archivo de configuración my.cnf
sed -i '/^\[mysqld\]$/a\
server-id=20\n\
replicate-do-db=asteriskcdrdb\n\
skip_slave_start\n\
read_only' /etc/my.cnf

systemctl restart mariadb
cd /tmp

query="mysql -u root -p$password asteriskcdrdb -e "
$query"CHANGE MASTER TO MASTER_HOST='$master_host',MASTER_USER='root',MASTER_PASSWORD='$master_password',MASTER_LOG_FILE='$filename',MASTER_LOG_POS=$pos;"
$query"START SLAVE;"
clear
echo "Tu servidor esclavo ha iniciado correctamente"