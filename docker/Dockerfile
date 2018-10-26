FROM resin/rpi-raspbian

RUN apt-get update && apt-get -y upgrade

# Get python + deps.  Most of these are actually for netifaces install
RUN apt-get install -y git python3 python3-pip python3-dev gcc python-rpi.gpio

RUN apt-get install -y python3-pip
#RUN python3 -m pip install RPi.GPIO

ADD https://api.github.com/repos/robotarium/vizier/git/refs/heads/master version.json
RUN git clone https://github.com/robotarium/vizier
RUN cd vizier && python3 -m pip install .

ADD https://api.github.com/repos/robotarium/power_distribution/git/refs/heads/master version.json
RUN git clone https://github.com/robotarium/power_distribution
RUN cd power_distribution && python3 -m pip install . 

