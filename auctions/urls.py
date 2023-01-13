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
    path("addOrRemoveWatchlist/<int:id>", views.addOrRemoveWatchlist, name="addOrRemoveWatchlist"),
    path("watchlist", views.displayWatchlist, name="watchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>", views.add_bid, name="addBid"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
]
