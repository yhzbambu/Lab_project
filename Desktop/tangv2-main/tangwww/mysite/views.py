from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import datetime, random
from django.conf import settings
from mysite.models import Author, Poem, Album, Book, PoemEng, BookJpn, PoemJpn,  Dynasty
from django.db.models import Q
import jieba
import requests, re, ast, os
from pypinyin import lazy_pinyin, Style
from django.core import serializers
from django.conf.urls.static import static
import json
from django.db.models import Max

@login_required(login_url="/login/")
def multiple_poem_check_input(request): #解決同詩名同作者
	if request.method == "POST" and request.is_ajax:
		poem = Poem.objects.get(title = request.POST['title'], authorname = request.POST['author'], content=request.POST['content'])
		
		if request.POST['action'] == "eng":
			book = Book.objects.get(title = request.POST['book'])
			new = PoemEng(poem = poem, title = request.POST['translate_title'], translator=book.author, content = request.POST['translated_content'], book=book, page=request.POST['page'], feature=request.POST['feature'], formatted_content=request.POST['feature_content'], created_by=request.POST['created_by'])
		else:
			book = BookJpn.objects.get(title = request.POST['book'])
			new = PoemJpn(poem = poem, title = request.POST['translate_title'], style = request.POST['jpn_style'],translator=book.author, content = request.POST['translated_content'], book=book, page=request.POST['page'], feature=request.POST['feature'], formatted_content=request.POST['feature_content'], created_by=request.POST['created_by'])
		new.save()
		return HttpResponse(json.dumps({'data': "成功輸入資料庫, 按確定退出例外處裡"}), content_type='application/json')


@login_required(login_url="/login/")
def multiple_poem_check(request, author, poem, lang): #解決同詩名同作者
	ans = Poem.objects.filter(authorname=author, title=poem)
	if lang == "eng":
		book = Book.objects.all()
		is_jpn = False
	if lang == "jpn":
		book = BookJpn.objects.all()
		is_jpn = True
	context={}
	context['is_jpn'] = is_jpn
	context['poem_founded']=ans
	context['author']=author
	context['title']=poem
	context['lang']=lang
	context['book']=book
	return render(request, "multiple_poem_check.html", context)

def cut_nkust(raw):
	results = list()
	return results

def cut_jieba(raw):
	sentences = raw.split("\r\n")
	results = list()
	for sentence in sentences:
		result = list()
		result = "／".join(jieba.cut(sentence))
		results.append(result)	
	return results

def cut_ngram(raw):
	url = 'http://aipro.nkust.org:100/cgi-bin/tang_poem_new.py?Text1={}'
	results = list()
	raw = raw.replace("。", "，")
	raw = raw.replace("；", "，")
	sentences = raw.split("\r\n")
	for sentence in sentences:
		result = list()
		html = requests.get(url.format(sentence)).text
		try:
			result = ""
			temp = re.search('\[(.*?)\]', html).group()
			result = "／".join(ast.literal_eval(temp))
			results.append(result)
		except:
			pass	
	return results

def cut_ckip(raw):
	from ckiptagger import WS 
	ws = WS(os.path.join(settings.BASE_DIR, "./data/data"))
	results = "／".join(ws([raw])[0])						
	return results

def index(request):
	now = datetime.datetime.now()
	lucky_id = random.randint(1, 57614)
	try:
		lucky = Poem.objects.get(id=lucky_id)
	except:
		lucky = Poem.objects.get(id=1)
	content = lucky.content.replace("。", "。\n")
	content.replace("；", "；\n")
	content.replace("？", "？\n")
	return render(request, "index.html", locals())

def albumsetting(request):
	title = request.POST.get('title')
	collection = request.POST.get('collection')
	try:
		albumsave = Album.objects.create(title=title,anthology=collection)
	except:
		pass
	return render(request, "albumsetting.html", locals())

