import requests
import time
import os
import glob

url = 'https://53aa-2804-389-8023-950-ddbc-9923-12f4-2332.ngrok-free.app/classify'
folder_path = './fotos_teste/'
image_paths = glob.glob(os.path.join(folder_path, '*.jpg'))


def classify_image(image_path):
    if os.path.isfile(image_path):
        with open(image_path, 'rb') as image_file:
            response = requests.post(url, files={'image': image_file})

        if response.status_code == 200:
            if response.content:
                try:
                    classification = response.json()
                    print(f"Imagem: {image_path}")
                    print(f"Arquitetura: {classification['architecture']}")
                    print(f"Probabilidade: {classification['likelihood']:.2%}")
                except ValueError as e:
                    print(f"A resposta não está no formato JSON: {e}")
            else:
                print(f"A resposta está vazia.")
        else:
            print(f"Erro: Código de status {response.status_code}. Resposta: {response.text}")
    else:
        print(f"O arquivo {image_path} não existe.")


start_time = time.time()

for image_path in image_paths:
    classify_image(image_path)
    print("\n")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo gasto: {elapsed_time:.4f} segundos")
