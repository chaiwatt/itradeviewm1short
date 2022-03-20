from django.shortcuts import render,redirect
# from datetime import date, datetime, time
import pandas as pd
import MetaTrader5 as mt5
from django.http import HttpRequest, JsonResponse,HttpResponse
from json import dumps
from django.db.models import Q
from .models import BackTestOHLCTimeframe, CurrentView, OhlcImage,Symbol,TimeFrame,BackTest,BackTestSize,BackTestInterval,BackTestOHLC,Setting,MyAccount,Broker,Spec,SearchType,SearchReport,StdBarSize,LotSizeFactor,BackTestOHLCTimeframe,OhlcImage
import requests
symbol = 'USDJPY'
from django.utils import timezone
from django.core import serializers
import time
import numpy as np
import math
from datetime import datetime,timedelta
import pytz
import pyrebase
import base64
from django.core.files.base import ContentFile
import operator
import sys
import uuid

config ={
    'apiKey': "AIzaSyBWkbdZu6r0giHnxVwGrqJaHXoQIk2_TWk",
    'authDomain': "itrader-32c33.firebaseapp.com",
    'databaseURL': "https://itrader-32c33-default-rtdb.firebaseio.com",
    
    'projectId': "itrader-32c33",
    'storageBucket': "itrader-32c33.appspot.com",
    'messagingSenderId': "915590837295",
    'appId': "1:915590837295:web:783b66e023b0a7bbeb42da"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

#symbol = 'EURUSD'
# timeframe = 'M1';
# dataframe = mt5.TIMEFRAME_M1


def index(request):
    # symbol_fb = database.child('Data').child('symbol').get().val()
    # lotsize_fb = database.child('Data').child('lotsize').get().val()
    # database.child("Data").update({"symbol": "USDJPY"})
    # database.child("Data").child("tp").remove()
    # print (symbol_fb)
    # print (lotsize_fb)

    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    # print (accountinfo)
    currentview = CurrentView.objects.first()
    tf = TimeFrame.objects.get(id = currentview.timeframe_id)
    timeframe = tf.name
    dataframe = getattr(mt5, f'TIMEFRAME_{timeframe}')
    _symbol = Symbol.objects.get(id = currentview.symbol_id)
    symbol = _symbol.name
    
    symbol_info=mt5.symbol_info(symbol)
    # print (symbol_info)

    # lasttick=mt5.symbol_info_tick(symbol)
    # print(lasttick)

    # print(pipChange(symbol_info.bid,symbol_info.ask,symbol_info.digits))
    # print(pipPricePerLotsize(symbol_info.name,symbol_info.digits,symbol_info.ask,symbol_info.trade_contract_size,1))
    # print(pipChange(symbol_info.bid,symbol_info.ask,symbol_info.digits) * pipPricePerLotsize(symbol_info.name,symbol_info.digits,symbol_info.ask,symbol_info.trade_contract_size,1))
    # print(stopLossPrice(0.1,accountinfo.balance))
    # print(getLotSize(stopLossPrice(0.01,accountinfo.balance),100, pipPricePerLotsize(symbol_info.name,symbol_info.digits,symbol_info.ask,symbol_info.trade_contract_size,1)))

    symbol_price = mt5.symbol_info_tick(symbol)._asdict()

    # print(symbol_price)
    
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, dataframe, 0, 500))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s',utc=True)
    ohlcs = []
    orders = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs.append(ohlc)

    positions=mt5.positions_get()
    # print(positions)

    if positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s',utc=True)
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        # print(df)
        
        for i, data in df.iterrows():
            # print('ticket {0} time {1} volume {2} type {3} profit {4} symbol {5}'.format(data['ticket'],data['time'], data['volume'],data['type'],data['profit'],data['symbol']))
            # _symbol = Symbol.objects.filter(name = data['symbol']).first()
            # _timeframe = TimeFrame.objects.filter(name = data['symbol']).first()
            _data = {
                'symbol':data['symbol'],
                'lot':data['volume'] ,
                'profit':data['profit'],
                'position':data['ticket'],
                'type':data['type'],
                'comment':data['comment'],
            }
            orders.append(_data)
        # print(orders)
    data = {
        'orders':orders,
        'symbol':symbol,
        'series':ohlcs, 
        'price': 
        {
            'ask':symbol_price['ask'],
            'bid':symbol_price['bid'],
            'timeframe':timeframe
        }
    }

    data = dumps(data)
    return render(request,'index.html',{
        'orders': orders,
        'resData': data,
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id).order_by('name'),
        'timeframes':TimeFrame.objects.all(),
        
        'searchreports':SearchReport.objects.all().order_by('-id')[:30],
        'currentview':currentview,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1,symbol_id = currentview.symbol_id),   
        'orderbuyentryspecobjects' : Spec.objects.filter(spec_type = 1,status = 1,symbol_id = currentview.symbol_id,order_type = 0), 
        'ordersellentryspecobjects' : Spec.objects.filter(spec_type = 1,status = 1,symbol_id = currentview.symbol_id,order_type = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1,symbol_id = currentview.symbol_id)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1,symbol_id = currentview.symbol_id)), 
    })

def pipChange(fromPrice,toPrice,degit):
    multipleNum = 10
    if degit % 2 == 0:
        multipleNum = 1
    
    # math.pow(10, 1*degit)
    pip = ((toPrice - fromPrice) * math.pow(10, 1*degit))/multipleNum
    return pip 

def pipPricePerLotsize(symbol,degit,currentPrice,contractSize,lotsize):
    if symbol[0:3] == 'USD':
        return (((math.pow(10, (-1)*degit))/currentPrice)*contractSize)*lotsize
    else:
        return ((math.pow(10, (-1)*degit))*contractSize)*lotsize

def stopLossPrice(percent,balance):
    return percent * balance

def getLotSize(stoplostPrice,numPips,pipPrice):
    return stoplostPrice/(numPips*pipPrice)

def getohlc(request):  
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    currentview = CurrentView.objects.first()
    tf = TimeFrame.objects.get(id = currentview.timeframe_id)
    timeframe = tf.name
    dataframe = getattr(mt5, f'TIMEFRAME_{timeframe}')
    _symbol = Symbol.objects.get(id = currentview.symbol_id)
    symbol = _symbol.name

    symbol_price = mt5.symbol_info_tick(symbol)._asdict()
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, dataframe, 0, 600))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s',utc=True)
    ohlcs = []
    orders = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs.append(ohlc)
    positions=mt5.positions_get()
    # print(positions)

    if positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s',utc=True)
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        # print(df)
        
        for i, data in df.iterrows():
           
            _data = {
                'symbol':data['symbol'],
                'lot':data['volume'] ,
                'profit':data['profit'],
                'position':data['ticket'],
                'type':data['type'],
                'comment':data['comment'],
            }
            orders.append(_data)
        # print(orders)

    data = {
        'orders':orders,
        'symbol':symbol,
        'series':ohlcs, 
        'searchreports': serializers.serialize('json', SearchReport.objects.all().order_by('-id')[:30]),
        'price': 
        {
            'ask':symbol_price['ask'],
            'bid':symbol_price['bid'],
            'timeframe':timeframe
        }
    }
    
    return JsonResponse(data)

def getSymbolData(request):
    setting = Setting.objects.first()
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    currentview = CurrentView.objects.first()
    currentview.symbol_id = request.POST['selectedSymbol']
    currentview.timeframe_id = request.POST['selectedTimeframe']
    currentview.save()

    currentview = CurrentView.objects.first()
    tf = TimeFrame.objects.get(id = currentview.timeframe_id)
    timeframe = tf.name
    dataframe = getattr(mt5, f'TIMEFRAME_{timeframe}')
    _symbol = Symbol.objects.get(id = currentview.symbol_id)
    symbol = _symbol.name

    symbol_price = mt5.symbol_info_tick(symbol)._asdict()
    
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, dataframe, 0, 500))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s',utc=True)
    ohlcs = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs.append(ohlc)

    data = {
        'symbol':symbol,
        'series':ohlcs, 
        'price': 
        {
            'ask':symbol_price['ask'],
            'bid':symbol_price['bid'],
            'timeframe':timeframe
        }
    }

    data = dumps(data)

    return redirect('/',{
        'resData': data,
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id),
        'timeframes':TimeFrame.objects.all()
    })
def lineNotification(request):

    # message = 'ทดสอบ'
    payload = {
        'message':request.POST['message']
    }
  
    url = 'https://notify-api.line.me/api/notify'
    token = 'p59HvOJlVFphWeUtCUmWTfyI5vLbWEUJoHiJXLgdELM'
    headers = {'Authorization':'Bearer '+token}
    result = requests.post(url, headers=headers , data = payload, files=None)    
    data = {
        'data':'nothing',
    }
    return JsonResponse(data)


# def _lineNotify(payload,file=None):
#     url = 'https://notify-api.line.me/api/notify'
#     token = 'p59HvOJlVFphWeUtCUmWTfyI5vLbWEUJoHiJXLgdELM'
#     headers = {'Authorization':'Bearer '+token}
#     result = requests.post(url, headers=headers , data = payload, files=file)    
#     return HttpRequest(None)

def backtest(request):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    # mt5.login(login,password,server)

    accountinfo = mt5.account_info()
    # print(account_info)

    backtest = BackTest.objects.last()
   

    backtestintervals = BackTestInterval.objects.all()
    

    return render(request,'backtest.html',{
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        'specs' : serializers.serialize('json', Spec.objects.all()), 
        'backtestintervals':backtestintervals,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'setting' : Setting.objects.first(),
        'backtestjobs' : BackTest.objects.all().order_by("-id"),
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1), 
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1)), 
        'searchtype': serializers.serialize('json', SearchType.objects.all()),
    })

