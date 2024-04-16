echo "Usuario del host esclavo"
read slave_user
echo "IP del host esclavo (Ejemplo: 192.168.0.3)"
read slave_host
echo "Contraseña del esclavo"
read slave_pass
echo "Contraseña de MYSQL"
read password
mkdir /var/log/mysql
chown mysql:mysql /var/log/mysql
mysql -u root -p -e "GRANT REPLICATION SLAVE ON *.* TO '$user'@'$slave' IDENTIFIED BY 'slave';flush privileges;quit;"
cat <<EOF >> /etc/my.cnf
[mysqld]
server-id               = 10
log_bin                 = /var/log/mysql/mysql-bin.log
expire_logs_days        = 10
max_binlog_size         = 100M
binlog_do_db            = asterisk
sync_binlog             = 1
EOF
systemctl restart mariadb
# Ejecutar el comando MySQL y capturar la salida en una variable
output=$(mysql -u root -p $password -e "use asterisk; FLUSH TABLES WITH READ LOCK;SHOW MASTER STATUS;")

# Imprimir la salida almacenada en la variable
echo "$output"