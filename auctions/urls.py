from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path('listing/<str:title>',views.listing,name='listing'),
    path('watchlist/view',views.watchlist,name='watchlist'),
    path("watchlist/add/<str:title>",views.watchlistAdd,name='watchlistAdd'),
    path('watchlist/remove/<str:title>',views.watchlistRem,name='watchlistRem'),
    path('listing/comment/<str:title>',views.comment,name='comment'),
    path('bid/<str:title>',views.bid,name='bid'),
    path('category/<str:category>',views.category,name='category'),
    path('category',views.menu,name='menu'),
    path('ended/<str:title>',views.ended,name='end')
]