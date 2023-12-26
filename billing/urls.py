from django.urls import path
from billing import views
urlpatterns = [
    path('', views.home_view, name='Home'),
    path('search/', views.search, name="Search"),
    path('Branch/', views.view_branch, name="Branch"),
    path('payment/', views.view_payment, name="Payment"),
    path('demandType/', views.view_demandtype, name='DemandType'),
    path('customer/', views.view_customer, name='Customer'),
    path('demandRate/', views.view_demandrate, name='DemandRate'),
    path('bill/', views.view_bill, name='Bill'),
    path('pay/', views.dopay, name='dopay'),
    path('UserSearch/', views.customerSearch, name='user_search'),
    path('register/', views.createSuperUser, name='register' ),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path("createstaffuser/", views.createstaffuser, name='staffuser'),
    path('createuser/', views.createuser, name='createuser'),
    path('options/<int:id>', views.payment_options, name='PayOptions'),
    path('paypal/initiate/<int:id>/', views.create_payment, name='initiate'),
    path('paypal/execute/<int:id>/', views.execute_payment, name='execute'),
    path('report/', views.report, name='Report'),
    path('customerperbranch/', views.customer_per_branch, name='CustomerBranch'),
    path('customerperbill/', views.customer_per_bill, name='CustomerBill'),
    path('customerbypay/', views.customer_by_paymentmethod, name='CustomerPayOptions'),
    path('customerbydemand/', views.customer_by_demandtype, name='CustomerDemandType'),
    path('customerbillperbranch/', views.totalbill_branch, name='totalbillbranch'),
    path('totalamountbyyear/', views.totalbill_year, name='totalbillyear')
]