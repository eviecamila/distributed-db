echo "Usuario del host esclavo"
read slave_user
echo "IP del host esclavo (Ejemplo: 192.168.0.3)"
read slave_host
echo "Contraseña de MYSQL"
read password
mkdir /var/log/mysql
chown mysql:mysql /var/log/mysql
query="mysql -u root -p $password asterisk -e "
$query"GRANT REPLICATION SLAVE ON *.* TO '$slave_user'@'$slave_host' IDENTIFIED BY 'slave';flush privileges;"
sed -i "s/[mysqld]/[mysqld]\nserver-id               = 10\nlog_bin                 = /var/log/mysql/mysql-bin.log\nexpire_logs_days        = 10\nmax_binlog_size         = 100M\nbinlog_do_db            = asterisk\nsync_binlog             = 1/g" /etc/my.cnf
systemctl restart mariadb
# Ejecutar el comando MySQL y capturar la salida en una variable
output=$($query"use asterisk; FLUSH TABLES WITH READ LOCK;SHOW MASTER STATUS;")

# Imprimir la salida almacenada en la variable
cd /tmp
mysqldump -u root -p $password asterisk > asteriskslave.sql
scp asteriskslave.sql $slave_user@$slave_host:/tmp
$query"UNLOCK TABLES;"

echo $output > out.txt
clear
echo "detalles del archivo"
echo $output
echo "fueron guardados en out.txt"
