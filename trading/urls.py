from django.urls import path
from . import views

urlpatterns = [
    path('get-balance/', views.get_balance_view, name='get_balance'),
    path('place-order/', views.place_order_view, name='place_order'),
    path('close-order/', views.close_order_view, name='close_order'),
    path('switch-position-mode/', views.switch_position_mode_view, name='switch_position_mode'),
    path('set-leverage/', views.set_leverage_view, name='set_leverage'),
    path('update-tp-sl/', views.update_tp_sl_view, name='update_tp_sl'),
    path('get-positions/', views.get_positions_view, name='get_positions')
]
