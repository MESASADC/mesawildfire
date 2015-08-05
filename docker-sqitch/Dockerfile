
FROM perl:latest

RUN apt-get clean && apt-get update && apt-get -y \
	install \
        vim \
        postgresql-client \
	&& apt-get clean

RUN cpan App::Sqitch
RUN cpan DBD::Pg

VOLUME ["/src"]
WORKDIR /src

ENTRYPOINT ["sqitch"]
