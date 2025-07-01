from django.urls import path
from .views import (
    ApiRootView,     
    TestView,      
    MakePayment,    
    STKPushCallbackView  
)

urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'), 
    path('test/', TestView.as_view(), name='test'),  
    path('make-payment/', MakePayment.as_view(), name='make_payment'),  
    path('stkpush-callback/', STKPushCallbackView.as_view(), name='stkpush_callback'),  
]


