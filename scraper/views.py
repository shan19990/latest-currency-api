from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse
from ipware import get_client_ip
import geoip2.database
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from .data import *


def conversions(request):
    try:
        from_curr = request.GET.get('from')
        amount = request.GET.get('amount')
        url = f'https://www.x-rates.com/table/?from={from_curr}&amount={amount}'
    except:
        return JsonResponse({"error": "Please enter a 'from' currency code and a 'amount' value"}, status=400)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {'title': soup.title.string, 'tables': []}
        
        tables = soup.find_all('table', class_='ratesTable')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    currency = cols[0].text.strip()
                    rate = cols[1].text.strip()
                    data['tables'].append({'currency': currency, 'rate': rate})

        if len(data['tables']) == 0:
            return JsonResponse({'error': 'Please enter valid inputs'}, status=400)

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def rates(request):
    try:
        from_curr = request.GET.get('from').lower()
        url = f'https://www.x-rates.com/table/?from={from_curr}&amount=1'
    except:
        return JsonResponse({"error": "Please enter a 'from' currency code"}, status=400)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {'title': soup.title.string, 'tables': []}
        
        tables = soup.find_all('table', class_='ratesTable')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    currency = cols[0].text.strip()
                    rate = cols[1].text.strip()
                    data['tables'].append({'currency': currency, 'rate': rate})

        if len(data['tables']) == 0:
            return JsonResponse({'error': 'Please enter valid inputs'}, status=400)

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def exchange_rate(request):
    try:
        from_curr = request.GET.get('from')
        to_curr = request.GET.get('to')
        amount = request.GET.get('amount')
        url = f'https://www.x-rates.com/calculator/?from={from_curr}&to={to_curr}&amount={amount}'
    except:
        return JsonResponse({"error": "Please enter a 'from' currency code, a 'to' currency code and a 'amount' value"}, status=400)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {'title': soup.title.string, 'from_currency': from_curr, 'to_currency': to_curr, 'amount': amount, 'converted_amount': None}
        
        converted_amount = soup.find('span', class_='ccOutputTrail').previous_sibling.strip()
        if converted_amount == "0.00":
            return JsonResponse({'error': 'Please enter valid inputs'}, status=400)
        
        data['converted_amount'] = converted_amount

        return JsonResponse(data)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def historical_currency(request):
    try:
        from_curr = request.GET.get('from_curr')
        amount = request.GET.get('amount')
        date = request.GET.get('date')
        url = f'https://www.x-rates.com/historical/?from={from_curr}&amount={amount}&date={date}'
    except:
        return JsonResponse({"error": "Please enter a 'from' currency code, a 'date' and a 'amount' value"}, status=400)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {'title': soup.title.string, 'tables': []}
        
        tables = soup.find_all('table', class_='ratesTable')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    currency = cols[0].text.strip()
                    rate = cols[1].text.strip()
                    data['tables'].append({'currency': currency, 'rate': rate})
                
                if currency == "0.00":
                    return JsonResponse({'error': 'Please enter valid inputs'}, status=400)

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def available_currencies(request):
    url = 'https://www.x-rates.com/table/?from=USD'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        data = {
            'title': soup.title.string,
            'currencies': []
        }
        
        options = soup.find_all('option')
        for option in options:
            currency = option['value']
            data['currencies'].append(currency)

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def daily_summary(request):
    try:
        date = request.GET.get('date')
        url = f'https://www.x-rates.com/historical/?amount=1&date={date}'
    except:
        return JsonResponse({"error": "Please enter a 'date' "}, status=400)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        data = {
            'title': soup.title.string,
            'date': date,
            'rates': []
        }
        
        tables = soup.find_all('table', class_='ratesTable')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    currency = cols[0].text.strip()
                    rate = cols[1].text.strip()
                    data['rates'].append({'currency': currency, 'rate': rate})

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def country(request):
    # Check if 'country' parameter is provided in the request
    if 'country' not in request.GET:
        return JsonResponse({'error': "Country parameter ('country') is required."}, status=400)

    # Get country name from request parameter and convert to lowercase
    country = request.GET.get('country').lower().replace(' ', '-')

    # URL of the specific country page on World Population Review
    url = f'https://worldpopulationreview.com/countries/{country}-population'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class 'my-5 mt-8 w-full'
        table = soup.find('table', class_='my-5 mt-8 w-full')

        if table:
            # Extract data from the table
            data = []
            rows = table.find_all('tr')

            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    category = columns[0].text.strip()
                    value = columns[1].text.strip()
                    data.append({category: value})
            
            if len(data):
                pass

            # Return the extracted data as JSON response
            return JsonResponse({'country': country, 'data': data})
        else:
            return JsonResponse({'error': 'Table with class "my-5 mt-8 w-full" not found on the page.'}, status=404)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

