#!/bin/bash

ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

### Load conf/config.ini configuration file ###
source <(grep = config.ini)

function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {
  log "INFO" "Installing ${SERVICE_NAME}"
  
  sudo cp ${SERVICE_PATH}/${SERVICE_NAME} /usr/local/bin/${SERVICE_NAME}

}

main "$@"
