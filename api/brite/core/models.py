from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RiskType(BaseModel):
    """Model for a generic risk specification."""

    # Fields
    description = models.TextField()
    name = models.CharField(max_length=191, db_index=True)
    user = models.ForeignKey(
        User,
        editable=False,
        on_delete=models.CASCADE,
        related_name='risk_types'
    )

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a single RiskType instance."""
        return reverse('risk_type-detail', args=[self.pk])

    def __str__(self):
        """String representing RiskType."""
        return self.name


class FieldType(models.Model):
    """Model for a generic risk specification."""
    CURRENCY = 'currency'
    DATE = 'date'
    ENUM = 'enum'
    NUMBER = 'number'
    TEXT = 'text'

    KINDS = (
        (CURRENCY, 'Currency'),
        (DATE, 'Date'),
        (ENUM, 'Enum'),
        (NUMBER, 'Number'),
        (TEXT, 'Text'),
    )

    # Fields
    kind = models.CharField(choices=KINDS, max_length=19)
    name = models.CharField(max_length=191, db_index=True)
    options = models.CharField(max_length=1024, null=True)
    required = models.BooleanField(default=True)
    risk_type = models.ForeignKey(
        RiskType,
        on_delete=models.CASCADE,
        related_name='field_types'
    )

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a single RiskType instance."""
        return reverse('field_type-detail', args=[self.pk])

    def __str__(self):
        """String representing RiskType."""
        return self.name


class Risk(BaseModel):
    """Model for a generic risk entry."""
    # Fields
    client = models.CharField(max_length=191, db_index=True)
    risk_type = models.ForeignKey(
        RiskType, on_delete=models.CASCADE, related_name='risks')

    # Metadata
    class Meta:
        ordering = ['client']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a single Risk entry."""
        return reverse('risk-detail', args=[self.pk])

    def __str__(self):
        """String representing RiskType."""
        return f'{self.client} ({self.risk_type.name})'


class Field(models.Model):
    """Model for a generic field entry."""
    # Fields
    field_type = models.ForeignKey(
        FieldType, on_delete=models.CASCADE, related_name='fields')
    risk = models.ForeignKey(
        Risk, on_delete=models.CASCADE, related_name='fields')
    value = models.CharField(max_length=191, db_index=True)

    # Metadata
    class Meta:
        ordering = ['risk', 'field_type']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a single Risk entry."""
        return reverse('field-detail', args=[self.pk])

    def __str__(self):
        """String representing RiskType."""
        return f'{self.value}'
