from django.db import models
import uuid
# Create your models here.


class DataSyncTestBooleanModel(models.Model):
    boolean_field = models.BooleanField(default=False)


class DataSyncTestEmailModel(models.Model):
    email_field = models.EmailField(max_length=254)


class DataSyncTestCharModel(models.Model):
    # Define choices as a tuple of tuples
    CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    ]

    char_field = models.CharField(max_length=100)
    choice_field = models.CharField(
        max_length=20, choices=CHOICES, default='option1')


class DataSyncTestDecimalModel(models.Model):
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2)


class DataSyncTestFloatModel(models.Model):
    float_field = models.FloatField()


class DataSyncTestIntegerModel(models.Model):
    integer_field = models.IntegerField()


class DataSyncTestUUIDModel(models.Model):
    uuid_field = models.UUIDField(
        default=uuid.uuid4, unique=True)


class DataSyncTestPositiveBigIntegerModel(models.Model):
    positive_big_integer_field = models.PositiveBigIntegerField()


class DataSyncTestPositiveIntegerModel(models.Model):
    positive_integer_field = models.PositiveIntegerField()


class DataSyncTestPositiveSmallIntegerModel(models.Model):
    positive_small_integer_field = models.PositiveSmallIntegerField()


class DataSyncTestSmallIntegerModel(models.Model):
    small_integer_field = models.SmallIntegerField()


class DataSyncTestBigIntegerModel(models.Model):
    big_integer_field = models.BigIntegerField()


class DataSyncTestDateModel(models.Model):
    date_field = models.DateField()


class DataSyncTestDateTimeModel(models.Model):
    date_time_field = models.DateTimeField()


class DataSyncTestTimeModel(models.Model):
    time_field = models.TimeField()


class DataSyncTestTextModel(models.Model):
    text_field = models.TextField()


class DataSyncTestSlugModel(models.Model):
    slug_field = models.SlugField(max_length=50)


class DataSyncTestURLModel(models.Model):
    url_field = models.URLField(max_length=200)


class DataSyncTestIPAddressModel(models.Model):
    ip_address_field = models.GenericIPAddressField()


class DataSyncTestGenericIPAddressModel(models.Model):
    generic_ip_address_field = models.GenericIPAddressField()


class DataSyncTestBinaryModel(models.Model):
    binary_field = models.BinaryField()


class DataSyncTestDurationModel(models.Model):
    duration_field = models.DurationField()


class DataSyncTestJSONModel(models.Model):
    json_field = models.JSONField(default=dict)


class DataSyncTestForeignKeyModel(models.Model):
    uuid_field = models.ForeignKey(
        DataSyncTestUUIDModel, on_delete=models.CASCADE,
        related_name="DataSyncTestForeignKeyModel_char_field"
    )
    integer_field = models.ForeignKey(
        DataSyncTestIntegerModel, on_delete=models.CASCADE,
        related_name="DataSyncTestForeignKeyModel_integer_field"
    )


class DataSyncTestOneToOneModel(models.Model):
    uuid_field = models.OneToOneField(
        DataSyncTestUUIDModel, on_delete=models.CASCADE,
        related_name="DataSyncTestOneToOneModel_char_field"
    )


class DataSyncTestManyToManyModel(models.Model):
    uuid_field = models.ManyToManyField(
        DataSyncTestUUIDModel,
        related_name="DataSyncTestManyToManyModel_char_field"
    )
