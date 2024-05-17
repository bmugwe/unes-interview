import requests
import pandas as pd
import base64
import os
import json

username = os.getenv('HIS_USERNAME') if os.getenv('HIS_USERNAME') != None else 'programmingtest'
password = os.getenv('HIS_password')  if os.getenv('HIS_password') != None else 'Kenya@2040'

encode_pass = (f"{username}:{password}".encode('utf-8'))
pass_to_base64 = base64.b64encode(encode_pass).decode('utf-8')

print(f"username: {username} password: {password} Base64 password: {pass_to_base64}")

url = "https://test.hiskenya.org/api/analytics.json?dimension=dx%3AotgQMOXuyIn%3Bm4RpD2hvoT4%3ByQFyyQBhXQf&dimension=pe%3A202301%3B202302%3B202303%3B202304%3B202305%3B202306%3B202307%3B202308%3B202309%3B202310%3B202311%3B202312&tableLayout=true&columns=dx&rows=pe&skipRounding=false&completedOnly=false&filter=ou%3AUSER_ORGUNIT"

# url_2 = input(f"input the url: ")

def fetchData(url):
    print(f'fethicng data from url:  {url}')
    payload = {}
    headers = {
    'Authorization': F'Basic {pass_to_base64}',
    'Cookie': 'JSESSIONID=A40DF5CC3CDF4A1A77F9A0A4B4C1A050'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(f" data fetched")
        return response
    except Exception as e:
        print(f"Error")
        return []
        

def TransformSave(response):
    if len(response)> 0:
        try:
            data = response.json()
            data_rows = data['rows']
            data_headers = data['headers']
            pd_data_rows = pd.DataFrame(data_rows)

            for col_name in pd_data_rows.columns:
                pd_data_rows.rename(columns={col_name: data_headers[col_name]['name']}, inplace=True)

            pd_data_rows.to_csv("khis_data.csv", index=False)
            print(f'Data transformed and saved')
        except Exception as e:
            print(f"Encountered the following error: {e}")
    else:
        print(f"The response is empty")

TransformSave(fetchData(url=url))
