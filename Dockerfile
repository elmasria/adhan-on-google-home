FROM ubuntu:21.10

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y apt-utils curl

RUN mkdir /etc/localtime

RUN ln -snf /usr/share/zoneinfo/$(curl https://ipapi.co/timezone) /etc/localtime

RUN apt-get install -y  build-essential avahi-daemon avahi-discover libnss-mdns libavahi-compat-libdnssd-dev

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash

RUN apt-get install -y nodejs

RUN node  -v

RUN mkdir /usr/local/app
WORKDIR /usr/local/app
COPY src src
COPY package.json .
RUN ls -lai

RUN npm install

# CMD ["service", "dbus", " start", "&&",  "service", "avahi-daemon", " start", "&&", "npm", "start"]
CMD service dbus start && service avahi-daemon start && npm run start
