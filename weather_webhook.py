import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

cities = {}
cities['Daejeon'] = {'lat': 36.3504,
                     'lon': 127.3845}
# url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

current_weather_url = (
    f'https://api.openweathermap.org/data/2.5/weather?lat={cities["Daejeon"]["lat"]}&lon={cities["Daejeon"]["lon"]}&appid={API_KEY}&units=metric&lang=kr'
    )
weather_description_map = {
    # ☀️ 맑음/햇빛
    "clear sky": "맑음",

    # 🌤️ 약간의 구름
    "few clouds": "약간의 구름",
    "scattered clouds": "흩어진 구름",   # 또는 "살짝 구름낌"
    "broken clouds": "구름 조금 많음",
    "overcast clouds": "흐림",

    # 🌧️ 비
    "light rain": "약한 비",
    "moderate rain": "보통 비",
    "heavy intensity rain": "강한 비",
    "very heavy rain": "매우 강한 비",
    "extreme rain": "극심한 비",
    "freezing rain": "어는 비",
    "light intensity shower rain": "약한 소나기",
    "shower rain": "소나기",
    "heavy intensity shower rain": "강한 소나기",
    "ragged shower rain": "불규칙한 소나기",

    # ⛈️ 천둥번개
    "thunderstorm": "천둥번개",
    "thunderstorm with light rain": "약한 비를 동반한 천둥번개",
    "thunderstorm with rain": "비를 동반한 천둥번개",
    "thunderstorm with heavy rain": "강한 비를 동반한 천둥번개",
    "light thunderstorm": "약한 천둥번개",
    "heavy thunderstorm": "강한 천둥번개",
    "ragged thunderstorm": "불규칙한 천둥번개",
    "thunderstorm with drizzle": "이슬비를 동반한 천둥번개",

    # 🌨️ 눈
    "light snow": "약한 눈",
    "snow": "눈",
    "heavy snow": "강한 눈",
    "sleet": "진눈깨비",
    "light shower sleet": "약한 소나기 진눈깨비",
    "shower sleet": "소나기 진눈깨비",
    "light rain and snow": "약한 비와 눈",
    "rain and snow": "비와 눈",
    "light shower snow": "약한 소나기 눈",
    "shower snow": "소나기 눈",
    "heavy shower snow": "강한 소나기 눈",

    # 🌫️ 안개/연무
    "mist": "엷은 안개",
    "smoke": "연기",
    "haze": "실안개",
    "sand/dust whirls": "모래/먼지 소용돌이",
    "fog": "안개",
    "sand": "모래",
    "dust": "먼지",
    "volcanic ash": "화산재",
    "squalls": "돌풍",
    "tornado": "토네이도"
}


def get_weather():
    response=requests.get(current_weather_url)
    if response.status_code == 200:
        data = response.json()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") # 현재 시간
        city = data['name'] # 도시 이름
        weather = data['weather'][0]['description'] # 날씨
        korean_weather = weather_description_map.get(weather,  weather)
        temp = data['main']['temp'] # 온도
        humidity = data['main']['humidity'] # 습도
        message = (
            f' {now} 기준, {city} 날씨 정보입니다.\n'
            f' 날씨: {korean_weather}\n'
            f' 온도: {temp}ºC\n'
            f' 습도: {humidity}%'
        )
        return message
    else:
        print(f'API 호출 실패: ', data)

def send_slack_message(message):
    slack_data = {'text': message}
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    if response.status_code != 200:
        print(f"Slack 메시지 전송 실패: {response.status_code}, {response.text}")


if __name__ == "__main__":
    weather_message = get_weather()
    send_slack_message(weather_message)