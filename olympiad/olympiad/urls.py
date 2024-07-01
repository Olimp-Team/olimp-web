from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import start_page
from main.views import page_not_found

urlpatterns = [

    path('admin/', admin.site.urls),
    # Пока нет главной страницы перенаправление на страницу входа
    path('', start_page.as_view(), name='start_page'),
    # Главное приложение
    path('main/', include('main.urls', namespace='main')),
    path('docs/', include('docs.urls', namespace='docs')),
    path('register/', include('register.urls', namespace='register')),
    path('result/', include('result.urls', namespace='result')),
    path('classroom/', include('classroom.urls', namespace='classroom')),
    path('calendar/', include('calendar_olimp.urls', namespace='calendar')),
    # Приложения авторизации
    path('users/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
