from tkinter import ttk
from tkinter import *
from tkinter import messagebox as MessageBox


import sqlite3
class Product:
	db_name = 'database.db'

	def __init__(self,window):
		self.wind = window
		self.wind.title('Aplicacion de productos')

		#Creando el contenedor#
		frame = LabelFrame(self.wind, text = 'Registra un nuevo producto')
		frame.grid(row = 0, column = 0, columnspan = 3, pady =20)

		#Input para Nombre:#
		Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
		self.name = Entry(frame)
		self.name.focus()
		self.name.grid(row = 1, column = 1)

		#Input para Precio#
		Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
		self.price = Entry(frame)
		self.price.grid(row = 2, column = 1)

		#Boton para agregar Productos#
		ttk.Button(frame, text = 'Guardar Producto', command = self.agregar_productos).grid(row = 3, columnspan = 2, sticky = W + E)
		ttk.Button(frame, text = 'Licencia', command = self.prueba).grid(row = 4, columnspan = 2, sticky = W + E)
		ttk.Button(frame, text = 'Salir', command = quit).grid(row = 5, columnspan = 2, sticky = W + E)
		


		#Mensaje de salida#
		self.message = Label(text = '', fg = 'red')
		self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

		#Tabla#
		self.tree = ttk.Treeview(height = 10, columns = 2)
		self.tree.grid(row = 4, column = 0, columnspan = 2)
		self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
		self.tree.heading('#1', text = 'Precio', anchor = CENTER)

		#Llenado de filas
		self.obtener_productos()

		#Botones de Eliminar y Editar
		ttk.Button(text = 'Eliminar', command = self.eliminar_producto).grid(row = 5, column = 0, sticky = W + E)
		ttk.Button(text = 'Editar', command = self.editar_producto).grid(row = 5, column = 1, sticky = W + E)

		



	def correr_query(self, query, parameters = ()):
		with sqlite3.connect(self.db_name) as conn:
			cursor = conn.cursor()
			result = cursor.execute(query, parameters)
			conn.commit()
		return result

	def obtener_productos(self):
		#Limpiando tablas
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)
		
		#Quering Datos
		query = 'SELECT * FROM producto ORDER BY nombre DESC'
		db_rows = self.correr_query(query)
		for row in db_rows:
			self.tree.insert('',0,text = row[1], values = row[2])
		
	def validando(self):
		return len(self.name.get()) !=0 and len(self.price.get()) !=0



	def agregar_productos(self):
		if self.validando():
			# print(self.name.get())
			# print(self.price.get())
			query = 'INSERT INTO producto VALUES(NULL, ?,?)'
			parameters = (self.name.get(), self.price.get())
			self.correr_query(query, parameters)
			self.obtener_productos()
			# print('Datos Guardados')
			self.message['text'] = 'Producto {} agregado correctamente'.format(self.name.get())
			self.name.delete(0, END)
			self.price.delete(0, END)
		else:
			self.message['text'] = 'El nombre y precio es requerido'
			self.obtener_productos()

	def eliminar_producto(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]

		except IndexError as e:
			self.message['text'] = 'Selecciona un dato'
			return
		self.message['text'] = ''
		name = self.tree.item(self.tree.selection())['text']
		query = 'DELETE FROM producto WHERE nombre = ?'
		self.correr_query(query, (name, ))
		self.message['text'] = 'El dato {} se ha borrado satisfactoriamente'.format(name)
		self.obtener_productos()

	def editar_producto(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.message['text'] = 'Selecciona un dato'
			return
		name = self.tree.item(self.tree.selection())['text']
		old_price = self.tree.item(self.tree.selection())['values'][0]
		self.edit_wind = Toplevel()
		self.edit_wind.title = 'Editar producto'

		#Nombre viejo
		Label(self.edit_wind, text = 'Nombre antiguo: ').grid(row = 0, column = 1)
		Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)

		#Nuevo nombre
		Label(self.edit_wind,text = 'Nuevo nombre: ').grid(row = 1, column = 1)
		new_name = Entry(self.edit_wind)
		new_name.grid(row = 1, column = 2)

		#Precio antiguo
		Label(self.edit_wind, text = 'Precio antiguo: ').grid(row = 2, column = 1)
		Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)

		#Nuevo precio
		Label(self.edit_wind,text = 'Precio nuevo: ').grid(row = 3, column = 1)
		new_price = Entry(self.edit_wind)
		new_price.grid(row = 3, column = 2)

		Button(self.edit_wind, text = 'Actualizar', command = lambda:self.editar_datos(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)

	def editar_datos(self, new_name, name, new_price, old_price):
		query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
		parameters = (new_name, new_price, name, old_price)
		self.correr_query(query, parameters)
		self.edit_wind.destroy()
		self.message['text'] = 'Dato {} actualizado correctamente'.format(name)
		self.obtener_productos()

	def prueba(self):
		MessageBox.showinfo("Licencia", "Desarrollado Por Fredy May Rodriguez") # título, mensaje

	def quit():
		window.destroy()

		
if __name__=="__main__":
	window = Tk()
	window.iconbitmap("database.ico")
	application = Product(window)
	window.mainloop()

