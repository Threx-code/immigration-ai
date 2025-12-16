from log_entry.models import LogEntry
from log_entry.factories.factories import LogEntryFactory

class LogEntrySeeder:
    def seed(self, count=1000):

        for _ in range(count):
            LogEntryFactory()
