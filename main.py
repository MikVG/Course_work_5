import requests
import json


#URL='https://api.hh.ru/vacancies/'

#URL='https://api.hh.ru/dictionaries'
path='1122462'
URL=f'https://api.hh.ru/employers/{path}'

#params = {'text': vacancy, 'areas': 113, 'per_page': 20, 'page': 3}
text = 'Skyeng'
#RUR
#params = {'text': text}

#params = {'employer_id': '1122462'}

#for num in range(5):
#params = {'area': 113, 'per_page': 100, 'page': num}
responce = requests.get(URL)#, params=params)

    #print(responce.status_code)

data = responce.json()#['items']

print(data)

    # for i in range(len(data)):
    #     try:
    #         #if 'Сбер' in data[i]['name']:
    #         print(data[i]['id'], data[i]['name'])
    #     except KeyError:
    #         continue

with open('List.json', 'w', encoding='UTF-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)