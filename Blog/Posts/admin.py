from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'timestamp']
	#list_display_links = ('first_name', 'last_name')
	#list_filter = ('is_staff', 'company')
	#ordering = ['date_created']
    #search_fields = ['question_text']
	class Meta:
		model = Post
		
admin.site.register(Post, PostAdmin)