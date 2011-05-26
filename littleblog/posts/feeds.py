from django.contrib.syndication.views import Feed
from littleblog.posts.models import Post

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

