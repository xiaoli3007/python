#coding:utf-8
from django.contrib import admin
from models import User, Blog, Photo, PhotoData, BlogPhoto, Video, Book
# Register your models here.


class BlogInline(admin.TabularInline):
    model = Blog
#
class PhotoInline(admin.TabularInline):
    model = Photo

class UserAdmin(admin.ModelAdmin):
    # inlines = [BlogInline, PhotoInline]
    fields = ('name', 'url', 'blognums')
    list_display = ('name','url','blognums')

class BlogAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)

class PhotoDataAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'filepath')

class BlogPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'local_default_image')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'filepath', 'thumb', 'add_time')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'filepath')
    search_fields = ('title',)

admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoData, PhotoDataAdmin)
admin.site.register(BlogPhoto, BlogPhotoAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Book, BookAdmin)
