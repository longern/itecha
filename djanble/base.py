import re
from itertools import chain

import tablestore
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.sqlite3.base import (
    Database,
    DatabaseWrapper as Sqlite3DatabaseWrapper,
)


def do_nothing(*args, **kwargs):
    pass


def row_as_dict(row: tablestore.Row) -> dict:
    row_dict = {}
    for item in chain(row.primary_key, row.attribute_columns):
        key, value, *_ = item
        row_dict[key] = value
    return row_dict


class Cursor:
    def __init__(self, conn):
        self.conn: tablestore.OTSClient = conn

    def select(self, sql, params):
        sql = re.sub(" LIMIT \d*$", "", sql)
        sql = re.sub(" ORDER BY [^ ]*( (ASC|DESC))?$", "", sql)
        select_match = re.match(
            'SELECT (.*) FROM "([^ ]*)"(?: WHERE "(.*)"\."id" = %s)?$', sql
        )
        if not select_match:
            raise ValueError(sql)
        table_name = select_match.groups()[1]
        columns = [
            re.sub(".*\.", "", column)[1:-1]
            for column in select_match.groups()[0].split(", ")
        ]
        if select_match.groups()[2]:
            _, row, _ = self.conn.get_row(
                table_name, [("_partition", 0), ("id", params[0])]
            )
            row_list = [row]
        else:
            consumed, next_primary_key, row_list, _ = self.conn.get_range(
                table_name,
                "FORWARD",
                [("_partition", 0), ("id", tablestore.INF_MIN)],
                [("_partition", 0), ("id", tablestore.INF_MAX)],
            )

        result = []
        for row in row_list:
            row_dict = row_as_dict(row)
            result.append([row_dict.get(column, None) for column in columns])

        self.rowcount = len(result)
        self.result = iter(result)

    def insert(self, sql: str, params):
        insert_match = re.match('INSERT INTO "([^ ]*)" \([^)]*\) VALUES \(.*\)$', sql)
        if not insert_match:
            raise ValueError(sql)

        table_name = insert_match.groups()[0]
        primary_keys = [("_partition", 0), ("id", tablestore.PK_AUTO_INCR)]
        consumed, return_row = self.conn.put_row(
            table_name,
            tablestore.Row(primary_keys, []),
            return_type=tablestore.ReturnType.RT_PK,
        )

        self.lastrowid = row_as_dict(return_row)["id"]
        self.rowcount = 1

    def update(self, sql: str, params):
        insert_match = re.match(
            'UPDATE "([^ ]*)" SET ((?:"(?:[^"]*)" = (?:%s|NULL),? )+)WHERE ".*"\."id" = %s$',
            sql,
        )
        if not insert_match:
            raise ValueError(sql)

        params_iter = iter(params)

        assignments = {}
        for assignment_expr in insert_match.groups()[1].split(","):
            lhs, rhs = assignment_expr.strip().split(" = ")
            if rhs == "%s":
                param = next(params_iter)
                if isinstance(param, memoryview):
                    param = bytearray(param)
                assignments[lhs.strip('"')] = param
            elif rhs.upper() == "NULL":
                assignments[lhs.strip('"')] = None

        table_name = insert_match.groups()[0]
        primary_keys = [("_partition", 0), ("id", params[-1])]
        row = tablestore.Row(primary_keys, {"PUT": list(assignments.items())})
        self.conn.update_row(table_name, row, tablestore.Condition("EXPECT_EXIST"))

        self.rowcount = 1

    def execute(self, sql: str, params=None):
        self.result = []
        statement = sql.split()[0].lower()
        print(sql, params)

        if not hasattr(self, statement):
            raise ValueError("Statement not supported.")

        return getattr(self, statement)(sql, params)

    def fetchmany(self, size=1):
        ret = []
        for _ in range(size):
            try:
                ret.append(next(self.result))
            except StopIteration:
                break
        return ret

    def fetchone(self):
        return next(self.result)

    close = do_nothing


class DatabaseIntrospection(BaseDatabaseIntrospection):
    def table_names(self, cursor: Cursor, include_views=False):
        return cursor.conn.list_table()


class DatabaseOperations(BaseDatabaseOperations):
    def quote_name(self, name):
        if name.startswith('"') and name.endswith('"'):
            return name
        return '"{}"'.format(name)


class DatabaseFeatures(BaseDatabaseFeatures):
    uses_savepoints = False
    atomic_transactions = False


class DatabaseWrapper(BaseDatabaseWrapper):
    introspection_class = DatabaseIntrospection
    client_class = BaseDatabaseClient
    creation_class = BaseDatabaseCreation
    features_class = DatabaseFeatures
    ops_class = DatabaseOperations

    Database = Database
    operators = Sqlite3DatabaseWrapper.operators

    SchemaEditorClass = BaseDatabaseSchemaEditor

    def get_connection_params(self) -> None:
        settings_dict: dict = self.settings_dict
        protocol = "https"
        kwargs = {
            "end_point": f"{protocol}://{settings_dict['HOST']}",
            "access_key_id": self.settings_dict["USER"],
            "access_key_secret": self.settings_dict["PASSWORD"],
            "instance_name": self.settings_dict["NAME"],
        }
        return kwargs

    def get_new_connection(self, conn_params):
        self.conn = tablestore.OTSClient(**conn_params)
        return self.conn

    def create_cursor(self, name) -> None:
        return Cursor(self.conn)

    init_connection_state = do_nothing
    set_autocommit = do_nothing
    commit = do_nothing
    rollback = do_nothing
    close = do_nothing
