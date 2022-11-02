from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'pub_date')
    search_fields = ('title', 'author')
    list_filter = ('review', 'author', 'pub_date')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'pub_date', 'score')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author', 'pub_date', 'score')
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title)
