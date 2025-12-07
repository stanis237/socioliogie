from django.core.management.base import BaseCommand
from content.models import Video, Course

class Command(BaseCommand):
    help = 'Remove video URLs that are not valid YouTube URLs (placeholders or invalid links)'

    def handle(self, *args, **options):
        videos = Video.objects.all()
        removed_count = 0

        for video in videos:
            if 'youtube.com' not in video.url and 'youtu.be' not in video.url:
                # Remove invalid video URLs (placeholders)
                video.delete()
                self.stdout.write(f'Removed invalid video {video.id} ({video.title}) with URL {video.url}')
                removed_count += 1

        self.stdout.write(f'Successfully removed {removed_count} invalid video URLs.')
