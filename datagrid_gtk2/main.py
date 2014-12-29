# -*- coding: utf-8 -*-

"""Main module of the datagrid_gtk2 package, used to start an example."""

import logging
import sys
import os

import pygtk
pygtk.require('2.0')

import gtk
import gobject

from ui.grid import DataGridContainer, DataGridController
from db.sqlite import SQLiteDataSource
from db import EmptyDataSource

logger = logging.getLogger(__name__)


def setup_logging():
    """Sets up logging to std out."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)


def main():
    """Example usage of the datagrid-gtk2 package."""
    logger.info("Starting a datagrid-gtk2 example.")

    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           os.path.pardir, 'example_data', 'chinook.sqlite')

    win = gtk.Window()
    datagrid_container = DataGridContainer(win)
    controller = DataGridController(datagrid_container,
                                    EmptyDataSource(),
                                    has_checkboxes=False)
    datagrid_container.grid_vbox.reparent(win)

    win.set_default_size(600, 400)
    win.connect("delete-event", lambda *args: gtk.main_quit())
    win.show()

    tables = gtk.Window()
    tables.set_title("Choose a table")

    table_list = gtk.TreeView()
    column = gtk.TreeViewColumn("")
    table_list.append_column(column)
    cell = gtk.CellRendererText()
    column.pack_start(cell, True)
    column.add_attribute(cell, 'text', 0)

    table_store = gtk.ListStore(str)
    for item in "album artist employee genre track".split():
        table_store.append([item])
    table_list.set_model(table_store)

    def select_table(selection):
        model, iterator = selection.get_selected()
        if iterator:
            table_name = model[iterator][0]
            controller.bind_datasource(SQLiteDataSource(
                db_path, table_name,
                ensure_selected_column=False, display_all=True
            ))
    table_list.get_selection().connect("changed", select_table)

    tables.add(table_list)
    tables.set_default_size(300, 400)
    gobject.idle_add(tables.show_all)

    gtk.main()


if __name__ == '__main__':
    setup_logging()
    main()