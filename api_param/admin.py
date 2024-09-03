from django.contrib import admin

from .models import (
    Param,
    Keyword,
    Email,
    ParamKeyword,
    ParamEmail,
)


class ParamKeywordInline(admin.TabularInline):
    model = ParamKeyword
    extra = 1
    pass

class ParamEmailInline(admin.TabularInline):
    model = ParamEmail
    extra = 1
    pass


@admin.register(Param)
class ParamAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'relevant', 'source', 'forum', 'created_at', 'updated_at')
    inlines = (ParamKeywordInline, ParamEmailInline)
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', 'created_at', 'updated_at')
    pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at', 'updated_at')
    pass


@admin.register(ParamKeyword)
class ParamKeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'param', 'keyword', 'created_at', 'updated_at')
    pass


@admin.register(ParamEmail)
class ParamEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'param', 'email', 'created_at', 'updated_at')
    pass
