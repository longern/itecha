from django.contrib.admin.models import LogEntry, LogEntryManager

# Change the model manager to one that doesn't log
class NoLogEntryManager(LogEntryManager):
    """The No LogEntry Model Manager."""

    def __init__(self, model=None):
        super().__init__()
        self.model = model

    def log_action(self, *args, **kwargs):
        pass

    def get_queryset(self):
        # No queries
        return super().get_queryset().none()


LogEntry.objects = NoLogEntryManager(LogEntry)
