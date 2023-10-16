from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from api.views import RegisterUserView,LoginUserView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    re_path(r'^rosetta/', include('rosetta.urls')),
    path(_('blog/'), include("blog.urls")),
    path(_('auth/'), include('authentication.urls')),
    path(_('api/'), include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/register/', RegisterUserView.as_view()),
    path('api/auth/login/', LoginUserView.as_view()),
    path('rest-auth/', include('dj_rest_auth.urls')),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('',include("main.urls"))
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)