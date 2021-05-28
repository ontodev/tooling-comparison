FROM obolibrary/odkfull:v1.2.28
LABEL maintainer="james@overton.ca"

RUN apt-get install -y time
CMD python3 src/run.py
