from django.db import models
# from django_unixdatetimefield import UnixDateTimeField

class Broker(models.Model):
    name=models.CharField(max_length=50)
    class Meta:
        db_table = "brokers" 

class MyAccount(models.Model):
    broker=models.ForeignKey(Broker, on_delete=models.CASCADE)
    login=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    server=models.CharField(max_length=100)
    account_type=models.CharField(max_length=1)
   
    class Meta:
        db_table = "my_accounts" 

class Setting(models.Model):
    myaccount=models.ForeignKey(MyAccount, on_delete=models.CASCADE)
    demobalance=models.FloatField(default = 1000)
    exitmode=models.IntegerField(default = 1,null=True)
    numorder=models.IntegerField(default = 1,null=True)
    class Meta:
        db_table = "settings" 

class TimeFrame(models.Model):
    name=models.CharField(max_length=10)
    class Meta:
        db_table = "time_frames" 

class Symbol(models.Model):
    broker=models.ForeignKey(Broker, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    status=models.CharField(max_length=1)
    pipdistant=models.IntegerField(default = 5,null=True)

    class Meta:
        db_table = "symbols"

class BackTestInterval(models.Model):
    interval=models.IntegerField()
    class Meta:  
        db_table = "backtest_interval"         

class SymbolData(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    class Meta:
        db_table = "symbol_datas"

class CurrentView(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    class Meta:
        db_table = "current_views"

class BackTestSize(models.Model):
    size=models.IntegerField()
    class Meta:
        db_table = "backtest_sizes"

class BackTest(models.Model):
    code=models.CharField(max_length=100)
    symbolname=models.CharField(max_length=100, default = None)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    timeframename=models.CharField(max_length=100, default = None)
    backtestsize=models.ForeignKey(BackTestSize, on_delete=models.CASCADE)
    interval=models.ForeignKey(BackTestInterval, on_delete=models.CASCADE)
    status=models.CharField(max_length=1, default = 0)
    class Meta:
        db_table = "back_tests"

# class BackTestSymbol(models.Model):
#     backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
#     symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
#     class Meta:  
#         db_table = "back_test_symbols"

class BackTestOHLC(models.Model):
    backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    date=models.DateTimeField()
    open=models.FloatField()
    high=models.FloatField()
    low=models.FloatField()
    close=models.FloatField()
    tick=models.IntegerField()
    class Meta:
        db_table = "back_test_ohlcs"

class BackTestOHLCTimeframe(models.Model):
    backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    timeframename=models.CharField(max_length=100, default = None)
    date=models.DateTimeField()
    open=models.FloatField()
    high=models.FloatField()
    low=models.FloatField()
    close=models.FloatField()
    tick=models.IntegerField()
    class Meta:
        db_table = "back_test_ohlc_timeframes"
        
class Spec(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    parameter=models.CharField(max_length=100)
    entry_value=models.CharField(max_length=20)
    exit_value=models.CharField(max_length=20)
    parameter_type=models.CharField(max_length=20)
    compare_reverse=models.CharField(max_length=1, default = 1)
    status=models.CharField(max_length=1, default = 1)
    spec_type=models.CharField(max_length=1, default=1)
    order_type=models.CharField(max_length=1, default = 0)

    class Meta:
        db_table = "specs"

        
class SearchType(models.Model):
    trend=models.CharField(max_length=1, default=1)
    pattern=models.CharField(max_length=1, default = 0)
    class Meta:
        db_table = "search_types"

class SearchReport(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    order_type=models.CharField(max_length=100, default=None)
    symbolname=models.CharField(max_length=10, default=None)
    timeframename=models.CharField(max_length=10, default=None)
    # onorder=models.CharField(max_length=1, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "search_reports"   

class StdBarSize(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    symbolname=models.CharField(max_length=100, default=None)
    timeframe=models.CharField(max_length=10, default=None)
    value=models.FloatField(max_length=15, null=True)
    stoplostpip=models.IntegerField(default = 20)
    stoplostpercent=models.FloatField(default = 0.015)
    lotsizeoffset=models.FloatField(default = 1)
    class Meta:
        db_table = "std_bar_sizes"   
            
class LotSizeFactor(models.Model):
    
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    timeframename=models.CharField(max_length=10)
    factor=models.FloatField(default=1)
    class Meta:
        db_table = "lot_size_factors"          

class OhlcImage(models.Model):
    symbol=models.CharField(max_length=100, default=None)
    timeframes_from_m1 = models.TextField(blank=True, null=True)
    timeframes_from_latest = models.TextField(blank=True, null=True)
    ohlc = models.TextField(blank=True, null=True)
    ohlc_zoom = models.TextField(blank=True, null=True)
    class Meta:
        db_table = "ohlc_images"                  