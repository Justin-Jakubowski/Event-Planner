# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Import core packages
import os
import pymysql

# Import Flask 
from flask import Flask

# Inject Flask magic
app = Flask(__name__)

app.secret_key = "asdfghjkl"

dbConn = pymysql.connect(
    host = "pamplin-bit2020.mysql.database.azure.com",
    port = 3306,
    user = "bit4444group06",
    password = "oX9nhTA82YV8TPOf",
    database = "bit4444group06",
    ssl = {
        'ca':'DigiCertGlobalRootCA.crt.pem'
    },
    cursorclass = pymysql.cursors.DictCursor
)

cursor = dbConn.cursor()

# Import routing to render the pages
from app import views
