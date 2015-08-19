FROM phusion/baseimage

RUN apt-get update && apt-get upgrade -y && apt-get install -y  python-pip nano vim gdal-bin libgeos-c1 && apt-get clean

RUN apt-get install -y libpq-dev
RUN apt-get install -y python-dev

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt

EXPOSE 8000

CMD ["/start.sh"]

