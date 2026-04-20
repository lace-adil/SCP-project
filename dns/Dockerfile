FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /



RUN apt update && apt install openssh-server curl sudo net-tools iproute2 -y


RUN curl -o webmin-setup-repo.sh https://raw.githubusercontent.com/webmin/webmin/master/webmin-setup-repo.sh && sh webmin-setup-repo.sh -f
RUN apt install --install-recommends webmin usermin -y


# Install the BIND DNS package
RUN apt install -y bind9



COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create admin user to SSH into
RUN useradd admin && echo "admin:SCP!PROJECT" | chpasswd && mkdir /home/admin && chown admin:admin /home/admin && echo "/bin/bash" | chsh admin && usermod -aG sudo admin


ENTRYPOINT ["/bin/bash", "-c", "/entrypoint.sh"]