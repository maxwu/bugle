from django.conf.urls import patterns, include, url
from django.contrib import admin

from bugle.bugle_site import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bugle_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^example/', views.AnalyticsIndexView, name='example')
    url(r'^line_chart/json', views.line_chart_json, name='line_chart_json'),
    url(r'^line_chart/', views.line_chart, name='line_chart'),

)