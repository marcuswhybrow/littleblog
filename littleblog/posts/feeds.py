from django.contrib.syndication.views import Feed
from littleblog.posts.models import Post, Tag

class PostFeed(Feed):
    title = 'Article Feed'
    link = '/posts/'
    
    def items(self):
        return Post.objects.order_by('-pub_date')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.body_html
    
    def item_pubdate(self, item):
        return item.pub_date

class TagFeed(PostFeed):
    title = 'Tag Feed'
    link = '/posts/django/feed/'

    def __call__(self, request, slug, *args, **kwargs):
        try:
            self.tag = Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            self.tag = None

        return super(TagFeed, self).__call__(request, *args, **kwargs)

    def items(self):
        return self.tag.posts.all()
