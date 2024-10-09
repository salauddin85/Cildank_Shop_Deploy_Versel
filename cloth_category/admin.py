from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Sub_Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']

class Sub_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Sub_Category,Sub_CategoryAdmin)