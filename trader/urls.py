"""trader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chart import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.index,name='index'),
    path('getohlc',views.getohlc,name='getohlc'),
    path('getsingleohlc',views.getsingleohlc,name='getsingleohlc'),
    path('createbacktest',views.createbacktest ,name='createbacktest'),
    path('deletebacktest',views.deletebacktest ,name='deletebacktest'),
    path('getbacktestjob',views.getbacktestjob ,name='getbacktestjob'),
    path('spec',views.spec ,name='spec'),
    path('changespecusage',views.changespecusage ,name='changespecusage'),
    path('clonespec',views.clonespec ,name='clonespec'),
    path('getentryspec',views.getentryspec ,name='getentryspec'),
    path('changespecentrypointvalue',views.changespecentrypointvalue ,name='changespecentrypointvalue'),
    path('changesymbolstatus',views.changesymbolstatus ,name='changesymbolstatus'),
    path('deleteallbacktest',views.deleteallbacktest ,name='deleteallbacktest'),
    path('jogtest',views.jogtest ,name='jogtest'),
    path('backtest',views.backtest,name='backtest'),
    path('backtesting',views.backtesting,name='backtesting'),
    path('getSymbolData',views.getSymbolData,name='getSymbolData'),
    path('lineNotification',views.lineNotification,name='lineNotification'),
    path('symbolsetting',views.symbolsetting,name='symbolsetting'),
    path('',views.search,name='search'),
    path('entrybuyposition',views.entrybuyposition,name='entrybuyposition'),
    path('openorder',views.openorder,name='openorder'),
    path('closeorder',views.closeorder,name='closeorder'),
    path('updatesearchreport',views.updatesearchreport,name='updatesearchreport'),
    path('symboldata',views.symboldata,name='symboldata'),
    path('manualcloseorder',views.manualcloseorder,name='manualcloseorder'),
    path('savefirstfoundstatus',views.savefirstfoundstatus,name='savefirstfoundstatus'),
    path('updatestdbarsize',views.updatestdbarsize,name='updatestdbarsize'),
    path('updatedemobalance',views.updatedemobalance,name='updatedemobalance'),
    path('getalltimeframedata',views.getalltimeframedata,name='getalltimeframedata'),
    path('manualaddbarsize',views.manualaddbarsize,name='manualaddbarsize'),
    path('deletesymbol',views.deletesymbol,name='deletesymbol'),
    path('getdemobalance',views.getdemobalance,name='getdemobalance'),
    path('changedemobalance',views.changedemobalance,name='changedemobalance'),
    path('orders',views.orders,name='orders'),
    path('copyrange',views.copyrange,name='copyrange'),
    path('getsymbolinfo',views.getsymbolinfo,name='getsymbolinfo'),
    path('getorders',views.getorders,name='getorders'),
    path('getapisymbols',views.getapisymbols,name='getapisymbols'),
    path('uploadimage',views.uploadimage,name='uploadimage'),
    path('getordersymbols',views.getordersymbols,name='getordersymbols'),
    path('setting',views.setting,name='setting'),
    path('savesetting',views.savesetting,name='savesetting'),
    path('searchsymbol',views.searchSymbol,name='searchsymbol'),
    path('searchsingleohlc',views.searchSingleOhlc,name='searchsingleohlc'),
    path('chart',views.Chart,name='chart'),
    path('saveopenorder',views.saveopenorder,name='saveopenorder'),
    
]
