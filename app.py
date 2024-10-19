from flask import Flask, request, jsonify
from alpr_service import ALPRService
from telegram_service import TelegramService
import os

app = Flask(__name__)
alpr_service = ALPRService()
telegram_service = TelegramService()

@app.route('/process_plate', methods=['POST'])
def process_plate():
    try:
        # Recebe a imagem enviada (ex: imagem da câmera de vigilância)
        image = request.files['image']
        
        # Verifica se o arquivo é uma imagem válida
        if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({"status": "error", "message": "Arquivo inválido. Envie uma imagem."}), 400
        
        image.save('temp_image.jpg')

        # Reconhece a placa usando a API Plate Recognizer
        plate = alpr_service.recognize_plate('temp_image.jpg')
        os.remove('temp_image.jpg')  # Remove a imagem temporária

        if plate:
            # Envia a placa ao bot do Telegram
            response = telegram_service.send_plate_to_bot(plate)

            # Verifica a resposta e notifica o administrador se necessário
            if response and 'notification' in response['result']['text']:
                telegram_service.notify_admin(f"Alerta: Placa {plate} encontrada!")

            return jsonify({"status": "success", "plate": plate}), 200
        else:
            return jsonify({"status": "error", "message": "Placa não encontrada"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
