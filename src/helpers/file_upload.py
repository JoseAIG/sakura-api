from flask import request
import os, time, s3
from werkzeug.utils import secure_filename


def uploadFiles(fieldName: str, s3Directory: str):
    if fieldName not in request.files:
        raise Exception('Invalid file field name provided')
    else:
        filesUploaded = 0
        filesURL = []
        files = request.files.getlist(fieldName)
        for file in files:
            if file.filename != '':
                filename = secure_filename(str(time.time()*1000) + "-" + file.filename)
                file.save(filename)
                fileURL = s3.uploadFile(s3Directory, filename)
                filesURL.append(fileURL)
                os.remove(filename)
                filesUploaded += 1
        return filesURL