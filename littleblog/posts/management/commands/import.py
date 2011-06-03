from django.core.management.base import BaseCommand, CommandError
from littleblog.posts.models import Post
from django.contrib.auth.models import User
from datetime import datetime
from django.db import IntegrityError
import yaml

class Command(BaseCommand):
    args = '<comments>'
    help = 'Imports wordpress posts from an exported YAML version of the ' \
        'wordpress comments table.'
    
    def handle(self, *args, **options):
        try:
            self.posts_path = args[0]
        except IndexError:
            raise CommandError('1 argument required: ' + self.args)
        
        try:
            user = User.objects.get(pk=1)
        except User.DoesNotExist:
            print 'Django user could not be found to attribute posts to.'
            return
        
        try:
            posts_file = open(self.posts_path, 'r')
            
            print 'Reading YAML file...'
            posts = yaml.load(posts_file.read())
            
            print 'Importing posts...'
            for post in posts:
                """
                Possible yaml keys:
                
                ID, post_author, post_date, post_date_gmt, post_content,
                post_title, post_category, post_excerpt, post_status,
                comment_status, ping_status, post_password, post_name,
                to_ping, pinged, post_modified, post_podified_gmt,
                post_content_iltered, post_parent, guid, menu_order,
                post_type, post_mime_type, comment_count
                """
                if post['post_type'] == 'post':
                    try:
                        new_post = Post.objects.create(
                            author=user,
                            title=post['post_title'],
                            body_markdown=post['post_content'],
                            # pub_date=datetime.strptime(post['post_date_gmt'], '%Y-%m-%d %H:%M:%S'),
                            # edit_date=datetime.strptime(post['post_modified_gmt'], '%Y-%m-%d %H:%M:%S'),
                            guid='%(id)s http://marcuswhybrow.net/?p=%(id)s' % {'id': post['ID']},
                        )
                    except IntegrityError:
                        pass
                        
        except KeyboardInterrupt:
            return