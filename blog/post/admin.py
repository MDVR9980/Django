from django.contrib import admin
from . import models

class FilterByTitle(admin.SimpleListFilter):
    title = "کلید های پرتکرار"
    parameter_name = "title"

    def lookups(self, request, model_admin):
        return (
            ('android', 'اندروید'),
            ('computer', "کامپیوتر"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains = self.value())

class CommentInline(admin.TabularInline):
    model = models.Comment

# class CommentInline(admin.StackedInline):
#     model = models.Comment

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status", "show_image")
    list_editable = ("status",)
    list_filter = ("status", FilterByTitle)
    search_fields = ("body",)
    inlines = (CommentInline,)
    # fields = ["title"]

# admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Message)
admin.site.register(models.Like)