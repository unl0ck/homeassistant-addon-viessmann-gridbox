# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
  org.opencontainers.image.source="https://github.com/unl0ck/homeassistant-addon-viessmann-gridbox" \
  org.opencontainers.image.authors="Simon Helming <simon@helming.xyz>" \
  maintainer="Simon Helming <simon@helming.xyz>"\
  io.hass.type="addon" \
  org.opencontainers.image.created=${BUILD_DATE} \
  org.opencontainers.image.revision=${BUILD_REF} \
  org.opencontainers.image.version=${BUILD_VERSION}

ENV LOGFIRE_TOKEN=${LOGFIRE_TOKEN}
ENV LOGFIRE_TOKEN_EDGE=${LOGFIRE_TOKEN_EDGE}

RUN \
  apk add --no-cache \
  python3 py3-pip
RUN ln -sf python3 /usr/bin/python
COPY rootfs /


# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH
RUN \
  curl -sSLf -o /usr/bin/tempio \
  "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# Copy root filesystem
COPY GridboxConnector/ /build/GridboxConnector
COPY cloudSettings.json /data/cloudSettings.json
COPY cloudSettings.json /build/cloudSettings.json

RUN cd /build/GridboxConnector && pip install -r requirements.txt

COPY rootfs /

