import csv
import json
from random import choice

from django.conf import settings


def get_fake_data(file_name):
    print()
    with open(f'{settings.BASE_DIR / "createCSV/services/schema/fake_data"}\\{file_name}', 'r') as data:
        return json.load(data)


def get_fake_full_name():
    return get_fake_data('full name.json')


def get_fake_date():
    return get_fake_data('date.json')


def get_fake_job():
    return get_fake_data('job.json')


def get_fake_email():
    return get_fake_data('email.json')


def get_fake_company():
    return get_fake_data('company.json')


def get_specific_number_random_data(column_types):
    pass


def get_schema(csv_file_path: str, delimiter: str, quotechar: str):
    with open(csv_file_path) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter, quotechar=quotechar)
        return list(reader)[0]


def add_row_with_fake_data_to_csv_file(schema, row_number, csv_writer, delimiter, quotechar):
    map_types_to_fake_data = {
        'full name': get_fake_full_name,
        'company': get_fake_company,
        'job': get_fake_job,
        'email': get_fake_email,
        'date': get_fake_date
    }

    csv_schema = get_schema(schema.csv_file.path, delimiter, quotechar)

    needed_types_fake_data = set(csv_schema.values())
    fake_data_by_types = {}
    for type_fake_data in needed_types_fake_data:
        fake_data_by_types[type_fake_data] = map_types_to_fake_data[type_fake_data]()

    csv_writer.writerow(csv_schema.keys())
    for row in range(row_number):
        row_data = [choice(fake_data_by_types[column_type]) for column_type in csv_schema.values()]
        csv_writer.writerow(row_data)


def get_schema_data_with_column_id(schema: dict) -> list:
    schema_serial_number = 1
    schema_columns = []
    for column_name, column_type in schema.items():
        schema_columns.append({'name': column_name, 'type': column_type, 'serial_number': schema_serial_number})
        schema_serial_number += 1
    return schema_columns


# def add_schema_serial_number():