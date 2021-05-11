#這個程式的目的是為了要把每一首詩中的作者和Author資料表建立連線之用
#只要執行一次就好了（已執行過了）

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tangwww.settings')
django.setup()

from mysite.models import Author, Poem

authors = Author.objects.all()
poem = Poem.objects.all()

for p in poem:
    try:
        target_author = authors.get(name=p.authorname)
        print(target_author.id, target_author.name, p.author)
        author = Author.objects.get(id=target_author.id)
        p.author = author
        p.save()
    except:
        print("something error!")