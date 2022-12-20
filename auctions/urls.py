from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.createListing, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.displayCategories, name="categories"),
    path("categories/<str:category>", views.selectedCategoryListing, name="choosenCategory"),
    path("listings/<int:id>", views.listing, name="listings"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.displayWatchlist, name="watchlist")

    

    # path("list/<str:list_url>", views.list_view, name="list"),
    # path("watchlist", views.watchlist, name="watchlist"),
    # path("bid", views.add_bid, name="bid")

 
]
