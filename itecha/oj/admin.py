from django.contrib import admin
from .models import Contest, Problem, Submission

try:
    from import_export.admin import ImportExportMixin
except ImportError:
    ImportExportMixin = type("ImportExportMixin", (), {})


@admin.register(Contest)
class ContestAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("title", "created_at")


@admin.register(Submission)
class SubmissionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("problem_title", "creator_name", "score", "created")
    show_full_result_count = False

    def problem_title(self, obj):
        return getattr(obj.problem, "title", None)

    def creator_name(self, obj):
        return getattr(obj.creator, "username", None)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("problem", "creator")
