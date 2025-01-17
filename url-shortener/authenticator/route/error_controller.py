from flask import Blueprint, jsonify
from model.error import BadRequest, NotFound, InternalServer, Forbidden, Conflict

error_controller = Blueprint("error_controller", __name__)


@error_controller.app_errorhandler(NotFound)
@error_controller.app_errorhandler(BadRequest)
@error_controller.app_errorhandler(InternalServer)
@error_controller.app_errorhandler(Forbidden)
@error_controller.app_errorhandler(Conflict)
def error_handler(e):
    return jsonify(e.payload), e.status_code