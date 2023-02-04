from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash as gen_key
from werkzeug.security import check_password_hash as check_key
from config import ruta, secret_key
from flask_cors import CORS
from flask_mail import Mail, Message
from random import randint
import datetime

#inicio de la base de datos
db = SQLAlchemy()

#inicio del servidor-aplicaión FLask
app = Flask('CRM')

#Uso de cors para permitir acceso desde las peticiones ajax o fetch
cors = CORS(app)

#Asignamos la dirección a la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{ruta}/database.db'

#Configuración del servicio de correos
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME'] = 'jesusmcalderonv2002@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'jesusmcalderonv2002@gmail.com'
app.config['MAIL_PASSWORD'] = 'eejijulawluqaaqk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Asignamos la clave secreta
app.secret_key = secret_key
#Iniciamos la base de datos cuando se cree nuestra aplicación
db.init_app(app)

#En esta sección vamos a crear nuestras tablas de base de datos usando clases de python, con la ayuda del orm (sqlachemy)
#----------------------------------------------------------------
#Definimos la primera tabla que es lade usuario para almacenar cada usuario
#El nombre que le demos a esta clase sera el nombre de nuestra tabla y los atributos serán columnas

#Tabla usuario (User)

#  id  |   username   |   password
#  1   |   jesus_dev  |   python_l
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), nullable=False, unique=True)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)

#Tabla de preregistro
class Preregister(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), nullable=False, unique=True)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	code = db.Column(db.Integer, nullable=False)

class Compras_temporal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	forma_pago = db.Column(db.String(30), nullable=False)
	fecha = db.Column(db.String(15), nullable=False)
	hora = db.Column(db.String(10), nullable=False)
	descripcion = db.Column(db.String(200))
	proveedor = db.Column(db.String(100), nullable=False)
	id_proveedor = db.Column(db.String, nullable=False)
	concepto = db.Column(db.String(200))
	autoriza = db.Column(db.String(200))
	area = db.Column(db.String(10))
	vehiculo = db.Column(db.String(200))
	kilometraje = db.Column(db.String)
	importe = db.Column(db.String)
	iva = db.Column(db.String)
	total = db.Column(db.String)
	detalle = db.Column(db.String(200))
	editor_user = db.Column(db.String(200))
	estado = db.Column(db.String(30))

class Compras(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	forma_pago = db.Column(db.String(30), nullable=False)
	fecha = db.Column(db.String(15), nullable=False)
	hora = db.Column(db.String(10), nullable=False)
	descripcion = db.Column(db.String(200))
	proveedor = db.Column(db.String(100), nullable=False)
	id_proveedor = db.Column(db.Integer, nullable=False)
	concepto = db.Column(db.String(200))
	autoriza = db.Column(db.String(200))
	area = db.Column(db.String(10))
	vehiculo = db.Column(db.String(200))
	kilometraje = db.Column(db.Float)
	importe = db.Column(db.Float)
	iva = db.Column(db.Float)
	total = db.Column(db.Float)
	detalle = db.Column(db.String(200))
	editor_user = db.Column(db.String(200))
	estado = db.Column(db.String(30))


user = 'Jesús Calderón'


@app.route('/')
def index():
	return render_template('base.html')

@app.route('/compras', methods = ['POST', 'GET'])
def compras():
	conceptos = ['AGUA', 'AGUINALDO', 'APORTACIONES INFONAVIT', 'APORTACIONES SAR', 'ARRENDAMIENTO A PERSONA FISICA RESIDENTE NACIONAL']
	areas = ['TEXTIL', 'CONSTRUCCIÓN', 'INSUMOS']
	vehiculos = ['NINGUNO','AZF-128', 'AZF-827']
	#ventas = ['AGUINALDO', 'Nada', 3884.54, 388.6, 4273.14, 'Aceptado']
	ventas = db.session.query(Compras_temporal).all()
	pagos = ["EFECTIVO", "CHEQUE", "TRANSFERENCIA", "TARJETA DE DEBITO"]
	proveedores = ['NINGUNO','BODEGA', 'SURTIDORA']
	if request.method == 'GET':
		return render_template('compras.html',proveedores = proveedores ,pagos = pagos ,ventas = ventas, vehiculos = vehiculos, conceptos = conceptos, areas = areas)
	elif request.method == 'POST':
		pago = request.form['pago']
		fecha = request.form['fecha']
		hora = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}'
		proveedor = request.form['proveedor']
		descripcion = f'{pago} {proveedor}'
		documento = request.form['documento']
		concepto = request.form['concepto']
		autoriza = user
		area = request.form['area']
		vehiculo = request.form['vehiculo']
		detalle = request.form['detalle']

		if vehiculo != 'NINGUNO':
			kilometraje = request.form['kilometraje']
		else:
			kilometraje = 0.0
		importe = request.form['importe']
		iva = request.form['iva']
		total = request.form['total']
		editor_user = user
		estado = 'Pendiente'

		try:
			new_compra_temp = Compras_temporal(forma_pago = pago, fecha = fecha, hora = hora, descripcion = descripcion, proveedor = proveedor, id_proveedor = 18, concepto = concepto, autoriza = user, area = area, vehiculo = vehiculo, kilometraje = kilometraje, importe = "{:.2f}".format(float(importe)), iva = iva, total = total, detalle = detalle, editor_user = 'Administrador', estado = estado)
			db.session.add(new_compra_temp)
			db.session.commit()
			print('Registrado')
		except:
			print('Error')
		return redirect('/compras')
		


@app.route('/vehiculos/api/<string:placa>')
def vehiculos_api(placa):
	vehiculos = {'AZF-128': 28.5, 'AZF-827': 34.1}

	return jsonify(vehiculos[f'{placa.upper()}'])

@app.route('/proveedor/api/<string:proveedor>')
def proveedores_api(proveedor):
	proveedores = {'BODEGA': 192735293, 'SURTIDORA': 218327823493}

	return jsonify(proveedores[f'{proveedor.upper()}'])


if __name__=='__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)