def country_cities(request):
    # Check if 'country' parameter is provided in the request
    if 'country' not in request.GET:
        return JsonResponse({'error': "Country parameter ('country') is required."}, status=400)

    # Get country name from request parameter and convert to lowercase
    country = request.GET.get('country').lower().replace(' ', '-')

    # URL of the specific country cities page on World Population Review
    url = f'https://worldpopulationreview.com/countries/{country}-population'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with city data
        table = soup.find('table', class_='tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white')

        if table:
            # Extract data from the table
            data = []

            # Extract rows from the table body
            rows = table.find('tbody').find_all('tr')

            for row in rows:
                # Extract city name from <th>
                city = row.find('th').text.strip()

                # Extract population from <td>
                population = row.find('td').text.strip().replace(',', '')  # Remove commas from population number

                data.append({'city': city, 'population': int(population)})


            # Return the extracted data as JSON response
            return JsonResponse({'country': country, 'cities': data})

        else:
            return JsonResponse({'error': 'City data table not found for the country.'}, status=404)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

def world_cities(request):
    # Default parameters
    order = request.GET.get('order', 'asc')  # Default order is ascending
    count = int(request.GET.get('count', 10))  # Default count is 10, convert to int

    # Validate count to prevent excessively large requests
    if count < 1 or count > 100:
        return JsonResponse({'error': 'Count must be between 1 and 100.'}, status=400)

    # URL of the world cities page on World Population Review
    url = f'https://worldpopulationreview.com/world-cities'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        cities = []
        page = 1
        while len(cities) < 100:  # Fetch multiple pages to gather enough data for sorting
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table with class 'tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white'
            table = soup.find('table', class_='tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white')

            if not table:
                return JsonResponse({'error': 'Table not found on the webpage.'}, status=404)

            # Extract data from the table
            rows = table.find_all('tr')

            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 3:  # Ensure there are enough columns for city, country, and population
                    city = columns[0].text.strip()
                    country = columns[1].text.strip()
                    population = columns[2].text.strip().replace(',', '')  # Remove commas from population number
                    cities.append({'city': city, 'country': country, 'population': int(population)})

            page += 1  # Move to the next page

        # Sort cities based on population (ascending or descending)
        cities_sorted = sorted(cities, key=lambda x: x['population'], reverse=(order == 'desc'))

        # Slice the list to return only the specified count
        cities_to_return = cities_sorted[:count]

        # Return the extracted data as JSON response
        return JsonResponse({'cities': cities_to_return})

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

def country_historic(request):
    # Check if 'country' parameter is provided in the request
    if 'country' not in request.GET:
        return JsonResponse({'error': "Country parameter ('country') is required."}, status=400)

    # Get country name from request parameter and convert to lowercase
    country = request.GET.get('country').lower().replace(' ', '-')

    # URL of the specific country page on World Population Review
    url = f'https://worldpopulationreview.com/countries/{country}-population'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables with class 'tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white'
        tables = soup.find_all('table', class_='tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white')

        if len(tables) > 1:
            # Extract data from the historic table (second table)
            historic_data = []

            # Extract rows from the table body
            rows = tables[1].find('tbody').find_all('tr')

            for row in rows:
                city = row.find('th').text.strip()
                population = row.find('td').text.strip().replace(',', '')
                historic_data.append({'city': city, 'population': int(population)})

            # Return the extracted historic data as JSON response
            return JsonResponse({'country': country, 'historic_data': historic_data})

        else:
            return JsonResponse({'error': 'Historic data table not found for the country.'}, status=404)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)


def country_future(request):
    # Check if 'country' parameter is provided in the request
    if 'country' not in request.GET:
        return JsonResponse({'error': "Country parameter ('country') is required."}, status=400)

    # Get country name from request parameter and convert to lowercase
    country = request.GET.get('country').lower().replace(' ', '-')

    # URL of the specific country page on World Population Review
    url = f'https://worldpopulationreview.com/countries/{country}-population'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables with class 'tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white'
        tables = soup.find_all('table', class_='tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white')

        if len(tables) > 2:
            # Extract data from the future table (third table)
            future_data = []

            # Extract rows from the table body
            rows = tables[2].find('tbody').find_all('tr')

            for row in rows:
                city = row.find('th').text.strip()
                population = row.find('td').text.strip().replace(',', '')
                future_data.append({'city': city, 'population': int(population)})

            # Return the extracted future data as JSON response
            return JsonResponse({'country': country, 'future_data': future_data})

        else:
            return JsonResponse({'error': 'Future data table not found for the country.'}, status=404)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

def continent(request):
    url = 'https://worldpopulationreview.com/continents'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the first table on the page
        table = soup.find('table', class_='table')

        if table:
            # Extract data from the table
            data = []

            # Extract rows from the table body
            rows = table.find('tbody').find_all('tr')

            for row in rows:
                columns = row.find_all('td')
                continent = columns[0].text.strip()
                population = columns[1].text.strip()
                world_share = columns[2].text.strip()

                data.append({
                    'continent': continent,
                    'population': population,
                    'world_share': world_share
                })

            # Return the extracted data as JSON response
            return JsonResponse({'continents': data})

        else:
            return JsonResponse({'error': 'Table not found on the webpage.'}, status=404)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

