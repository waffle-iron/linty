from django.contrib import admin

from interface.models import Build, Repo


@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    class Meta:
        model = Repo


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    class Meta:
        model = Build
