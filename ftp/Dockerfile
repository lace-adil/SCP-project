FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /



RUN apt update && apt install vsftpd openssh-server sudo -y

COPY ./vsftpd.conf /etc/vsftpd.conf


RUN mkdir -p /var/run/vsftpd/empty


RUN mkdir -p ftp ftp/scp_files ftp/incidents_files ftp/other_files

# Create admin user to SSH into
RUN useradd admin && echo "admin:SCP!PROJECT" | chpasswd && mkdir /home/admin && chown admin:admin /home/admin && echo "/bin/bash" | chsh admin && usermod -aG sudo admin


COPY entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.sh"]