def backtesting(request):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    # mt5.login(login,password,server)

    accountinfo = mt5.account_info()
    # print(account_info)

    backtest = BackTest.objects.last()
   
    backtestintervals = BackTestInterval.objects.all()
    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    # ids = StdBarSize.objects.filter(value = 1000).values('symbol_id').distinct()

    return render(request,'backtest.html',{
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = ids).order_by('name'),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        'specs' : serializers.serialize('json', Spec.objects.all()), 
        'backtestintervals':backtestintervals,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'setting' : Setting.objects.first(),
        'backtestjobs' : BackTest.objects.all().order_by("-id"),
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1), 
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1)), 
        'searchtype': serializers.serialize('json', SearchType.objects.all()),
    })


def createbacktest(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()


    btsize = BackTestSize.objects.filter(id = int(request.POST.get('size'))).first().size + 250

    backtestsymbol = request.POST.get('backtestsymbol')

    tf = TimeFrame.objects.get(id = request.POST.get('timeframe'))
    backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf.name}')

    symbol = Symbol.objects.filter(id = backtestsymbol).first()

    newBackTest = BackTest(symbol_id= backtestsymbol,timeframename= tf.name,symbolname= symbol.name,code= datetime.now(tz=timezone.utc).strftime("%Y-%m-%d-%H-%M-%S"),backtestsize_id= request.POST.get('size'),timeframe_id= request.POST.get('timeframe'), interval_id=request.POST.get('interval'))
    newBackTest.save()

    backtestid = newBackTest.id 
    backtest_symbol = Symbol.objects.filter(id=backtestsymbol).first()



    # print(getbacktestohlcdata(backtest_symbol.name,tf.name))



    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(backtest_symbol.name, backtestdataframe, 0, btsize))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s',utc=True)

    bulk_list = list()
    for j, data in getbacktestohlcdata(backtest_symbol.name,tf.name).tail(btsize).iterrows():
        bulk_list.append(
            BackTestOHLC(backtest_id=newBackTest.id,symbol_id=backtestsymbol,date=data['time'], open=data['open'], high=data['high'], low=data['low'], close=data['close'], tick=data['tick_volume']))
    BackTestOHLC.objects.bulk_create(bulk_list)   

    addBackTestOHLCTimeframe(btsize,newBackTest.id,backtestsymbol,backtest_symbol.name)
    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = backtestid)),
        'backtestjobs' : serializers.serialize('json', BackTest.objects.all().order_by("-id")), 
    }

    return JsonResponse(data)


def getbacktestohlcdata(symbol,tf):
    symbol_info_tick_dict = mt5.symbol_info_tick(symbol)
    dt_object = datetime.fromtimestamp(symbol_info_tick_dict.time, tz=pytz.timezone("UTC"))
    # print('present date')
    # print(dt_object)

    hour  = timedelta(hours=1)
    initial_datetime = datetime(dt_object.year, dt_object.month, dt_object.day, dt_object.hour, dt_object.minute, 0)
    formatted_date = initial_datetime - hour 
    # print('minute 4 hour')
    # print(formatted_date)

    stdate = str(formatted_date.year) + '-' + str(formatted_date.month).zfill(2) + "-"+ str(formatted_date.day).zfill(2) +"T" + str(formatted_date.hour).zfill(2) + ":"+str(formatted_date.minute).zfill(2)+":00Z"

    # print(stdate)


    # stdate = str(dt_object.year) + '-' + str(dt_object.month).zfill(2) + "-"+ str(dt_object.day).zfill(2) +"T00:00:00Z"
    to_datetime = datetime.strptime(stdate.strip().replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
   
    if tf == 'M1':
        timeframe = 5

    elif tf == 'M5':
        timeframe = 25

    elif tf == 'M15':
        timeframe = 100

    elif tf == 'M30':
        timeframe = 200

    elif tf == 'H1':
        timeframe = 390

    elif tf == 'H4':
        timeframe = 1600
    
    elif tf == 'D1':
        timeframe = 10000   

    
    minute = int(to_datetime.minute/timeframe)*timeframe

    initial_datetime = datetime(to_datetime.year, to_datetime.month, to_datetime.day, to_datetime.hour, minute, 0)
    total_minutes = timedelta(minutes=timeframe * 200)
    from_datetime = initial_datetime - total_minutes 

    utc_from = datetime(from_datetime.year, from_datetime.month, from_datetime.day,from_datetime.hour,minute, tzinfo=pytz.timezone("UTC"))
    utc_to = datetime(to_datetime.year, to_datetime.month, to_datetime.day,to_datetime.hour,to_datetime.minute, tzinfo=pytz.timezone("UTC"))
    dframe = getattr(mt5, f'TIMEFRAME_{tf}')
    rates = mt5.copy_rates_range(symbol, dframe, utc_from, utc_to)

    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s',utc=True)
    return rates_frame


def getbacktestohlch4(symbol,num):
    symbol_info_tick_dict = mt5.symbol_info_tick(symbol)
    dt_object = datetime.fromtimestamp(symbol_info_tick_dict.time, tz=pytz.timezone("UTC"))
    # print('present date')
    # print(dt_object)

    hour  = timedelta(hours=4)
    initial_datetime = datetime(dt_object.year, dt_object.month, dt_object.day, dt_object.hour, dt_object.minute, 0)
    formatted_date = initial_datetime - hour 
    # print('minute 4 hour')
    # print(formatted_date)

    stdate = str(formatted_date.year) + '-' + str(formatted_date.month).zfill(2) + "-"+ str(formatted_date.day).zfill(2) +"T" + str(formatted_date.hour).zfill(2) + ":"+str(formatted_date.minute).zfill(2)+":00Z"

    # print(stdate)

    to_datetime = datetime.strptime(stdate.strip().replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
    numofbar = num
    timeframe = 240
    minute = int(to_datetime.minute/timeframe)*timeframe

    initial_datetime = datetime(to_datetime.year, to_datetime.month, to_datetime.day, to_datetime.hour, minute, 0)
    total_minutes = timedelta(minutes=timeframe * numofbar)
    from_datetime = initial_datetime - total_minutes 

    utc_from = datetime(from_datetime.year, from_datetime.month, from_datetime.day,from_datetime.hour,minute, tzinfo=pytz.timezone("UTC"))
    utc_to = datetime(to_datetime.year, to_datetime.month, to_datetime.day,to_datetime.hour,to_datetime.minute, tzinfo=pytz.timezone("UTC"))

    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H4, utc_from, utc_to)

    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s',utc=True)
    return rates_frame   


def addBackTestOHLCTimeframe(btsize,backtest_id,symbolid,symbol):
    bulk_list = list()
    timeframes = ["M1","M5", "M15", "M30", "H1", "H4", "D1"]
    _timeframe_offset = [3,3, 2, 1, 1, 1, 1]
    for idx, tf in enumerate(timeframes):
        # backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf}')
        
        # ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, backtestdataframe, 0, btsize*_timeframe_offset[idx]))
        # ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s',utc=True)
        
        for j, data in getbacktestohlcdata(symbol,tf).tail(btsize).iterrows():
            bulk_list.append(
                BackTestOHLCTimeframe(backtest_id=backtest_id,timeframe_id=(idx+1),timeframename=tf,symbol_id=symbolid,date=data['time'], open=data['open'], high=data['high'], low=data['low'], close=data['close'], tick=data['tick_volume']))

    BackTestOHLCTimeframe.objects.bulk_create(bulk_list)   
    return

def deleteallbacktest(request):
    BackTest.objects.all().delete()
    data = {
        'backtestjobs' :  serializers.serialize('json', BackTest.objects.all().order_by("-id")), 
    }
    return JsonResponse(data)

def deletebacktest(request):
    BackTest.objects.filter(id = request.POST.get('id')).delete()
    data = {
        'backtestjobs' :  serializers.serialize('json', BackTest.objects.all().order_by("-id")), 
    }
    return JsonResponse(data)

def getbacktestjob(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()

    id = request.POST.get('id')
    symbolid = request.POST.get('symbol_id')
    symbol = Symbol.objects.filter(id = symbolid).first()
    symbol_info=mt5.symbol_info(symbol.name)

    fullstring = "StackAbuse"
    usdbase = 1

    if symbol.name.find('USD') == -1:
        usbasesymbol = symbol.name[0:3] + 'USD'
        _sb = mt5.symbol_info_tick(usbasesymbol)
        if _sb != None:
            usdbase = _sb.ask

    calculationInfo ={
        'symbol': symbol_info.name,
        'bid' : symbol_info.bid,
        'ask' : symbol_info.ask,
        'degit' : symbol_info.digits,
        'spread' : symbol_info.spread,
        'trade_contract_size' : symbol_info.trade_contract_size,
        'balance' : accountinfo.balance,
        'pipdistant' : symbol.pipdistant,
    }

    barsize = {
        'barsize': StdBarSize.objects.filter(symbol_id = symbolid, timeframe = request.POST.get('timeframe')).first().value,
    }
    lotsizefactor = {
        'factor': LotSizeFactor.objects.filter(timeframename = request.POST.get('timeframe')).first().factor,
    }
    # print(LotSizeFactor.objects.filter(timeframename = request.POST.get('timeframe')).first().factor)
    ids = StdBarSize.objects.all().values('symbol_id').distinct()


    isMarketClose = 0    
    if datetime.today().strftime('%A') == 'Saturday' or datetime.today().strftime('%A') == 'Sunday':
        isMarketClose = 1
    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = id)),
        'symbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = ids).order_by('name')),
        'timeframes': serializers.serialize('json', TimeFrame.objects.all()),
        'intervals': serializers.serialize('json', BackTestInterval.objects.all()),
        'backtestsizes': serializers.serialize('json', BackTestSize.objects.all()),
        'ohlcs': serializers.serialize('json', BackTestOHLC.objects.filter(backtest_id = id)),
        'ohlctimeframes': serializers.serialize('json', BackTestOHLCTimeframe.objects.filter(backtest_id = id)),
        'entryspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =1)),
        'exitspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =2)),
        'barsize' : serializers.serialize('json', StdBarSize.objects.filter(symbol_id = symbolid, timeframe = request.POST.get('timeframe'))),
        'barsizes' : serializers.serialize('json', StdBarSize.objects.filter(symbol_id = symbolid)),
        'lotsizefactor' : lotsizefactor,
        'usdbase' : usdbase,
        'setting' : serializers.serialize('json', Setting.objects.all()),
        'calculationInfo' : calculationInfo,
        'isMarketClose': isMarketClose
    }
    return JsonResponse(data)    

