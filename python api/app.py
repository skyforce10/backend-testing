import json

from flask import Flask, flash, render_template, redirect, url_for, request, session
import pymysql
from flask import jsonify
import uuid
import os.path
from os import path
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# create subclass database for connection to mysql
class Database:
    def connect(self):
        # return pymysql.connect("phonebook-mysql", "dev", "dev", "crud_flask")
        return pymysql.connect(host="localhost", user="root", password="1234", database="blogsite", charset='utf8mb4')


# get all blogs
@app.route('/getallblogs')
def get_data_blogs():
    try:
        # connect to database
        conn = Database.connect(None)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # select all blogs from table
        cursor.execute("SELECT * FROM blogs")
        rows = cursor.fetchall()
        # convert result to json
        resp = jsonify(rows)
        resp.status_code = 200
        # return result as json
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# get all categories
@app.route('/getallcategs')
def get_data_categs():
    try:
        conn = Database.connect(None)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM category")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# get all authors
@app.route('/getallauthor')
def get_data_author():
    try:
        conn = Database.connect(None)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM author")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# update blog
@app.route('/updateblog', methods=['POST', 'GET'])
def update_blog():
    try:
        # if method is POST get data from json request
        if request.method == 'POST':
            _json = request.json
            _id_blog = json['idblog']
            _title = _json['title']
            _content = _json['content']
            _tags = _json['tags']
            _category = _json['category']
            _author = _json['author']
        else:
            # if method is GET get data from URL
            _id_blog = request.args.get('idblog')
            _title = request.args.get('title')
            _content = request.args.get('content')
            _tags = request.args.get('tags')
            _category = request.args.get('category')
            _author = request.args.get('author')
        if _id_blog:
            conn = Database.connect(None)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # build sql query
            if _title or _content or _tags or _category or _author:
                sql_update = "update blogs set "
            if _title:
                sql_update = sql_update+"title='"+_title+"',"
            if _content:
                sql_update = sql_update+"content='"+_content+"',"
            if _tags:
                sql_update = sql_update+"tags='"+_tags+"',"
            if _category:
                sql_update = sql_update+"category='"+_category+"',"
            if _author:
                sql_update = sql_update+"author='"+_author+"',"

            if _title or _content or _tags or _category or _author:
                sql_update = sql_update[:-1]
                # update data
                sql_update = sql_update+" where idblogs='"+_id_blog+"'"
                cursor.execute(sql_update)
                conn.commit()
        else:
            return 'No id entered'
        return 'successful update'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# add new blog
@app.route('/addblog', methods=['POST', 'GET'])
def add_new_blog():
    try:
        if request.method == 'POST':
            _json = request.json
            _id_blog = uuid.UUID
            _title = _json['title']
            _content = _json['content']
            _tags = _json['tags']
            _category = _json['category']
            _author = _json['author']
        else:
            _id_blog = uuid.uuid4()
            _title = request.args.get('title')
            _content = request.args.get('content')
            _tags = request.args.get('tags')
            _category = request.args.get('category')
            _author = request.args.get('author')
        # =================================insert data
        # validate the received values
        conn = Database.connect(None)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if _title and _content:
            cursor.execute("SELECT idCategory FROM category where idCategory =%s", _category)
            if cursor.rowcount > 0:
                cat_exists = 1
            else:
                cat_exists = 0
            # check author if exists
            cursor.execute("SELECT idAuthor FROM author where idAuthor =%s", _author)
            if cursor.rowcount > 0:
                author_exists = 1
            else:
                author_exists = 0
            # check category if existed
            if cat_exists and author_exists:
                sql = "INSERT INTO blogs(idblogs, title, content , tags, category, author) " \
                      "VALUES(%s, %s, %s, %s, %s, %s)"
                data = (_id_blog, _title, _content, _tags, _category, _author)
                cursor.execute(sql, data)
                conn.commit()
                if not path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                if 'file' in request.files:

                    file = request.files['file']
                    # empty file without a filename.
                    if file.filename == '':
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(UPLOAD_FOLDER, filename))
                            return 'No selected file'

                resp = jsonify('Blog added successfully!')
                resp.status_code = 200
                return resp
            else:
                return 'Category or author not exists'
            return jsonify('Success')
        else:
            return jsonify('Please fill all mandatory fields')

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# delete data from table blog
@app.route('/delete_data', methods=['GET'])
def delete_data():
    try:
        id_blog = request.args.get('idblog')
        conn = Database.connect(None)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if id_blog is None:
            cursor.execute("delete from blogs")
        else:
            cursor.execute("delete from blogs where idblogs=%s", id_blog)
        conn.commit()
        resp = jsonify('delete successful')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# error message (optional)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# check file validation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
    app.run()
