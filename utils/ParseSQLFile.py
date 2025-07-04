import os

import sqlparse
from simple_ddl_parser import DDLParser


def parse(file_name):
    work_dir = os.getcwd().replace('\\', '/')
    with open(f'{work_dir}/uploads/{file_name}', 'r', encoding='utf-8') as f:
        sql = f.read()
        parser = DDLParser(sql).run(json_dump=True)
        print( parser)