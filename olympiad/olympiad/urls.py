from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import StartPage
from main.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    # Пока нет главной страницы, перенаправление на страницу входа
    path('', StartPage.as_view(), name='start_page'),
    # Главное приложение
    path('main/', include('main.urls', namespace='main')),
    path('docs/', include('docs.urls', namespace='docs')),
    path('register/', include('register.urls', namespace='register')),
    path('result/', include('result.urls', namespace='result')),
    path('school/', include('school.urls', namespace='school')),
    path('classroom/', include('classroom.urls', namespace='classroom')),
    path('calendar/', include('calendar_olimp.urls', namespace='calendar')),
    # Приложения авторизации
    path('users/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),
    path('friends/', include('friends.urls', namespace='friends')),
    path('chat/', include('chat.urls')),
]

# Обработка медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработка ошибки 404
handler404 = page_not_found
