from contextlib import closing
import sqlite3
import tempfile

from datagrid_gtk3.ui.grid import default_get_full_path


TEST_DATA = {
    'people': {
        'metadata': [
            ('__id', 'INTEGER PRIMARY KEY'),
            ('first_name', 'TEXT'),
            ('last_name', 'TEXT'),
            ('age', 'INTEGER'),
            ('start_date', 'INTEGER'),
            ('image_path', 'TEXT')
        ],
        'data': [
            (1, 'Dee', 'Timberlake', 30, 1286755200,
             'file://' + default_get_full_path('icons/image.png')),
            (2, 'Steve', 'Austin', 35, 1318291200,
             'file://' + default_get_full_path('icons/calendar22.png')),
            (3, 'Oscar', 'Goldman', 50, 1349913600, None)
        ]
    },
    'files': {
        'metadata': [
            ('__id', 'TEXT PRIMARY KEY'),
            ('__parent', 'TEXT'),
            ('filename', 'TEXT'),
            ('flatname', 'TEXT'),
            ('children_len', 'INTEGER'),
        ],
        'data': [
            # The structure here is:
            #   file-0
            #   file-1
            #   folder-0/
            #       file-0-0
            #       file-0-1
            #   folder-1/
            #       file-1-0
            #       file-1-1
            #       folder-1-0
            #           file-1-0-0
            ('file-0', None,
             'file-0', 'file-0', 0),
            ('file-1', None,
             'file-1', 'file-1', 0),
            ('folder-0', None,
             'folder-0', 'folder-0', 2),
            ('folder-1', None,
             'folder-1', 'folder-1', 3),
            ('file-0-0', 'folder-0',
             'file-0-0', 'folder-0/file-0-0', 0),
            ('file-0-1', 'folder-0',
             'file-0-1', 'folder-0/file-0-1', 0),
            ('file-1-0', 'folder-1',
             'file-1-0', 'folder-1/file-1-0', 0),
            ('file-1-1', 'folder-1',
             'file-1-1', 'folder-1/file-1-1', 0),
            ('folder-1-0', 'folder-1',
             'folder-1-0', 'folder-1/folder-1-0', 1),
            ('file-1-0-0', 'folder-1-0',
             'file-1-0-0', 'folder-1-0/file-1-0-0', 0),
        ]
    },
}


def create_db(database):
    """Create a test SQLite DB for use with data grid tests.

    :param str database: one of :mod:`.TEST_DATA` keys
    :return: path to created DB temporary file
    :rtype: str
    """
    test_data = TEST_DATA[database]

    with tempfile.NamedTemporaryFile(delete=False) as fi:
        with closing(sqlite3.connect(fi.name)) as conn:
            with closing(conn.cursor()) as cursor:
                columns = [' '.join(md) for md in test_data['metadata']]
                cursor.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (
                    database, ', '.join(columns)))

                columns_names = [md[0] for md in test_data['metadata']]
                for data in test_data['data']:
                    insert_sql = "INSERT INTO %s (%s) VALUES (%s)" % (
                        database, ', '.join(columns_names),
                        (', '.join('?' for i in columns_names)))
                    cursor.execute(insert_sql, data)
                conn.commit()
    return fi.name
