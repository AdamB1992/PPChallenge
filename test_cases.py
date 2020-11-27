import requests
import json

plates = [{"plate":"M-PP123"}, {"plate":"L-ZZ042"}, {"plate":"G-ZZ98"}, {},{"plate":"YUHJ-YH23"}]

for plate in plates:
    r1 = requests.post('http://127.0.0.1:5000/plate',json = plate)
    print(r1)

r2 = requests.get('http://127.0.0.1:5000/plate')
print(r2)
print(r2.text)
