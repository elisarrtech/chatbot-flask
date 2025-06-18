from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configura Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Chatbot Responses").sheet1  # Nombre de tu hoja

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Guarda en Google Sheets (ajusta los nombres de los campos)
        sheet.append_row([data['nombre'], data['email'], data['mensaje']])
        
        return render_template('gracias.html', data=data)
    
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
