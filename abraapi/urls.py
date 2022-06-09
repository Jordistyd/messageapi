from django.urls import path
from .views import Login, Messages

appname = "abraapi"

urlpatterns = [
    # Login view
    path("loginuser", Login.login_user, name="log_user"),
    path("allmessages/<str:user_name>", Messages.show_all_messages, name="show_all"),
    path("message/<str:username>", Messages.show_single_message, name="show_message"),
    path("unread/<str:user_name>", Messages.show_unread_messages, name="show_unread_message"),
    path("delete/<str:user_name>/<str:subject>/<str:type_delete>", Messages.delete_message, name="show_unread_message"),
    path("write", Messages.post_new_message, name="post_new_message"),

]