def jogtest(request):
    id = request.POST.get('id')
    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = id)),
        
    }
    return JsonResponse(data)

def symbolsetting(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    return render(request,'symbol.html',{
        'symbols':Symbol.objects.filter(broker_id=myaccount.broker_id),
    }) 

def changesymbolstatus(request):
    id = request.POST.get('id')
    symbol = Symbol.objects.filter(id = id).first()
    symbol.status = request.POST['status']
    symbol.save()
    data = {
        'backtest': serializers.serialize('json', Symbol.objects.filter(id = id)),
    }
    return JsonResponse(data)

def spec(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    
    # print(accountinfo)

    # ids = Spec.objects.all().values_list('symbol_id', flat=True).distinct('symbol_id')
    ids = Spec.objects.all().values('symbol_id').distinct()
    # print(ids)
    # print(Symbol.objects.filter(id__in = ids))

    return render(request,'spec.html',{
        'accountinfo' : accountinfo,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'symbols':Symbol.objects.filter(id__in = ids,status=1),
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1), 
        'exitspecobjects' : Spec.objects.filter(spec_type = 2), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2)), 
    })  


def changespecusage(request):
    id = request.POST.get('id')
    symbolid = request.POST.get('symbol')
    spec = Spec.objects.filter(id = id,symbol_id=symbolid).first()
    spec.status = request.POST['status']
    spec.save()
    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1, status=1)),
    }
    return JsonResponse(data)

def changespecentrypointvalue(request):
    id = request.POST.get('id')
    symbolid = request.POST.get('symbol')
    val = request.POST['value'];
    # print(val)
    spec = Spec.objects.filter(id = id,symbol_id=symbolid).first()
   
    if spec.parameter_type == 'equal':
       if spec.exit_value ==  val:
          spec.exit_value = spec.entry_value

    spec.entry_value = request.POST['value']
    spec.save()

    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1, status=1)),
    }
    return JsonResponse(data)

def clonespec(request):
    symbolid = request.POST.get('id')
    Spec.objects.filter(~Q(symbol_id=symbolid)).delete()
    basespec = Spec.objects.filter(symbol_id=symbolid)


    symbols = Symbol.objects.filter(~Q(id=symbolid))
    # print(symbols)

    for symbol in symbols.iterator():
        for base in basespec.iterator():
            # print(base.name)
            newspec = Spec(
                    name= base.name,
                    parameter= base.parameter,
                    entry_value= base.entry_value,
                    exit_value= base.exit_value,
                    parameter_type= base.parameter_type,
                    compare_reverse= base.compare_reverse,
                    status= base.status,
                    spec_type= base.spec_type,
                    order_type= base.order_type,
                    symbol_id = symbol.id
                )
            newspec.save()

    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1, symbol_id=symbolid, status=1)),
    }
    return JsonResponse(data)

def getentryspec(request):
    symbolid = request.POST.get('id')
    data = {
        'spec': serializers.serialize('json', Spec.objects.filter(spec_type = 1, symbol_id=symbolid)),
    }
    return JsonResponse(data)

def setting(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    stdbalance= accountinfo.balance/2500
    lotinfo = {
        'balance': accountinfo.balance,
        'lotsize': "{:.2f}".format(stdbalance),
        'gbpcloseprice': "{:.2f}".format(stdbalance*100),
        'nonegbpcloseprice': "{:.2f}".format(stdbalance*75),
    }
    return render(request,'setting.html',{
        'setting': setting,
        'accountinfo': accountinfo,
        'lotinfo': lotinfo,
    })  

def search(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    

    backtest = BackTest.objects.last()
   
    backtestintervals = BackTestInterval.objects.all()
    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    # ids = StdBarSize.objects.filter(value = 1000).values('symbol_id').distinct()
    positions=mt5.positions_get()
    positionsymbol = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            print(position.symbol)
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  

    greenOrred = []
    searchs = Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = ids).exclude(id__in = positionsymbol) 
    
    for search in searchs:
        allred = True
        allgreen = True
        _ohlcs_m1 = []
        m1_data = pd.DataFrame(mt5.copy_rates_from_pos(search.name, mt5.TIMEFRAME_M1, 0, 70))
        m1_data['time']=pd.to_datetime(m1_data['time'], unit='s',utc=True)
        for i, data in m1_data.iterrows():
            ohlc = {
                'open':float(data['open']) ,
                'high':float(data['high']),
                'low':float(data['low']) ,
                'close':float(data['close']), 
            }
            _ohlcs_m1.append(ohlc)

        ohlcs_m1_arr = _ohlcs_m1[-1:][0]

      
        m1from_m1_data = {
            'open':ohlcs_m1_arr['open'],
            'high':ohlcs_m1_arr['high'],
            'low':ohlcs_m1_arr['low'],
            'close':ohlcs_m1_arr['close'], 
        }    

        if float(m1from_m1_data['close']) > float(m1from_m1_data['open']) :
            allred = False
        else:
            allgreen = False


        ohlcs_m5_arr = _ohlcs_m1[-5:]
        max_high_ohlcs_m5 = 0
        for i in ohlcs_m5_arr:
            if i['high'] > max_high_ohlcs_m5:
                max_high_ohlcs_m5 = i['high']
                
        min_low_ohlcs_m5 = max_high_ohlcs_m5        
        for i in ohlcs_m5_arr:
            if i['low'] < min_low_ohlcs_m5:
                min_low_ohlcs_m5 = i['low']

        open_ohlcs_m5 = ohlcs_m5_arr[0]['open']
        close_ohlcs_m5 = ohlcs_m5_arr[len(ohlcs_m5_arr)-1]['close']

        m5from_m1_data = {
            'open':open_ohlcs_m5,
            'high':max_high_ohlcs_m5,
            'low':min_low_ohlcs_m5,
            'close':close_ohlcs_m5, 
        }

        if float(m5from_m1_data['close']) > float(m5from_m1_data['open']) :
            allred = False
        else:
            allgreen = False


        ohlcs_m15_arr = _ohlcs_m1[-15:]
        max_high_ohlcs_m15 = 0
        for i in ohlcs_m15_arr:
            if i['high'] > max_high_ohlcs_m15:
                max_high_ohlcs_m15 = i['high']
                
        min_low_ohlcs_m15 = max_high_ohlcs_m15        
        for i in ohlcs_m15_arr:
            if i['low'] < min_low_ohlcs_m15:
                min_low_ohlcs_m15 = i['low']

        open_ohlcs_m15 = ohlcs_m15_arr[0]['open']
        close_ohlcs_m15 = ohlcs_m15_arr[len(ohlcs_m15_arr)-1]['close']

        m15from_m1_data = {
            'open':open_ohlcs_m15,
            'high':max_high_ohlcs_m15,
            'low':min_low_ohlcs_m15,
            'close':close_ohlcs_m15, 
        }

        if float(m15from_m1_data['close']) > float(m15from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m30_arr = _ohlcs_m1[-30:]
        max_high_ohlcs_m30 = 0
        for i in ohlcs_m30_arr:
            if i['high'] > max_high_ohlcs_m30:
                max_high_ohlcs_m30 = i['high']
                
        min_low_ohlcs_m30 = max_high_ohlcs_m30        
        for i in ohlcs_m30_arr:
            if i['low'] < min_low_ohlcs_m30:
                min_low_ohlcs_m30 = i['low']

        open_ohlcs_m30 = ohlcs_m30_arr[0]['open']
        close_ohlcs_m30 = ohlcs_m30_arr[len(ohlcs_m30_arr)-1]['close']

        m30from_m1_data = {
            'open':open_ohlcs_m30,
            'high':max_high_ohlcs_m30,
            'low':min_low_ohlcs_m30,
            'close':close_ohlcs_m30, 
        }

        if float(m30from_m1_data['close']) > float(m30from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        if allred == True or allgreen == True:
            # m5_body = abs(m5from_m1_data['open'] - m5from_m1_data['close'])
            # std_m5_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M5').first().value
            # m5_percent = ((std_m5_barsize - m5_body)/m5_body)*100

            # m15_body = abs(m15from_m1_data['open'] - m15from_m1_data['close'])
            # std_m15_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M15').first().value
            # m15_percent = ((std_m15_barsize - m15_body)/m15_body)*100
            
            # if m5_percent < 0 and m15_percent < 0 :
            greenOrred.append(search.id)

    # print(greenOrred)
    isMarketClose = 0    
    if datetime.today().strftime('%A') == 'Saturday' or datetime.today().strftime('%A') == 'Sunday':
        isMarketClose = 1
    return render(request,'search.html',{
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = greenOrred).order_by('name'),
        # 'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id).order_by('name'),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        'specs' : serializers.serialize('json', Spec.objects.all()), 
        'backtestintervals':backtestintervals,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'setting' : Setting.objects.first(),
        'backtestjobs' : BackTest.objects.all().order_by("-id"),
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1), 
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1)), 
        'searchtype': serializers.serialize('json', SearchType.objects.all()),
        'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = greenOrred) ),
        # 'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id) ),
        'isMarketClose' : isMarketClose
    })

