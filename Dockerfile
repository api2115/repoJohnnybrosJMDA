FROM mysql/mysql-server

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_ROOT_HOST=%

COPY mysqlsampledatabase.sql /docker-entrypoint-initdb.d/

EXPOSE 3306