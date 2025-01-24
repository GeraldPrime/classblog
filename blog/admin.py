from django.contrib import admin
from .models import Post,Category

# admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'date_posted', 'content', 'image')  # Display columns in the post list view
    list_filter = ('category',)  # Add filter by category in the sidebar
    search_fields = ('title', 'content')  # Enable searching by title and content
    

admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Customize columns in the list view
    search_fields = ('name',)  # Enable searching by category name
    list_filter = ('name',)  # Add filter options based on category name
    
# admin.site.register(Category)
admin.site.register(Category,CategoryAdmin)
