from django.urls import path
from . import views
from .views import medicine_detail,register,login,customer,addtoCart,viewCart,cartDelete,Checkout,viewOrder,comments,prescriptionUpload,viewPrescription
urlpatterns = [
    path('medicinelist', views.medicine_list, name='medicine_list'),
    path('add/', views.add_medicine, name='add_medicine'),
    path('update/<int:pk>/', views.update_medicine, name='update_medicine'),
    path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
     path('search-medicine/', views.search_medicine, name='search_medicine'),
     path("",views.index,name="index"),
      path('medicine/<int:medicine_id>/', medicine_detail, name='medicine_detail'),
      path('register',register,name='register'),
      path('login',login,name="login"),
      path("customer",customer,name="customer"),
      path("addtocart",addtoCart,name="addtoCart"),
      path('cartview/',viewCart,name="viewCart"),
      path("cartdelete/<int:itemid>/",views.cartDelete,name="cartDelete"),
      path("order",views.order,name="oreder"),
      path("checkout",Checkout,name="Checkout"),
      path("vieworder",viewOrder,name="viewOrder"),
      path("comments",comments,name="comments"),
      path("prescription",prescriptionUpload,name="prescriptionUpload"),
      path("viewprescription",viewPrescription,name="viewPrescription"),
      path("prescriptioncheckout",views.prescriptionCheckout,name="prescriptionCheckout"),


]
