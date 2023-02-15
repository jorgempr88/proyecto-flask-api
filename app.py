from flask import Flask, jsonify, request
from db import Session, engine,connection_db
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cre3t'


#BD
app.config['SQLALCHEMY_DATABASE_URI']= connection_db
app.config['AQLALCHEMY_TRACK_MODIFICATIONS']= False
db= SQLAlchemy(app)
session= Session()
from models import *

@app.route("/hola", methods=['GET'])
def hola():
    return jsonify({"message": "Endpoint desde hola"})

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
    token = None

    if 'x-access-tokens' in request.headers:
        token = request.headers['x-access-tokens']

    if not token:
        return jsonify({'message': 'falta un token válido'})

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
         #current_user = Users.query.filter_by(public_id=data['public_id']).first()
    except:
        return jsonify({'message': 'el token no es válido'})

    return f(data['public_id'],*args, **kwargs)
   return decorator

@app.route('/login', methods=['GET'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'Respuesta':'Por favor verificar'})
   
    with engine.connect() as con:
        user = con.execute(f"select * from usuario where username='{auth.username}'").one()
        print(user)

    if check_password_hash(user[3], auth.password):
        token = jwt.encode({'public_id': user[1], 
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
         app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')}) 
    else:
        return jsonify({'Respuesta': "contraseña incorrecta"})



@app.route("/create_user", methods=["POST"])
@token_required
def create_user(current_user):
    if current_user=='administrador':
        data = json.loads(request.data)
        if "email" not in data:
            return jsonify({"Respuesta": "No se esta enviando el Email!"})
        if "password" not in data:
            return jsonify({"Respuesta": "No se esta enviando el Password!"})
        if len(data['email'])==0:
            return jsonify({"Respuesta": "No puede estar vacio!"})
        if len(data['password'])==0:
            return jsonify({"Respuesta": "No puede estar vacio!"})
        
        with engine.connect() as con:
            has_password = generate_password_hash(data['password'], method='sha256')
            nuevo_usuario = Usuario(username=data['username'], email=data['email'], password=has_password)
            session.add(nuevo_usuario)
            try:
                session.commit()
            except:
                return jsonify({"respuesta":"Usuario ya existe en la case de datos!!!"})        

        return jsonify({"respuesta":"Usuario creado correctamente!"})
    else:
        return jsonify({'Respuesta': 'usuario no tiene permitido el acceso'})

@app.route('/obtener_venta', methods=['GET'])
@token_required
def obtener_venta(current_user):
    data = json.loads(request.data)
    print(data)
    if 'username' not in data:
        return jsonify({"respuesta":"Username no enviado, validar datos"})
    with engine.connect() as con:
        obtener_usuario = f"select * from usuario where username = '{data['username']}'"
        respuesta = con.execute(obtener_usuario).one()
        obtener_venta= f"select venta from ventas where username_id = '{respuesta[0]}'"
        respuesta_ventas = con.execute(obtener_venta)
        respuesta_ventas = [i[0] for i in respuesta_ventas]
        return jsonify({"venta_usuario": {"usuario":data['username'], "ventas":respuesta_ventas}})
        
if __name__=="__main__":
    app.run(debug=True)