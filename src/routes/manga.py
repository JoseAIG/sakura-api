from flask import Blueprint, request
from controllers.manga_controller import getUserMangas, createManga, updateManga, deleteManga, getManga


manga_bp = Blueprint('manga_bp', __name__)


@manga_bp.route("/manga", methods=['GET', 'POST', 'PUT'])
def manga():
    if(request.method == 'GET'):
        return getUserMangas()
    if(request.method == 'POST'):
        return createManga()
    if(request.method == 'PUT'):
        return updateManga()

@manga_bp.route("/manga/<id>", methods=['GET', 'DELETE'])
def manga_id(id):
    if(request.method == 'GET'):
        return getManga(id)
    if(request.method == 'DELETE'):
        return deleteManga(id)
