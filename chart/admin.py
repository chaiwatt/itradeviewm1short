from django.contrib import admin

from .models import Symbol,SymbolData,TimeFrame,CurrentView,BackTest

# Register your models here.

admin.site.register(Symbol)
admin.site.register(SymbolData)
admin.site.register(TimeFrame)
admin.site.register(CurrentView)
admin.site.register(BackTest)

