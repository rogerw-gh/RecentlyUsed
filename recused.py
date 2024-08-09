#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  recused.py
#  
#  Created 2022 Roger Whiteley rogerw-gh
#
#  Updated August 2024 with fixes for Ubuntu LTS 22.04
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  list of recently used expanded to 300... 31.03.2023
#
#!/usr/bin/env python3
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import GLib, Gtk, AyatanaAppIndicator3, GObject
import time
from threading import Thread
import os
import subprocess

# --- set the number of recently used files to appear below
n = 300
# ---

home = os.environ["HOME"]
recdata = os.path.join(home, "/home/rogerw/.local/share/recently-used.xbel")
currpath = os.path.dirname(os.path.realpath(__file__))

class Indicator():
    def __init__(self):
        self.app = 'show_recent'
        iconpath = os.path.join(currpath, "recent.png")
        self.indicator = AyatanaAppIndicator3.Indicator.new(
            self.app, iconpath,
            AyatanaAppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)       
        self.indicator.set_menu(self.create_menu())
        # the thread:
        self.update = Thread(target=self.check_recent)
        # daemonize the thread to make the indicator stopable
        self.update.daemon = True
        self.update.start()

    def get_files(self):
        # create the list of recently used files
        used = [l for l in open(recdata) if \
                all([
                    '<bookmark href="file://' in l,
                    not "/tmp" in l,
                    "." in l,
                     ])]
        relevant = [l.split('="') for l in set(used)]
        relevant = [[it[1][7:-7], it[-2][:-10]] for it in relevant]
        relevant.sort(key=lambda x: x[1])
        return [item[0].replace("%20", " ") for item in relevant[::-1][:n]]

    def create_menu(self):
        # creates the (initial) menu
        self.menu = Gtk.Menu()
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        self.menu.append(menu_sep)
        # item_quit.show() 
        self.menu.show_all()
        return self.menu

    def open_file(self, *args):
        # opens the file with the default application
        index = self.menu.get_children().index(self.menu.get_active())
        selection = self.menu_items2[index]
        subprocess.Popen(["xdg-open", selection])

    def set_new(self):
        # update the list, appearing in the menu
        for i in self.menu.get_children():
            self.menu.remove(i)
        for file in self.menu_items2:
            sub = Gtk.MenuItem.new_with_label(file)
            self.menu.append(sub)
            sub.connect('activate', self.open_file)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        self.menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem.new_with_label('Quit')
        item_quit.connect('activate', self.stop)
        self.menu.append(item_quit)
        self.menu.show_all()

    def check_recent(self):
        self.menu_items1 = []
        while True:
            time.sleep(3)
            self.menu_items2 = self.get_files()
            if self.menu_items2 != self.menu_items1:
                GLib.idle_add(
                    self.set_new, 
                    priority=GLib.PRIORITY_DEFAULT
                    )
            self.menu_items1 = self.menu_items2

    def stop(self, source):
        Gtk.main_quit()

Indicator()
# this is where we call GObject.threads_init()
#GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
