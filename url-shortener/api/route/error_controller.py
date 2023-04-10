from flask import Blueprint, jsonify
from model.error import BadRequest, NotFound, InternalServer

error_controller = Blueprint("error_controller", __name__)


@error_controller.app_errorhandler(NotFound)
@error_controller.app_errorhandler(BadRequest)
@error_controller.app_errorhandler(InternalServer)
def error_handler(e):
    return jsonify(e.payload), e.status_code