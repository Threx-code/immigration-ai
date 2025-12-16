import random
import uuid
import factory
from django.utils import timezone
from faker import Faker

from log_entry.models import LogEntry

fake = Faker()

class LogEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LogEntry

    id = factory.LazyFunction(uuid.uuid4)
    level = factory.LazyAttribute(lambda _: fake.random_element(elements=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']))
    logger_name = factory.LazyAttribute(lambda _: fake.word())
    message = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
    timestamp = factory.LazyFunction(lambda: timezone.now() - timezone.timedelta(days=random.randint(0, 30)))
    pathname = factory.LazyAttribute(lambda _: fake.file_path())
    lineno = factory.LazyAttribute(lambda _: random.randint(1, 1000))  # safe int
    func_name = factory.LazyAttribute(lambda _: fake.word())
    process = factory.LazyAttribute(lambda _: random.randint(1, 2_000_000_000))  # avoid overflow
    thread = factory.LazyAttribute(lambda _: fake.word())