@login_required(login_url="/login/")
def set_newauthor(request):
	if request.is_ajax() and request.method == 'POST' and request.POST['action'] == "check_data":
		data = Author.objects.filter(name=request.POST["user_input"])
		print(data)
		if(len(data) == 0):
			return HttpResponse(json.dumps({'status': "good"}), content_type='application/json')
		else:
			return HttpResponse(json.dumps({'status': "bad"}), content_type='application/json')
	if request.is_ajax() and request.method == 'POST' and request.POST['action'] == "commit":
		dynasty = Dynasty.objects.get(author_dynasty = "未知")
		new = Author(name=request.POST["name"], desc = request.POST["desc"] , dynasty = dynasty)
		new.save()
		return HttpResponse(json.dumps({'status': "good"}), content_type='application/json')
	else:
		return render(request,"set_newauthor.html",locals())
		
@login_required(login_url="/login/")
def set_newbook(request):
	if request.is_ajax() and request.method == 'POST' and request.POST['action'] == "book_eng":
		data = Book(author = request.POST['author'] , title= request.POST['title'], desc = request.POST['des'], pub_year=request.POST['pub_year'] )
		data.save()
		return HttpResponse(json.dumps({'good': "good"}), content_type='application/json')
	if request.is_ajax() and request.method == 'POST' and request.POST['action'] == "book_jpa":
		data = BookJpn(author = request.POST['author'] , title= request.POST['title'], desc = request.POST['des'], pub_year=request.POST['pub_year'] )
		data.save()
		return HttpResponse(json.dumps({'good': "good"}), content_type='application/json')
	return render(request, "set_newbook.html")
	
@login_required(login_url="/login/")
def set_newpoem(request):
	if request.is_ajax() and request.method == 'POST' and request.POST['action'] == "user_input_author": #check user input author
		search_result =  Author.objects.filter(name=request.POST.get('user_input'))
		search_result_comments_json = serializers.serialize('json', search_result, use_natural_foreign_keys=True, use_natural_primary_keys=True)
		#print(search_result_comments_json)
		return HttpResponse(search_result_comments_json, content_type='application/json')
	elif request.is_ajax() and request.method == 'POST' and request.POST['action'] == "user_input_poem_title": #check user input title
		search_result =  Poem.objects.filter(title=request.POST['user_input'], authorname=request.POST['author'])
		print(len(search_result))
		search_result_json = serializers.serialize('json', search_result, use_natural_foreign_keys=True, use_natural_primary_keys=True)
		#print(search_result_json)
		return HttpResponse(search_result_json, content_type='application/json')
	elif request.is_ajax() and request.method == 'POST' and request.POST['action'] == "user_commit_chi": #中文輸入
		author = Author.objects.get(name=request.POST['author'])
		authorname = request.POST['author']
		title = request.POST['title']
		style = request.POST['style']
		captured = request.POST['caputred']
		content = request.POST['content']
		created_by = request.POST['created_by']
		user_input =  Poem(author=author ,authorname = authorname, title = title, style= style, content=content, captured= captured ,cutted='',created_by=created_by)
		user_input.save()
		return HttpResponse(json.dumps({'good': "good"}), content_type='application/json')
	elif request.is_ajax() and request.method == 'POST' and request.POST['action'] == "user_commit_eng": #英文輸入
		author = Author.objects.get(name=request.POST['author'])
		authorname = request.POST['author']
		title = request.POST['title']
		book = request.POST['book']
		translate_title = request.POST['translate_title']
		page = request.POST['page']
		feature_checkbox = request.POST['feature_checkbox']
		translated_content = request.POST['translated_content']
		translated_feature_content = request.POST['translated_feature_content']
		created_by = request.POST['created_by']
		poem = Poem.objects.get(title = title, authorname = authorname)
		book = Book.objects.get(pk = book)
		new = PoemEng(poem = poem, title = title, translator=book.author, content = translated_content, book=book, page=page, feature=feature_checkbox, formatted_content=translated_feature_content, created_by=created_by)
		new.save()
		return HttpResponse(json.dumps({'good': "good"}), content_type='application/json')
	elif request.is_ajax() and request.method == 'POST' and request.POST['action'] == "user_commit_jpa": #日文輸入
		author = Author.objects.get(name=request.POST['author'])
		authorname = request.POST['author']
		title = request.POST['title']
		book = request.POST['book']
		translate_title = request.POST['translate_title']
		page = request.POST['page']
		style = request.POST['style']
		feature_checkbox = request.POST['feature_checkbox']
		translated_content = request.POST['translated_content']
		translated_feature_content = request.POST['translated_feature_content']
		created_by = request.POST['created_by']
		poem = Poem.objects.get(title = title, authorname = authorname)
		book = BookJpn.objects.get(pk = book)
		new = PoemJpn(poem = poem, title = title, translator=book.author, content = translated_content, book=book, page=page,style=style , feature=feature_checkbox, formatted_content=translated_feature_content, created_by=created_by)
		new.save()
		return HttpResponse(json.dumps({'good': "good"}), content_type='application/json')
	else:
		eng_book = Book.objects.all()
		jpn_book = BookJpn.objects.all()
		#print(eng_book)
		return render(request, "set_newpoem2.html", locals())

