import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.base import ContentFile
from django.urls import reverse

from .services.schema.schema import add_row_with_fake_data_to_csv_file

AUTH_USER_MODEL = get_user_model()


class SchemaModel(models.Model):
    title = models.CharField(max_length=50)
    csv_file = models.FileField(blank=True)
    delimiter = models.CharField(max_length=5, null=True)
    quotechar = models.CharField(max_length=5, null=True)
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        content = self.get_csv_file_content(columns=kwargs.pop('columns'))
        self.csv_file.name = f'{self.owner.pk}/{self.title}.csv'
        self.csv_file.save(self.csv_file.name, content, kwargs)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('schema', kwargs={'pk': self.pk})

    def get_csv_file_content(self, columns):
        columns.sort(key=lambda x: x['order'])
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer, delimiter=self.delimiter, quotechar=self.quotechar)
        csv_writer.writerow([column['column_name'] for column in columns])
        csv_writer.writerow([column['column_type'] for column in columns])
        return ContentFile(csv_buffer.getvalue().encode('utf-8'))


class CreatedCSV(models.Model):
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE)
    file = models.FileField(blank=True)
    date_create = models.DateField(auto_now_add=True, null=True )

    def save(self, *args, **kwargs):
        content = self.get_csv_file_content(row_number=kwargs.pop('row_number'))
        self.file.name = f'{self.schema.owner.pk}/created/{self.schema.title}.csv'
        self.file.save(self.file.name, content, kwargs)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('download_csv', kwargs={'pk': self.pk})

    def get_csv_file_content(self, row_number):
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer, delimiter=self.schema.delimiter, quotechar=self.schema.quotechar)
        add_row_with_fake_data_to_csv_file(schema=self.schema, row_number=row_number, csv_writer=csv_writer,
                                           delimiter=self.schema.delimiter,
                                           quotechar=self.schema.quotechar)
        return ContentFile(csv_buffer.getvalue().encode('utf-8'))
