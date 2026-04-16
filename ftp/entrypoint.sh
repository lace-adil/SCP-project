service ssh start
service vsftpd start
chown root:root /ftp -R
mkdir -p ftp ftp/files/scp_files ftp/files/incidents_files ftp/files/other_files
#chmod -R 777 /ftp
#chmod 755 /ftp
tail -f /dev/null