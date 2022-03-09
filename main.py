#!/usr/bin/env python
from email import message
from flask import Flask, message_flashed, request, render_template, url_for, redirect, jsonify
from settings import PORT_FLASK, DEBUG, cnx
import pandas as pd
import os
import datetime


app = Flask(__name__)

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


                cursor.close()
                """cursor.close()
                cnx.close()"""
                return render_template('template.index.html', choices_status=CHOICES_STATUS, choices_types=CHOICES_TYPES, update_date=today)
        
       
        except Exception as ex:
            return render_template('template.400.html', message=ex)

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
                """cursor.close()
                cnx.close()"""
                return redirect(url_for('index'))

        except Exception as ex:
            return render_template('template.400.html', message=ex)


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
            cnx.commit()
            """cursor.close()
            cnx.close()"""
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
            cnx.commit()
            """cursor.close()
            cnx.close()"""
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
                devices_qr = ("SELECT id, name FROM devices ")
                cursor.execute(devices_qr)
                CHOICES_DEVICES_ID = {}
                for (id, name) in cursor:
                    CHOICES_DEVICES_ID[id] = name

                """cursor.close()
                cnx.close()"""
                return render_template('template.readings.html', choices_devices_id=CHOICES_DEVICES_ID, updated_at=today )

                
        except Exception as ex:
            return render_template('template.400.html', message=ex)
        
    
    if request.method == 'POST':

        if cnx.is_connected():

            device_id = request.form['device_id']
            current_power = request.form['current_power']
            updated_at = request.form['updated_at']
            

            cursor = cnx.cursor()
            qr = ("SELECT id, type_id, current_kw, name, status_id FROM devices " "WHERE id={}".format(device_id))
            cursor.execute(qr)
  
            result = []
            for (id, type_id, current_kw, name, status_id) in cursor:
                result.append(id)
                result.append(type_id)
                result.append(current_kw)
                result.append(name)
                result.append(status_id)

            cursor.close()

            if result[4] == 4:

                add_reading = (
                    "INSERT INTO readings " 
                    "(device_id, type_id, current_power, updated_at)" 
                    "VALUES (%(device_id)s, %(type_id)s, %(current_power)s, %(updated_at)s)"
                )

                data_reading = {
                    'device_id': result[0],
                    'type_id': result[1],
                    'current_power': current_power,
                    'updated_at': updated_at
                    }

                cursor = cnx.cursor()
                cursor.execute(add_reading, data_reading)
                cnx.commit()
                """cursor.close()
                cnx.close()"""
                return redirect(url_for('createReading'))

            else:
                message_flashed = 'El dispositivo se encuentra en matenimiento'
                return render_template('template.400.html', message_flashe=message_flashed)

        else:
            return render_template('template.400.html', message='400')


@app.route('/api/binnacle', methods=['GET'])
def binnacle():
    if request.method == 'GET':
        if cnx.is_connected():
            cursor = cnx.cursor()
            qr = ("SELECT * FROM readings")
            cursor.execute(qr)
            readings = []
            
            for (id, device_id, type_id, current_power, updated_at) in cursor:
                readings.append({
                    'id':id,
                    'device_id':device_id, 
                    'type_id':type_id,
                    'current_power':current_power,
                    'updated_at':updated_at,
                    })

            """cursor.close()
            cnx.close()"""
            return jsonify(readings)

        else:
            return render_template('template.400.html', message='400')

@app.route('/api/device/binnacles', methods=['GET'])
def binnaclesdeviceId():
    if request.method == 'GET':
        if cnx.is_connected():
            device_id = request.args.get('device_id')
            cursor = cnx.cursor()
            qr = ("SELECT * FROM readings " "WHERE device_id={}".format(device_id))
            cursor.execute(qr)
            readings = []
            
            for (id, device_id, type_id, current_power, updated_at) in cursor:
                readings.append({
                    'id':id,
                    'device_id':device_id, 
                    'type_id':type_id,
                    'current_power':current_power,
                    'updated_at':updated_at,
                    })

            """cursor.close()
            cnx.close()"""
            return jsonify(readings)

        else:
            return render_template('template.400.html', message='400')

@app.route('/api/devices/type/binnacles', methods=['GET'])
def binnaclestypesId():
    if request.method == 'GET':
        if cnx.is_connected():
            type_id = request.args.get('type_id')
            cursor = cnx.cursor()
            qr = ("SELECT * FROM readings " "WHERE type_id={}".format(type_id))
            cursor.execute(qr)
            readings = []
            
            for (id, device_id, type_id, current_power, updated_at) in cursor:
                readings.append({
                    'id':id,
                    'device_id':device_id, 
                    'type_id':type_id,
                    'current_power':current_power,
                    'updated_at':updated_at,
                    })
            """cursor.close()
            cnx.close()"""
            return jsonify(readings)

        else:
            return render_template('template.400.html', message='400')

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

            """cursor.close()
            cnx.close()"""
            return jsonify(devices)

        else:
            return render_template('template.400.html', message='400')

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
        """cursor.close()
        cnx.close()"""
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
        """cursor.close()
        cnx.close()"""
        return jsonify(devices_type)

if __name__ == "__main__":
    app.run()