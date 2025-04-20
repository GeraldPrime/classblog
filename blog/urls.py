from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static
    

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('', views.home, name='home-page'),
    path('home/', views.home, name='home-page'),
    path('user/', views.user_home, name='user-home'),
    path('create_post/', views.create_post, name='create_post'),
    path('signout/', views.signout, name='signout'),
    path('post/<int:id>/', views.single_post,name="single_post"),
    path('update/<int:id>/', views.update_post,name="update_post"),
    path('delete/<int:id>/', views.delete_post,name="delete_post"),
    
]
if settings.DEBUG:  # Only serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)