# Path to the GeoLite2-City.mmdb file
GEOIP_DB_PATH = os.path.join(os.path.dirname(__file__), 'GeoLite2-City.mmdb')

def receive_location(request):
    if request.method == 'GET':
        # Get the client's IP address
        client_ip, is_routable = get_client_ip(request)
        print(client_ip)
        if client_ip is None:
            return JsonResponse({
                'error': 'Unable to retrieve client IP address.'
            }, status=400)

        try:
            # Open the GeoLite2 database
            with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
                # Retrieve location information for the client's IP address
                response = reader.city(client_ip)

                # Extract relevant location data
                city = response.city.name if response.city.name else "Unknown"
                region = response.subdivisions.most_specific.name if response.subdivisions.most_specific.name else "Unknown"
                country = response.country.name if response.country.name else "Unknown"
                postal_code = response.postal.code if response.postal.code else "Unknown"
                latitude = response.location.latitude if response.location.latitude else "Unknown"
                longitude = response.location.longitude if response.location.longitude else "Unknown"

                location_data = {
                    'city': city,
                    'region': region,
                    'country': country,
                    'postal_code': postal_code,
                    'latitude': latitude,
                    'longitude': longitude
                }

            # Perform web scraping
            url = "http://example.com"  # Replace with the target URL
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            scraped_data = soup.title.string if soup.title else "No title found"

            return JsonResponse({
                'message': 'Data retrieved successfully.',
                'client_ip': client_ip,
                'location': location_data,
                'scraped_data': scraped_data
            })

        except geoip2.errors.AddressNotFoundError:
            return JsonResponse({
                'error': 'Location data not found for the IP address.'
            }, status=404)

        except Exception as e:
            return JsonResponse({
                'error': f'An error occurred: {str(e)}'
            }, status=500)

    else:
        return JsonResponse({
            'error': 'Method not allowed. Only GET requests are supported.'
        }, status=405)

def ip_geolocation(request, ip_address):
    try:
        # Open the GeoLite2 database
        with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
            # Retrieve location information for the IP address
            response = reader.city(ip_address)

            # Extract relevant location data
            city = response.city.name
            region = response.subdivisions.most_specific.name
            country = response.country.name
            postal_code = response.postal.code
            latitude = response.location.latitude
            longitude = response.location.longitude

            # Construct JSON response
            data = {
                'ip_address': ip_address,
                'city': city,
                'region': region,
                'country': country,
                'postal_code': postal_code,
                'latitude': latitude,
                'longitude': longitude
            }

            return JsonResponse(data)

    except geoip2.errors.AddressNotFoundError:
        return JsonResponse({'error': 'Location not found for this IP address'}, status=404)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

def world_population(request):
    try:
        # Setup WebDriver (Ensure you have ChromeDriver installed and in PATH)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        # URL of the Worldometers world population page
        url = "https://www.worldometers.info/"

        # Open the URL
        driver.get(url)

        try:
            # Find the 6th div element
            div_elements = driver.find_elements(By.TAG_NAME, 'div')
            if len(div_elements) >= 6:
                target_div = div_elements[5]  # Index 5 corresponds to the 6th div element (zero-based index)

                # Extract text content from the target div
                div_text = target_div.text.strip()

                # Split text content into lines and remove first and last line if they are headers/footers
                lines = div_text.splitlines()[1:-1]

                # Remove empty lines
                lines = [line for line in lines if line.strip()]

                # Filter out lines that match any category in categories_to_remove
                categories_to_remove = [
                    'GOVERNMENT & ECONOMICS',
                    'SOCIETY & MEDIA',
                    'ENVIRONMENT',
                    'FOOD',
                    'WATER',
                    'ENERGY',
                    'HEALTH'
                ]
                lines = [line for line in lines if not any(category in line for category in categories_to_remove)]

                # Remove special characters like '$' and ',' from each line
                cleaned_lines = []
                for line in lines:
                    cleaned_line = line.replace('$ ', '').replace(',', '').replace('-', '').replace(' tons', '').replace(' MWh', '')
                    cleaned_lines.append(cleaned_line)

                data = {}
                i = 0
                while i < len(cleaned_lines):
                    if cleaned_lines[i].isdigit():
                        value = cleaned_lines[i].strip()
                        i += 1
                        if i < len(cleaned_lines):
                            key = cleaned_lines[i].strip()
                            while i + 1 < len(cleaned_lines) and not cleaned_lines[i + 1].isdigit():
                                i += 1
                                key += " " + cleaned_lines[i].strip()
                            data[key] = value
                    else:
                        key = cleaned_lines[i].strip()
                        while i + 1 < len(cleaned_lines) and not cleaned_lines[i + 1].isdigit():
                            i += 1
                            key += " " + cleaned_lines[i].strip()
                        i += 1
                        if i < len(cleaned_lines):
                            value = cleaned_lines[i].strip()
                            data[key] = value
                    i += 1

                # Close the WebDriver
                driver.quit()

                # Return JSON response with the structured data
                return JsonResponse({
                    'data': data
                })

            else:
                raise ValueError('There are less than 6 div elements on the page.')

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

