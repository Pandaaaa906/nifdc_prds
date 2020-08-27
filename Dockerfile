FROM tiangolo/uwsgi-nginx:python3.6 AS nifdc_base
ENV TZ=Asia/Shanghai
RUN mkdir -p ~/.pip
RUN echo "[global]\nindex-url = https://pypi.mirrors.ustc.edu.cn/simple/" | tee ~/.pip/pip.conf
RUN git config --global http.sslverify false
COPY requirements /tmp
RUN pip install -r /tmp/requirements
RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y

FROM nifdc_base

COPY ./cron_nifdc /etc/cron.d/cronpy
COPY ./nifdc_prds /app
COPY ./entrypoint.sh /
RUN chmod -R 744 /entrypoint.sh
WORKDIR /app

ENTRYPOINT /entrypoint.sh