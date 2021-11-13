from flask import Blueprint, request
from controllers.comments_controller import deleteComment, deleteReply, getChapterComments, createComment, editComment, deleteComment, createReply, editReply, deleteReply

comments_bp = Blueprint('comments_bp', __name__)

@comments_bp.route("/chapter/<chapterID>/comments", methods=['GET', 'POST'])
def comments(chapterID):
    if(request.method == 'GET'):
        return getChapterComments(chapterID)
    if(request.method == 'POST'):
        return createComment(chapterID)


@comments_bp.route("/comment/<commentID>", methods=['PUT', 'DELETE'])
def comment(commentID):
    if(request.method == 'PUT'):
        return editComment(commentID)
    if(request.method == 'DELETE'):
        return deleteComment(commentID)


@comments_bp.route("/comment/<commentID>/replies", methods=['POST'])
def replies(commentID):
    if(request.method == 'POST'):
        return createReply(commentID)


@comments_bp.route("/reply/<replyID>", methods=['PUT', 'DELETE'])
def reply(replyID):
    if(request.method == 'PUT'):
        return editReply(replyID)
    if(request.method == 'DELETE'):
        return deleteReply(replyID)