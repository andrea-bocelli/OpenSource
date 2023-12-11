from basicEnvironment import settings
import requests

def geocoding(address, coordinate:None=""):
    response = requests.get(
        f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}&coordinate={coordinate}",
        headers={
            "X-NCP-APIGW-API-KEY-ID": settings.NAVER_API_KEY_ID,
            "X-NCP-APIGW-API-KEY": settings.NAVER_API_KEY,
        })
    
    if response.status_code == 200:
        return response.json()
    print(response.status_code)
    return None

def reverse_geocoding(latitude, longitude):
    response = requests.get(
        f"https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?request=coordsToaddr&coords={longitude},{latitude}&sourcecrs=epsg:4326&output=json&orders=addr,admcode",
        headers={
            "X-NCP-APIGW-API-KEY-ID": settings.NAVER_API_KEY_ID,
            "X-NCP-APIGW-API-KEY": settings.NAVER_API_KEY,
        })
    
    if response.status_code == 200:
        return response.json()
    print(response.status_code)
    return None
    