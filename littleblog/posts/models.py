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
    body_html = models.TextField(blank=True, editable=False)

    # Published/Edited times
    pub_date = models.DateTimeField(auto_now_add=True, editable=False,
                                    db_index=True)
    edit_date = models.DateTimeField(auto_now=True, editable=False,
                                     db_index=True)

    def save(self, *args, **kwargs):
        from django.template.defaultfilters import slugify
        import markdown
        
        self.slug = slugify(self.title)
        self.body_html = markdown.markdown(self.body_markdown)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('posts:post_detail', (), {
            'slug': self.slug,
        })

    def __unicode__(self):
        return self.title
