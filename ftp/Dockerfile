FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /



RUN apt update && apt install vsftpd -y

COPY ./vsftpd.conf /etc/vsftpd.conf


RUN mkdir -p /var/run/vsftpd/empty


RUN mkdir -p ftp ftp/scp_files ftp/incidents_files ftp/other_files



ENTRYPOINT ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]