#en el caso de que se te mueva la POS o el filename para la replicacion

echo "IP del host esclavo (Ejemplo: 192.168.0.3)"
read master_host
echo "Contraseña de MYSQL"
read password
echo "Nombre del archivo, ejemplo: mysql-bin.000001"
read filename
echo "Posicion, ejemplo: 32"
read $pos
read posmysql -u root -p$password asterisk -e "stop slave; CHANGE MASTER TO MASTER_HOST='$master_host',MASTER_USER='root',MASTER_PASSWORD='$master_password',MASTER_LOG_FILE='$filename',MASTER_LOG_POS=$pos;"
$query"START SLAVE;"