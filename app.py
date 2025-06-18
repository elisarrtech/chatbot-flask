import os
import json
from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuración segura para Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Modo desarrollo vs producción
if os.getenv('ENVIRONMENT') == 'PRODUCTION':
    # Para Render (usando variable de entorno)
    creds_json = os.getenv('GOOGLE_CREDS_JSON')
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    # Para desarrollo local
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

# Usa ID de hoja en lugar del nombre (más seguro)
HOJA_ID = "1Sojtik9qh_nmK5EXjgnAGKDcSCbU_OCoc5y09DB5fvc"  # Reemplaza con el ID de tu hoja
sheet = client.open_by_key(HOJA_ID).sheet1

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        try:
            # Validación básica de campos
            required_fields = ['nombre', 'email', 'mensaje']
            if not all(field in data for field in required_fields):
                return "Faltan campos requeridos", 400
                
            # Guarda en Google Sheets con manejo de errores
            sheet.append_row([
                data['nombre'],
                data['email'],
                data['mensaje']
            ])
            return render_template('gracias.html', data=data)
            
        except Exception as e:
            app.logger.error(f"Error al guardar en Sheets: {str(e)}")
            return "Ocurrió un error al procesar tu mensaje", 500
    
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=os.getenv('ENVIRONMENT') != 'PRODUCTION')