def searchSymbol(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    isMarketClose = 0    
    if datetime.today().strftime('%A') == 'Saturday' or datetime.today().strftime('%A') == 'Sunday':
        isMarketClose = 1
    symbol = 'USDJPY'
    check = Symbol.objects.filter(name=request.GET.get('symbol'))   
    if(len(check) !=0):
        symbol = request.GET.get('symbol','')
    return render(request,'search_gbpusd.html',{
        'isMarketClose' : isMarketClose,
        'symbol' : symbol
    })

def orders(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    

    backtest = BackTest.objects.last()
   
    backtestintervals = BackTestInterval.objects.all()
    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    # ids = StdBarSize.objects.filter(value = 1000).values('symbol_id').distinct()
    positions=mt5.positions_get()
    positionsymbol = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            # print(position.symbol)
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  

    return render(request,'orders.html',{
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = positionsymbol).order_by('name'),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        'specs' : serializers.serialize('json', Spec.objects.all()), 
        'backtestintervals':backtestintervals,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'setting' : Setting.objects.first(),
        'backtestjobs' : BackTest.objects.all().order_by("-id"),
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1), 
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1)), 
        'searchtype': serializers.serialize('json', SearchType.objects.all()),
        'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = positionsymbol)),
    })

def searchSingleOhlc(request):
    sb = request.POST.get('symbol')
    symbolid = 4
    check = Symbol.objects.filter(name=request.POST.get('symbol'))
    # print(len(check))
    if(sb != '' and len(check) != 0):
         symbolid = Symbol.objects.filter(name=request.POST.get('symbol')).first().id
     
    timeframeid = TimeFrame.objects.filter(name=request.POST.get('timeframe')).first().id

    return JsonResponse(getNewsingleohlc(symbolid,timeframeid))

def getNewsingleohlc(symbolid,timeframeid):
    # timeframeid = 1
    # symbolid = 4

    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()

    _symbol = Symbol.objects.filter(id = symbolid).first()
    _timeframe = TimeFrame.objects.filter(id = timeframeid).first()

    ohlcs_m1 = []
    ohlcs_m5 = []
    ohlcs_m15 = []
    ohlcs_m30 = []
    ohlcs_h1 = []
    ohlcs_h4 = []
    # ohlcs_d1 = []

    ohlc_data_m1 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M1, 0, 450))
    ohlc_data_m1['time']=pd.to_datetime(ohlc_data_m1['time'], unit='s',utc=True)
    for i, data in ohlc_data_m1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m1.append(ohlc)

    ohlc_data_m5 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M5, 0, 450))
    ohlc_data_m5['time']=pd.to_datetime(ohlc_data_m5['time'], unit='s',utc=True)
    for i, data in ohlc_data_m5.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m5.append(ohlc)


    ohlc_data_m15 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M15, 0, 450))
    ohlc_data_m15['time']=pd.to_datetime(ohlc_data_m15['time'], unit='s',utc=True)
    for i, data in ohlc_data_m15.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m15.append(ohlc)

    ohlc_data_m30 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M30, 0, 450))
    ohlc_data_m30['time']=pd.to_datetime(ohlc_data_m30['time'], unit='s',utc=True)
    for i, data in ohlc_data_m30.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m30.append(ohlc)

    ohlc_data_h1 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_H1, 0, 450))
    ohlc_data_h1['time']=pd.to_datetime(ohlc_data_h1['time'], unit='s',utc=True)
    for i, data in ohlc_data_h1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_h1.append(ohlc)

    ohlc_data_h4 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_H4, 0, 450))
    ohlc_data_h4['time']=pd.to_datetime(ohlc_data_h4['time'], unit='s',utc=True)
    for i, data in ohlc_data_h4.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_h4.append(ohlc)    

    symbol_info=mt5.symbol_info(_symbol.name)

    usdbase = 1

    if symbol_info.name.find('USD') == -1:
        usbasesymbol = symbol_info.name[0:3] + 'USD'
        _sb = mt5.symbol_info_tick(usbasesymbol)
        if _sb != None:
            usdbase = _sb.ask

    calculationInfo ={
        'symbol': symbol_info.name,
        'bid' : symbol_info.bid,
        'ask' : symbol_info.ask,
        'degit' : symbol_info.digits,
        'spread' : symbol_info.spread,
        'trade_contract_size' : symbol_info.trade_contract_size,
        'balance' : accountinfo.balance,
    }

    isMarketClose = 0    
    if datetime.today().strftime('%A') == 'Saturday' or datetime.today().strftime('%A') == 'Sunday':
        isMarketClose = 1

    stdbarsize = [
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M1').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M5').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M15').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M30').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'H1').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'H4').first().value,
    ]

    data = {
        'ohlcs_m1':ohlcs_m1,
        'ohlcs_m5':ohlcs_m5,
        'ohlcs_m15':ohlcs_m15,
        'ohlcs_m30':ohlcs_m30,
        'ohlcs_h1':ohlcs_h1,
        'ohlcs_h4':ohlcs_h4,
        'calculationInfo' : calculationInfo,
        'isMarketClose' : isMarketClose,
        'stdbarsize' : stdbarsize
    }
      
    return data 

