from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests

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
