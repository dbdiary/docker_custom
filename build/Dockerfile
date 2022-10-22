FROM apache/airflow:2.4.1
USER root
RUN  apt-get update \
  && apt-get install -y gcc \
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get clean 
USER airflow
RUN  pip install --no-cache-dir apache-airflow-providers-databricks \
&& pip install --no-cache-dir  mysqlclient \
&& pip install --no-cache-dir mysql-connector
