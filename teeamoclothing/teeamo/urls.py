from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index,name="Home"),
path("allproducts/", views.allproducts,name="allproducts"),
path("largeprints/", views.largeprints,name="largeprints"),
path("regularprints/", views.regularprints,name="regularprints"),
path("login/",views.loginpage,name="login"),
path("tiedye/",views.tiedye,name="tiedye"),
path("productdetail/<int:id>",views.productdetail,name="productdetail"),
path("searchresult/",views.searchresult,name="searchresult"),
path("signup/",views.handlesignup,name="handlesignup"),
path("cart/", views.cart ,name="cart"),
path("checkout/", views.checkout ,name="checkout"),
path("update_item/", views.updateItem ,name="update_item"),
path("addtocart/", views.addtocart ,name="addtocart"),
path("policy/",views.policy,name="policy"),
path("about/",views.about,name="about"),
path("process_order/",views.processOrder,name="process_order"),
path("handle_login/",views.handle_login,name="handle_login"),
path("myaccount/",views.myaccount,name="myaccount"),
path("logout/",views.logout_view,name="logout"),
path("change_password/",views.change_password,name="change_password"),
path("handle_change_password/",views.handle_change_password,name="handle_change_password"),
path("my_orders/",views.my_orders,name="my_orders"),
path('handlerequest/', views.handlerequest, name='handlerequest'),
path("order_details/<int:id>",views.order_details,name="order_details"),
path('reset_password/',auth_views.PasswordResetView.as_view(template_name="teeamo/password_reset.html"),
name="reset_password"),
path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="teeamo/password_reset_sent.html"),
name="password_reset_done"),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
template_name="teeamo/password_reset_confirm.html"),
name="password_reset_confirm"),
path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(
template_name="teeamo/password_reset_complete.html"), name="password_reset_complete"),






]