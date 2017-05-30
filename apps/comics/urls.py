from django.conf.urls import url, include
from . import views

urlpatterns = [
    # ============== #
    url(r'^test$',views.test),
    url(r'^addtest$',views.add_test),
    # FOR TESTING ONLY
    # ============== #
    url(r'^$', views.index),
    url(r'^admin$', views.admin),
    url(r'^dashboard$', views.admin_login),
    url(r'^register$', views.register),
    url(r'^dashboard/products$', views.product_view),
    url(r'^dashboard/orders$', views.orders_view),
    url(r'^dashboard/users$', views.admin_users),
    url(r'admin_logout$', views.admin_logout),
    url(r'admin_prod_search$', views.admin_prod_search),
    url(r'user_update/(?P<user_id>\d+)$', views.user_update),
    url(r'user_delete/(?P<user_id>\d+)$', views.user_delete),
    url(r'^products_main$', views.products_main),
    url(r'^search_comics$', views.search_comics),
    # url(r'^sort_comics$', views.sort_comics),
    url(r'^product/category/(?P<category_id>\d+)$',views.product_category),
    #url(r'^product_spotlight/$', views.product_spotlight),
    url(r'^product_spotlight/(?P<product_id>\d+)$', views.product_spotlight),
    url(r'^shopping_cart$', views.shopping_cart),
    url(r'product_adder$', views.product_adder),
    url(r'^display_test$', views.display_test),
    url(r'^charge/(?P<order_id>\d+)$', views.charge, name="charge"),
    url(r'^charge/(?P<order_id>\d+)/process$', views.charge_process),
    url(r'product_edit/(?P<product_id>\d+)$', views.product_edit),
    url(r'product_delete/(?P<product_id>\d+)$', views.product_delete),
    url(r'product_update/(?P<product_id>\d+)$', views.product_update),
    #url(r'create_order/(?P<order_id>\d+)$', views.create_order)
    url(r'^user_register$', views.user_registration),
    url(r'^user_login$', views.user_login),
    url(r'^checkout$', views.display_login_registration),
    url(r'^add_cart/(?P<product_id>\d+)$', views.add_cart),
    url(r'^create_order$', views.order_create),
    url(r'^order/success', views.order_success),
    url(r'^register/me$',views.register_me),
]
