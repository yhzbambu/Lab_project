from django.contrib import admin
from mysite.models import Author, Poem, Album, Album2Poem, Book, PoemEng, BookJpn, PoemJpn,Dynasty

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name',  'count', 'counter', 'desc']

admin.site.register(Author, AuthorAdmin)

class PoemAdmin(admin.ModelAdmin):
    list_display = ['author', 'authorname', 'title', 'style','content', 'captured','cutted','created_by','created_at']

admin.site.register(Poem, PoemAdmin)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title']

admin.site.register(Album, AlbumAdmin)

class Album2PoemAdmin(admin.ModelAdmin):
	list_display = ['album', 'poem']

admin.site.register(Album2Poem, Album2PoemAdmin)

class BookAdmin(admin.ModelAdmin):
	list_display = ['author', 'title', 'pub_year', 'desc']

admin.site.register(Book, BookAdmin)

class PoemEngAdmin(admin.ModelAdmin):
	list_display = ['poem', 'title',  'translator','content','book','page','feature','formatted_content','created_by','created_at']

admin.site.register(PoemEng, PoemEngAdmin)

class BookJpnAdmin(admin.ModelAdmin):
	list_display = ['author', 'title', 'pub_year', 'desc']

admin.site.register(BookJpn, BookJpnAdmin)

class PoemJpnAdmin(admin.ModelAdmin):
	list_display = [ 'poem', 'title',  'translator','content', 'style','book','page','feature','formatted_content','created_by','created_at']

admin.site.register(PoemJpn, PoemJpnAdmin)

class DynastyAdmin(admin.ModelAdmin):
	list_display = [ 'author_dynasty']

admin.site.register(Dynasty, DynastyAdmin)