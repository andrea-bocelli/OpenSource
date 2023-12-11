from basicEnvironment import settings
import requests
def get_data(metroCd, cityCd):
    response = requests.get(
    f"https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do?metroCd={metroCd}&cityCd={cityCd}&apiKey={settings.EVCHARGE_API_KEY}&returnType=json"
    )

    if response.status_code == 200:
        return response.json()
    print(response.status_code)
    return None

def get_code():
    response = requests.get(f"https://bigdata.kepco.co.kr/openapi/v1/commonCode.do?codeTy=cityCd&apiKey={settings.EVCHARGE_API_KEY}&returnType=json")
    
    if response.status_code == 200:
        return response.json()
    print(response.status_code)
    return None
