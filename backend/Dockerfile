FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=myfoodapp
ENV POSTGRES_DB=food-app-db

RUN mkdir /docker-entrypoint-initdb.d

COPY data.sql /docker-entrypoint-initdb.d

CMD ["postgres", "-h", "localhost", "-p", "5432"]