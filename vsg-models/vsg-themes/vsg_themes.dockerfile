FROM python:3.10-slim-bookworm

# requirements
RUN apt-get update && apt-get install vim make curl -y

# clean apt cache
RUN apt clean -y

## ------------------------------------------------------
# variables that we are going to need to run our code
ENV BASE_PATH /app
ENV LIB_PATH ${BASE_PATH}/
ENV SVC_PATH ${BASE_PATH}/vsg-models/vsg-themes
ENV CFG_PATH ${BASE_PATH}/config

ENV PROJECT_ROOT ${SVC_PATH}

## -----------------------------------------------------
# create svc and related folders in docker container
RUN mkdir -p ${LIB_PATH}
RUN mkdir -p ${SVC_PATH}
RUN mkdir -p ${CFG_PATH}

## -----------------------------------------------------
# COPY DEPENDENCIES
COPY vsg-utils ${LIB_PATH}/vsg-utils/

# COPY PROJECT
COPY vsg-models/vsg-themes/ ${SVC_PATH}/

# docker optimization in case the developer changes the config file
# putting this instruction here avoid to reinstall the entire platform
# all over again
COPY config/ ${CFG_PATH}/

## ------------------------------------------------------
# Install system
# change to working directory of the service
WORKDIR ${SVC_PATH}

# install system
RUN make install
