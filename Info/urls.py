from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

]

urlpatterns += [   
    path('stock_detail/', views.stock_page, name='stock_page'),
]

urlpatterns += [   
    path('form/', views.stock_form, name='stock_form'),
]


urlpatterns += [   
    path('stockform/', views.stock_detail_form, name='stock_detail_form'),
]


urlpatterns += [   
    path('formgraph/', views.stock_graph_form, name='stock_graph_form'),
]

urlpatterns += [   
    path('stockgraph/', views.display_graph, name='stock_graph'),
]