def world_top20_population(request):
    # Setup WebDriver (Ensure you have ChromeDriver installed and in PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    url = 'https://www.worldometers.info/world-population/#top20'

    try:
        # Load the URL
        driver.get(url)

        # Wait for the page to load (adjust wait time as needed)
        time.sleep(1)

        # Find the div element by its unique class name
        target_div = driver.find_element(By.CLASS_NAME, 'col-md-8')

        # Extract text, class, and id attributes
        data = target_div.text.strip()

        data = data.split('\n')[1:-1]
        
        dict_data = []

        for d in range(len(data)):
            if d % 2 == 0:
                rank = data[d].split(" ")[0]
                country = data[d].split(" ")[1]
                population = data[d+1]
                
                temp = {
                    "rank":rank,
                    "country":country,
                    "population":population,
                }
                
                dict_data.append(temp)

    finally:
        # Close the browser session
        driver.quit()

    # Return the div detail as JSON response
    return JsonResponse({'data': dict_data},status=200)

def country_population(request):
    try:
        country = request.GET.get('country').lower().replace(' ', '-')
    except:
        return JsonResponse({"error":"Please enter a valid country in URL"},status=400)
    url = f"https://www.worldometers.info/world-population/{country}-population/"

    print(url)

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)

        time.sleep(1)

        # Find all elements with class "maincounter-number"
        elements = driver.find_elements(By.CLASS_NAME, 'maincounter-number')

        if not elements :
            return JsonResponse({"error":"Please enter a valid country in URL. Check out our Country list API and the code to fetch the live population of any country"},status=400)

        # Extract text from each element
        data = [element.text for element in elements]

        if data[0] == "retrieving data..." :
            return JsonResponse({"info":"Something went wrong, please try again after some time"})

        # Return data as JSON response
        return JsonResponse({'population': data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def country_links(request):
    try:
        url = f"https://www.worldometers.info/world-population/population-by-country/"

        options = webdriver.ChromeOptions()
        # Uncomment the line below to run Chrome in headless mode (without opening a browser window)
        # options.add_argument('--headless')
        
        driver = webdriver.Chrome(options=options)
        

        try:
            driver.get(url)

            time.sleep(1)

            # Find the table element by its id "example2"
            table = driver.find_element(By.ID, 'example2')

            # Find all rows (tr elements) in the table
            rows = table.find_elements(By.TAG_NAME, 'tr')

            country_data_list = []

            # Loop through each row, starting from the second row (index 1) to skip the header row
            for row in rows[1:]:
                # Find all columns (td elements) in the row
                columns = row.find_elements(By.TAG_NAME, 'td')

                # Ensure there are at least 2 columns (first column for country name and second column for link)
                if len(columns) >= 3:
                    # Extract text from the first column (country data)
                    country_data = columns[1].text.strip()

                    link_element = columns[1].find_element(By.TAG_NAME, 'a')
                    country_link = link_element.get_attribute('href')
                    print(country_link)
                    parts = country_link.split("/")
                    print(parts[-2])
                    code = parts[-2].split("-p")[0]
                    print(code)
                    country_data_list.append({
                        'country': country_data,
                        'country_code': code
                    })

            # Return data as JSON response
            return JsonResponse({'list': country_data_list},status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)},status=400)

        finally:
            driver.quit()

    except Exception as e:
        return JsonResponse({"error": str(e)},status=400)

