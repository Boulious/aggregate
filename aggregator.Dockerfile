FROM amazonlinux

WORKDIR /app
COPY ./aggregateTransactions.py /app/aggregateTransactions.py
COPY ./requirements.txt .
RUN yum update -y &&\
yum install -y "@Development tools" python3-pip &&\
python3 -m pip install -r requirements.txt

ENV REGION="eu-west-1"
ENV BUCKET="batch-sourcedata"
ENV MONTH="202010"
CMD python3 /app/aggregateTransactions.py ${REGION} ${BUCKET} ${MONTH}