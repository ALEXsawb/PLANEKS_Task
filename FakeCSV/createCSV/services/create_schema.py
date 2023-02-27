import re
from typing import Tuple

from ..forms import CreateSchemas, EmptySchemaColumn


def get_cleared_data_from_request(request_data: dict,
                                  schema_dat_form_name: str = 'schema_data',
                                  columns_form_name: str = 'columns') -> Tuple[dict]:
    schema_data = {}
    columns_data = {}
    for key, value in request_data.items():
        if schema_dat_form_name in key:
            schema_data[re.search(r"\[(.*?)\]", key).group(1)] = value
        elif columns_form_name in key:
            id_ = re.search(r"\[(.*?)\]", key).group(1)
            column_key_name = re.search(r"\[(.*?)\]", key.split(f'{id_}]')[1]).group(1)
            if id_ not in columns_data:
                columns_data[id_] = {}
            columns_data[id_][column_key_name] = value
        else:
            raise ValueError(f'Request data must not contain this field - {key}')

    schema = CreateSchemas(schema_data)
    if not schema.is_valid():
        raise ValueError(f'Schema form got invalid data')

    columns = []
    for column_id, column in columns_data.items():
        column_clear_data = EmptySchemaColumn(column)
        columns.append(column)
        if not column_clear_data.is_valid():
            raise ValueError(f'Column field got invalid data')

    return schema_data, columns
