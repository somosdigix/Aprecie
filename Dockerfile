FROM python:3.4

RUN mkdir /src
WORKDIR /src

# RUN apt-get update
# RUN apt-get install -y --no-install-recommends unixodbc unixodbc-dev freetds-bin freetds-common freetds-dev libct4 libsybdb5

# RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
#   unixodbc unixodbc-dev freetds-dev freetds-common freetds-bin tdsodbc libct4 libsybdb5

# ADD freetds.conf /etc/freetds/freetds.conf
# ADD odbc.ini /etc/odbc.ini
# ADD odbcinst.ini /etc/odbcinst.ini

# /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . /src

# ENV SSH_PASSWD "root:Docker!"
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends dialog \
#     && apt-get update \
# 	&& apt-get install -y --no-install-recommends openssh-server \
# 	&& echo "$SSH_PASSWD" | chpasswd 

# COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222

ENTRYPOINT ["init.sh"]