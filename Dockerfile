FROM baseimage_borrowbot

ENV SERVICE_NAME collection_reddit_raw
ENV BASE_PATH $SVC_PATH/$SERVICE_NAME/
WORKDIR $BASE_PATH
RUN mkdir $BASE_PATH/logs

# Install Dependencies
RUN apt-get update --fix-missing
RUN apt-get install --assume-yes libmariadbclient-dev gcc git

ADD ./requirements.txt $BASE_PATH/requirements.txt
RUN pip install -r requirements.txt

RUN git clone https://github.com/project-earth/lib_collection.git $LIB_PATH/lib_collection
RUN pip install $LIB_PATH/lib_collection

# Install Service
ADD . $BASE_PATH
RUN pip install .

ENTRYPOINT $BASE_PATH/entrypoint.sh