def albumshow(request,albumname):
	album = Album.objects.get(title=albumname) #選集名稱
	albumtext = album.anthology.split("\r\n")
	
	albuminfo = list()
	for item in albumtext:
		temp = dict()
		author, title = item.split(",")
		temp['author'] = author.strip()
		temp['title'] = title.strip()
		albuminfo.append(temp)
	found_poem = list()
	for p in albuminfo:
		target = Poem.objects.filter(authorname__contains=p['author'].strip()).filter(title__contains=p['title'].strip())
		if len(target)>0:
			found_poem.append(target[0])
		else:
			print("Can't find the {}:{}!".format(author, title))

	return render(request, "albumshow.html", locals())

def all_sentence(request, sentence=""):
	result = ""
	if sentence != "":
		target = Poem.objects.filter(content__contains=sentence.strip()).first()
		if target:
			result = target.content + "/" + target.authorname
	return HttpResponse(result)

def next_sentence(request, sentence=""):
	result = ""
	if sentence != "":
		target = Poem.objects.filter(content__contains=sentence.strip()).first()
		if target:
			p = target.content
			p = p.replace("？", ",")
			p = p.replace("。", ",")
			p = p.replace("，", ",")
			p = p.replace("；", ",")
			words = p.split(",")
			for index, word in enumerate(words):
				if sentence in word and (index+1)<len(words):
					result = words[index+1]
					break
	return HttpResponse(result)

def authors(request):
	authors = Author.objects.all().order_by('-counter')
	dynasty = Dynasty.objects.all()
	if request.method=="GET":
		try:
			dynasty_res = request.GET.get('dynasty')
			dynasty_id = Dynasty.objects.filter(author_dynasty=dynasty_res)
			filter_author = Author.objects.filter(dynasty=dynasty_id[0].id)
		except:
			pass
	elif request.method=="POST":
		try:
			dynasty_resss = request.POST.get('dynastysss')
			change_res = request.POST.get('change_name')
			dynasty_id = Dynasty.objects.filter(author_dynasty=dynasty_resss)
			filter_authors = Author.objects.filter(name=change_res)#.update(dynasty=dynasty_id[0].id)
			if len(filter_authors) == 0:
				no_found_name = True
			else:
				found_name = True
				filter_authors.update(dynasty=dynasty_id[0].id)
		except:
			pass		
	# author_all = Author.objects.all()
	# with open('./class_no_author/no_all_notang_author.txt','r',encoding='utf-8') as f:
	# 	no_author = f.readlines()
	# 	author_no = list()
	# 	for au in no_author:
	# 		author_no.append(au.replace('\n',''))
	# for i in author_all:
	# 	if str(i.name) in author_no:
	# 		print(str(i.name))
	# 		author_one = Author.objects.filter(name=i.name).update(dynasty=14)
	return render(request, "authors.html", locals())