def getsingleohlc(request):   
    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()

    timeframeid = request.POST.get('timeframe')
    symbolid = request.POST.get('symbol')

    _symbol = Symbol.objects.filter(id = symbolid).first()
    _timeframe = TimeFrame.objects.filter(id = timeframeid).first()
    # dataframe = getattr(mt5, f'TIMEFRAME_{_timeframe.name}')

    ohlcs_m1 = []
    ohlcs_m5 = []
    ohlcs_m15 = []
    ohlcs_m30 = []
    ohlcs_h1 = []
    # ohlcs_h4 = []
    # ohlcs_d1 = []

    ohlc_data_m1 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M1, 0, 450))
    ohlc_data_m1['time']=pd.to_datetime(ohlc_data_m1['time'], unit='s',utc=True)
    for i, data in ohlc_data_m1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m1.append(ohlc)

    ohlc_data_m5 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M5, 0, 450))
    ohlc_data_m5['time']=pd.to_datetime(ohlc_data_m5['time'], unit='s',utc=True)
    for i, data in ohlc_data_m5.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m5.append(ohlc)


    ohlc_data_m15 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M15, 0, 450))
    ohlc_data_m15['time']=pd.to_datetime(ohlc_data_m15['time'], unit='s',utc=True)
    for i, data in ohlc_data_m15.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m15.append(ohlc)

    ohlc_data_m30 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M30, 0, 2))
    ohlc_data_m30['time']=pd.to_datetime(ohlc_data_m30['time'], unit='s',utc=True)
    for i, data in ohlc_data_m30.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m30.append(ohlc)

    ohlc_data_h1 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_H1, 0, 2))
    ohlc_data_h1['time']=pd.to_datetime(ohlc_data_h1['time'], unit='s',utc=True)
    for i, data in ohlc_data_h1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_h1.append(ohlc)
      
    ohlctimeframe = []
    ohlctimeframe = [
        
        {'h1': ohlcs_h1[len(ohlcs_h1)-1]},
        {'m30': ohlcs_m30[len(ohlcs_m30)-1]},
        {'m15': ohlcs_m15[len(ohlcs_m15)-1]},          
        {'m5': ohlcs_m5[len(ohlcs_m5)-1]},     
        {'m1': ohlcs_m1[len(ohlcs_m1)-1]},     
    ]
  
    m1barsize = [
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M1').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M5').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M15').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M30').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'H1').first().value,
        # StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'H4').first().value,
    ]

    symbol_info=mt5.symbol_info(_symbol.name)

    usdbase = 1

    if symbol_info.name.find('USD') == -1:
        usbasesymbol = symbol_info.name[0:3] + 'USD'
        _sb = mt5.symbol_info_tick(usbasesymbol)
        if _sb != None:
            usdbase = _sb.ask

    calculationInfo ={
        'symbol': symbol_info.name,
        'bid' : symbol_info.bid,
        'ask' : symbol_info.ask,
        'degit' : symbol_info.digits,
        'spread' : symbol_info.spread,
        'trade_contract_size' : symbol_info.trade_contract_size,
        'balance' : accountinfo.balance,
    }

    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    positions=mt5.positions_get()
    positionsymbol = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            # print('position')
            # print(position.symbol)
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  
    # print(positionsymbol)
    greenOrred = []
    searchs = Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = ids).exclude(id__in = positionsymbol) 
    
    for search in searchs:
        allred = True
        allgreen = True
        _ohlcs_m1 = []
        m1_data = pd.DataFrame(mt5.copy_rates_from_pos(search.name, mt5.TIMEFRAME_M1, 0, 70))
        m1_data['time']=pd.to_datetime(m1_data['time'], unit='s',utc=True)
        for i, data in m1_data.iterrows():
            ohlc = {
                'open':float(data['open']) ,
                'high':float(data['high']),
                'low':float(data['low']) ,
                'close':float(data['close']), 
            }
            _ohlcs_m1.append(ohlc)

        ohlcs_m1_arr = _ohlcs_m1[-1:][0]

      
        m1from_m1_data = {
            'open':ohlcs_m1_arr['open'],
            'high':ohlcs_m1_arr['high'],
            'low':ohlcs_m1_arr['low'],
            'close':ohlcs_m1_arr['close'], 
        }    

        if float(m1from_m1_data['close']) > float(m1from_m1_data['open']) :
            allred = False
        else:
            allgreen = False



        ohlcs_m5_arr = _ohlcs_m1[-5:]
        max_high_ohlcs_m5 = 0
        for i in ohlcs_m5_arr:
            if i['high'] > max_high_ohlcs_m5:
                max_high_ohlcs_m5 = i['high']
                
        min_low_ohlcs_m5 = max_high_ohlcs_m5        
        for i in ohlcs_m5_arr:
            if i['low'] < min_low_ohlcs_m5:
                min_low_ohlcs_m5 = i['low']

        open_ohlcs_m5 = ohlcs_m5_arr[0]['open']
        close_ohlcs_m5 = ohlcs_m5_arr[len(ohlcs_m5_arr)-1]['close']

        m5from_m1_data = {
            'open':open_ohlcs_m5,
            'high':max_high_ohlcs_m5,
            'low':min_low_ohlcs_m5,
            'close':close_ohlcs_m5, 
        }

        if float(m5from_m1_data['close']) > float(m5from_m1_data['open']) :
            allred = False
        else:
            allgreen = False


        ohlcs_m15_arr = _ohlcs_m1[-15:]
        max_high_ohlcs_m15 = 0
        for i in ohlcs_m15_arr:
            if i['high'] > max_high_ohlcs_m15:
                max_high_ohlcs_m15 = i['high']
                
        min_low_ohlcs_m15 = max_high_ohlcs_m15        
        for i in ohlcs_m15_arr:
            if i['low'] < min_low_ohlcs_m15:
                min_low_ohlcs_m15 = i['low']

        open_ohlcs_m15 = ohlcs_m15_arr[0]['open']
        close_ohlcs_m15 = ohlcs_m15_arr[len(ohlcs_m15_arr)-1]['close']

        m15from_m1_data = {
            'open':open_ohlcs_m15,
            'high':max_high_ohlcs_m15,
            'low':min_low_ohlcs_m15,
            'close':close_ohlcs_m15, 
        }

        if float(m15from_m1_data['close']) > float(m15from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m30_arr = _ohlcs_m1[-30:]
        max_high_ohlcs_m30 = 0
        for i in ohlcs_m30_arr:
            if i['high'] > max_high_ohlcs_m30:
                max_high_ohlcs_m30 = i['high']
                
        min_low_ohlcs_m30 = max_high_ohlcs_m30        
        for i in ohlcs_m30_arr:
            if i['low'] < min_low_ohlcs_m30:
                min_low_ohlcs_m30 = i['low']

        open_ohlcs_m30 = ohlcs_m30_arr[0]['open']
        close_ohlcs_m30 = ohlcs_m30_arr[len(ohlcs_m30_arr)-1]['close']

        m30from_m1_data = {
            'open':open_ohlcs_m30,
            'high':max_high_ohlcs_m30,
            'low':min_low_ohlcs_m30,
            'close':close_ohlcs_m30, 
        }

        if float(m30from_m1_data['close']) > float(m30from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        if allred == True or allgreen == True:
            
            # m5_body = abs(m5from_m1_data['open'] - m5from_m1_data['close'])
            
            # std_m5_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M5').first().value
            # m5_percent = ((std_m5_barsize - m5_body)/m5_body)*100

            # print(m5_body)
            # print('--------------')
            # m15_body = abs(m15from_m1_data['open'] - m15from_m1_data['close'])
            # std_m15_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M15').first().value
            # m15_percent = ((std_m15_barsize - m15_body)/m15_body)*100
            
            # if m5_body > std_m5_barsize :
            greenOrred.append(search.id)

    
    # print(greenOrred)
    isMarketClose = 0    
    if datetime.today().strftime('%A') == 'Saturday' or datetime.today().strftime('%A') == 'Sunday':
        isMarketClose = 1

    data = {
        'symbol':_symbol.name,
        'timeframe':_timeframe.name,
        'm1barsize' : m1barsize,
        'ohlc':ohlcs_m1, 
        'ohlctimeframe':ohlctimeframe, 
        'entryspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =1)),
        'exitspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =2)),
        'calculationInfo': calculationInfo,
        'usdbase': usdbase,
        'barsize' : serializers.serialize('json', StdBarSize.objects.filter(symbol_id = symbolid, timeframe = 'M1')),
        'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = greenOrred)),
        # 'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id)),
        'isMarketClose' : isMarketClose
    }

    return JsonResponse(data)

def getapisymbols(request): 
    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    positions=mt5.positions_get()
    positionsymbol = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            # print('position')
            # print(position.symbol)
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  
    # print(positionsymbol)
    greenOrred = []
    searchs = Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = ids).exclude(id__in = positionsymbol) 

    for search in searchs:
        allred = True
        allgreen = True
        _ohlcs_m1 = []
        m1_data = pd.DataFrame(mt5.copy_rates_from_pos(search.name, mt5.TIMEFRAME_M1, 0, 70))
        m1_data['time']=pd.to_datetime(m1_data['time'], unit='s',utc=True)
        for i, data in m1_data.iterrows():
            ohlc = {
                'open':float(data['open']) ,
                'high':float(data['high']),
                'low':float(data['low']) ,
                'close':float(data['close']), 
            }
            _ohlcs_m1.append(ohlc)

        ohlcs_m1_arr = _ohlcs_m1[-1:][0]

        m1from_m1_data = {
            'open':ohlcs_m1_arr['open'],
            'high':ohlcs_m1_arr['high'],
            'low':ohlcs_m1_arr['low'],
            'close':ohlcs_m1_arr['close'], 
        }    

        if float(m1from_m1_data['close']) > float(m1from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m5_arr = _ohlcs_m1[-5:]
        max_high_ohlcs_m5 = 0
        for i in ohlcs_m5_arr:
            if i['high'] > max_high_ohlcs_m5:
                max_high_ohlcs_m5 = i['high']
                
        min_low_ohlcs_m5 = max_high_ohlcs_m5        
        for i in ohlcs_m5_arr:
            if i['low'] < min_low_ohlcs_m5:
                min_low_ohlcs_m5 = i['low']

        open_ohlcs_m5 = ohlcs_m5_arr[0]['open']
        close_ohlcs_m5 = ohlcs_m5_arr[len(ohlcs_m5_arr)-1]['close']

        m5from_m1_data = {
            'open':open_ohlcs_m5,
            'high':max_high_ohlcs_m5,
            'low':min_low_ohlcs_m5,
            'close':close_ohlcs_m5, 
        }

        if float(m5from_m1_data['close']) > float(m5from_m1_data['open']) :
            allred = False
        else:
            allgreen = False


        ohlcs_m15_arr = _ohlcs_m1[-15:]
        max_high_ohlcs_m15 = 0
        for i in ohlcs_m15_arr:
            if i['high'] > max_high_ohlcs_m15:
                max_high_ohlcs_m15 = i['high']
                
        min_low_ohlcs_m15 = max_high_ohlcs_m15        
        for i in ohlcs_m15_arr:
            if i['low'] < min_low_ohlcs_m15:
                min_low_ohlcs_m15 = i['low']

        open_ohlcs_m15 = ohlcs_m15_arr[0]['open']
        close_ohlcs_m15 = ohlcs_m15_arr[len(ohlcs_m15_arr)-1]['close']

        m15from_m1_data = {
            'open':open_ohlcs_m15,
            'high':max_high_ohlcs_m15,
            'low':min_low_ohlcs_m15,
            'close':close_ohlcs_m15, 
        }

        if float(m15from_m1_data['close']) > float(m15from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m30_arr = _ohlcs_m1[-30:]
        max_high_ohlcs_m30 = 0
        for i in ohlcs_m30_arr:
            if i['high'] > max_high_ohlcs_m30:
                max_high_ohlcs_m30 = i['high']
                
        min_low_ohlcs_m30 = max_high_ohlcs_m30        
        for i in ohlcs_m30_arr:
            if i['low'] < min_low_ohlcs_m30:
                min_low_ohlcs_m30 = i['low']

        open_ohlcs_m30 = ohlcs_m30_arr[0]['open']
        close_ohlcs_m30 = ohlcs_m30_arr[len(ohlcs_m30_arr)-1]['close']

        m30from_m1_data = {
            'open':open_ohlcs_m30,
            'high':max_high_ohlcs_m30,
            'low':min_low_ohlcs_m30,
            'close':close_ohlcs_m30, 
        }

        if float(m30from_m1_data['close']) > float(m30from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        # if search.name == 'USDJPY':
        #     print('------------')
        #     print(open_ohlcs_m30)
        #     print(close_ohlcs_m30)
        #     print(min_low_ohlcs_m30)
        #     print(max_high_ohlcs_m30)

        # ohlcs_h1_arr = _ohlcs_m1[-60:]
        # max_high_ohlcs_h1 = 0
        # for i in ohlcs_h1_arr:
        #     if i['high'] > max_high_ohlcs_h1:
        #         max_high_ohlcs_h1 = i['high']
                
        # min_low_ohlcs_h1 = max_high_ohlcs_h1        
        # for i in ohlcs_h1_arr:
        #     if i['low'] < min_low_ohlcs_h1:
        #         min_low_ohlcs_h1 = i['low']

        # open_ohlcs_h1 = ohlcs_h1_arr[0]['open']
        # close_ohlcs_h1 = ohlcs_h1_arr[len(ohlcs_h1_arr)-1]['close']

        # h1from_m1_data = {
        #     'open':open_ohlcs_h1,
        #     'high':max_high_ohlcs_h1,
        #     'low':min_low_ohlcs_h1,
        #     'close':close_ohlcs_h1, 
        # }

        # if float(h1from_m1_data['close']) > float(h1from_m1_data['open']) :
        #     allred = False
        # else:
        #     allgreen = False

        if allred == True or allgreen == True:
            # m5_body = abs(m5from_m1_data['open'] - m5from_m1_data['close'])
            # std_m5_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M5').first().value
            # m5_percent = ((std_m5_barsize - m5_body)/m5_body)*100

            # m15_body = abs(m15from_m1_data['open'] - m15from_m1_data['close'])
            # std_m15_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M15').first().value
            # m15_percent = ((std_m15_barsize - m15_body)/m15_body)*100
            
            # if m5_percent < 0 and m15_percent < 0 :
            greenOrred.append(search.id)

    # print(greenOrred)
    data = {
        'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = greenOrred)),
        # 'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id)),
    }
    return JsonResponse(data)

def getorders(request):   
    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)
    accountinfo = mt5.account_info()

    timeframeid = request.POST.get('timeframe')
    symbolid = request.POST.get('symbol')

    # print(timeframeid)

    _symbol = Symbol.objects.filter(id = symbolid).first()
    _timeframe = TimeFrame.objects.filter(id = timeframeid).first()
    # dataframe = getattr(mt5, f'TIMEFRAME_{_timeframe.name}')

    ohlcs_m1 = []
    ohlcs_m5 = []
    ohlcs_m15 = []
    ohlcs_m30 = []
    ohlcs_h1 = []
    # ohlcs_h4 = []
    # ohlcs_d1 = []

    ohlc_data_m1 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M1, 0, 450))
    ohlc_data_m1['time']=pd.to_datetime(ohlc_data_m1['time'], unit='s',utc=True)
    for i, data in ohlc_data_m1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'],
            'high':data['high'],
            'low':data['low'],
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m1.append(ohlc)

    ohlc_data_m5 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M5, 0, 450))
    ohlc_data_m5['time']=pd.to_datetime(ohlc_data_m5['time'], unit='s',utc=True)
    for i, data in ohlc_data_m5.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'],
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m5.append(ohlc)

    ohlc_data_m15 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M15, 0, 450))
    ohlc_data_m15['time']=pd.to_datetime(ohlc_data_m15['time'], unit='s',utc=True)
    for i, data in ohlc_data_m15.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'],
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m15.append(ohlc)

    ohlc_data_m30 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_M30, 0, 2))
    ohlc_data_m30['time']=pd.to_datetime(ohlc_data_m30['time'], unit='s',utc=True)
    for i, data in ohlc_data_m30.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m30.append(ohlc)

    ohlc_data_h1 = pd.DataFrame(mt5.copy_rates_from_pos(_symbol.name, mt5.TIMEFRAME_H1, 0, 2))
    ohlc_data_h1['time']=pd.to_datetime(ohlc_data_h1['time'], unit='s',utc=True)
    for i, data in ohlc_data_h1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_h1.append(ohlc)

      
    ohlctimeframe = []
    ohlctimeframe = [
        
        # {'h4': ohlcs_h4[len(ohlcs_h4)-1]},
        {'h1': ohlcs_h1[len(ohlcs_h1)-1]},
        {'m30': ohlcs_m30[len(ohlcs_m30)-1]},
        {'m15': ohlcs_m15[len(ohlcs_m15)-1]},          
        {'m5': ohlcs_m5[len(ohlcs_m5)-1]},     
        {'m1': ohlcs_m1[len(ohlcs_m1)-1]},     
    ]

    m1barsize = [
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M1').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M5').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M15').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'M30').first().value,
        StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'H1').first().value,
        # StdBarSize.objects.filter(symbol_id = symbolid,timeframe = 'H4').first().value,
    ]

    symbol_info=mt5.symbol_info(_symbol.name)

    usdbase = 1

    if symbol_info.name.find('USD') == -1:
        usbasesymbol = symbol_info.name[0:3] + 'USD'
        _sb = mt5.symbol_info_tick(usbasesymbol)
        if _sb != None:
            usdbase = _sb.ask

    calculationInfo ={
        'symbol': symbol_info.name,
        'bid' : symbol_info.bid,
        'ask' : symbol_info.ask,
        'degit' : symbol_info.digits,
        'spread' : symbol_info.spread,
        'trade_contract_size' : symbol_info.trade_contract_size,
        'balance' : accountinfo.balance,
    }

    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    positions=mt5.positions_get()
    positionsymbol = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  

    greenOrred = []
    searchs = Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = positionsymbol)
    
    for search in searchs:
        allred = True
        allgreen = True
        _ohlcs_m1 = []
        m1_data = pd.DataFrame(mt5.copy_rates_from_pos(search.name, mt5.TIMEFRAME_M1, 0, 70))
        m1_data['time']=pd.to_datetime(m1_data['time'], unit='s',utc=True)
        for i, data in m1_data.iterrows():
            ohlc = {
                'open':float(data['open']) ,
                'high':float(data['high']),
                'low':float(data['low']) ,
                'close':float(data['close']), 
            }
            _ohlcs_m1.append(ohlc)

        ohlcs_m1_arr = _ohlcs_m1[-1:][0]

      
        m1from_m1_data = {
            'open':ohlcs_m1_arr['open'],
            'high':ohlcs_m1_arr['high'],
            'low':ohlcs_m1_arr['low'],
            'close':ohlcs_m1_arr['close'], 
        }    

        if float(m1from_m1_data['close']) > float(m1from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m5_arr = _ohlcs_m1[-5:]
        max_high_ohlcs_m5 = 0
        for i in ohlcs_m5_arr:
            if i['high'] > max_high_ohlcs_m5:
                max_high_ohlcs_m5 = i['high']
                
        min_low_ohlcs_m5 = max_high_ohlcs_m5        
        for i in ohlcs_m5_arr:
            if i['low'] < min_low_ohlcs_m5:
                min_low_ohlcs_m5 = i['low']

        open_ohlcs_m5 = ohlcs_m5_arr[0]['open']
        close_ohlcs_m5 = ohlcs_m5_arr[len(ohlcs_m5_arr)-1]['close']

        m5from_m1_data = {
            'open':open_ohlcs_m5,
            'high':max_high_ohlcs_m5,
            'low':min_low_ohlcs_m5,
            'close':close_ohlcs_m5, 
        }

        if float(m5from_m1_data['close']) > float(m5from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m15_arr = _ohlcs_m1[-15:]
        max_high_ohlcs_m15 = 0
        for i in ohlcs_m15_arr:
            if i['high'] > max_high_ohlcs_m15:
                max_high_ohlcs_m15 = i['high']
                
        min_low_ohlcs_m15 = max_high_ohlcs_m15        
        for i in ohlcs_m15_arr:
            if i['low'] < min_low_ohlcs_m15:
                min_low_ohlcs_m15 = i['low']

        open_ohlcs_m15 = ohlcs_m15_arr[0]['open']
        close_ohlcs_m15 = ohlcs_m15_arr[len(ohlcs_m15_arr)-1]['close']

        m15from_m1_data = {
            'open':open_ohlcs_m15,
            'high':max_high_ohlcs_m15,
            'low':min_low_ohlcs_m15,
            'close':close_ohlcs_m15, 
        }

        if float(m15from_m1_data['close']) > float(m15from_m1_data['open']) :
            allred = False
        else:
            allgreen = False

        ohlcs_m30_arr = _ohlcs_m1[-30:]
        max_high_ohlcs_m30 = 0
        for i in ohlcs_m30_arr:
            if i['high'] > max_high_ohlcs_m30:
                max_high_ohlcs_m30 = i['high']
                
        min_low_ohlcs_m30 = max_high_ohlcs_m30        
        for i in ohlcs_m30_arr:
            if i['low'] < min_low_ohlcs_m30:
                min_low_ohlcs_m30 = i['low']

        open_ohlcs_m30 = ohlcs_m30_arr[0]['open']
        close_ohlcs_m30 = ohlcs_m30_arr[len(ohlcs_m30_arr)-1]['close']

        m30from_m1_data = {
            'open':open_ohlcs_m30,
            'high':max_high_ohlcs_m30,
            'low':min_low_ohlcs_m30,
            'close':close_ohlcs_m30, 
        }

        if float(m30from_m1_data['close']) > float(m30from_m1_data['open']) :
            allred = False
        else:
            allgreen = False


        if allred == True or allgreen == True:
            # m5_body = abs(m5from_m1_data['open'] - m5from_m1_data['close'])
            # std_m5_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M5').first().value
            # m5_percent = ((std_m5_barsize - m5_body)/m5_body)*100

            # m15_body = abs(m15from_m1_data['open'] - m15from_m1_data['close'])
            # std_m15_barsize = StdBarSize.objects.filter(symbolname = search.name,timeframe = 'M15').first().value
            # m15_percent = ((std_m15_barsize - m15_body)/m15_body)*100
            
            # if m5_percent < 0 and m15_percent < 0 :
            greenOrred.append(search.id)

           

    isMarketClose = 0    
    if datetime.today().strftime('%A') == 'Saturday' or datetime.today().strftime('%A') == 'Sunday':
        isMarketClose = 1

    positions=mt5.positions_get()
    positionsymbol = []
    orders = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            # print(position.symbol)
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  
            orders.append({
                'symbol' : position.symbol,
                'ticket' : position.ticket,
                'lot' : position.volume,
                'type' : position.type,
                'profit' : position.profit,
                'comment' : position.comment,
            })   


    data = {
        'symbol':_symbol.name,
        'timeframe':_timeframe.name,
        'm1barsize' : m1barsize,
        'ohlc':ohlcs_m1, 
        'ohlctimeframe':ohlctimeframe, 
        'entryspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =1)),
        'exitspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =2)),
        'calculationInfo': calculationInfo,
        'usdbase': usdbase,
        'barsize' : serializers.serialize('json', StdBarSize.objects.filter(symbol_id = symbolid, timeframe = 'M1')),
        'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = greenOrred)),
        # 'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id)),
        'isMarketClose' : isMarketClose,
        'orders' : orders
        
    }

    return JsonResponse(data)

def getordersymbols(request):
    # setting = Setting.objects.first()
    # myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    # if not mt5.initialize():
    #     print("initialize() failed")
    #     mt5.shutdown()

    # mt5.login(myaccount.login,myaccount.password,myaccount.server)
    # accountinfo = mt5.account_info()

    # positions=mt5.positions_get()
    # positionsymbol = []
    # if positions==None:
    #     print("No positions found")
    # elif len(positions)>0:
    #     for position in positions:
    #         sb = Symbol.objects.filter(name=position.symbol).first()
    #         positionsymbol.append(sb.id)  
    # # greenOrred = []
    # # searchs = Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = positionsymbol)
    # print(positionsymbol)
    # data = {
    #     'apisymbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id,id__in = positionsymbol)), 
    # }
    # return JsonResponse(data)
    positions=mt5.positions_get()
    positionsymbol = []
    orders = []
    if positions==None:
        print("No positions found")
    elif len(positions)>0:
        for position in positions:
            # print(position.symbol)
            sb = Symbol.objects.filter(name=position.symbol).first()
            positionsymbol.append(sb.id)  
            orders.append({
                'symbol' : position.symbol,
                'ticket' : position.ticket,
                'lot' : position.volume,
                'type' : position.type,
                'profit' : position.profit,
                'comment' : position.comment,
            })  
    data = {
         'orders' : orders
    }
    return JsonResponse(data)        


def getsymbolinfo(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    symbol = request.POST.get('symbol')
    symbol_info=mt5.symbol_info(symbol)
    
    ohlcs_m1 = []
    ohlcs_m5 = []
    ohlcs_m15 = []
    ohlcs_m30 = []
    ohlcs_h1 = []

    ohlc_data_m1 = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 450))
    ohlc_data_m1['time']=pd.to_datetime(ohlc_data_m1['time'], unit='s',utc=True)
    for i, data in ohlc_data_m1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m1.append(ohlc)

    ohlc_data_m5 = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 450))
    ohlc_data_m5['time']=pd.to_datetime(ohlc_data_m5['time'], unit='s',utc=True)
    for i, data in ohlc_data_m5.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m5.append(ohlc)


    ohlc_data_m15 = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 450))
    ohlc_data_m15['time']=pd.to_datetime(ohlc_data_m15['time'], unit='s',utc=True)
    for i, data in ohlc_data_m15.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m15.append(ohlc)

    ohlc_data_m30 = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M30, 0, 2))
    ohlc_data_m30['time']=pd.to_datetime(ohlc_data_m30['time'], unit='s',utc=True)
    for i, data in ohlc_data_m30.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_m30.append(ohlc)

    ohlc_data_h1 = pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 2))
    ohlc_data_h1['time']=pd.to_datetime(ohlc_data_h1['time'], unit='s',utc=True)
    for i, data in ohlc_data_h1.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
        }
        ohlcs_h1.append(ohlc)
      
    ohlctimeframe = []
    ohlctimeframe = [
        
        {'h1': ohlcs_h1[len(ohlcs_h1)-1]},
        {'m30': ohlcs_m30[len(ohlcs_m30)-1]},
        {'m15': ohlcs_m15[len(ohlcs_m15)-1]},          
        {'m5': ohlcs_m5[len(ohlcs_m5)-1]},     
        {'m1': ohlcs_m1[len(ohlcs_m1)-1]},     
    ]

    calculationInfo ={
        'symbol': symbol_info.name,
        'bid' : symbol_info.bid,
        'ask' : symbol_info.ask,
        'degit' : symbol_info.digits,
        'spread' : symbol_info.spread,
        'trade_contract_size' : symbol_info.trade_contract_size,
        'balance' : accountinfo.balance,
    }
    
    data = {
        'ohlctimeframe': ohlctimeframe,
        'calculationInfo': calculationInfo,
        'barsize' : serializers.serialize('json', StdBarSize.objects.filter(symbol_id = Symbol.objects.filter(name = symbol).first().id, timeframe = 'M1')),
    }
    return JsonResponse(data)

