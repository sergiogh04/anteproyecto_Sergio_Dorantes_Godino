from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anime/', include(('pagina_main.urls', 'anime'), namespace='anime')),  # Namespace correcto
    path('', include('pagina_main.urls')),  # Esto SIEMPRE debe ir al final
]
