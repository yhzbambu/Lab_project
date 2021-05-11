"""tangwww URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index),
    #path('change_dynasty/', views.change_dynasty),                #更改作者朝代
    path('authors/', views.authors),                #作者列表
    path('poetry/<str:author>/', views.poetry),     #列出指定作者所有的詩
    path('poetry/', views.poetry),                  #顯示所有的詩
    path('edit/<int:id>/', views.edit),             #進行中英文標記
    path('update/<int:id>/', views.update),         #編輯詩的內容
    path('kwsearch/', views.kwsearch),              #以關鍵字查詢
    path('kwsearch/<str:kw>/', views.kwsearch),
    path('album/', views.album),                    #以選集的方式查詢
    path('album/<str:albumname>/', views.albumshow),#查看選集內容
    path('album-eng/', views.album_eng),            #查詢英譯本資訊
    path('album-eng/<int:album_id>/', views.album_eng_content),            #查看配對英譯本的詩
    path('show-eng-poem/<int:eng_poem_id>/', views.show_eng_poem), #顯示配對英譯本的詩
    path('pinyin/<int:pid>/', views.pinyin_list),    #中文及拼音並列檢視
    path('englist/', views.englist),                #英文詩檢索資訊
    path('search/', views.search),                  #以詩名關鍵字查詢
    path('cut-main/', views.search_and_cut),        #以詩名關鍵字查詢並提供斷詞介面
    path('cut-main-result/', views.cut_main_result),#前述之斷詞結果
    path('cut-check/', views.searchcut_and_check),  #以詩名關鍵字查詢並提供斷詞檢核介面
    path('api/poem/', views.rand_poem),             #隨機傳回一首詩
    path('api/poem/all/<str:sentence>/', views.all_sentence), #提供某句詩的完整詩句
    path('api/poem/next/<str:sentence>/', views.next_sentence), #提供某句詩的下一句
    path('api/poem/<str:author>/', views.rand_poem),#隨機傳回指定作者的一首詩
    path('api/cut/<int:method>/<str:content>/', views.cut_api), #提供斷詞工具的API
    path('api/cut/', views.cut_api),                #提供斷詞工具的API
    path('api/cut/<int:method>/', views.cut_api),   #提供斷詞工具的API
    path('api/cutsave/<int:pid>/<str:cutted>/', views.cutsave_api), #透過API儲存斷詞結果
    path('api/saveeng/<int:bid>/<int:pid>/<str:title>/<str:content>/', views.saveeng_api), #儲存英文譯本的API
    path('api/savejpn/<int:bid>/<int:pid>/<str:title>/<str:content>/', views.savejpn_api), #儲存日文譯本的API
    path('albumsetting/', views.albumsetting),      #設定選集
    path('set_newpoem/', views.set_newpoem, name = 'set_newpoem'),      #輸入新詩
    path('set_newbook/', views.set_newbook, name = 'set_newbook'),      #設定新譯本
    path('set_newAuthor/', views.set_newauthor, name = 'set_newauthor'),      #輸入新作者
    path('multiple_poem_check/<str:author>/<str:poem>/<str:lang>', views.multiple_poem_check), #解決同詩名同作者(輸入翻譯詩時)
    path('multiple_poem_check_input', views.multiple_poem_check_input, name='multiple_poem_check_input'),
    path('jieba-cut/', views.jiebacut),             #使用jieba進行斷詞
    path('ngram-cut/', views.ngramcut),             #使用ngram進行斷詞（阮老師版本）
    path('ckip-cut/', views.ckipcut),               #中研院CKIP斷詞
    path('compare-cut/', views.comparecut),         #綜合比較三種斷詞方法 
    path('delete/<int:id>/<str:kw>/', views.delete),
    path('engedit/<int:id>/', views.engedit),       #編輯英文譯本
    path('engedit/', views.engedit),                #編輯英文譯本（執行儲存的功能）
    path('dbstatus/', views.dbstatus),              #資料庫資料概觀
    path('chart/', views.chart),                    #作者作品數量排行圖表製作
    path('kwchart/', views.kwchart),                #關鍵字圖表製作
    path('login/', views.login),                    #登入
    path('logout/', views.logout),                  #登出
    path('admin/', admin.site.urls),                #後台管理頁面
]

urlpatterns += staticfiles_urlpatterns()