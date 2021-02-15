from django.contrib import admin
from .models import Problem, Submission

try:
    from import_export.admin import ImportExportMixin
except ImportError:
    ImportExportMixin = type("ImportExportMixin", (), {})


@admin.register(Problem)
class ProblemAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(ImportExportMixin, admin.ModelAdmin):
    pass
