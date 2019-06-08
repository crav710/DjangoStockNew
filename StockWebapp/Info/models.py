from django.db import models
import uuid
# Create your models here.

class Stock(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for particular Stock Symbol')
	stock_symbol=models.CharField(max_length=20,help_text='Enter the Stock Symbol')
	
	class Meta:
		ordering=['-stock_symbol']

	def get_absolute_url(self):
		return reverse('model-detail-view', args=[str(self.id)])

	def __str__(self):
		return self.stock_symbol