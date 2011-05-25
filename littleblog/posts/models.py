from django.db import models

class Post(models.Model):
    """A blog post entry"""

    # The author of this post
    author = models.ForeignKey('auth.User', related_name='posts', db_index=True)

    # True if the post if visible on the site to unauthenticated users
    visible = models.BooleanField(default=True, db_index=True)

    # The title of the post
    title = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True, editable=False)

    # Markdown components
    body_markdown = models.TextField()
    body_html = models.TextField()

    def save(self, *args, **kwargs):
        # Get the slug from the title
        from django.template.defaultfilters import slugify
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('posts:post_detail', (), {
            'slug': self.slug,
        })

    def __unicode__(self):
        return self.title
