from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    # Renders
    path('', views.index, name='index'),
    path('dashboard', views.dashboard),
    path('new', views.new),
    path('stats', views.stats),
    path('edit', views.edit),
    # Functions
    path('attempt_login', views.attempt_login),
    path('attempt_reg', views.attempt_reg),
    path('logout', views.logout),
]