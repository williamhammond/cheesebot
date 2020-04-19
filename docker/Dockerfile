FROM python:3.7-slim

USER root
ARG VERSION=4.10

RUN apt-get update && apt-get install --assume-yes --no-install-recommends --no-show-upgraded \ 
    git \
    make \
    wget \
    unzip

RUN wget http://blzdistsc2-a.akamaihd.net/Linux/SC2.$VERSION.zip \
    && unzip -P iagreetotheeula SC2.$VERSION.zip \
    && rm *.zip

