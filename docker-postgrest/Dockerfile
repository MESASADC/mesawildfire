FROM centos

RUN yum install -y tar wget postgresql-devel

ENV POSTGREST_VERSION 0.2.10.0

RUN wget http://github.com/begriffs/postgrest/releases/download/v${POSTGREST_VERSION}/postgrest-${POSTGREST_VERSION}-linux.tar.xz
RUN tar --xz -xvf postgrest-${POSTGREST_VERSION}-linux.tar.xz
RUN mv postgrest-${POSTGREST_VERSION} /usr/local/bin/postgrest

EXPOSE 3000

CMD set -x && source /ENV && \ 
    postgrest  --db-host $POSTGREST_DB_HOST       --db-port $POSTGREST_DB_PORT \
               --db-name $POSTGREST_DB_NAME       --db-user $POSTGREST_DB_USER \
               --db-pass $POSTGREST_DB_PASS       --db-pool $POSTGREST_DB_POOL \
               --anonymous $POSTGREST_DB_ANONYMOUS --port 3000      \
               --v1schema $POSTGREST_V1SCHEMA     $POSTGREST_VARGS
