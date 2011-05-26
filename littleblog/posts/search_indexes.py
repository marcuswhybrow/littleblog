from haystack import site, indexes
from littleblog.posts.models import Post
import datetime

class PostIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Post.objects.all()

site.register(Post, PostIndex)
