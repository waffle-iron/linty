from django.contrib import admin

from interface.models import Result


class ResultAdmin(admin.ModelAdmin):
    class Meta:
        model = Result
