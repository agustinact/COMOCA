import sqlite3
from sqlite3 import Error

class QueriesSQLite:
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error 1 '{e}' occurred")

        return connection

    def execute_query(connection, query, data_tuple):
        cursor = connection.cursor()
        try:
            cursor.execute(query, data_tuple)
            connection.commit()
            print("Query executed successfully")
            return cursor.lastrowid
        except Error as e:
            print(f"The error now is '{e}' occurred")

    def execute_read_query(connection, query, data_tuple=()):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query, data_tuple)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error 2 '{e}' occurred")
        
        # esto es nuevo
    def create_tables():
        connection = QueriesSQLite.create_connection("nuevaDB.sqlite")

        tabla_productos = """
        CREATE TABLE IF NOT EXISTS productos(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         detalle TEXT NOT NULL
        );
        """
        tabla_proveedores = """
        CREATE TABLE IF NOT EXISTS proveedores(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         nombre TEXT NOT NULL,
         domicilio TEXT NOT NULL,
         cuit INT NOT NULL,
         mail TEXT,
         telefono TEXT,
         cp INT,
         provincia TEXT
        );
        """
        
        tabla_clientes = """
        CREATE TABLE IF NOT EXISTS clientes(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         nombre TEXT NOT NULL,
         facturacion TEXT NOT NULL,
         domicilio TEXT NOT NULL,
         cuit INT NOT NULL,
         mail TEXT,
         telefono INT,
         cp INT,
         provincia TEXT
        );
        """

        tabla_stock = """
        CREATE TABLE IF NOT EXISTS stock(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         cod_caja TEXT NOT NULL,
         id_producto INTEGER NOT NULL,
         id_proveedor INTEGER NOT NULL,
         peso INTEGER NOT NULL,
         tropa TEXT NOT NULL,
         fecha_ingreso DATE NOT NULL,
         fecha_vencimiento DATE NOT NULL,
         id_pallet TEXT NOT NULL,
         n_factura TEXT NOT NULL,
         FOREIGN KEY(id_proveedor) REFERENCES proveedores(id),
         FOREIGN KEY(id_producto) REFERENCES productos(id)
        );    
        """

        tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios(
         username TEXT PRIMARY KEY, 
         nombre TEXT NOT NULL, 
         password TEXT NOT NULL,
         tipo TEXT NOT NULL
        );
        """

        tabla_remitos = """
        CREATE TABLE IF NOT EXISTS remitos(
         id INTEGER PRIMARY KEY AUTOINCREMENT, 
         id_remito INT NOT NULL,
         cliente TEXT NOT NULL,
         total REAL NOT NULL, 
         fecha DATE NOT NULL,
         factura TEXT
        );
        """
        
        tabla_romaneos = """
        CREATE TABLE IF NOT EXISTS romaneos(
         id INTEGER PRIMARY KEY AUTOINCREMENT, 
         cliente TEXT NOT NULL,
         proveedor TEXT NOT NULL,
         fecha DATE NOT NULL, 
         producto TEXT NOT NULL,
         peso REAL NOT NULL,
         precio REAL NOT NULL,
         total REAL NOT NULL,
         estado TEXT NOT NULL,
        );
        """
        tabla_facturas = """
        CREATE TABLE IF NOT EXISTS facturas(
         id INTEGER PRIMARY KEY AUTOINCREMENT, 
         n_factura TEXT NOT NULL,
         estado TEXT NOT NULL
        );
        """
        
        tabla_pallets = """
        CREATE TABLE IF NOT EXISTS pallets(
         id INTEGER PRIMARY KEY AUTOINCREMENT, 
         id_pallet TEXT NOT NULL,
         proveedor TEXT NOT NULL,
         peso_total REAL NOT NULL,
         fecha DATE NOT NULL, 
         producto TEXT NOT NULL,
         estado TEXT NOT NULL
        );
        """


        tabla_salidas = """
        CREATE TABLE IF NOT EXISTS salidas(
         id INTEGER PRIMARY KEY, 
         id_remito TEXT NOT NULL,
         cod_caja TEXT NOT NULL, 
         producto TEXT NOT NULL,
         cliente TEXT NOT NULL,
         peso INTEGER NOT NULL,
         tropa TEXT NOT NULL,
         fecha_egreso DATE NOT NULL,
         id_proveedor INTEGER NOT NULL,
         id_pallet TEXT NOT NULL,
         f_proveedor TEXT NOT NULL,
         FOREIGN KEY(id_remito) REFERENCES remitos(id_remito),
         FOREIGN KEY(cod_caja) REFERENCES stock(cod_caja),
         FOREIGN KEY(cliente) REFERENCES stock(nombre)
        );
        """
        
        tabla_producto_proveedor = """
        CREATE TABLE IF NOT EXISTS producto_proveedor (
        ID_Producto INT,
        ID_Proveedor INT,
        PRIMARY KEY (ID_Producto, ID_Proveedor),
        FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        FOREIGN KEY (ID_Proveedor) REFERENCES Proveedores(ID_Proveedor)
        );
        """


        QueriesSQLite.execute_query(connection, tabla_productos, tuple())
        QueriesSQLite.execute_query(connection, tabla_proveedores, tuple())
        QueriesSQLite.execute_query(connection, tabla_stock, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_usuarios, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_salidas, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_remitos, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_producto_proveedor, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_clientes, tuple()) 
        QueriesSQLite.execute_query(connection, tabla_pallets, tuple())
        QueriesSQLite.execute_query(connection, tabla_facturas, tuple())
        
if __name__=="__main__":
    create_tables = QueriesSQLite.create_tables()
    connection = QueriesSQLite.create_connection("nuevaDB.sqlite")


    # agregar_ventas = """
    # INSERT INTO 
    #     productos (detalle)
    # VALUES
    #     (Asado,Vacio,Matambre,Bondiola,Roastbeef,Pechuga)
    # """

    # # agregar_columna = """ALTER TABLE ventas ADD COLUMN forma_pago TEXT NOT NULL"""
    # # QueriesSQLite.execute_query(connection, agregar_columna, tuple())
    

    # QueriesSQLite.execute_query(connection, agregar_ventas, tuple())
    
    # agregar_stock = """
    # INSERT INTO 
    #     stock (id_producto, id_proveedor, peso, cod_caja)
    # VALUES
    #     (1, 1, 20, 11122),
    #     (1, 1, 18, 11123),
    #     (1, 2, 21, 11124),
    #     (2, 2, 20, 11126),
    #     (3, 2, 18, 11155),
    #     (3, 5, 21, 11177),
    #     (4, 1, 20, 11188),
    #     (4, 1, 18, 13333),
    #     (5, 2, 21, 12222),
    #     (6, 2, 20, 11111),
    #     (6, 2, 18, 11999),
    #     (6, 5, 21, 11456)
        
    # """

    # QueriesSQLite.execute_query(connection, agregar_stock, tuple())
    
    # agregar_producto_proveedor = """
    # INSERT INTO 
    #     producto_proveedor (ID_Producto, ID_Proveedor)
    # VALUES
    #     (1, 1),
    #     (1, 2),
    #     (2, 2),
    #     (3, 2),
    #     (3, 3),
    #     (4, 4),
    #     (4, 1),
    #     (5, 3),
    #     (6, 3)
        
    # """

    # QueriesSQLite.execute_query(connection, agregar_producto_proveedor, tuple())
    

    
    # select_ventas = "SELECT * from ventas"
    # ventas = QueriesSQLite.execute_read_query(connection, select_ventas)
    # for venta in ventas:
    #      print(venta)

    # agregar_ventas_d = """
    # INSERT INTO 
    #     ventas_detalle
    # VALUES
    #     (3, '2', 1000.5, '222', 1),
    #     (4, '3', 890.5, '333', 3),
    #     (5, '4', 10000.0, '444', 10),
    #     (6, '5', 254.75, '555', 2),
    #     (7, '6', 467.0, '666', 1)
    # """
    # QueriesSQLite.execute_query(connection, agregar_ventas_d, tuple())

    # select_ventas_d = "SELECT * from ventas_detalle"
    # ventas_d = QueriesSQLite.execute_read_query(connection, select_ventas_d)
    # for venta_d in ventas_d:
    #      print(venta_d)


    # create_product_table = """
    # CREATE TABLE IF NOT EXISTS productos(
    #  codigo TEXT PRIMARY KEY, 
    #  nombre TEXT NOT NULL, 
    #  precio REAL NOT NULL, 
    #  cantidad INTEGER NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, create_product_table, tuple()) 


    # create_user_table = """
    # CREATE TABLE IF NOT EXISTS usuarios(
    #  username TEXT PRIMARY KEY, 
    #  nombre TEXT NOT NULL, 
    #  password TEXT NOT NULL,
    #  tipo TEXT NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, create_user_table, tuple()) 


    # crear_producto = """
    # INSERT INTO
    #   productos (codigo, nombre, precio, cantidad)
    # VALUES
    #     ('111', 'leche 1l', 20.0, 20),
    #     ('222', 'cereal 500g', 50.5, 15), 
    #     ('333', 'yogurt 1L', 25.0, 10),
    #     ('444', 'helado 2L', 80.0, 20),
    #     ('555', 'alimento para perro 20kg', 750.0, 5),
    #     ('666', 'shampoo', 100.0, 25),
    #     ('777', 'papel higiénico 4 rollos', 35.5, 30),
    #     ('888', 'jabón para trastes', 65.0, 5)
    # """
    # QueriesSQLite.execute_query(connection, crear_producto, tuple()) 

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)


    usuario_tuple=('marianoc', 'Administardor', '110784', 'admin')
    crear_usuario = """
    INSERT INTO
      usuarios (username, nombre, password, tipo)
    VALUES
        (?,?,?,?);
    """
    QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple) 


    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)

    # neuva_data=('Persona 55', '123', 'admin', 'persona1')
    # actualizar = """
    # UPDATE
    #   usuarios
    # SET
    #   nombre=?, password=?, tipo = ?
    # WHERE
    #   username = ?
    # """
    # QueriesSQLite.execute_query(connection, actualizar, neuva_data)

    # neuva_data=('CL01', 'CONJUNTO X1', 2000.0, 1)
    # actualizar = """
    # INSERT INTO
    #   promos (codigo, detalle, precio, unidades)
    # VALUES
    #     (?,?,?,?);
    # """
    # QueriesSQLite.execute_query(connection, actualizar, neuva_data)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)



    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)

    # producto_a_borrar=('prm01',)
    # borrar = """DELETE from promos where id_promo = ?"""
    # QueriesSQLite.execute_query(connection, borrar, producto_a_borrar)

    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)
    
    
    
    # create_customer = ('CLIENTE_1','FRIGORIFICO SRL', 'DOMICILIO 123', 30000000001, 'agustin.automacion@gmail.com', 12345678, 2000, 'BUENOS AIRES')
    # query_cliente   = "INSERT INTO clientes(nombre, facturacion, domicilio, cuit, mail, telefono, cp, provincia) VALUES (?,?,?,?,?,?,?,?)"
    # QueriesSQLite.execute_query(connection, query_cliente, create_customer)
    
    # create_supplier = ('PROVEEDOR_1', 'DOMICILIO 123', 30000000001, 'mail@ejemplo.com', 12345678, 2000, 'BUENOS AIRES')
    # query_supplier   = "INSERT INTO proveedores(nombre, domicilio, cuit, mail, telefono, cp, provincia) VALUES (?,?,?,?,?,?,?)"
    # QueriesSQLite.execute_query(connection, query_supplier, create_supplier)
    
    # create_producto = """
    # INSERT INTO 
    #     productos (detalle)
    # VALUES
    #     ('MATAMBRE'),
    #     ('VACIO'),
    #     ('BONDIOLA'),
    #     ('PECHITO'),
    #     ('ASADO'),
    #     ('ROAST BEEF'),
    #     ('CUADRIL')

    # """

    # QueriesSQLite.execute_query(connection, create_producto, tuple())


    # create_entradas = """
    # INSERT INTO 
    #     stock (cod_caja, id_producto, id_proveedor, peso, tropa, fecha_ingreso, fecha_vencimiento, id_pallet, n_factura)
    # VALUES
    #     (11111111, 1, 1, 12, 123, '2024-01-06', '2024-08-06', 'CP01', '0001-20000000'),
    #     (22222222, 1, 1, 15, 123, '2024-01-06', '2024-08-06', 'CP01', '0001-20000000'),
    #     (33333333, 1, 1, 17, 123, '2024-02-06', '2024-08-06', 'CP02', '0001-20000000'),
    #     (44444444, 1, 1, 12, 124, '2024-02-06', '2024-08-06', 'CP03', '0001-20000003'),
    #     (55555555, 2, 1, 22, 125, '2024-03-06', '2024-08-06', 'CP04', '0001-20000004'),
    #     (66666666, 2, 1, 21, 125, '2024-04-06', '2024-08-06', 'CP04', '0001-20000005'),
    #     (77777777, 3, 1, 12, 126, '2024-04-06', '2024-08-06', 'CP04', '0001-20000006'),
    #     (88888888, 4, 1, 33, 127, '2024-04-06', '2024-08-06', 'CP55', '0001-20000007'),
    #     (99999999, 5, 1, 21, 127, '2024-05-06', '2024-08-06', 'CP101', '0001-20000008'),
    #     (10101010, 6, 1, 11, 128, '2024-06-06', '2024-08-06', 'CP103', '0001-20000010')

    # """

    # QueriesSQLite.execute_query(connection, create_entradas, tuple())