FROM arm32v6/alpine

RUN apk update && apk upgrade

# Get python + deps.  Most of these are actually for netifaces install
RUN apk add git python3 python3-dev gcc musl-sdev linux-headers python-rpi.gpio

ADD https://api.github.com/repos/robotarium/vizier/git/refs/heads/master version.json
RUN git clone https://github.com/robotarium/vizier
RUN cd vizier && python3 -m pip install .

ADD https://api.github.com/repos/robotarium/power_distribution/git/refs/heads/master version.json
RUN git clone https://github.com/robotarium/power_distribution
RUN cd gritsbot_2 && python3 -m pip install . 

