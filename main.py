from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

app = FastAPI()

 #Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes (cambia esto en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

#inicia el server: uvicorn main:app --reload
#salir del server: Ctrl + C

#url local: http://127.0.0.1:8000

# crear entidad user
class User(BaseModel):
    #id: int
    id: Optional[int] = None
    nombre: str
    codigo: str
    estado: str

#variable 
next_id = 4
#

#Users base de datos imaginaria
users_list = [User(id=1,nombre="Juan",codigo= "1234", estado= "Inicial"),
              User(id=2,nombre="Eddy",codigo= "4567", estado= "En desarrollo"),
              User(id=3,nombre="Ana",codigo= "9101", estado= "Completada")]

@app.get("/clientes")
async def users():
    return users_list

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.head("/")
async def root_head():
    # Personalizar los encabezados
    headers = {"X-Custom-Header": "Valor personalizado"}
    return Response(headers=headers)

    
@app.get("/clientes/buscar/{codigo}")
async def buscar_cliente(codigo: str ):
   if search_user_codigo(codigo):
       print("ok")
       return search_user_codigo(codigo)
   else:
       raise HTTPException(status_code=404, detail="Cliente no encontrado") 

#prueba 
#app.get("/clientes/buscar/{id}")
#async def user(id: int ):
#    print("Ok")
#    users = filter(lambda user: user.id == id ,users_list) #Filter busca el id en users_list
 #   print("ok2")
#    try:                                                      #Tratar para no obtener errores
#        return list(users)[0]                                    # Obtiene el id pedido 
#    except:
#        return {"error":"No se ha encontrado el usuario"}
#    
             

@app.post("/cliente/", response_model= User, status_code=201)  ## Http response status code por defecto 201, response model es para la documentacion
async def user(user: User):
    global next_id
    if type(search_user_codigo(user.codigo)) == User:   #TYPE se utiliza porque se comparan tipos de objetos
        raise HTTPException(status_code=404, detail="El usuario ya existe") ##raise te interrumpe la ejecucion con el error status code 404
        return {"error":"El usuario existe"}
    else:
        user.id = next_id
        users_list.append(user)
        next_id += 1
        return  user 

          
       
               

#busca el cliente que le pongo en el json por nombre y codigo con un id cualquiera y estado random y me busca el correcto
@app.post("/find/", response_model= User, status_code=202)  
async def user(user: User):
    if type(search_user_nombre(user.nombre)) == User:  
        if type(search_user_codigo(user.codigo)) == User:
            
            return search_user_codigo(user.codigo)      
        
        else:
            raise HTTPException(status_code=404, detail="El usuario no existe")
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
@app.put("/actualizar/") 
async def user(user: User):
    
    found = False


    for index,saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

@app.delete("/delete/{codigo}")
async def user(codigo: str):

    found = False

    for index,saved_user in enumerate(users_list):
        if saved_user.codigo == codigo:
            del users_list[index]  # del: comando que elimina
            found = True
            return {"Se elimino el usuario"}
    
    if not found:
        return {"No se encontro el usuario"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Usa el puerto de la variable de entorno o 8000 por defecto
    uvicorn.run(app, host="0.0.0.0", port=port)


def search_user(id: int):
    users = filter(lambda user: user.id == id ,users_list) #Filter busca el id en users_list
    try:                                                      #Tratar para no obtener errores
        return list(users)[0]                                    # Obtiene el id pedido 
    except:
        return {"error":"No se ha encontrado el usuario"}
    
def search_user_nombre(nombre: str):
    users = filter(lambda user: user.nombre == nombre ,users_list) #Filter busca el id en users_list
    try:                                                      #Tratar para no obtener errores
        return list(users)[0]                                    # Obtiene el id pedido 
    except:
        return HTTPException(status_code=404, detail="El usuario no existe")
    
def search_user_codigo(codigo: str):
    users = filter(lambda user: user.codigo == codigo ,users_list) #Filter busca el id en users_list
    try:                                                      #Tratar para no obtener errores
        return list(users)[0]                                    # Obtiene el id pedido 
    except:
        #raise HTTPException(status_code=404, detail="El usuario no existe")
        return
