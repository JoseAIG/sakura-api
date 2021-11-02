from flask import Blueprint, request
from controllers.manga_controller import createManga, getManga


manga_bp = Blueprint('manga_bp', __name__)


@manga_bp.route("/manga", methods=['POST', 'PUT', 'DELETE'])
def manga():
    if(request.method == 'POST'):
        return createManga()
    if(request.method == 'PUT'):
        return {'status':200, 'message':'Operation in process'}, 200
    if(request.method == 'DELETE'):
        return {'status':200, 'message':'Operation in process'}, 200

@manga_bp.route("/manga/<id>", methods=['GET'])
def manga_id(id):
    if(request.method == 'GET'):
        return getManga(id)
