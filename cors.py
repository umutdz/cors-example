import requests, pymysql
import time
from flask import app, request, jsonify, json, Flask
import os


DB_NAME = os.environ.get("DB NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")

def get_connection(host, instance_name = ""):
    connection = None
    retry_count = 0
    while retry_count < 3:
        try:
            unix_socket = "/cloudsql/" + instance_name if instance_name else None
            connection = pymysql.connect(host=host,user=DB_USERNAME,password=DB_PASSWORD,charset='utf8mb4',port=DB_PORT,connect_timeout=10,unix_socket=unix_socket,cursorclass=pymysql.cursors.DictCursor)
            print("success")
            retry_count += 1
        except Exception as e:
            pass
    return connection

def valid(*args):
    for variable in args:
        if not type(variable): return False
        if variable in ["", " ", None, "None", "undefined", "null"]: return False
    return True

def run():
    url = request.referrer if valid(request.referrer) else request.headers.get("Referer")
    host_to_allow = "*"
    if valid(url):
        url_parts = url.split("://")
        host_to_allow = url_parts[0] + '://' + url_parts[1].split("/")[0]

    headers = {
        'Access-Control-Allow-Origin': host_to_allow,
        'Cache-Control': 'private',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Credentials': 'true'}

    try:
        connection = get_connection(DB_NAME)
        cursor = connection.cursor()
        time.sleep(20)
        cursor.close()
        connection.close()        
        return jsonify({"status": "OK", "source": "run"}), 200, headers
    except Exception as e:
        return jsonify({"error": str(e), "source": "run"}), 500, headers
