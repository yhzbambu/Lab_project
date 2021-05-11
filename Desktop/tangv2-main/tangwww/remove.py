import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tangwww.settings')
django.setup()

from mysite.models import Poem

target = Poem.objects.filter(title__icontains="（")
print(len(target))
