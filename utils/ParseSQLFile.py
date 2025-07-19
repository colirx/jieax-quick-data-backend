import json
import os

import sqlparse
from simple_ddl_parser import DDLParser

from pojo.SQLPojo import Column, Reference, Table, Type


def parse(file_name, work_dir=None):
    tables = init_tables(file_name, work_dir)
    references = init_reference_nodes(tables)

def init_tables(file_name, work_dir):
    if not work_dir:
        work_dir = os.getcwd().replace('\\', '/')
    sql = ''
    with open(f'{work_dir}/uploads/{file_name}', 'r', encoding='utf-8') as f:
        sql = f.read()
        f.close()
    if not sql:
        raise Exception('sql is empty')
    tables = []
    # noinspection PyTypeChecker
    for table_json in json.loads(DDLParser(sql).run(json_dump=True)):
        table_name = table_json['table_name']
        uniques = table_json['primary_key']
        columns = []
        for column_json in table_json['columns']:
            column_name = column_json['name']
            column_type = column_json['type']
            column_size = int(column_json['size']) if column_json['size'] else 0
            column_unique = column_json['unique']
            column_unique = (column_unique and column_unique == 'true') or (column_name in uniques)
            column_nullable = column_json['nullable']
            column_nullable = (column_nullable and column_nullable == 'true')
            column_default = column_json['default']
            column_comment = column_json['comment']
            column_comment = column_comment.encode().decode('unicode_escape')
            # column_comment 去除两边的 '
            column_comment = column_comment[1:-1]
            column_reference = column_json['references']
            column = Column(column_name, column_type, column_size, column_unique, column_nullable, column_default, column_comment)
            if column_type == Type.DECIMAL:
                column_s_size = int(column_json['s_size']) if column_json['s_size'] else 0
                column.s_size = column_s_size
            if column_reference:
                column_reference_table = column_reference['table']
                column_reference_column = column_reference['column']
                reference = Reference(column_reference_table, column_reference_column)
                column.reference = reference
            columns.append(column)
        comment = table_json['comment'] if 'comment' in table_json else None
        comment = comment.encode().decode('unicode_escape') if comment else None
        tables.append(Table(table_name, columns, comment))
    return tables


def init_reference_nodes(tables):
    references = []

parse('INIT_DDL.sql', 'D:/workspace/jieax/jieax-quick-data-backend/')
