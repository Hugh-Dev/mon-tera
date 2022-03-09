#!/usr/bin/env python

from random import choices
from flask import Flask, request, render_template, url_for, redirect, jsonify
from settings import PORT_FLASK, DEBUG, cnx
import pandas as pd
import os
import datetime


app = Flask(__name__)

"""CHOICES_TYPES = {
    'Celda': 'celda',
    'Aerogenerador': 'aerogenerador',
    'Turbina hidroelectrica': 'turbina_hidroelectrica'
} 

CHOICES_STATUS = {
    'En operacion':'1',
    'En mantenimiento':'0'
}"""

today = datetime.datetime.today()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        try:
            if cnx.is_connected():

                cursor = cnx.cursor()

                """Choices status"""
                status_qr = ("SELECT * FROM status ")
                cursor.execute(status_qr)
                CHOICES_STATUS = {}
                for (status_id, status_name)  in cursor:
                    CHOICES_STATUS[status_id] = status_name

                """Choices types"""
                types_qr = ("SELECT * FROM types ")
                cursor.execute(types_qr)
                CHOICES_TYPES = {}
                for (type_id, type_name)  in cursor:
                    CHOICES_TYPES[type_id] = type_name



                return render_template('template.index.html', choices_status=CHOICES_STATUS, choices_types=CHOICES_TYPES, update_date=today)

                
        except Exception as ex:
            return render_template('template.400.html', msg=ex)

        if os.path.exists('./csv/dispositivos.csv'):
            
            dispositivos = pd.read_csv('./csv/dispositivos.csv')
            id = dispositivos['id']
            count_id = len(id)
            if id.size > 0:
                count_id += 1
            else:
                count_id += 1
            id = count_id
            return render_template('template.index.html', choices_types=CHOICES_TYPES, id=id, update_date=today, choices_status=CHOICES_STATUS )
        else:
            dispositivos_csv = pd.DataFrame(columns=['id', 'name', 'type', 'create_date', 'update_date', 'current_kw', 'status'])
            os.makedirs('./csv', exist_ok=True)
            dispositivos_csv.to_csv('./csv/dispositivos.csv', index=False)
            dispositivos = pd.read_csv('./csv/dispositivos.csv')
            id = dispositivos['id']
            count_id = len(id)
            if id.size > 0:
                count_id += 1
            else:
                count_id += 1
            id = count_id
            return render_template('template.index.html', choices_types=CHOICES_TYPES, id=id, update_date=today)
        
    
    if request.method == 'POST':
        
        try:
            if cnx.is_connected():

                name = request.form['name']
                type_id = request.form['type_id']
                created_at = request.form['created_at']
                updated_at = request.form['updated_at']
                current_kw = request.form['current_kw']
                status_id = request.form['status_id']

                cursor = cnx.cursor()

                add_device = (
                    "INSERT INTO devices " 
                    "(name, type_id, created_at, updated_at, current_kw, status_id)" 
                    "VALUES (%(name)s, %(type_id)s, %(created_at)s, %(updated_at)s, %(current_kw)s, %(status_id)s)"
                )

                data_device = {
                    'name':name,
                    'type_id': type_id,
                    'created_at':created_at,
                    'updated_at':updated_at,
                    'current_kw':current_kw,
                    'status_id':status_id
                    }

                cursor.execute(add_device, data_device)
                cnx.commit()
          
                return redirect(url_for('index'))

        except Exception as ex:
            print(ex)
            return render_template('template.400.html', msg=ex)


@app.route('/create/type', methods=['GET', 'POST'])
def CreateTypes():
    if request.method == 'GET':
        return render_template('template.types.html')
    
    if request.method == 'POST':

        if cnx.is_connected():
            type_name = request.form['type_name']
            cursor = cnx.cursor()

            add_types = (
                "INSERT INTO types " 
                "(type_name)" 
                "VALUES (%(type_name)s)"
            )

            data_types = {
                'type_name': type_name,
                }

            cursor.execute(add_types, data_types)

            # Make sure data is committed to the database
            cnx.commit()
            #cursor.close()
            #cnx.close()
            return render_template('template.types.html')

        else:
        
            return redirect(url_for('index'))


