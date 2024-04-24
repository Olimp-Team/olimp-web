from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import start_page

from main.views import page_not_found

urlpatterns = [

    path('admin/', admin.site.urls),
    # Пока нет главной страницы перенаправление на страницу входа
    path('', start_page, name='start_page'),
    # Главное приложение
    path('main/', include('main.urls', namespace='main')),
    path('docs/', include('docs.urls', namespace='docs')),
    # Приложения авторизации
    path('auth/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),

]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found