def entrybuyposition(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    symbol = "USDJPY"
    symbol_info = mt5.symbol_info(symbol)     

    # print(symbol_info)   
    filling_type = 1

    filling_type = symbol_info.filling_mode - 1

    lot = 0.1
    # point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL, # mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": 0.0,
        "tp": 0.0,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling_type,
    }
    
    # send a trading request
    result = mt5.order_send(request)
    # print(result)  
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
    
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))
    time.sleep(100)
    # create a close request
    position_id=result.order
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY, # mt5.ORDER_TYPE_SELL,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling_type,
    }
    result=mt5.order_send(request)
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)
    else:
        print("4. position #{} closed, {}".format(position_id,result))
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    
    mt5.shutdown()

    data = {
        'entryspecs': '',
    }
    
    return JsonResponse(data)
    
def openorder(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    # print(accountinfo)

    ordertype = request.POST.get('ordertype')   
    lot = float(request.POST.get('lot'))

    symbol = request.POST.get('symbol') #Symbol.objects.filter(id = request.POST.get('symbol') ).first().name
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {'buy': 0, 'sell': 1};
    price_dict = {'buy': float(tick.ask), 'sell': float(tick.bid)};

    deviation = 20
    n = int(setting.numorder)
    for i in range(n):
        myuuid = str(uuid.uuid4().hex[:8])
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot),
            "type": order_dict[ordertype],
            "price": price_dict[ordertype],
            "sl": 0.0,
            "tp": 0.0,
            "deviation": deviation,
            "magic": 234000,
            "comment": symbol,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        # send a trading request
        result = mt5.order_send(request)
        print(result) 

    positions=mt5.positions_get()
    # print(positions)
    orders = []
    if positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s',utc=True)
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        # print(df)
        
        for i, data in df.iterrows():
           
            _data = {
                'symbol':data['symbol'],
                'lot':data['volume'] ,
                'profit':data['profit'],
                'position':data['ticket'],
                'type':data['type'],
                'comment':data['comment'],
            }
            orders.append(_data)

    data = {
        'orders':orders,
        'result':result,
        # 'searchreports': serializers.serialize('json', SearchReport.objects.all().order_by('-id')[:30]),
    }
    
    return JsonResponse(data)