# def change_dynasty(request):
# 	dynasty = Dynasty.objects.all()
# 	if request.method == "POST":
# 		dynasty_res = request.POST.get('dynasty')
# 		change_res = request.POST.get('change_name')
# 		dynasty_id = Dynasty.objects.filter(author_dynasty=dynasty_res)
# 		filter_author = Author.objects.filter(name=change_res).update(dynasty=dynasty_id[0].id)
# 		if filter_author == 0:
# 			no_found_name = True

# 	return render(request, "author_change_dynasty.html", locals())

@login_required(login_url="/login/")
def engedit(request, id=0):

	if request.method=="POST":
		try:
			engbookid = request.POST.get('engbookid')
			poemengid = request.POST.get('poemengid')
			id = poemengid
			targetbook = Book.objects.get(id=engbookid)
			target2edit = PoemEng.objects.get(id=poemengid)
			target2edit.book = targetbook
			target2edit.save()
			return redirect("/show-eng-poem/{}/".format(id))
		except Exception as e:
			print(str(e))
			pass

	books = Book.objects.all()
	try:
		target = PoemEng.objects.get(id=id)
	except:
		pass
	return render(request, "engedit.html", locals())

def poetry(request, author='105'):
	try:
		selected_author = Author.objects.get(id=author)
		selected_author.counter = selected_author.counter + 1
		selected_author.save()
	except:
		pass
	top10 = Author.objects.all().order_by('-counter')[:10]
	selected_poetry = Poem.objects.filter(author=author).order_by("-content")
	numbers = len(selected_poetry)
	return render(request, "poetry.html", locals())

def update(request, id=1):
    if request.method == "POST":
        authorname = request.POST.get("authorname").strip()
        try:
            author = Author.objects.get(name=authorname)
        except:
            author = 1
            print("author name ", authorname)
            print("Can't find the author")
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        try:
            target = Poem.objects.get(id=id)
            target.author = author
            target.authorname = authorname
            target.title = title
            target.content = content
            target.save()
        except:
        	print("Can't save the record")
        	pass
    else:
        try:
        	target = Poem.objects.get(id=id)
        except:
        	print("Can't find the poem")
        	pass
    return render(request, "update.html", locals())

def delete(request, id=0, kw=""):
	#pass
	# 如需開啟刪除功能，請把以下的註解移除即可。
	if id>0 and kw!="":
		try:
			target = Poem.objects.get(id=id)
			target.delete()
		except:
			pass
	return redirect("/kwsearch/{}/".format(kw))

@login_required(login_url="/login/")
def edit(request, id=1):
	chi_poem = Poem.objects.get(id=id)
	eng_poem = PoemEng.objects.filter(poem=chi_poem.id)
	jpn_poem = PoemJpn.objects.filter(poem=chi_poem.id)
	books = Book.objects.all()
	jpnbooks = BookJpn.objects.all()
	return render(request, "edit.html", locals())

def pinyin_list(request, pid=1):
	poem = Poem.objects.get(id=pid)
	content = poem.content
	raw = content
	content = content.replace("。", "\n")
	content = content.replace("，", "\n")
	pinyin_results = " ".join(lazy_pinyin(raw))
	pinyin_results = pinyin_results.replace("。", "\n")
	pinyin_results = pinyin_results.replace("，", "\n")
	bopomofo = " ".join(lazy_pinyin(raw, style=Style.BOPOMOFO))
	bopomofo = bopomofo.replace("。", "\n")
	bopomofo = bopomofo.replace("，", "\n")
	data = zip(	content.split("\n"), 
				pinyin_results.split("\n"),
				bopomofo.split("\n"))
	return render(request, "pinyinlist.html", locals())

