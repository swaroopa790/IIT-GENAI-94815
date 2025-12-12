from math_utils import add, multiply
from api_module import get_weather

def main():
    print("=== Math Module Demo ===")
    print("2 + 3 =", add(2, 3))
    print("4 * 5 =", multiply(4, 5))

    print("\n=== Weather API Demo ===")
    city = input("Enter city name: ")
    weather = get_weather(city)
    if "error" in weather:
        print(weather["error"])
    else:
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Wind Speed: {weather['wind_speed']} m/s")

if __name__ == "__main__":
    main()
