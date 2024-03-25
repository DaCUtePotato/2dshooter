import socket
import requests

def get_website_location(website):
    try:
        ip_address = socket.gethostbyname(website)
        url = f"http://api.ipstack.com/{ip_address}?access_key=YOUR_API_KEY"
        response = requests.get(url)
        data = response.json()
        city = data["city"]
        region = data["region_name"]
        country = data["country_name"]
        return city, region, country
    except socket.gaierror:
        return "Could not resolve hostname."
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
website = input("Enter the website URL: ")
city, region, country = get_website_location(website)
if isinstance(city, tuple):
    print("Error:", city[0])
else:
    print(f"The website {website} is likely located in {city}, {region}, {country}.")