#隨機傳回一首唐詩
def rand_poem(request, author=""):
	if author =="":
		max_id = Poem.objects.all().aggregate(max_id=Max("id"))['max_id']
		while True:
			pk = random.randint(1, max_id)
			poem = Poem.objects.filter(pk=pk).first()
			if poem:
				result = poem.content
				break
	else:
		poem = Poem.objects.filter(authorname=author.strip())
		if poem:
			target = random.choice(poem)
			result = target.content
		else:
			result = "找不到該作者的詩作"
	return HttpResponse(result)

# 以詩名進行檢索
def search(request):
	if request.POST:
		keyword = request.POST.get('keyword')
		if len(keyword)>0:
			selected_author = keyword
			selected_poetry = Poem.objects.filter(title__contains=keyword)
			numbers = len(selected_poetry)
		else:
			numbers = 0
	else:
		numbers = 0
	return render(request, "search.html", locals())

# 詩詞檢索作為斷詞檢核之用
def searchcut_and_check(request):
	if request.POST:
		keyword = request.POST.get('keyword')
		if len(keyword)>0:
			target_keyword = keyword
			selected_poetry = Poem.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
			numbers = len(selected_poetry)
		else:
			numbers = 0
	else:
		numbers = 0
	return render(request, "searchcut-and-check.html", locals())

# 詩詞檢索作為斷詞之用
def search_and_cut(request):
	if request.POST:
		keyword = request.POST.get('keyword')
		if len(keyword)>0:
			target_keyword = keyword
			selected_poetry = Poem.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
			numbers = len(selected_poetry)
		else:
			numbers = 0
	else:
		numbers = 0
	return render(request, "search-and-cut.html", locals())

#查找詩句再斷詞的介面
def cut_main_result(request):
	numbers = 0
	jieba_results = ""
	if request.method == "POST":
		raw = request.POST.get("text2cut").strip()
		jieba_results = cut_jieba(raw)
		# sentences = raw.split("\r\n")
		# jieba_results = list()
		# for sentence in sentences:
		# 	result = list()
		# 	result = "／".join(jieba.cut(sentence))
		# 	jieba_results.append(result)	

	# url = 'http://aipro.nkust.org:100/cgi-bin/tang_poem_new.py?Text1={}'
	# ngram_results = ""
	# if request.method == "POST":
	# 	raw = request.POST.get("text2cut").strip()
		ngram_results = cut_ngram(raw)
		# ngram_results = list()
		# raw = raw.replace("。", "，")
		# raw = raw.replace("；", "，")
		# sentences = raw.split("\r\n")
		# for sentence in sentences:
		# 	result = list()
		# 	html = requests.get(url.format(sentence)).text
		# 	try:
		# 		result = ""
		# 		temp = re.search('\[(.*?)\]', html).group()
		# 		result = "／".join(ast.literal_eval(temp))
		# 		ngram_results.append(result)
		# 	except:
		# 		pass	
		# from ckiptagger import WS 
		# ws = WS(os.path.join(settings.BASE_DIR, "./data/data"))
		# ckip_results = "／".join(ws([raw])[0])						
		ckip_results = cut_ckip(raw)
	return render(request, "search-and-cut.html", locals())

# 以選集進行檢索
def album(request):
	albums = Album.objects.all()
	return render(request, "album.html", locals())

# 英譯本資訊檢索
def album_eng(request):
	books = Book.objects.all().order_by("-pub_year")
	return render(request, "album-eng.html", locals())

# 結巴斷詞用網頁
def jiebacut(request):

	results = ""
	if request.method == "POST":
		raw = request.POST.get("sentences").strip()
		results = cut_jieba(raw)
		# sentences = raw.split("\r\n")
		# results = list()
		# for sentence in sentences:
		# 	result = list()
		# 	result = "／".join(jieba.cut(sentence))
		# 	results.append(result)

	return render(request, "jieba-cut-interface.html", locals())

