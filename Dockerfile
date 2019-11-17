FROM baseimage

ENV SERVICE_NAME collection_reddit_raw
ENV BASE_PATH $SVC_PATH/$SERVICE_NAME/
WORKDIR $BASE_PATH


# ============= Dependencies ============= #
# install container wide dependencies
RUN apt-get update --fix-missing
RUN apt-get install --assume-yes default-libmysqlclient-dev gcc git

# install lib_borrowbot_core
RUN git clone https://github.com/borrowbot/lib_borrowbot_core.git $LIB_PATH/lib_borrowbot_core
RUN pip install -r $LIB_PATH/lib_borrowbot_core/requirements.txt
RUN pip install $LIB_PATH/lib_borrowbot_core

# install lib_learning library
RUN git clone https://github.com/frankwang95/lib_learning.git $LIB_PATH/lib_learning
RUN pip install -r $LIB_PATH/lib_learning/requirements_pipelines.txt
RUN pip install $LIB_PATH/lib_learning

# install pypi dependencies
ADD ./requirements.txt $BASE_PATH/requirements.txt
RUN pip install -r requirements.txt


# ============= Source & Entrypoint ============= #
ADD . $BASE_PATH
RUN pip install .

ENTRYPOINT $LIB_PATH/baseimage/entrypoint.sh
