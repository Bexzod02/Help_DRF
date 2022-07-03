from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    ### FBV


    path("", views.api_home),
    path('create/', views.api_post),
    path('<int:pk>/', views.api_detail),
    path('edit/<int:pk>/', views.api_put),
    path('delete/<int:pk>/', views.api_delete),
    path('api-rud/<int:pk>', views.api_rud),


    ### CBV
    path('cbv/list/', views.ProductListView.as_view()),
    path('cbv/create/', views.ProductCreateView.as_view()),
    path('cbv/retrive/<int:pk>/', views.ProductRetrive.as_view()),
    path('cbv/list-create/', views.ProductListCreateView.as_view()),
    # path('cbv/edit/<int:pk>/', views.ProductPutView.as_view())
    path('cbv/rud/<int:pk>/', views.ProductRetriveEditdeleteView.as_view(), name='rud-view'),
    path('cbv/daily/filt/', views.DayliProduct.as_view()),

    path('auth/token/', obtain_auth_token),
]
