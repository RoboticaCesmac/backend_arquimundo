import requests
import codon
import time

url = 'http://127.0.0.1:5000/classify'
image_path = './fotos_teste/grega2.jpg'

start_time = time.time()

with open(image_path, 'rb') as image_file:
    response = requests.post(url, files={'image': image_file})

if response.status_code == 200:
    classification = response.json()
    print(f"Architecture: {classification['architecture']}")
    print(f"Likelihood: {classification['likelihood']:.2%}")
else:
    print(f"Error: {response.text}")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo gasto: {elapsed_time:.4f} segundos")
