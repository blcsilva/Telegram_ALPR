import requests
from config import PLATE_RECOGNIZER_API_TOKEN

class ALPRService:
    def __init__(self):
        self.api_url = 'https://api.platerecognizer.com/v1/plate-reader/'
        self.headers = {'Authorization': f'Token {PLATE_RECOGNIZER_API_TOKEN}'}
        self.regions = ["br"]  # Modifique para sua região, se necessário

    def recognize_plate(self, image_path):
        # Faz a leitura da placa enviando a imagem para a API da Plate Recognizer
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                self.api_url,
                data={'regions': self.regions},  # Envia as regiões opcionalmente
                files={'upload': image_file},  # Arquivo da imagem
                headers=self.headers
            )
            if response.status_code == 200:
                # Extrai a placa da resposta JSON
                result = response.json()
                if result['results']:
                    plate = result['results'][0]['plate']
                    return plate
                else:
                    return None #exercicio
            else:
                raise Exception(f"Erro na API: {response.status_code}, {response.text}")
