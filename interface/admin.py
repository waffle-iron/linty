from django.contrib import admin

from interface.models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    class Meta:
        model = Result
