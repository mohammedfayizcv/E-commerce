from . import views
from django.urls import path

urlpatterns = [
   path('',views.funStore,name='store'),
   path('cart/',views.funCart,name='cart'),
   path('checkout/',views.funCheckOut,name='checkout'),
   
   path('update_item/',views.updateItem,name='update_item'),
   path('process_order/',views.processOrder,name='process_order')
   
]
