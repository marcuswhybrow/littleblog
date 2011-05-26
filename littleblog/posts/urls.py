from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView
from littleblog.posts.models import Post
from littleblog.posts.feeds import PostFeed

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Post, paginate_by=10), name='post_list'),
    url(r'^feed/$', PostFeed(), name='feed'),
    url(r'^(?P<slug>[^/]+)/$', DetailView.as_view(model=Post), name='post_detail'),
)
