"""
Flask settings for config project.
"""
import mysql.connector
from decouple import config

# SECURITY: secret host used in production!
PORT_FLASK = config('PORT_FLASK')
DEBUG = config('DEBUG')

config = {
    
    'host':config('HOST'),
    'port':config('PORT'),
    'user':config('USER'),
    'password':config('PASSWORD'),
    'database':config('DATABASE'),
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)


