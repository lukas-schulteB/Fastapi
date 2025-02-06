import mysql.connector 


# db = list()
# database = mysql.connector.connect( # LLAMAMOS AL FUNCION CONNECT PARA CONECTARNOS
#     host ='informatica.iesquevedo.es',
#     port = 3333,
#     ssl_disabled = True,
#     user ='root', #USUARIO QUE USAMOS NOSOTROS
#     password ='1asir', #CONTRASEÑA CON LA QUE NOS CONECTAMOS
#     database='oscar'
# ) 

# db = list()
database = mysql.connector.connect( # LLAMAMOS AL FUNCION CONNECT PARA CONECTARNOS
    host ='informatica.iesquevedo.es',
    port = 3333,
    ssl_disabled = True,
    user ='root', #USUARIO QUE USAMOS NOSOTROS
    password ='1asir', #CONTRASEÑA CON LA QUE NOS CONECTAMOS
    database='lukas'
) 