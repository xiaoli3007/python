#coding:utf-8
from django.contrib import admin
from models import User,Blog,Photo,PhotoData
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('name','url','blognums')

class UserInline(admin.TabularInline):
    model = User

class BlogAdmin(admin.ModelAdmin):
    inlines = [UserInline]  # Inline
    list_display = ('title',)

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    inlines = [UserInline]  # Inline
    list_display = ('title',)

class PhotoDataAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'filepath')


admin.site.register(User, UserAdmin)
admin.site.register(Blog)
admin.site.register(Photo)
admin.site.register(PhotoData)
