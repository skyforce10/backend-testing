# job-testing
 job testing projects
# =========================================================
# ===================language and library==================
development language: Python
framework: flask
library:
       pymysql: for mysql database
       jsonify:convert result to json format
       uuid:generate unique ID
       path,secure_filename: for checking image and upload
# =========================================================
# ===================Testing===============================
# get blogs (all or specific)
http://127.0.0.1:5000/getallblogs
or
http://127.0.0.1:5000/getallblogs?id_blog={ID}
# =========================================================
# get all categories
http://127.0.0.1:5000/getallcategs
# =========================================================
# get all authors
http://127.0.0.1:5000/getallauthor
# =========================================================
# add new blog
# GET method
http://127.0.0.1:5000/addblog?title=title1&content=content1&category=1&author=1
# POST method
http://127.0.0.1:5000/addblog
{title:title1,content:content1,category:1,author:1}
# =========================================================
# update blog
# GET method
http://127.0.0.1:5000/updateblog?title=title1&content=content1&category=1&author=1
# POST method
http://127.0.0.1:5000/updateblog
{title:title1,content:content1,category:1,author:1}
# =========================================================
# add new author
# GET method
http://127.0.0.1:5000/addauthor?f_name=mohamed&l_name=dakdouki
# POST method
http://127.0.0.1:5000/addauthor
{f_name:mohamed,l_name:dakdouki}
# =========================================================
# add new category
# GET method
http://127.0.0.1:5000/addcateg?categ_name=categ1&categ_Desc=categ desc
# POST method
http://127.0.0.1:5000/addcateg
{categ_name:categ1,categ_Desc:categ desc}
# =========================================================
# delete a blog
http://127.0.0.1:5000/delete_data?idblog={ID}
# =========================================================
# =========================================================