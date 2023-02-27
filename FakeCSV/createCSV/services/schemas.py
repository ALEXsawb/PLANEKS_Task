from django.urls import reverse

from ..models import SchemaModel


def get_schemas_completed_for_template(owner):
    schema_serial_number = 1
    schemas = SchemaModel.objects.filter(owner=owner).values('pk', 'title', 'date_update').order_by('-date_create')
    for schema in schemas:
        schema['serial_number'] = schema_serial_number
        schema['get_absolute_url'] = reverse('schema', kwargs={'pk': schema['pk']})
        schema_serial_number += 1
    return schemas
