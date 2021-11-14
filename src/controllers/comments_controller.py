from flask import request
from helpers.jwt_tools import authTokenRequired, decodeToken
from database import db
from models.comment import Comment, Reply
from models.user import User

def getChapterComments(chapterID):
    try:
        comments = Comment.query.filter_by(chapter_id = chapterID).order_by(Comment.id.asc()).all()
        chapterComments = []
        for comment in comments:
            # GATHER COMMENT REPLIES
            commentReplies = []
            for reply in comment.replies:
                user = User.query.get(reply.user_id)
                replyData = {'id': reply.id, 'userID': reply.user_id, 'username': user.username, 'commentID': reply.comment_id, 'content': reply.content, 'edited': reply.edited, 'dateCreated': reply.date_created.strftime("%d/%m/%Y")}
                commentReplies.append(replyData)
            # BUILD COMMENT DATA AND APPENT TO CHAPTER'S COMMENT LIST
            user = User.query.get(comment.user_id)
            commentData = {'id': comment.id, 'userID': comment.user_id, 'username': user.username, 'chapterID': comment.chapter_id, 'content': comment.content, 'edited': comment.edited, 'dateCreated': comment.date_created.strftime("%d/%m/%Y"), 'replies': commentReplies}
            chapterComments.append(commentData)
        return {'status': 200, 'chapterComments': chapterComments}, 200
    except Exception:
        return {'status': 500, 'message': 'Could not get chapter comments'}, 500

@authTokenRequired
def createComment(chapterID):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')

        newComment = Comment(userID, chapterID, request.json['content'])
        db.session.add(newComment)
        db.session.commit()

        return {'status': 200, 'message': 'Comment created'}, 200
    except Exception:
        return {'status': 500, 'message': 'Could not create comment'}, 500

@authTokenRequired
def editComment(commentID):
    try:
        # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET COMMENT AND CHECK IF EXISTS
        comment = Comment.query.get(commentID)
        if (comment is None):
            return {'status': 400, 'message': 'Comment does not exist'}, 400
        # CHECK IF USER CAN EDIT THE COMMENT
        if(user.id == comment.user_id):
            # CHECK IF PROVIDED COMMENT'S CONTENT IS THE SAME AS PREVIOUS
            if(comment.content != request.json['content']):
                comment.content = request.json['content']
                comment.edited = True
                db.session.commit()
                return {'status':200, 'message':'Comment successfully edited'}, 200
            else:
                return {'status':400, 'message':'Data provided is same as current'}, 400
        else:
            return {'status':403, 'message':'You can not edit this comment'}, 403

    except Exception:
        return {'status': 500, 'message': 'Could not create comment'}, 500

@authTokenRequired
def deleteComment(commentID):
    try:
        # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET COMMENT AND CHECK IF EXISTS
        comment = Comment.query.get(commentID)
        if (comment is None):
            return {'status': 400, 'message': 'Comment does not exist'}, 400
        # CHECK IF USER CAN DELETE THE COMMENT
        if(user.id == comment.user_id or user.admin):
            db.session.delete(comment)
            db.session.commit()
            return {'status':200, 'message':'Comment successfully deleted'}, 200
        else:
            return {'status':403, 'message':'You can not delete this comment'}, 403

    except Exception:
        return {'status': 500, 'message': 'Could not delete comment'}, 500

@authTokenRequired
def createReply(commentID):
    try:
        # GET USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        # GET COMMENT AND CHECK IF EXISTS
        comment = Comment.query.get(commentID)
        if (comment is None):
            return {'status': 400, 'message': 'Comment does not exist'}, 400

        newReply = Reply(userID, commentID, request.json['content'])
        db.session.add(newReply)
        db.session.commit()

        return {'status': 200, 'message': 'Replied successfully'}, 200
    except Exception:
        return {'status': 500, 'message': 'Could not create reply'}, 500

@authTokenRequired
def editReply(replyID):
    try:
        # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET REPLY AND CHECK IF EXISTS
        reply = Reply.query.get(replyID)
        if (reply is None):
            return {'status': 400, 'message': 'Reply does not exist'}, 400
        # CHECK IF USER CAN EDIT THE COMMENT
        if(user.id == reply.user_id):
            # CHECK IF PROVIDED COMMENT'S CONTENT IS THE SAME AS PREVIOUS
            if(reply.content != request.json['content']):
                reply.content = request.json['content']
                reply.edited = True
                db.session.commit()
                return {'status':200, 'message':'Reply successfully edited'}, 200
            else:
                return {'status':400, 'message':'Data provided is same as current'}, 400
        else:
            return {'status':403, 'message':'You can not edit this reply'}, 403
    except Exception:
        return {'status': 500, 'message': 'Could not edit reply'}, 500

@authTokenRequired
def deleteReply(replyID):
    try:
        # GET USER FROM USER'S ID PROVIDED IN JWT PAYLOAD
        token = request.headers['Authorization'].split(" ")[1]
        userID = decodeToken(token).get('id')
        user = User.query.get(userID)
        # GET COMMENT AND CHECK IF EXISTS
        reply = Reply.query.get(replyID)
        if (reply is None):
            return {'status': 400, 'message': 'Reply does not exist'}, 400
        # CHECK IF USER CAN DELETE THE COMMENT
        if(user.id == reply.user_id or user.admin):
            db.session.delete(reply)
            db.session.commit()
            return {'status':200, 'message':'Reply successfully deleted'}, 200
        else:
            return {'status':403, 'message':'You can not delete this reply'}, 403

    except Exception:
        return {'status': 500, 'message': 'Could not delete reply'}, 500