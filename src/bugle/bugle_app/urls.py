from django.conf.urls import patterns, include, url
from django.contrib import admin

from bugle.bugle_app import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bugle_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^example/', views.AnalyticsIndexView, name='example')
)