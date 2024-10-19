import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramService:
    def __init__(self):
        self.api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

    def send_plate_to_bot(self, plate):
        # Envia a placa para o bot do Telegram
        message = f"Verifique a placa: {plate}"
        response = requests.post(
            f'{self.api_url}/sendMessage',
            data={'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro no envio para o Telegram: {response.status_code}, {response.text}")

    def notify_admin(self, message):
        # Notifica o administrador caso uma placa marcada seja encontrada
        response = requests.post(
            f'{self.api_url}/sendMessage',
            data={'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        )
        if response.status_code != 200:
            raise Exception(f"Erro ao notificar o administrador: {response.status_code}, {response.text}")
