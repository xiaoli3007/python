#coding:utf-8
from django.contrib import admin
from models import User,Blog,Photo,PhotoData
# Register your models here.


class BlogInline(admin.TabularInline):
    model = Blog
#
class PhotoInline(admin.TabularInline):
    model = Photo

class UserAdmin(admin.ModelAdmin):
    inlines = [BlogInline, PhotoInline]
    list_display = ('name','url','blognums')

class BlogAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)

class PhotoDataAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'filepath')


admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoData, PhotoDataAdmin)
