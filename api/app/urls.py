from . import views as v
from django.urls import path

urlpatterns = [
    path('',v.apiOverview , name="apiOverview"),


    #users
    path('signup/',v.signup,name="signup"),
    path('addprofil/', v.addprofil , name="addprofil"),
    path('view_profil/<str:pk>/', v.view_profil , name="view_porfil"),

    #posts
    path('addpost/',v.addPost , name="addpost"),
    path('shop/',v.shop , name="shop"),
    path('view_post/<str:pk>/',v.postDetail ,name="postDetail"),
    path('update_post/<str:pk>/', v.postUpdate , name="postUpdate"),
    path('delete_post/<str:pk>/',v.postDelete,name="postDelete")
]
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns += [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/',v.UserAPI().as_view(),name="user"),
]
