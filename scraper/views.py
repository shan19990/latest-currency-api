from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse
from ipware import get_client_ip
import geoip2.database
import os

def conversions(request):
    from_curr = request.GET.get('from_curr')
    amount = request.GET.get('amount')
    url = f'https://www.x-rates.com/table/?from={from_curr}&amount={amount}'
    
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

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def rates(request):
    from_curr = request.GET.get('from_curr')
    url = f'https://www.x-rates.com/table/?from={from_curr}&amount=1'
    
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

        return JsonResponse(data)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def exchange_rate(request):
    from_curr = request.GET.get('from_curr')
    to_curr = request.GET.get('to_curr')
    amount = request.GET.get('amount')
    url = f'https://www.x-rates.com/calculator/?from={from_curr}&to={to_curr}&amount={amount}'
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {'title': soup.title.string, 'from_currency': from_curr, 'to_currency': to_curr, 'amount': amount, 'converted_amount': None}
        
        converted_amount = soup.find('span', class_='ccOutputTrail').previous_sibling.strip()
        data['converted_amount'] = converted_amount

        return JsonResponse(data)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def historical_currency(request):
    from_curr = request.GET.get('from_curr')
    amount = request.GET.get('amount')
    date = request.GET.get('date')
    url = f'https://www.x-rates.com/historical/?from={from_curr}&amount={amount}&date={date}'
    
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
    date = request.GET.get('date')
    url = f'https://www.x-rates.com/historical/?amount=1&date={date}'
    
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

def world_population(request):
    url = 'https://worldpopulationreview.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Default parameters
    default_number = 10  # Default number of rows to return
    default_order = 'desc'  # Default order ('desc' for descending, 'asc' for ascending)

    # Get parameters from request
    number = int(request.GET.get('count', default_number))
    order = request.GET.get('order', default_order)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing countries and their populations
        table = soup.find('table', class_='tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white')
        if table:
            # Extract table rows (excluding header)
            rows = table.find_all('tr')[1:]  # Skip header row

            # List to store data
            data = []

            # Prepare list of tuples (country, population) for sorting
            country_populations = []
            for row in rows:
                columns = row.find_all('td')
                country = columns[0].text.strip()
                population = columns[1].text.strip()
                country_populations.append((country, population))

            # Sort country_populations based on population in descending or ascending order
            if order == 'desc':
                country_populations.sort(key=lambda x: int(x[1].replace(',', '')), reverse=True)
            elif order == 'asc':
                country_populations.sort(key=lambda x: int(x[1].replace(',', '')))

            # Extract sorted data up to the specified number
            for i, (country, population) in enumerate(country_populations[:number]):
                data.append({'Country': country, 'Population': population})

            # Return the extracted data as JSON response
            return JsonResponse({'data': data})

        else:
            return JsonResponse({'error': 'Table not found on the webpage.'}, status=404)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

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
