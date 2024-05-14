# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM
LABEL org.opencontainers.image.source https://github.com/unl0ck/homeassistant-addon-viessmann-gridbox
RUN \
  apk add --no-cache \
  python3 py3-pip
RUN ln -sf python3 /usr/bin/python
COPY rootfs /
#WORKDIR /data

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
  curl -sSLf -o /usr/bin/tempio \
  "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# Copy root filesystem
COPY GridboxConnector/ /build/GridboxConnector
COPY cloudSettings.json /data/cloudSettings.json
COPY cloudSettings.json /build/.
WORKDIR /build/GridboxConnector
RUN pip install -r requirements.txt
COPY run.sh /run.sh
RUN chmod a+x /run.sh
COPY rootfs /
#CMD [ "/run.sh" ]
