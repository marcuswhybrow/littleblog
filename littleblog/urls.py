from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^articles/', include('littleblog.posts.urls', namespace='posts')),

    (r'^tag/(?P<trail>.*)/$', redirect_to, {'url': '/posts/tags/%(trail)s/'}),

    (r'^search/', include('haystack.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
