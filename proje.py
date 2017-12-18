#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from gi.repository import GdkPixbuf, GLib

class BetaFileManager(Gtk.Window):

    (COL_PATH, FILENAME, FILEICON, COL_IS_DIRECTORY,
        NUM_COLS) = range(5)

    Path = '/home'
    IconWidth = 70
    ArrayNextBack, CountNextBack = [Path], 1

    def __init__(self, BetaApp):

        self.window = Gtk.Window()
        self.window.set_default_size(650, 400)
        self.window.connect('destroy', Gtk.main_quit)
        #Gtk HeaderBar
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        self.Headerbar.props.title = self.Path
        self.window.set_titlebar(self.Headerbar)
        #sağ taraf buton
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-save-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.Headerbar.pack_end(button)
        #sağ taraf dosya arama
        self.entrysearch = Gtk.Entry()
        self.Headerbar.pack_end(self.entrysearch)
        #Sol tarfataki butonlar
        self.HeaderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.HeaderBox.get_style_context(), "linked")
        self.Geri = Gtk.Button()
        self.Geri.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.HeaderBox.add(self.Geri)
        self.Ileri = Gtk.Button()
        self.Ileri.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.HeaderBox.add(self.Ileri)
        self.Headerbar.pack_start(self.HeaderBox)
        #hederbar toogle


        #formbox
        self.FormBox = Gtk.VBox()
        self.window.add(self.FormBox)
        #toolbar
        self.Toolbar = Gtk.Toolbar()
        self.FormBox.pack_start(self.Toolbar, 0, 0, 0)
        #toolbar butonlar
        up_button = Gtk.ToolButton(stock_id=Gtk.STOCK_GO_UP)
        up_button.set_is_important(True)
        up_button.set_sensitive(False)
        self.Toolbar.insert(up_button, -1)
        home_button = Gtk.ToolButton(stock_id=Gtk.STOCK_HOME)
        home_button.set_is_important(True)
        self.Toolbar.insert(home_button, -1)
        self.ScrolledWindow = Gtk.ScrolledWindow()
        self.ScrolledWindow.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.ScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.FormBox.pack_start(self.ScrolledWindow, True, True, 1)
        #self.Path = '/home/linuxmt'
        IconViewStore = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, bool)
        self.Load(IconViewStore)

        IconView = Gtk.IconView(model=IconViewStore)
        IconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.ScrolledWindow.add(IconView)
        
        up_button.connect('clicked', self.up_clicked, IconViewStore)
        home_button.connect('clicked', self.home_clicked, IconViewStore)

        self.up_button = up_button
        self.home_button = home_button
        # we now set which model columns that correspond to the text
        # and pixbuf of each item
        IconView.set_text_column(self.FILENAME)
        IconView.set_pixbuf_column(self.FILEICON)
        IconView.set_item_width(self.IconWidth)
        IconView.grab_focus()

        # connect to the "item-activated" signal
        IconView.connect('item-activated', self.double_click, IconViewStore)
        self.Geri.connect('button-press-event', self.connect_FileBack, IconViewStore) 
        self.Ileri.connect('button-press-event', self.connect_FileNext, IconViewStore) 
    
        self.Geri.set_sensitive(False)
        self.Ileri.set_sensitive(False)

        self.window.show_all()

    def connect_FileBack(self, IconView, path, IconViewStore):
        if self.CountNextBack > 1: self.CountNextBack = self.CountNextBack - 1
        if self.CountNextBack is 1 :             
            self.Geri.set_sensitive(False
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        if len(self.ArrayNextBack) > self.CountNextBack:
            self.Ileri.set_sensitive(True)
        IconViewStore.clear()
        self.Load(IconViewStore)
        self.Headerbar.props.title = self.Path
    def connect_FileNext(self, IconView, path, IconViewStore):
        self.CountNextBack = self.CountNextBack + 1
        if self.CountNextBack is len(self.ArrayNextBack) :             
            self.Ileri.set_sensitive(False
                )
        if self.CountNextBack > 1 :             
            self.Geri.set_sensitive(True
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        IconViewStore.clear()
        self.Load(IconViewStore)
        self.Headerbar.props.title = self.Path

    def up_clicked(self, item, IconViewStore):
        self.Path = os.path.split(self.Path)[0]
        self.Load(IconViewStore)
        self.up_button.set_sensitive(self.Path != '/')
    def home_clicked(self, item, IconViewStore):
        self.Path = GLib.get_home_dir()
        self.Load(IconViewStore)
        self.up_button.set_sensitive(True)
    def double_click(self, IconView, tree_path, IconViewStore):
        iter_ = IconViewStore.get_iter(tree_path)
        (path, is_dir) = IconViewStore.get(iter_, self.COL_PATH, self.COL_IS_DIRECTORY)
        print path, is_dir
        if (is_dir is True) : 
            self.ArrayNextBack.insert(self.CountNextBack, path)
            self.CountNextBack = self.CountNextBack + 1
        if not is_dir:
            return
        self.Path = path
        self.Headerbar.props.title = self.Path
        IconViewStore.clear()
        self.Load(IconViewStore)
        self.up_button.set_sensitive(True)

        if len(self.ArrayNextBack) > 1:
            self.Geri.set_sensitive(True
                )
    def Load(self, IconViewStore):
        for FileName in os.listdir(self.Path):
            IconViewStore.append(
            (os.path.join(self.Path, FileName), 
                FileName, 
                self.FileIcon(os.path.join(self.Path, FileName)
                    ),
                os.path.isdir(os.path.join(self.Path, FileName)
                    )
                )
            )
    def FileIcon(self, path):
        fileicon = None
        giopath = Gio.file_new_for_path(path)
        query = giopath.query_info(Gio.FILE_ATTRIBUTE_STANDARD_ICON,
            Gio.FileQueryInfoFlags.NONE,
                    None)
        geticonnames = query.get_icon().get_names()
        icontheme = Gtk.IconTheme.get_default()
        for icon in geticonnames:
            try:
                fileicon = icontheme.load_icon(icon, 64, 0)
                break
            except GLib.GError:
                pass
        return fileicon
def main(BetaApp=None):
    BetaFileManager(BetaApp)
    Gtk.main()
if __name__ == '__main__':
    main()