# n-gram 斷詞用網頁
def ngramcut(request):

	results = ""
	if request.method == "POST":
		raw = request.POST.get("sentences").strip()
		results = cut_ngram(raw)
		# data = raw.replace("。", "，")
		# data = data.replace("；", "，")
		# sentences = data.split("\r\n")
		# for sentence in sentences:
		# 	result = list()
		# 	html = requests.get(url.format(sentence)).text
		# 	try:
		# 		result = ""
		# 		temp = re.search('\[(.*?)\]', html).group()
		# 		result = "／".join(ast.literal_eval(temp))
		# 		results.append(result)
		# 	except:
		# 		pass

	return render(request, "ngram-cut-interface.html", locals())

#CKIP斷詞系統
def ckipcut(request):
	results = ""
	if request.method == "POST":
		raw = request.POST.get("sentences").strip()
		# from ckiptagger import WS 
		# ws = WS(os.path.join(settings.BASE_DIR, "./data/data"))
		# results = "／".join(ws([raw])[0])
		results = cut_ckip(raw)

	return render(request, "ckip-cut-interface.html", locals())


# 綜合比較斷詞用網頁
def comparecut(request):

	results = ""
	if request.method == "POST":
		raw = request.POST.get("sentences").strip()
		results_ngram = cut_ngram(raw)
		results_jieba = cut_jieba(raw)
		results_ckip = cut_ckip(raw)
		# data = raw.replace("。", "，")
		# data = data.replace("；", "，")
		# sentences = data.split("\r\n")
		# for sentence in sentences:
		# 	result_jieba = list()
		# 	result_jieba = "／".join(jieba.cut(sentence))
		# 	results_jieba.append(result_jieba)

		# 	result_ngram = list()
		# 	html = requests.get(url.format(sentence)).text
		# 	try:
		# 		result = ""
		# 		temp = re.search('\[(.*?)\]', html).group()
		# 		result_ngram = "／".join(ast.literal_eval(temp))
		# 		results_ngram.append(result_ngram)
		# 	except:
		# 		pass
		# from ckiptagger import WS 
		# ws = WS(os.path.join(settings.BASE_DIR, "./data/data"))
		# results_ckip = "／".join(ws([raw])[0])

	return render(request, "compare-cut-interface.html", locals())

def album_eng_content(request,album_id):
	book = Book.objects.get(id=album_id)
	eng_poem = PoemEng.objects.filter(book=book.id)
	return render(request, "album-eng-content.html", locals())

def show_eng_poem(request,eng_poem_id):
	# get_book = Book.objects.all()
	get_eng_info = PoemEng.objects.get(id=eng_poem_id)
	# books = list()
	# for i in get_book:
	# 	books.append(str(i))
	# if request.method == "POST":
	# 	modify_book = request.POST.get('modify_name')
	# 	get_modify_book = Book.objects.get(title=modify_book)
	# 	get_eng_info.book = get_modify_book
	# 	get_eng_info.save()
	chi_poem = get_eng_info.poem.content.replace("，", "，\n")
	chi_poem = chi_poem.replace("。", "。\n")
	chi_poem = chi_poem.replace("？", "？\n")
	chi_poem = chi_poem.split("\n")
	eng_poem = get_eng_info.content.split("\n")
	return render(request, "show_eng_poem.html", locals())

# 首頁的詩內容關鍵字檢索
def kwsearch(request, kw=""):
	if request.POST:
		keyword = request.POST.get('kw')
		disp_num = int(request.POST.get('disp-num'))
		if len(keyword)>0:
			selected_author = keyword
			top10 = Author.objects.all().order_by('-counter')[:10]
			selected_poetry = Poem.objects.filter(content__contains=keyword)[:disp_num]
			numbers = len(selected_poetry)
			return render(request, "poetry.html", locals())
		else:
			return redirect('/')
	elif kw!="":
		keyword = kw
		disp_num = 50
		if len(keyword)>0:
			selected_author = keyword
			top10 = Author.objects.all().order_by('-counter')[:10]
			selected_poetry = Poem.objects.filter(content__contains=keyword)[:disp_num]
			numbers = len(selected_poetry)
			return render(request, "poetry.html", locals())
		else:
			return redirect('/')		
	else:
		return redirect("/")

