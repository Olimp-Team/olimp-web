from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Пока нет главной страницы перенаправление на страницу входа
    path('', redirect, name='redirect'),
    # Главное приложение
    path('main/', include('main.urls', namespace='main')),
    # Приложения авторизации
    path('auth/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),

]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
