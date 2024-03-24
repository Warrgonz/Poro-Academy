# from flask import Flask, render_template
# import db.conexion as database 

# app = Flask(__name__)

# db = database.dbConnection()

# @app.route('/')
# def home(): 
#     eventos = db['Eventos'] 
#     listaEventos = eventos.find()
#     return render_template ('index.html', eventos = listaEventos)