FROM baseimage

ENV SERVICE_NAME collection_raw_ingest
ENV BASE_PATH $SVC_PATH/$SERVICE_NAME/
WORKDIR $BASE_PATH
RUN mkdir $BASE_PATH/logs

RUN apt-get update --fix-missing
RUN apt-get install --assume-yes libmariadbclient-dev gcc

ADD ./requirements.txt $BASE_PATH/requirements.txt
RUN pip install -r requirements.txt
ADD . $BASE_PATH

ENTRYPOINT $BASE_PATH/entrypoint.sh
