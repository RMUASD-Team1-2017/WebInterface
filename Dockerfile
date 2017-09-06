FROM python:3.6.2-jessie

SHELL ["/bin/bash", "-c"]
RUN mkdir -p /usr/src/
ADD . /usr/src/app/
WORKDIR /usr/src/app/

#Install python requirements

RUN pip install -r requirements.txt
RUN ["chmod", "+x", "run.sh", "test.sh", "start.sh"]
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/start.sh"]
CMD ["run"]