def closeorder(request):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    clossall = request.POST.get('clossall')   

    positioncount=mt5.positions_total()
    # print(positioncount)

    positions=mt5.positions_get()
    # print(positions)

    if positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        profit = 0.5
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s',utc=True)
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)

        # df.query('type == 1 and profit > @profit', inplace = True)

        # df.query('profit > @profit', inplace = True)

        if clossall != 'closeall':
            df.query('profit > @profit', inplace = True) 

        # print(df)

        for i, data in df.iterrows():
            # print('ticket {0} time {1} volume {2} type {3} profit {4} symbol {5}'.format(data['ticket'],data['time'], data['volume'],data['type'],data['profit'],data['symbol']))
    
            deviation=20
            tick=mt5.symbol_info_tick(symbol)

            price_dict = {0: tick.ask, 1: tick.bid}

            type_dict = {0: 1, 1: 0}    

            request={
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": data['symbol'],
                "volume": data['volume'],
                "type": type_dict[int(data['type'])],
                "position": data['ticket'],
                "price": price_dict[int(data['type'])],
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result=mt5.order_send(request)
            # print(result)

        # print(df)
    
    data = {
        'entryspecs': '',
    }
    
    return JsonResponse(data)

def manualcloseorder(request):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    symbol = request.POST.get('symbol')   
    lot = float(request.POST.get('lot'))
    ordertype = int(request.POST.get('type'))
    position = int(request.POST.get('position'))   
    deviation=20
    tick=mt5.symbol_info_tick(symbol)

    price_dict = {0: tick.ask, 1: tick.bid}

    type_dict = {0: 1, 1: 0}    

    # print(tick.ask)

    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": type_dict[ordertype],
        "position": position,
        "price": price_dict[ordertype],
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result=mt5.order_send(request)
    print(result)
    positions=mt5.positions_get()
    # print(positions)
    orders = []
    if positions==None:
        print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s',utc=True)
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        # print(df)   
        for i, data in df.iterrows():
            _data = {
                'symbol':data['symbol'],
                'lot':data['volume'] ,
                'profit':data['profit'],
                'position':data['ticket'],
                'type':data['type'],
                'comment':data['comment'],
            }
            orders.append(_data)

    data = {
        'orders':orders,
        'searchreports': serializers.serialize('json', SearchReport.objects.all().order_by('-id')[:30]),
    }
    
    return JsonResponse(data)

def updatesearchreport(request):
    symbol = Symbol.objects.filter(name = request.POST.get('symbol')).first()
    timeframe = TimeFrame.objects.filter(name = request.POST.get('timeframe')).first()
    new = SearchReport(symbol_id = symbol.id,timeframe_id= timeframe.id,symbolname = symbol.name,timeframename= timeframe.name,order_type= request.POST.get('message'))
    new.save()
    
    data = {
        'entryspecs': '',
    }
    
    return JsonResponse(data)

def symboldata(request):

    currentview = CurrentView.objects.first()
    currentview.symbol_id = request.POST.get('symbol')
    currentview.timeframe_id = request.POST.get('timeframe')
    currentview.save()

    data = {
        'entryspecs': '',
    }
    
    return JsonResponse(data)


def savefirstfoundstatus(request):
    setting = Setting.objects.first()
    setting.firstfoundstatus = request.POST.get('status')
    setting.save()
    data = {
        'nothing': '',
    }
    
    return JsonResponse(data)

def updatestdbarsize(request):

    barsize = StdBarSize.objects.filter(symbol_id = request.POST.get('symbol_id'), timeframe= request.POST.get('timeframe')).first()
    barsize.value = request.POST.get('value')
    barsize.save()
    data = {
        'nothing': '',
    }
    
    return JsonResponse(data)    

def updatedemobalance(request):
    timezone = pytz.timezone("UTC")
    # print(request.POST.get('profit'))
    setting = Setting.objects.first()
    balance = setting.demobalance + float(request.POST.get('profit'))
    setting.demobalance = balance
    setting.save()
    data = {
        'balance': setting.demobalance,
    }
    
    return JsonResponse(data)    

def getalltimeframedata(request): 
    testdate = request.POST.get('currentdate') #"2022-01-28T4:20:00Z"
    symbol = request.POST.get('symbol')
    
    ohlcs_m1 = []
    ohlcs_m5 = []
    ohlcs_m15 = []
    ohlcs_m30 = []
    ohlcs_h1 = []
    ohlcs_h4 = []
    ohlcs_d1 = []
    # m1data = getpostdata(symbol,testdate,"M1",1700).tail(450)

    for i, data in getpostdata(symbol,testdate,"M1",1700).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_m1.append(ohlc)
    # print(ohlcs_m1)

    for i, data in getpostdata(symbol,testdate,"M5",1200).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_m5.append(ohlc)  

    for i, data in getpostdata(symbol,testdate,"M15",1100).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_m15.append(ohlc)

    for i, data in getpostdata(symbol,testdate,"M30",1100).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_m30.append(ohlc)

    for i, data in getpostdata(symbol,testdate,"H1",1100).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_h1.append(ohlc)
        # print(ohlc)

    for i, data in getpostdata(symbol,testdate,"H4",1100).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_h4.append(ohlc)

    for i, data in getpostdata(symbol,testdate,"D1",1100).tail(450).iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume'],
            'id':i
        }
        ohlcs_d1.append(ohlc)

    data = {
        'ohlcs_m1': ohlcs_m1,
        'ohlcs_m5': ohlcs_m5,
        'ohlcs_m15': ohlcs_m15,
        'ohlcs_m30': ohlcs_m30,
        'ohlcs_h1': ohlcs_h1,
        'ohlcs_h4': ohlcs_h4,
        'ohlcs_d1': ohlcs_d1,
    }
    
    return JsonResponse(data)      

