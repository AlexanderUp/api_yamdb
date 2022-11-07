from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug",)
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category", "description",)
    list_select_related = ("category",)
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "title", "pub_date", "score",)
    list_select_related = ("author", "title",)
    search_fields = ("title", "author",)
    list_filter = ("title", "author", "pub_date", "score",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "review", "pub_date",)
    list_select_related = ("author", "review",)
    search_fields = ("title", "author",)
    list_filter = ("review", "author", "pub_date",)
    empty_value_display = "-пусто-"


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "genre", "title",)
    list_select_related = ("genre", "title",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
