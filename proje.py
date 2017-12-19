#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from gi.repository import GdkPixbuf, GLib
import subprocess
HOME = os.environ['HOME']
pdict = {}
pdict['Home'] = {'path':HOME, 'icon':'gtk-quit'}
pdict['Çöp'] = {'path':'rash://', 'icon':'gtk-home'}
pdict['Root'] = {'path':'/', 'icon':'gtk-home'}
def tempread():
    global star
    try:
        with open(HOME+'/.config/_filemanager_py_mt_nr.star') as temp:
            star = temp.read()
    except:
        tempwrite(HOME)
    return star
def tempwrite(path):
    with open(HOME+'/.config/_filemanager_py_mt_nr.star', 'w') as temp:
        temp.write(path)
def places():
    with open(HOME+'/.config/user-dirs.dirs') as pla:
        places = pla.read().splitlines()
    places = [places.replace('"','').split('/')[-1] for places in places if places.startswith('#') is False]
    for add in places:
        pdict[add] = {'path':HOME+'/'+add, 'icon':'gtk-home'}
    return pdict
class BetaFileManager(Gtk.Window):
    (COL_PATH, FILENAME, FILEICON, COL_IS_DIRECTORY,
        NUM_COLS) = range(5)
    Path = tempread()
    IconWidth = 67
    ArrayNextBack, CountNextBack = [Path], 1
    state = False
    SelectPlacesItem = 0
    def __init__(self, BetaApp):
        self.window = Gtk.Window()
        self.window.set_default_size(850, 600)
        self.window.connect('destroy', Gtk.main_quit)
        #Gtk HeaderBar
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        self.Headerbar.props.title = self.Path
        self.window.set_titlebar(self.Headerbar)
        #sağ taraf buton
        self.ToggleButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-help")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.ToggleButton.add(image)
        self.Headerbar.pack_end(self.ToggleButton)
        #sağ taraf dosya arama
        self.entrysearch = Gtk.Entry()
        self.entrysearch.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            'system-search-symbolic')
        self.entrysearch.connect("changed", self.haha)
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
        #
        self.runrun()
        #formbox
        self.FormBox = Gtk.Box(homogeneous=False, spacing=5)
        self.window.add(self.FormBox)
        #toolbar
        self.placesstore = Gtk.ListStore(str, str)
        self.placestitle = Gtk.TreeViewColumn('')
        self.placestreeview = Gtk.TreeView(self.placesstore)

        for addplaces in places().keys():
            self.placesstore.append([addplaces+' '*30, pdict[addplaces]['icon']])
        self.placestreeview.append_column(self.placestitle)
        self.CellIcon = Gtk.CellRendererPixbuf()
        self.CellText = Gtk.CellRendererText()
        #self.CellIcon.set_property('cell-background', 'black')
        #self.CellText.set_property('cell-background', 'black')
        self.placestitle.pack_start(self.CellIcon, False)
        self.placestitle.pack_start(self.CellText, True)
        #places path icon
        self.placestitle.set_attributes(self.CellIcon, stock_id=1)
        #places path list
        self.placestitle.set_attributes(self.CellText, text=0)
        self.FormBox.add(self.placestreeview)

        #ScrolledWindowİCONVİEW
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
        IconView.set_text_column(self.FILENAME)
        IconView.set_pixbuf_column(self.FILEICON)
        IconView.set_item_width(self.IconWidth)
        IconView.grab_focus()
        IconView.connect('item-activated', self.double_click, IconViewStore)
        #self.ToggleButton.connect("toggled", self.on_button_toggled,IconViewStore, '1')
        self.Geri.connect('button-press-event', self.connect_FileBack, IconViewStore) 
        self.Ileri.connect('button-press-event', self.connect_FileNext, IconViewStore) 
        self.placestreeview.connect('button_press_event', self.get_selected_user, IconViewStore)
        #IconView.connect('button-press-event', self.on_button_press_event) 
        self.Geri.set_sensitive(False)
        self.Ileri.set_sensitive(False)
        self.window.show_all()

    def runrun(self):
        for link in self.Path.split('/')[1:]:
            print link
            button = Gtk.ToggleButton(link)
            button.connect("toggled", self.callback, link)
            button.set_border_width(0)
            button.show()
            self.HeaderBox.add(button)

    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        print widget.get_active()
        index = self.Path.index(widget.get_active())
        print self.path[0:index]

    def get_selected_user(self, widget, tree_path, IconViewStore):  
        SelectItem = self.placestreeview.get_selection()
        (name, value) = SelectItem.get_selected()
        self.SelectPlacesItem = pdict[name.get_value(value, 0).split()[0]]['path']
        self.Path = self.SelectPlacesItem
        self.Headerbar.props.title = self.Path
        IconViewStore.clear()
        self.Load(IconViewStore)
    def on_button_press_event(self, IconViewStore):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 3:
                print("Right CLick")
            elif event.button == 1:
                print("LEFT CLICK")
    def haha(self, entrysearch):
        print  self.entrysearch.get_text()
    def on_button_toggled(self, ToggleButton, IconViewStore, name):
        if self.ToggleButton.get_active():
            self.state = True
            IconViewStore.clear()
            self.Load(IconViewStore)
        else:
            self.state = False
            IconViewStore.clear()
            self.Load(IconViewStore)
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
    def double_click(self, IconView, tree_path, IconViewStore):
        iter_ = IconViewStore.get_iter(tree_path)
        (path, is_dir) = IconViewStore.get(iter_, self.COL_PATH, self.COL_IS_DIRECTORY)
        if (is_dir is True) : 
            tempwrite(path)
            self.ArrayNextBack.insert(self.CountNextBack, path)
            self.CountNextBack = self.CountNextBack + 1
        else:
            subprocess.call(('xdg-open', path))
        if not is_dir:
            return
        self.Path = path
        self.Headerbar.props.title = self.Path
        IconViewStore.clear()
        self.Load(IconViewStore)
        self.runrun()
        #self.up_button.set_sensitive(True)
        if len(self.ArrayNextBack) > 1:
            self.Geri.set_sensitive(True
                )
    def Load(self, IconViewStore):
        for FileName in os.listdir(self.Path):
            if FileName.startswith('.') is True and self.state is False:
                continue
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
