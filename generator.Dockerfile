FROM amazonlinux

WORKDIR /app
COPY ./generateTransactions.py .
COPY ./requirements.txt .
RUN yum update -y &&\
yum install -y "@Development tools" python3-pip &&\
python3 -m pip install -r requirements.txt 

ENV REGION="eu-west-1"
ENV BUCKET="batch-sourcedata"
ENV MONTH="202010"
ENV MLNSx2="5"
CMD python3 /app/generateTransactions.py ${REGION} ${BUCKET} ${MONTH} ${MLNSx2}