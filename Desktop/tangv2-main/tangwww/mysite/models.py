from django.db import models

#選集
class Album(models.Model):
    title = models.CharField(max_length=50)
    anthology = models.TextField(default=0)
    def __str__(self):
        return self.title
#選集的內容，多對多關係
class Album2Poem(models.Model):
    album = models.ForeignKey(to='Album', on_delete=models.CASCADE)
    poem = models.ForeignKey(to='Poem', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.album)
#作者 
class Author(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    counter = models.PositiveIntegerField(default=0)  #被檢索點擊之次數
    count = models.PositiveIntegerField(default=0)    #此作者詩作之數目
    dynasty = models.ForeignKey(to='Dynasty', on_delete=models.CASCADE, default = 'null')
    def __str__(self):
        return self.name

class Dynasty(models.Model):
    author_dynasty = models.CharField(max_length=20, default='abc')
    def __str__(self):
        return self.author_dynasty

#中文詩作
class Poem(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    authorname = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    style = models.CharField(max_length=255 , default= "null")
    content = models.TextField()
    captured = models.CharField(max_length=255 , default= "null")
    cutted = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, default = "null")
    created_at = models.DateTimeField(auto_now_add=True )
    
    def __str__(self):
        return "{}({})".format(self.title, self.author)
#英文譯本
class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    pub_year = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

#英文詩作
class PoemEng(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    translator = models.CharField(max_length=255, default = "null")
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page = models.PositiveIntegerField(default=0)
    feature = models.CharField(max_length=255, default = "000000")
    formatted_content = models.TextField(default = "null")
    created_by = models.CharField(max_length=255, default = "null")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

#英文譯本
class BookJpn(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    pub_year = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

#日文詩作
class PoemJpn(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default= "null")
    translator = models.CharField(max_length=255, default = "null")
    content = models.TextField()
    style = models.CharField(max_length=255, default = "null")
    book = models.ForeignKey(BookJpn, on_delete=models.CASCADE)
    page = models.PositiveIntegerField(default=0)
    feature = models.CharField(max_length=255, default = "000000")
    formatted_content = models.TextField(default = "null")
    created_by = models.CharField(max_length=255, default = "null")
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        return self.title        