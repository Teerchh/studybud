from django.urls import URLPattern, path
from . import views

urlpatterns: list[URLPattern] = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_page, name="register"),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("", views.index, name="home"),
    path("<uuid:id>/", views.room, name="room"),
    path("profile/<uuid:id>", views.user_profile, name="profile"),
    path("create_room/", views.create_room, name="create_room"),
    path("update_room/<uuid:id>/", views.update_room, name="update_room"),
    path("delete_room/<uuid:id>/", views.delete_room, name="delete_room"),
    path("delete_message/<uuid:id>/", views.delete_message, name="delete_message"),
    path("topics", views.browse_topics, name="topics"),
    path("activity", views.browse_activity, name="activity"),
]
