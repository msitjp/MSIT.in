from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


admin.autodiscover()

urlpatterns = [
    url(r'^msit/admin/login/?', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^', include('web.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = _('Maharaja Surajmal Institute of technology')
admin.site.index_title = _('MSIT Administration')
admin.site.site_title = _('MSIT Administration')