@app.route('/create/status', methods=['GET', 'POST'])
def CreateStatus():
    if request.method == 'GET':
        return render_template('template.status.html')
    
    if request.method == 'POST':

        if cnx.is_connected():
            status_name = request.form['status_name']
            print(status_name)
            cursor = cnx.cursor()

            add_status = (
                "INSERT INTO status " 
                "(status_name)" 
                "VALUES (%(status_name)s)"
            )

            data_status = {
                'status_name': status_name,
                }

            cursor.execute(add_status, data_status)

            # Make sure data is committed to the database
            cnx.commit()
            #cursor.close()
            #cnx.close()
            return render_template('template.status.html')

        else:
        
            return redirect(url_for('index'))


@app.route('/create/reading', methods=['GET', 'POST'])
def createReading():
    if request.method == 'GET':

        try:
            if cnx.is_connected():

                cursor = cnx.cursor()

                """Choices devices"""
                devices_qr = ("SELECT id, name, type_id FROM devices ")
                cursor.execute(devices_qr)
                CHOICES_DEVICES_ID = {}
                CHOICES_TYPES = {}
                for (id, name, type_id) in cursor:
                    CHOICES_DEVICES_ID[id] = name
                    CHOICES_TYPES['type_id'] = type_id




                return render_template('template.readings.html', choices_devices_id=CHOICES_DEVICES_ID, choices_types=CHOICES_TYPES, updated_at=today )

                
        except Exception as ex:
            print(ex)
            return render_template('template.400.html', msg=ex)
        
    
    if request.method == 'POST':

        if cnx.is_connected():
            status_name = request.form['status_name']
            print(status_name)
            cursor = cnx.cursor()

            add_status = (
                "INSERT INTO status " 
                "(status_name)" 
                "VALUES (%(status_name)s)"
            )

            data_status = {
                'status_name': status_name,
                }

            cursor.execute(add_status, data_status)

            # Make sure data is committed to the database
            cnx.commit()
            #cursor.close()
            #cnx.close()
            return render_template('template.status.html')

        else:
        
            return redirect(url_for('index'))



@app.route('/api/devices', methods=['GET'])
def devices():
    if request.method == 'GET':
        if cnx.is_connected():
            cursor = cnx.cursor()
            qr = ("SELECT * FROM devices")
            cursor.execute(qr)
            devices = []
            
            for (id, type_id, status_id, created_at, updated_at, current_kw, name) in cursor:
                devices.append({
                    'id':id, 
                    'type_id':type_id,
                    'status_id':status_id,
                    'created_at':created_at,
                    'updated_at':updated_at,
                    'current_kw':current_kw,
                    'name': name
                    })

            
            return jsonify(devices)

        else:
            return render_template('template.400.html')

@app.route('/api/device', methods=['GET'])
def deviceId():
    if request.method == 'GET':
        id = request.args.get('id')
        cursor = cnx.cursor()
        qr = ("SELECT * FROM devices " "WHERE id={}".format(id))
        cursor.execute(qr)
        device = []
        for (id, type_id, status_id, created_at, updated_at, current_kw, name) in cursor:
                device.append({
                    'id':id, 
                    'type_id':type_id,
                    'status_id':status_id,
                    'created_at':created_at,
                    'updated_at':updated_at,
                    'current_kw':current_kw,
                    'name': name
                    })

        return jsonify(device)


@app.route('/api/type/device', methods=['GET'])
def devicetypeId():
    if request.method == 'GET':
        type_id = request.args.get('type_id')
        cursor = cnx.cursor()
        qr = ("SELECT * FROM devices " "WHERE type_id={}".format(type_id))
        cursor.execute(qr)
        devices_type = []
        for (id, type_id, status_id, created_at, updated_at, current_kw, name) in cursor:
                devices_type.append({
                    'id':id, 
                    'type_id':type_id,
                    'status_id':status_id,
                    'created_at':created_at,
                    'updated_at':updated_at,
                    'current_kw':current_kw,
                    'name': name
                    })

        return jsonify(devices_type)

if __name__ == "__main__":
    app.run()