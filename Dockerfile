FROM fedora:28
LABEL maintainer "Chris Collins <collins.christopher@gmail.com>"


RUN dnf install --assumeyes python-pip python-devel make gcc\
      && pip --no-cache install web.py

WORKDIR /uwsgi
ENV UWSGI https://projects.unbit.it/downloads/uwsgi-latest.tar.gz
RUN curl $UWSGI | tar xzv --strip-components 1 \
      && make \
      && chmod +x uwsgi

WORKDIR /pyku
ENV PYKU https://github.com/clcollins/pyku/archive/v1.0.tar.gz 
COPY ./ ./

EXPOSE 9090

USER 1000

CMD [ "/uwsgi/uwsgi", "--http", ":9090", "--wsgi-file", "/pyku/pyku-web.py" ]
