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

    def _add_permalinks_to_body_header_elements(self):
        from django.template.defaultfilters import slugify
        import re

        regex = r'<(h[1-6]{1})>([^<]*)</\1>'
        iterable = re.finditer(regex, self.body_html)

        replacements = []
        identifiers = []
        for match in iterable:
            element, text = match.groups()
            identifier = slugify(text)

            # Get a unique identifier
            unique_identifier = identifier
            count = 2
            while unique_identifier in identifiers:
                unique_identifier = '%s-%d' % (identifier, count)
                count += 1
            identifiers.append(unique_identifier)

            replacement = r'<\1 id="%(id)s">\2 <a href="#%(id)s" ' \
                r'title="Permalink to this heading" ' \
                r'class="heading-permalink">&para;</a></\1>' \
                    % {'id': unique_identifier}

            before = self.body_html[match.start():match.end()]
            after = match.expand(replacement)
            replacements.append((before, after))

        for before, after in replacements:
            self.body_html = self.body_html.replace(before, after, 1)


    def save(self, *args, **kwargs):
        from django.template.defaultfilters import slugify
        import markdown
        
        self.slug = slugify(self.title)
        self.body_html = markdown.markdown(self.body_markdown)

        self._add_permalinks_to_body_header_elements()

        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('posts:post_detail', (), {
            'slug': self.slug,
        })

    def __unicode__(self):
        return self.title
