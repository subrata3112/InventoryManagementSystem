from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# import qr_functions
# import db_conn
import os
import uuid

# from mysql.connector import connect, Error

import psycopg2

def connect_to_db():

    try:
        connection = psycopg2.connect(

            host = "john.db.elephantsql.com",
            user = "iqxodjwg",
            password = "mi8fWdkQ2Ut6RhgZ_xi5lCWpehj6lnKl",
            database = "iqxodjwg",
            port = "5432"
        )

    except Error as e:
        print(str(e))

    else:
        return connection

def query_exec(query):

    connection = connect_to_db()
    # connection.autocommit(True)
    print(connection)
    cursor = connection.cursor()

    cursor.execute(query)
    # result = cursor.fetchone()
    connection.commit()
    # return result

def query_fetch(query):

    connection = connect_to_db()
    # connection.autocommit(True)
    # print(connection)
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    return result

    # except Error as e:

    #     print(str(e))

    # else:
        

import qrcode
import cv2
# import os

det=cv2.QRCodeDetector()

def generate_qr(mystring):
    img = qrcode.make(mystring)
    current_directory = os.getcwd()
    if os.path.basename(current_directory) != 'static':
        os.chdir('static')

    img.save(mystring +'.png')

def read_qr(mystring):

    img = cv2.imread(mystring)
    data, pts, st_code=det.detectAndDecode(img)
    return str(data)

# Create your views here.

def index(request):
    return render(request, "index.html")


def scanqr(request):

    data = read_qr('qr.png')

    search_query = "SELECT * FROM items_data WHERE id = '{id}'".format(id = data)

    result = query_fetch(search_query)

    if len(result) == 0:
        return render(request, "result.html", {"result_name": "not_found","result_price": "-"})

    else:
        return render(request, "result.html", {"result_name": result[1],"result_price": result[2]})



def add_item(request):

    name = request.POST['name']
    name = str(name)
    # print(name)
    price = request.POST['price']
    price = int(price)
    unique_id = str(uuid.uuid4())

    insert_query = "INSERT INTO items_data VALUES ('{id}','{item}','{item_price}')".format(id=unique_id,item = name,item_price = price)

    query_exec(insert_query)

    generate_qr(unique_id)

    return render(request, "success.html")

# def upload_and_scan(request):

#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         img = cv2.imread(myfile)
#         # fs = FileSystemStorage()
#         # filename = fs.save(myfile.name, myfile)
#         data, pts, st_code=det.detectAndDecode(img)
#         data = str(data)

#     search_query = "SELECT * FROM items_data WHERE id = '{id}'".format(id = data)

#     result = query_fetch(search_query)

#     if len(result) == 0:
#         return render(request, "result.html", {"result_name": "not_found","result_price": "-"})

#     else:
#         return render(request, "result.html", {"result_name": result[1],"result_price": result[2]})

