import os
import json
from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuración de Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

if os.getenv('ENVIRONMENT') == 'PRODUCTION':
    creds_json = os.getenv('GOOGLE_CREDS_JSON')
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

HOJA_ID = "1Sojtik9qh_nmK5EXjgnAGKDcSCbU_OCoc5y09DB5fvc"  # Cambia por tu hoja real

try:
    sheet = client.open_by_key(HOJA_ID).sheet1
    print("✅ Conexión con Google Sheets exitosa!")
except Exception as e:
    print(f"❌ Error de conexión a Google Sheets: {e}")
    raise

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        data = request.form.to_dict()

        required_fields = ['nombre', 'email', 'mensaje', 'edad', 'escolaridad',
                           'colonia', 'distanciaKelloggs', 'experienciaLaboral',
                           'mayorExperiencia']

        if not all(field in data for field in required_fields):
            return "Faltan campos requeridos", 400

        try:
            sheet.append_row([
                data['nombre'],
                data['email'],
                data['mensaje'],
                data['edad'],
                data['escolaridad'],
                data['colonia'],
                data['distanciaKelloggs'],
                data['experienciaLaboral'],
                data.get('ultimoTrabajo', ''),
                data.get('ultimoSueldo', ''),
                data['mayorExperiencia']
            ])
            return render_template('gracias.html', data=data)
        except Exception as e:
            app.logger.error(f"Error al guardar en Sheets: {str(e)}")
            return "Error al procesar la solicitud", 500

    return render_template('chatbot.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_msg = request.json.get('msg')
    # Aquí puedes colocar la lógica real de respuestas
    response = f"Gracias por tu mensaje: {user_msg}"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.getenv('ENVIRONMENT') != 'PRODUCTION')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

