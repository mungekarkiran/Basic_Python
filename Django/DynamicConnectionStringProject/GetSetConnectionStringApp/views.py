from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# from .models import * 

# import the sql and connect libraries for psycopg2
from psycopg2 import sql, connect


# Create your views here.

def index(request):
    return render(request, 'index.htm')

def CreatePage(request):
    return render(request, 'CreatePage.htm')

def UpdatePage(request):
    return render(request, 'UpdatePage.htm')

def DeletePage(request):
    return render(request, 'DeletePage.htm')


def setConnectionString(request):
    if request.method == 'POST':
        try:
            # declare a new PostgreSQL connection object
            conn = connect(
                user = request.POST['USER'], # 'postgres'
                password = request.POST['PASSWORD'], # 'kiran'
                host = request.POST['HOST'], # 'localhost'
                dbname = request.POST['NAME'], # 'DjangoDB'
            )
            # print the connection if successful
            print ("psycopg2 connection:", conn)

            #Create a cursor connection object to a PostgreSQL instance and print the connection properties.
            cursor = conn.cursor()
            # print('cursor : ',cursor)
            # print('connection.get_dsn_parameters() : ',conn.get_dsn_parameters(),"\n")

            #Display the PostgreSQL version installed
            # cursor.execute("SELECT version();")
            # record = cursor.fetchone()
            # print("You are connected into the - ", record,"\n")
            # You are connected into the -  ('PostgreSQL 11.3, compiled by Visual C++ build 1914, 64-bit',)
            # return render(request, 'crudPage.htm',{'cursor':cursor})
        except Exception as err:
            print ("psycopg2 connect() ERROR:", err)
            conn = None
        
        tName = request.POST['TNAME']
        cName = request.POST['CNAME']
        cValue = request.POST['CVALUE']
        pg_insert = "INSERT INTO "+tName+" ("+cName+") VALUES ("+cValue+")"
        cursor.execute(pg_insert)
        #Commit transaction and prints the result successfully
        conn.commit()
        count = cursor.rowcount
        print (count, "Successfully inserted")

    return render(request, 'index.htm')

# def 