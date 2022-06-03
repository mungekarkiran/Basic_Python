from django.shortcuts import render, HttpResponse
import yfinance as yf
import json
import logging

logging.basicConfig(filename='activity_logs.log', level = logging.INFO, format='%(asctime)s %(message)s')

# Create your views here.
def indexPage(request):
    context = {
        'variable' : 'hello django!!!',
        'flage' : 0
    }
    
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        logging.info(f'Symbol : {symbol} ')
        
        df = yf.download(symbol, period='2wk', progress=False)
        # print('df :', df)
        if len(df) > 0:
            df['pct_change_price'] = df['Close'].pct_change() * 100
            df.index = df.index.strftime('%Y-%m-%d')

            last_trade_price = df['Close'][-1]
            second_last_trade_price = df['Close'][-2]
            ohlc = [symbol, str(df.index[-1]), df['Open'][-1], df['High'][-1], df['Low'][-1], df['Close'][-1]]
            price_change_today = round(last_trade_price - second_last_trade_price, 4)

            json_records = json.loads(df.reset_index().to_json(orient ='records'))

            context.update({'msg': f'{symbol} : Data found.', 'flage':1, 
            'symbol':symbol, 'ohlc':ohlc, 'last_trade_price':last_trade_price, 
            'price_change_today':price_change_today, 'data': json_records})

        else:
            context.update({'msg': f'{symbol} : No data found.', 'flage':0})

        
        # try:
        #     pass
        # except Exception as e:
        #     print('Error : ',e)
        # df['pct_price_change'] = df['Close'].pct_change() * 100
        # df = df.round(4)
        # df.index = df.index.strftime('%Y-%m-%d')

    
    # return HttpResponse('This is indexPage ....')
    print(context.keys())
    return render(request, 'index.html', context)

def about(request):
    # return HttpResponse('This is about ....')
    return render(request, 'about.html')

def services(request):
    return HttpResponse('This is services ....')