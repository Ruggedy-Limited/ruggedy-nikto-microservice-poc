##########################################################################
# Ruggedy Nikto MicroService Docker Container                            #
# Author: Ruggedy.io                                                     #
# Version 0.1 Beta                                                       #
##########################################################################

FROM ubuntu:16.04
MAINTAINER Ruggedy <hello@ruggedy.io>

##########################################################################
# Initial Server and Environment Settings                                #
##########################################################################

RUN DEBIAN_FRONTEND=noninteractive
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LC_CTYPE=UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=C
ENV TERM xterm

##########################################################################
# Repositories                                                           #
##########################################################################

RUN apt-get update
RUN apt-get upgrade -y --force-yes
RUN apt-get install -y --force-yes \
    supervisor \
    cron \
    curl \
    python-pip \
    libssl-dev \
    libcurl4-openssl-dev \
    python-dev \
    sqlite \
    nikto 

RUN pip install pycurl flask flask-restful flask-jsonpify flask-sqlalchemy

##########################################################################
# Configure Supervisor                                                   #
##########################################################################

RUN mkdir -p /var/log/supervisor
ADD Files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
VOLUME ["/var/log/supervisor"]

##########################################################################
# Install and start the cron                                             #
##########################################################################

ADD Files/targets.txt /usr/bin/
ADD Files/parse.py /usr/bin/
RUN chmod +x /usr/bin/parse.py
ADD Files/crontab /etc/cron.d/nikto-cron
RUN chmod 0600 /etc/cron.d/nikto-cron
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/nikto-cron

CMD ["/usr/bin/supervisord"]

EXPOSE 5000
