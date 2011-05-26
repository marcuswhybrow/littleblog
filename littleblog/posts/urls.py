from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView
from littleblog.posts.models import Post, Tag
from littleblog.posts.feeds import PostFeed, TagFeed

urlpatterns = patterns('',
    url(r'^feed/$', PostFeed(), name='post_feed'),

    url(r'^tags/$', ListView.as_view(model=Tag, paginate_by=10), name='tag_list'),
    url(r'^tags/(?P<slug>[\w-]+)/$', DetailView.as_view(model=Tag), name='tag_detail'),
    url(r'^tags/(?P<slug>[\w-]+)/feed/$', TagFeed(), name='tag_detail_feed'),

    url(r'^$', ListView.as_view(model=Post, paginate_by=10), name='post_list'),
    url(r'^(?P<slug>[^/]+)/$', DetailView.as_view(model=Post), name='post_detail'),
)
