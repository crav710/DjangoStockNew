from django import forms
from django.utils.translation import ugettext_lazy as _
import datetime
    
class StockForm(forms.Form):
    stock_symbol = forms.CharField()


    def get_symbol(self):
    	symbol=self.cleaned_data['stock_symbol']
    	print(symbol)
    	return symbol



# ID,SYMBOL,NO_SHARES,PURCHASE_PRICE,CURRENT_PRICE,PURCHASE_DATE
class StockInfoForm(forms.Form):
	stock_symbol=forms.CharField()
	share_count=forms.IntegerField()
	purchase_price=forms.IntegerField()
	current_price=forms.IntegerField()
	purchase_date=forms.DateField(initial=datetime.date.today)

	def get_time(self):
		time=self.cleaned_data['purchase_date']
		print(time)
		return time


class StockGraph(forms.Form):
	stock_symbol=forms.CharField()


