from django.urls import path
from .import views

urlpatterns = [
    path("", views.index,name="Home"),
path("allproducts/", views.allproducts,name="allproducts"),
path("largeprints/", views.largeprints,name="largeprints"),
path("regularprints/", views.regularprints,name="regularprints"),
path("login/",views.login,name="login"),
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
#path("emptycart/",views.emptycart,name="emptycart"),




]