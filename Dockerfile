# Version 0.1-dev
# DO NOT RUN THIS AS PRODUCTION
FROM streamweaver/evennia
MAINTAINER Scott Turnbull "streamweaver@gmail.com"

VOLUME /opt/eldennia
WORKDIR /opt/eldennia

EXPOSE 4000 4001 5000 5001 8000 8001 8021 8022

ENTRYPOINT ["evennia"]
