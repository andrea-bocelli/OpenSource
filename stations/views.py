from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils import naver_api, EVCharge_api

# Create your views here.
class StationView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')
            if None in (latitude, longitude):
                return Response({
                    "status": "error",
                    "error": "Invalid input value",
                }, status=status.HTTP_400_BAD_REQUEST)

            
            # Coordinates to Address
            address_json = naver_api.reverse_geocoding(latitude, longitude)['results'][0]['region']
            metroNm = address_json['area1']['name']
            cityNm = address_json['area2']['name']
            
            # Address to MetroCd/CityCd
            codes = EVCharge_api.get_code()['data']
            filtered_data = next(item for item in codes if item['uppoCdNm'] == metroNm and item['codeNm'] == cityNm)
            metroCd = filtered_data['uppoCd']
            cityCd = filtered_data['code']
            
            # MetroCd/CityCd to Evcharge_list
            evcharge_list = EVCharge_api.get_data(metroCd, cityCd)['data']
            
            # 거리 기준 계산
            times = 1
            for evcharge in evcharge_list:
                address = evcharge['stnAddr']
                coordinate = longitude+","+latitude
                
                coords_json = naver_api.geocoding(address, coordinate)
                # geocoding에서 인식하지 못하는 주소는 동 단위까지만 호출
                if not coords_json['addresses']:
                    short_address = " ".join(address.split()[:3])
                    coords_json = naver_api.geocoding(short_address, coordinate)
                
                evcharge['x'] = coords_json['addresses'][0]['x']
                evcharge['y'] = coords_json['addresses'][0]['y']
                evcharge['distance'] = coords_json['addresses'][0]['distance']
                print(f'{times} data retrieved')
                times += 1
                
            evcharge_list.sort(key=lambda x : float(x.get('distance', 0)))
            return Response({
                "status": "success",
                "message": "Ev charge stations retrieved successfully",
                "data": evcharge_list,
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Session expired or not found",
        }, status=status.HTTP_401_UNAUTHORIZED)