def getpostdata(symbol,presentdatedate,_timeframe,num):
    pd.set_option('display.max_columns', 500) # number of columns to be displayed
    pd.set_option('display.width', 1500)      # max table width to display

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    timezone = pytz.timezone("UTC")
    numofbar = num
    timeframe = 15
    if _timeframe == 'M1':
        timeframe = 1
    elif _timeframe == 'M5':
        timeframe = 5
    elif _timeframe == 'M15':
        timeframe = 15
    elif _timeframe == 'M30':
        timeframe = 30
    elif _timeframe == 'H1':
        timeframe = 60
    elif _timeframe == 'H4':
        timeframe = 240
    elif _timeframe == 'D1':
        timeframe = 1440    

    to_datetime = datetime.strptime(presentdatedate.strip().replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
    # print(to_datetime)
    # to_datetime = to_datetime + timedelta(hours=7)
    minute = int(to_datetime.minute/timeframe)*timeframe
    # print(to_datetime)

    initial_datetime = datetime(to_datetime.year, to_datetime.month, to_datetime.day, to_datetime.hour, minute, 0)

    total_minutes = timedelta(minutes=timeframe * numofbar)

    from_datetime = initial_datetime - total_minutes 
    # print('==============================================')
    # print(total_minutes)
    # print('Timeframe: ' + _timeframe)
    # print ("From date",  from_datetime.year,  from_datetime.month,  from_datetime.day , from_datetime.hour,  from_datetime.minute)
    # print ("To date ",  to_datetime.year,  to_datetime.month,  to_datetime.day , to_datetime.hour,  to_datetime.minute)

    utc_from = datetime(from_datetime.year, from_datetime.month, from_datetime.day,from_datetime.hour,minute, tzinfo=timezone)
    utc_to = datetime(to_datetime.year, to_datetime.month, to_datetime.day,to_datetime.hour,to_datetime.minute, tzinfo=timezone)

    rates = []
    if _timeframe == 'M1':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, utc_from, utc_to)
    elif _timeframe == 'M5':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, utc_from, utc_to)
    elif _timeframe == 'M15':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M15, utc_from, utc_to)
    elif _timeframe == 'M30':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M30, utc_from, utc_to)
    elif _timeframe == 'H1':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H1, utc_from, utc_to)
    elif _timeframe == 'H4':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H4, utc_from, utc_to)
    elif _timeframe == 'D1':
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, utc_from, utc_to)
    mt5.shutdown()

    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s',utc=True)

    # print(_timeframe)
    # print(rates_frame)
    return rates_frame   

def manualaddbarsize(request):
    ids = StdBarSize.objects.all().values('symbol_id').distinct()
    symbols = Symbol.objects.filter().exclude(id__in = ids)
    for  symbol in symbols:
        m1 = StdBarSize(symbolname = symbol.name,timeframe= 'M1',value = 1000,symbol_id = symbol.id)
        m1.save()

        m5 = StdBarSize(symbolname = symbol.name,timeframe= 'M5',value = 1000,symbol_id = symbol.id)
        m5.save()

        m15 = StdBarSize(symbolname = symbol.name,timeframe= 'M15',value = 1000,symbol_id = symbol.id)
        m15.save()

        m30 = StdBarSize(symbolname = symbol.name,timeframe= 'M30',value = 1000,symbol_id = symbol.id)
        m30.save()

        h1 = StdBarSize(symbolname = symbol.name,timeframe= 'H1',value = 1000,symbol_id = symbol.id)
        h1.save()

        h4 = StdBarSize(symbolname = symbol.name,timeframe= 'H4',value = 1000,symbol_id = symbol.id)
        h4.save()

        d1 = StdBarSize(symbolname = symbol.name,timeframe= 'D1',value = 1000,symbol_id = symbol.id)
        d1.save()

        w1 = StdBarSize(symbolname = symbol.name,timeframe= 'W1',value = 1000,symbol_id = symbol.id)
        w1.save() 

    data = {
        'balance': '',
    }
    
    return JsonResponse(data)  


def deletesymbol(request):
    id = 65
    Symbol.objects.filter(id = id).delete()
    data = {
        'backtestjobs' :  '', 
    }
    return JsonResponse(data)    


def getdemobalance(request):
    data = {
        'balance': Setting.objects.first().demobalance,
    }
    return JsonResponse(data)    


def changedemobalance(request):
    setting = Setting.objects.first()
    setting.demobalance = request.POST.get('balance')
    setting.save()

    data = {
        'balance': Setting.objects.first().demobalance,
    }
    return JsonResponse(data)     


def copyrange(request):
    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")

    # utc_from = datetime(2022, 2, 7,0,5, tzinfo=timezone)
    # utc_to = datetime(2022, 2, 7,1,10, tzinfo=timezone)

    utc_from = datetime(2022, 2, 6,23,49, tzinfo=timezone)
    utc_to = datetime(2022, 2, 8,3,49, tzinfo=timezone)

    # print(utc_from)
    # print(utc_to)
    rates = mt5.copy_rates_range("USDJPY", mt5.TIMEFRAME_M1, utc_from, utc_to)
    mt5.shutdown()

    rates_frame = pd.DataFrame(rates)
    # convert time in seconds into the 'datetime' format
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    # display data
    print("\nDisplay dataframe with data")
    # print(rates_frame)

    data = {
        'balance': '',
    }
    return JsonResponse(data)  

def uploadimage(request):
    
    # print(request.POST.get('fname'))
    # image_data = request.POST.get('base64_tf_from_m1')
    # format, imgstr = image_data.split(';base64,')
   
    # ext = format.split('/')[-1]
    # data = ContentFile(base64.b64decode(imgstr))  
    # file_name = request.POST.get('fname') + '.' + ext
    # print(image_data)
    
    ohlcimage = OhlcImage(symbol = request.POST.get('fname') ,
    timeframes_from_m1 = request.POST.get('base64_tf_from_m1'),
    timeframes_from_latest = request.POST.get('base64_tf_all'),
    ohlc = request.POST.get('base64_ohlc'),
    ohlc_zoom = request.POST.get('base64_ohlc_zoom')
    )
    ohlcimage.save()
    res = {
        'balance': '',
    }
    return JsonResponse(res)  

def savesetting(request):
    print(request.POST.get('numberorder'))
    setting = Setting.objects.first()
    setting.numorder = request.POST.get('numberorder')
    setting.save()

    request.POST.get('fname')
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()

    return redirect('/setting',{
        'setting':setting,
        'accountinfo':accountinfo
    })

def Chart(request):
    return render(request,'chart.html',{
        'isMarketClose' : ''
    })


def openorder(request):
    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)
    accountinfo = mt5.account_info()

    stdbalance= accountinfo.balance/2500
    lotinfo = {
        'balance': accountinfo.balance,
        'lotsize': "{:.2f}".format(stdbalance),
        'takeprofit': "{:.2f}".format(stdbalance*100),
        'stoplost': "{:.2f}".format(stdbalance*60),
    }

    return render(request,'openorder.html',{
        'setting': setting,
        'lotinfo': lotinfo,
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id).order_by('name'),
    })   

def saveopenorder(request):
    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)
    accountinfo = mt5.account_info()

    symbolid = request.POST.get('symbol')
    lotsize = request.POST.get('lotsize')
    tradestyle = request.POST.get('tradestyle')
    takeprofit = request.POST.get('takeprofit')
    stoplost = request.POST.get('stoplost')
    numoforder = request.POST.get('numoforder')
    ordertype = request.POST.get('ordertype')
    

    stdbalance= accountinfo.balance/2500
    lotinfo = {
        'balance': accountinfo.balance,
        'lotsize': "{:.2f}".format(stdbalance),
        'takeprofit': "{:.2f}".format(stdbalance*100),
        'stoplost': "{:.2f}".format(stdbalance*60),
    }
   
    return redirect('/openorder',{
        'setting': setting,
        'lotinfo': lotinfo,
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id).order_by('name'),
    })
