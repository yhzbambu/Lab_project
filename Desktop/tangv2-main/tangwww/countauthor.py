#這個程式的目的是為了要計算每一位詩人所寫的詩數量
#把沒有詩作的作者刪除，並把結果以字典的方式儲存在author-poem-count.txt中
#本程式也會更新所有作者的詩作數目，放在Author的count欄位中
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tangwww.settings')
django.setup()

from mysite.models import Author, Poem

authors = Author.objects.all()

counts = list()
delnum = 0
for a in authors:
	temp = dict()
	num = Poem.objects.filter(author=a).count()
	if num > 0:
		temp['name'] = a.name
		temp['count'] = num
		counts.append(temp)
		a.count = num
		a.save()
		print(a.name, num)
	else:
		print(a.name+" will to be deleted!")
		a.delete()
		delnum += 1

with open("author-poem-count.txt", "w") as fp:
	fp.write(str(counts))
print("Done")
print(delnum, " author were deleted!")