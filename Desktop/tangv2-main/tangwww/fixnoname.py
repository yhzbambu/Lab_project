#把作者為不詳及無名氏的合併在一起
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tangwww.settings')
django.setup()

from mysite.models import Author, Poem

noname_author = Author.objects.get(name="不詳")
nobody_author = Author.objects.get(name="無名氏")
noname_author_poem = Poem.objects.filter(author=noname_author)
nobody_author_poem = Poem.objects.filter(author=nobody_author)

print("不詳詩作共", len(noname_author_poem), "首")
print("無名氏詩作共", len(nobody_author_poem), "首")

for target in noname_author_poem:
	print(target.author)
	# target.author = nobody_author
	# target.save()
	# print(target.title, "改變作者為無名氏")
print("Done")