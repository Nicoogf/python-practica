from pytube import YouTube 
import pandas as pd 
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

file_path = "listado/lista.xlsx"
sheet_name = "Hoja1"
column_name = "videos"


#Credenciales

directorio_credenciales = "credentials_module.json"
id_folder = ""

#Iniciar Sesion en Drive

def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers={8092})
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales



def subir_archivo(ruta_archivo , id_folder ) :
    credenciales = login()
    archivo = credenciales.CreateFile({"parents":[{"kind" : "drive#fileLink" , \
                                                    "id" : id_folder}]})
    archivo["title"] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

def main():
    df= pd.read_excel(file_path,sheet_name=sheet_name)
    column_data = df[column_name]
    videos= column_data.values
    print(videos)


if __name__ == "__main__" :
    main()