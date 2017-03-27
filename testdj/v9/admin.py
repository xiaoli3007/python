from django.contrib import admin
from models import Testse
# Register your models here.
class TestseAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'filepath')


admin.site.register(Testse, TestseAdmin)