def country_historican_statistic(request):
    try:
        country = request.GET.get('country').lower().replace(' ', '-')
    except:
        return JsonResponse({"error":"Please enter a valid country in URL"},status=400)
    url = f"https://www.worldometers.info/world-population/{country}-population/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)

        time.sleep(1)

        # Find the table element by its class name
        table = driver.find_element(By.CLASS_NAME, 'table-list')

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')

        table_data = []

        country_data = {
            "Year": None,
            "Population": None,
            "Yearly % Change": None,
            "Yearly Change": None,
            "Migrants (net)": None,
            "Median Age": None,
            "Fertility Rate": None,
            "Density (P/Km²)": None,
            "Urban Pop %": None,
            "Urban Population": None,
            "Country's Share of World Pop": None,
            "World Population": None,
            "India Global Rank": None
        }

        # Iterate over each row and extract column data
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and len(columns) >= len(country_data):
                row_data = {
                    key: columns[index].text.strip() if columns[index].text.strip() != "" else None
                    for index, key in enumerate(country_data.keys())
                }
                table_data.append(row_data)


        # Return data as JSON response
        return JsonResponse({'data': table_data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def country_historical(request):
    try:
        country = request.GET.get('country').lower().replace(' ', '-')
    except:
        return JsonResponse({"error": "Please enter a valid country in the URL"},status=400)

    url = f"https://www.worldometers.info/world-population/{country}-population/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)
        print("Page loaded")

        time.sleep(1)

        # Find all tables on the page
        tables = driver.find_elements(By.TAG_NAME, 'table')
        print(f"Number of tables found: {len(tables)}")
        
        # Check if there are at least two tables on the page
        if len(tables) < 2:
            return JsonResponse({"error": "Could not find the second table on the page"},status=400)

        # Select the second table (index 1)
        table = tables[1]
        #print(table.get_attribute('outerHTML'))

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')
        print(f"Number of rows found: {len(rows)}")

        table_data = []

        # Regular expression pattern for extracting data from <td> tags
        pattern = re.compile(r'<td>(.*?)</td>')

        # Iterate over each row and extract column data
        for index, row in enumerate(rows[1:]):  # Skip the header row
            row_html = row.get_attribute('outerHTML')
            matches = pattern.findall(row_html)
            if len(matches) >= 2:
                year = matches[0].strip()
                population = matches[1].strip()
                print(f"Year: {year}, Population: {population}")
                if year and population:
                    table_data.append({year: population})

        # Return data as JSON response
        return JsonResponse({'data': table_data},status=200)

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()
        print("WebDriver session closed")

def country_forecast_statistic(request):
    try:
        country = request.GET.get('country').lower().replace(' ', '-')
    except:
        return JsonResponse({"error":"Please enter a valid country in URL"},status=400)
    url = f"https://www.worldometers.info/world-population/{country}-population/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)
        time.sleep(1)

        # Find all table elements by their class name
        tables = driver.find_elements(By.CLASS_NAME, 'table-list')

        if len(tables) < 2:
            return JsonResponse({"error": "Could not find the 5th table with the class 'table-list'"},status=400)

        # Select the 5th table (index 4)
        table = tables[1]

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')

        table_data = []

        country_data_keys = [
            "Year", "Population", "Yearly % Change", "Yearly Change", 
            "Migrants (net)", "Median Age", "Fertility Rate", "Density (P/Km²)", 
            "Urban Pop %", "Urban Population", "Country's Share of World Pop", 
            "World Population", "India Global Rank"
        ]

        # Iterate over each row and extract column data
        for row in rows[1:]:  # Skip the header row if there's one
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and len(columns) >= len(country_data_keys):
                row_data = {
                    key: columns[index].text.strip() if columns[index].text.strip() != "" else None
                    for index, key in enumerate(country_data_keys)
                }
                table_data.append(row_data)

        # Return data as JSON response
        return JsonResponse({'data': table_data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def country_city_population(request):
    try:
        country = request.GET.get('country').lower().replace(' ', '-')
    except:
        return JsonResponse({"error":"Please enter a valid country in URL"},status=400)
    url = f"https://www.worldometers.info/world-population/{country}-population/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)
        time.sleep(1)

        # Find all table elements by their class name
        tables = driver.find_elements(By.CLASS_NAME, 'table-list')

        if len(tables) < 3:
            return JsonResponse({"error": "Could not find the 5th table with the class 'table-list'"},status=400)

        # Select the 5th table (index 4)
        table = tables[2]

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')

        city_data = []

        # Iterate over each row and extract column data
        for row in rows[1:]:  # Skip the header row if there's one
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and len(columns) >= 3:
                rank = columns[0].text.strip()
                city = columns[1].text.strip()
                population = columns[2].text.strip()
                if rank and city and population:
                    city_data.append({"Rank": rank, "City": city, "Population": population})

        # Return data as JSON response
        return JsonResponse({'data': city_data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def world_historical(request):
    url = "https://www.worldometers.info/world-population/world-population-by-year/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)
        time.sleep(1)

        # Find the table with the specified class
        table = driver.find_element(By.CSS_SELECTOR, '.table.table-hover.table-condensed')

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')

        table_data = []

        # Iterate over each row and extract column data
        for row in rows[1:]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and len(columns) >= 5:
                year = columns[0].text.strip()
                world_population = columns[1].text.strip()
                yearly_change = columns[2].text.strip()
                net_change = columns[3].text.strip()
                density = columns[4].text.strip()
                table_data.append({
                    "Year": year,
                    "World Population": world_population,
                    "Yearly Change": yearly_change,
                    "Net Change": net_change,
                    "Density (P/Km²)": density
                })

        # Return data as JSON response
        return JsonResponse({'data': table_data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def world_forecast(request):
    url = "https://www.worldometers.info/world-population/world-population-projections/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)
        time.sleep(1)

        # Find the table with the specified class
        table = driver.find_element(By.CSS_SELECTOR, '.table.table-hover.table-condensed')

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')

        table_data = []

        # Iterate over each row and extract column data
        for row in rows[1:]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and len(columns) >= 5:
                year = columns[0].text.strip()
                world_population = columns[1].text.strip()
                yearly_change = columns[2].text.strip()
                net_change = columns[3].text.strip()
                density = columns[4].text.strip()
                table_data.append({
                    "Year": year,
                    "World Population": world_population,
                    "Yearly Change": yearly_change,
                    "Net Change": net_change,
                    "Density (P/Km²)": density
                })

        # Return data as JSON response
        return JsonResponse({'data': table_data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def country_counts(request):
    url = "https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # Load the URL
        driver.get(url)
        time.sleep(1)

        # Find the element with the specified class
        counter = driver.find_element(By.CLASS_NAME, 'maincounter-number')

        # Extract the text content
        country_count = counter.text.strip()

        # Return data as JSON response
        return JsonResponse({'country_count': country_count},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def country_flags(request):
    url = "https://www.worldometers.info/geography/flags-of-the-world/"

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        flag_data = {}

        # Find all div elements with class="col-md-4"
        flag_divs = soup.find_all('div', class_='col-md-4')

        # Iterate over each div to extract country name and href
        for div in flag_divs:
            country_tag = div.find('div', style='font-weight:bold; padding-top:10px')
            a_tag = div.find('a')

            if country_tag and a_tag:
                country = country_tag.text.strip()
                href = a_tag.get('href')

                # Adjust href to get full URL if needed
                if href.startswith('/'):
                    href = 'https://www.worldometers.info' + href

                flag_data[country] = href

        # Return data as JSON response
        return JsonResponse({'flags': flag_data},status=200)

    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors
        return JsonResponse({'error': str(e)},status=400)

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'error': str(e)},status=400)


def crypto_currency(request):
    url = "https://in.investing.com/crypto/currencies/"

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    try:
        # Load the URL
        driver.get(url)
        time.sleep(1)

        # Find the table with the specified class
        table = driver.find_element(By.CSS_SELECTOR, '.datatable_table__DE_1_')

        print(table)

        # Find all rows (tr elements) in the table body
        rows = table.find_elements(By.TAG_NAME, 'tr')

        table_data = []

        # Iterate over each row and extract column data
        for row in rows[1:]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns and len(columns) >= 5:
                crypto = columns[3].text.strip()
                parts = crypto.split('\n')
                name = parts[0]
                ticker = ''.join(filter(str.isalpha, parts[1]))
                value = columns[4].text.strip()
                table_data.append({
                    "Crypto Currency": name,
                    'Crypto':ticker,
                    "Value":value,
                })

        # Return data as JSON response
        return JsonResponse({'data': table_data},status=200)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)},status=400)

    finally:
        # Close the WebDriver session
        driver.quit()

def crypto_currency_individual(request):
    try:
        crypto = request.GET.get('crypto').lower().replace(' ', '-')
        url = f"https://in.investing.com/crypto/{crypto}/"
    except Exception as e:
        return JsonResponse({"error": "Please enter a valid crypto in URL"}, status=400)

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(1)

        # Try to get data for a specific cryptocurrency
        price_element = driver.find_element(By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]')
        price = price_element.text.strip()

        return JsonResponse({'crypto': crypto, 'price': price}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    finally:
        driver.quit()


metals = {
    "Aluminum": "al",
    "Cobalt": "co",
    "Copper": "cu",
    "Gallium": "ga",
    "Gold": "au",
    "Indium": "in",
    "Iridium": "ir",
    "Iron Ore": "fe",
    "Lead": "pb",
    "Lithium": "li",
    "Molybdenum": "mo",
    "Neodymium": "nd",
    "Nickel": "ni",
    "Palladium": "pd",
    "Platinum": "pt",
    "Rhodium": "rh",
    "Ruthenium": "ru",
    "Silver": "ag",
    "Steel Rebar": "st",
    "Tellurium": "te",
}

units = {
    "Pound": "lb",
    "Metric Ton": "mt",
    "Troy Ounce": "oz",
    "Gram": "g",
    "Kilogram": "kg",
    "Short Ton": "t",
}

date_ranges = {
    "1": "1",
    "5": "5",
    "10": "10",
    "20": "20",
}


def commodities_metals(request):
    try:
        metal = request.GET.get('metal').lower()
        unit = request.GET.get('unit').lower()
        date_range = request.GET.get('date_range')

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        if not metal or not unit or not date_range:
            return JsonResponse({
                "error": "Please enter a 'metal', a 'unit' and a 'date_range'",
                "metals": list(metals.keys()),
                "units": list(units.keys()),
                "date_ranges": list(date_ranges.values())
            }, status=400)
        
        if not metal or not unit or not date_range:
            return JsonResponse({"error": "Invalid parameters"}, status=400)

        # Construct the URL
        url = f"https://www.dailymetalprice.com/metalprices.php?c={metal}&u={unit}&d={date_range}"
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url)
            time.sleep(1)
            
            # Scrape the table data
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', class_='table table-striped table-hover table-condensed success')

            headers = [th.text.strip() for th in table.find_all('th')]
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip the header row
                cells = [td.text.strip() for td in tr.find_all('td')]
                print(cells)
                cell = {
                    "Date":cells[1],
                    "Price":cells[0],
                }
                rows.append(cell)

            return JsonResponse({"data": rows}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        finally:
            driver.quit()
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def commodities_metals_currency(request):
    try:
        country = request.GET.get('country').capitalize()
        currency_code = country_currency_codes.get(country)

        if not currency_code:
            return JsonResponse({
                "error": "Invalid or missing 'country' parameter",
                "available_countries": list(country_currency_codes.keys())
            }, status=400)

        url = f"https://www.dailymetalprice.com/metalpricescurr.php?x={currency_code}"

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url)
            time.sleep(2)

            # Scrape the first table
            table = driver.find_element(By.CSS_SELECTOR, 'table.table.table-striped.table-hover.table-condensed.success')
            rows = table.find_elements(By.TAG_NAME, 'tr')

            table_data = []
            headers = ["Commodity", "Price", "Unit", "Date"]

            for row in rows[1:]:  # Skip the header row
                columns = row.find_elements(By.TAG_NAME, 'td')
                if len(columns) == 4:  # Ensure there are exactly 4 columns
                    row_data = {
                        headers[0]: columns[0].text.strip(),
                        headers[1]: columns[1].text.strip(),
                        headers[2]: columns[2].text.strip(),
                        headers[3]: columns[3].text.strip(),
                    }
                    table_data.append(row_data)

            return JsonResponse({'data': table_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        finally:
            driver.quit()

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def time_capitals(request):
    try:
        url = "https://www.timeanddate.com/worldclock/?low=c"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='zebra fw tb-theme')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        for row in table.find_all('tr'):
            columns = row.find_all(['th', 'td'])
            if len(columns) >= 2:
                city = columns[0].text.strip('*')
                date = columns[1].text.strip().split()[1]
                table_data.append({city: date})
                city = columns[2].text.strip('*')
                date = columns[3].text.strip().split()[1]
                table_data.append({city: date})
                try:
                    city = columns[4].text.strip('*')
                    date = columns[5].text.strip().split()[1]
                    table_data.append({city: date})
                except:
                    pass

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def time_popular(request):
    try:
        url = "https://www.timeanddate.com/worldclock/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='zebra fw tb-theme')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        for row in table.find_all('tr'):
            columns = row.find_all(['th', 'td'])
            if len(columns) >= 2:
                city = columns[0].text.strip('*')
                date = columns[1].text.strip().split()[1]
                table_data.append({city: date})
                city = columns[2].text.strip('*')
                date = columns[3].text.strip().split()[1]
                table_data.append({city: date})
                try:
                    city = columns[4].text.strip('*')
                    date = columns[5].text.strip().split()[1]
                    table_data.append({city: date})
                except:
                    pass

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def time_extended(request):
    try:
        url = "https://www.timeanddate.com/worldclock/full.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='zebra fw tb-theme')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        for row in table.find_all('tr'):
            columns = row.find_all(['th', 'td'])
            if len(columns) >= 2:
                city = columns[0].text.strip('*')
                date = columns[1].text.strip().split()[1]
                table_data.append({city: date})
                city = columns[2].text.strip('*')
                date = columns[3].text.strip().split()[1]
                table_data.append({city: date})
                try:
                    city = columns[4].text.strip('*')
                    date = columns[5].text.strip().split()[1]
                    table_data.append({city: date})
                except:
                    pass

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def time_country(request):
    try:
        country = request.GET.get('country').lower().replace(' ', '-')
        url = f"https://www.timeanddate.com/worldclock/{country}/"
        print(url)
    except Exception as e:
        return JsonResponse({"error": "Please enter a valid crypto in URL"}, status=400)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        table = soup.find('table', class_='zebra fw tb-wc zebra')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        for row in table.find_all('tr'):
            columns = row.find_all(['th', 'td'])
            if len(columns) >= 2:
                city = columns[0].text.strip('*')
                date = columns[1].text.strip().split()[1]
                table_data.append({city: date})
                city = columns[2].text.strip('*')
                date = columns[3].text.strip().split()[1]
                table_data.append({city: date})
                try:
                    city = columns[4].text.strip('*')
                    date = columns[5].text.strip().split()[1]
                    table_data.append({city: date})
                except:
                    pass

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def time_country_city(request):
    try:
        country = request.GET.get('country', '').strip().lower().replace(' ', '-')
        city = request.GET.get('city', '').strip().lower().replace(' ', '-')
        if not country or not city:
            return JsonResponse({"error": "Please provide both country and city names in the URL"}, status=400)

        url = f"https://www.timeanddate.com/worldclock/{country}/{city}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract time
        div_qlook = soup.find('div', id='qlook', class_='bk-focus__qlook')
        if not div_qlook:
            return JsonResponse({"error": "Time information not found on the page"}, status=400)

        span_time = div_qlook.find('span')
        if not span_time:
            return JsonResponse({"error": "Time span not found within div"}, status=400)

        time = span_time.text.strip()

        # Extract table data
        table = soup.find('table', class_='table table--left table--inner-borders-rows')
        if not table:
            return JsonResponse({"error": "Details table not found on the page"}, status=400)

        table_data = {}
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all(['th', 'td'])
            if len(columns) == 2:
                key = columns[0].text.strip().strip(':')
                value = columns[1].text.strip()
                table_data[key] = value

        # Include time in the response
        table_data['Time'] = time

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def weather_capitals(request):
    try:
        url = "https://www.timeanddate.com/weather/?low=c"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class 'zebra fw tb-theme'
        table = soup.find('table', class_='zebra fw tb-theme')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        rows = table.find_all('tr')

        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) >= 4:
                city = columns[0].text.strip()
                time = columns[1].text.strip()
                temp = time.split(" ")[1]
                weather = columns[2].text.strip()
                temperature = columns[3].text.strip()
                table_data.append({
                    "city": city,
                    "time": temp,
                    "temperature": temperature
                })

        return JsonResponse({'data': table_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def weather_popular(request):
    try:
        url = "https://www.timeanddate.com/weather/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class 'zebra fw tb-theme'
        table = soup.find('table', class_='zebra fw tb-theme')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        rows = table.find_all('tr')

        print(rows)

        for row in rows[1:]:  # Skip the header row
            #print(row)
            columns = row.find_all('td')
            city = columns[0].text.strip()
            time = columns[1].text.strip()
            temp = time.split(" ")[1]
            temperature = columns[3].text.strip()
            table_data.append({
                "city": city,
                "time": temp,
                "temperature": temperature
            })

        return JsonResponse({'data': table_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def weather_extended(request):
    try:
        url = "https://www.timeanddate.com/weather/?low=5"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class 'zebra fw tb-theme'
        table = soup.find('table', class_='zebra fw tb-theme')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        table_data = []
        rows = table.find_all('tr')

        print(rows)

        for row in rows[1:]:  # Skip the header row
            #print(row)
            columns = row.find_all('td')
            city = columns[0].text.strip()
            time = columns[1].text.strip()
            temp = time.split(" ")[1]
            temperature = columns[3].text.strip()
            table_data.append({
                "city": city,
                "time": temp,
                "temperature": temperature
            })

        return JsonResponse({'data': table_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def translate_date(hindi_date):
    for hindi, english in translation_dict.items():
        hindi_date = hindi_date.replace(hindi, english)
    return hindi_date

def weather_country_city_forecast(request):
    try:
        country = request.GET.get('country', '').strip().lower().replace(' ', '-')
        city = request.GET.get('city', '').strip().lower().replace(' ', '-')

        url = f"https://www.timeanddate.com/weather/{country}/{city}/ext"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='zebra')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        headers = []
        table_data = []

        # Extract headers
        thead = table.find('thead')
        if thead:
            header_rows = thead.find_all('tr')
            for header_row in header_rows:
                headers = [th.get_text().strip() for th in header_row.find_all('th')]

        # Extract data from rows
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                row_header = row.find('th').get_text().strip() if row.find('th') else None
                row_data = {}
                if row_header:
                    row_data["Date"] = translate_date(row_header)  # Include the date field from <th> element
                for i, col in enumerate(columns):
                    key = headers[i + 1] if i + 1 < len(headers) else f'Column {i + 1}'
                    if key == "":
                        key = "Wind Direction"
                    if key == "Wind Direction" and col.find('span'):
                        row_data[key] = col.find('span').get('title', '').strip()
                    else:
                        row_data[key] = col.get_text().strip()
                table_data.append(row_data)

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def weather_country_city_today(request):
    try:
        country = "india"  # Hardcoded for India
        city = "kolkata"   # Hardcoded for Kolkata

        url = f"https://www.timeanddate.com/weather/{country}/{city}/hourly"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='zebra')
        if not table:
            return JsonResponse({"error": "Table not found on the page"}, status=400)

        headers = []
        table_data = []

        # Extract headers
        thead = table.find('thead')
        if thead:
            header_rows = thead.find_all('tr')
            for header_row in header_rows:
                headers = [th.get_text().strip() for th in header_row.find_all('th')]

        # Extract data from rows
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                row_header = row.find('th').get_text().strip() if row.find('th') else None
                row_data = {}
                if row_header:
                    row_data["Date"] = translate_date(row_header)  # Include the date field from <th> element
                for i, col in enumerate(columns):
                    key = headers[i + 1] if i + 1 < len(headers) else f'Column {i + 1}'
                    if key == "":
                        key = "Wind Direction"
                    if key == "Wind Direction" and col.find('span'):
                        row_data[key] = col.find('span').get('title', '').strip()
                    else:
                        row_data[key] = col.get_text().strip()
                table_data.append(row_data)

        return JsonResponse({'data': table_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)