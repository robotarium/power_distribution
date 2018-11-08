FROM resin/rpi-raspbian

COPY qemu-arm-static /usr/bin

RUN apt-get update && apt-get -y upgrade

# Get python + deps.  Most of these are actually for netifaces install
RUN apt-get install -y git python3 python3-pip python3-dev gcc python-rpi.gpio

RUN apt-get install -y python3-pip
RUN python3 -m pip install RPi.GPIO

ADD https://api.github.com/repos/robotarium/vizier/git/refs/heads/master version.json
RUN git clone https://github.com/robotarium/vizier
RUN cd vizier && python3 -m pip install .

ADD https://api.github.com/repos/robotarium/power_distribution/git/refs/heads/master version.json
RUN git clone https://github.com/robotarium/power_distribution
RUN cd power_distribution && python3 -m pip install . 

ARG ROBO_HOST
ARG ROBO_PORT

ENV ROBO_HOST ${ROBO_HOST}
ENV ROBO_PORT ${ROBO_PORT}

# Has to be in this format!  Docker doesn't like to interpret the env variables properly in JSON form
ENTRYPOINT python3 power_distribution/powdist/firmware.py -host ${ROBO_HOST} -port ${ROBO_PORT} power_distribution/config/mac_list.json
CMD [ ]