# 英文翻譯檢索頁面
def englist(request):
	selected_poetry = PoemEng.objects.all()
	numbers = len(selected_poetry)
	return render(request, "englist.html", locals())

def login(request):
	user_all = User.objects.all()
	name = request.POST.get('username')
	password = request.POST.get('password')
	try:
		user = auth.authenticate(username=name, password=password) #使用者驗證
	except:
		user = None
	if user is not None:   #若驗證成功，以 auth.login(request,user) 登入
		if user.is_active:
			auth.login(request,user) #登入成功
			return redirect('/') # 輸出到網頁上  #登入成功產生一個 Session，重導到<index.html>
			message = '登入成功!'
		else:
			message = '帳號尚未啟用!'
	else:
		message = '登入失敗!'
	return render(request,"login.html",locals())  #登入失敗則重導回<login.html>	

def logout(request):
    auth.logout(request)
    return redirect('/')

def cut_api(request, method=0, content="牀前明月光"):
	if content=="":
		data = {'result': 'fail'}
	else:
		if method==0: 		#系統輔助斷詞
			raw = content.strip()
			results = cut_nkust(raw)
			data = {'result': results}
		elif method==1: 	#N-Gram斷詞
			raw = content.strip()
			results = cut_ngram(raw)
			data = {'result': results}
		elif method==2:		#結巴斷詞
			raw = content.strip()
			results = cut_jieba(raw)
			data = {'result': results}			
		elif method==3:		#CKIP斷詞
			raw = content.strip()
			results = cut_ckip(raw)
			data = {'result': results}			
		else:
			data = {'result': content}
	return JsonResponse(data)

#透過API儲存英文譯本
def saveeng_api(request, bid=0, pid=0, title="", content=""):
    try:
    	target_poem = Poem.objects.get(id=pid)
    	target_book = Book.objects.get(id=bid)
    	target = PoemEng(poem=target_poem, book=target_book, title=title, content=content)
    	target.save()
    	data = {"result": "OK"}
    except Exception as e:
    	print(str(e))
    	data = {"result": "Fail"}
    return JsonResponse(data)

#透過API儲存日文譯本
def savejpn_api(request, bid=0, pid=0, title="", content=""):
    try:
    	target_poem = Poem.objects.get(id=pid)
    	target_book = BookJpn.objects.get(id=bid)
    	target = PoemJpn(poem=target_poem, book=target_book, title=title, content=content)
    	target.save()
    	data = {"result": "OK"}
    except Exception as e:
    	print(str(e))
    	data = {"result": "Fail"}
    return JsonResponse(data)


#透過API儲存斷詞結果
def cutsave_api(request, pid=0, cutted=""):
	if pid==0 or cutted=="":
		data = {"result": "Fail"}
	else:
		try:
			target = Poem.objects.get(id=pid)
			target.cutted = cutted.strip()
			target.save()
			data = {"result": "OK"}
		except:
			data = {"result": "Fail"}	
	return JsonResponse(data)

#資料庫資訊概觀
def dbstatus(request):
	poem_count = Poem.objects.all().count()
	eng_poem_count = PoemEng.objects.all().count()
	book_count = Book.objects.all().count()
	cutted_count = poem_count - Poem.objects.filter(cutted="").count()
	return render(request, "dbstatus.html", locals())

#統計圖表製作
def chart(request):
	top_authors = Author.objects.all().order_by("-count")[:20]
	return render(request, "chart.html", locals())

def kwchart(request):

	if request.method=="POST":
		keywords = request.POST.get('kwlist')
	else:
		keywords = "春, 夏, 秋, 冬, 風, 花, 雪, 月"
	kwlist = [kw.strip() for kw in keywords.split(",")]
	kwcount = list()
	for kw in kwlist:
		kwcount.append(Poem.objects.filter(content__contains=kw).count())
	return render(request, "kwchart.html", locals())