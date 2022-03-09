#!/usr/bin/env python
from flask import Flask, request, render_template, url_for, redirect
from settings import PORT_FLASK, DEBUG, cnx
import pandas as pd
import os
import datetime


app = Flask(__name__)

CHOICES_TYPES = {
    'Celda': 'celda',
    'Aerogenerador': 'aerogenerador',
    'Turbina hidroelectrica': 'turbina_hidroelectrica'
} 

CHOICES_STATUS = {
    'En operacion':'1',
    'En mantenimiento':'0'
}

today = datetime.datetime.today()

print(today)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        try:
            if cnx.is_connected():
                cursor = cnx.cursor()
                cursor = cnx.cursor()
                qr = ("SELECT * FROM status ")
                cursor.execute(qr)
                CHOICES_STATUS = {}
                for (status_id, status_name)  in cursor:
                    CHOICES_STATUS[status_id] = status_name

                return render_template('template.index.html', choices_status=CHOICES_STATUS )

                
        except Exception as ex:
            return render_template('template.index.html', msg=ex)

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
        id = request.form['id']
        name = request.form['name']
        type = request.form['tipodispositivoId']
        create_date = request.form['create_date']

        print(id, name, type, create_date)
        return render_template('template.400.html')


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

if __name__ == "__main__":
    app.run()