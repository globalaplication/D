#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from gi.repository import GdkPixbuf, GLib
import subprocess
HOME = os.environ['HOME']
filedict = {}
selectitem = []
pdict = {}
pdict['Ev'] = {'path':HOME, 'icon':'gtk-quit'}
pdict['Rash'] = {'path':'rash://', 'icon':'gtk-home'}
pdict['Root'] = {'path':'/', 'icon':'gtk-quit'}
pdict['Diskler'] = {'path':'/media/linuxmt', 'icon':'gtk-quit'}
def tempread():
    global star
    try:
        with open(HOME+'/.config/_filemanager_py_mt_nr.star') as temp:
            star = temp.read()
    except:
        tempwrite(HOME)
    return star
def configaddplaces(newplaces):
    with open(HOME+'/.config/_filemanager_py_mt_nr.places', 'a') as places:
        places.write(newplaces+'\n')
def tempwrite(path):
    with open(HOME+'/.config/_filemanager_py_mt_nr.star', 'w') as temp:
        temp.write(path)
def places():
    with open(HOME+'/.config/user-dirs.dirs') as pla:
        places = pla.read().splitlines()
    places = [places.replace('"','').split('/')[-1] for places in places if places.startswith('#') is False]
    for add in places:
        pdict[add] = {'path':HOME+'/'+add, 'icon':'gtk-home'}
    with open(HOME+'/.config/_filemanager_py_mt_nr.places') as pla:
        places = pla.read().splitlines()
    for add in places:
        pdict[os.path.split(add)[1]] = {'path':add, 'icon':'gtk-home'}
    return pdict
class BetaFileManager(Gtk.Window):
    (COL_PATH, FILENAME, FILEICON, COL_IS_DIRECTORY,
        NUM_COLS) = range(5)
    Path = tempread()
    IconWidth = 60
    ArrayNextBack, CountNextBack = [Path], 1
    state = False
    SelectPlacesItem = 0
    CtrL = False
    def __init__(self, BetaApp):
        self.window = Gtk.Window()
        self.window.set_default_size(900, 700)
        self.window.connect('destroy', Gtk.main_quit)
        #Context Menu
        self.menu = Gtk.Menu()
        menu_bluutooth = Gtk.MenuItem("Bluutooth")
        menu_bluutooth.connect("activate", self.callback, 'Bluutooth')
        menu_add_places = Gtk.MenuItem('Konuma Ekle')
        menu_add_places.connect("activate", self.callback, 'Konuma Ekle')
        menu_kopyala = Gtk.MenuItem("Kopyala")
        menu_kopyala.connect("activate", self.callback, 'Kopyala')
        menu_tasi = Gtk.MenuItem("Taşı")
        menu_tasi.connect("activate", self.callback, 'Taşı')
        menu_kes = Gtk.MenuItem("Kes")
        menu_kes.connect("activate", self.callback, 'Kes')
        menu_sil = Gtk.MenuItem("Sil")
        menu_sil.connect("activate", self.callback, 'Sil')
        self.menu.append(menu_sil)
        self.menu.append(menu_kopyala)
        self.menu.append(menu_tasi)
        self.menu.append(menu_kes)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(menu_bluutooth)
        self.menu.append(menu_add_places)
        self.menu.show_all()
        #Gtk HeaderBar
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        self.Headerbar.props.title = self.Path
        self.window.set_titlebar(self.Headerbar)
        #sağ taraf buton
        self.ToggleButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-stop")
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
        self.FormBox = Gtk.Box(homogeneous=False, spacing=6)
        self.window.add(self.FormBox)
        #toolbar
        self.placesstore = Gtk.ListStore(str, str)
        self.placestitle = Gtk.TreeViewColumn('Konumlar')
        self.placestreeview = Gtk.TreeView(self.placesstore)
        for addplaces in places().keys():
            self.placesstore.append([addplaces+' '*25, pdict[addplaces]['icon']])
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

        #self.diskstore = Gtk.ListStore(str, str)
        #self.disktitle = Gtk.TreeViewColumn('Konumlar')
        #self.disktreeview = Gtk.TreeView(self.diskstore)

        #for diskplaces in self.diskler():
        #    self.diskstore.append([diskplaces+' '*30, 'gtk-home'])
        #self.disktreeview.append_column(self.disktitle)
        #self.CellIcon = Gtk.CellRendererPixbuf()
        #self.CellText = Gtk.CellRendererText()
        #self.CellIcon.set_property('cell-background', 'black')
        #self.CellText.set_property('cell-background', 'black')
        #self.disktitle.pack_start(self.CellIcon, False)
        #self.disktitle.pack_start(self.CellText, True)
        #places path icon
        #self.disktitle.set_attributes(self.CellIcon, stock_id=1)
        #places path list
        #self.disktitle.set_attributes(self.CellText, text=0)
        #self.FormBox.add(self.disktreeview)

        #ScrolledWindowİCONVİEW
        self.ScrolledWindow = Gtk.ScrolledWindow()
        self.ScrolledWindow.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.ScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.FormBox.pack_start(self.ScrolledWindow, True, True, 1)
        #self.Path = '/home/linuxmt'
        self.IconViewStore = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, bool)
        self.Load(self.IconViewStore)

        self.IconView = Gtk.IconView(model=self.IconViewStore)
        self.IconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.ScrolledWindow.add(self.IconView)

        self.IconView.set_text_column(self.FILENAME)
        self.IconView.set_pixbuf_column(self.FILEICON)
        self.IconView.set_item_width(self.IconWidth)

        self.IconView.grab_focus()
        self.IconView.connect('item-activated', self.double_click, self.IconViewStore)
        self.ToggleButton.connect("toggled", self.on_button_toggled, self.IconViewStore, '1')
        self.Geri.connect('button-press-event', self.connect_FileBack, self.IconViewStore) 
        self.Ileri.connect('button-press-event', self.connect_FileNext, self.IconViewStore) 
        self.placestreeview.connect('button_press_event', self.get_selected_user, self.IconViewStore)
        self.IconView.connect('button_press_event', self.on_button_press_event, self.IconViewStore)
        self.window.connect("key-press-event", self.on_win_key_press_event)

        self.Geri.set_sensitive(False)
        self.Ileri.set_sensitive(False)
        self.window.show_all()

    def diskler(self):
        diskler = [diskler.split()[-1] for diskler in subprocess.check_output("df -h", 
                    shell=True).splitlines()[1:] if diskler.split()[-1].startswith('/media')]
        return diskler
    def runrun(self):
        for link in self.Path.split('/')[1:]:
            self.button = Gtk.ToggleButton(link, use_underline = True)
            self.button.set_active(True)
            #self.button.set_sensitive(0)
            self.button.connect("toggled", self.callback, link)
            self.button.set_border_width(0)
            self.button.show()
            self.HeaderBox.add(self.button)
    def callback(self, widget, data = None):
            if (data == 'Konuma Ekle'): configaddplaces(selectitem[-1])
    def get_selected_user(self, tv, event, IconViewStore):  
        if event.button == 1:
            pthinfo = self.placestreeview.get_path_at_pos(event.x, event.y)
            if pthinfo != None:
                (path,col,cellx,celly) = pthinfo
                self.placestreeview.grab_focus()
                self.placestreeview.set_cursor(path,col,0)
            selection = self.placestreeview.get_selection()
            (model, iter) = selection.get_selected()
        self.SelectPlacesItem = pdict[model[iter][0].split()[0]]['path']
        self.Path = self.SelectPlacesItem
        self.Headerbar.props.title = self.Path
        tempwrite(self.Path)
        self.IconViewStore.clear()
        self.Load(self.IconViewStore)
    def cb1(self):
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return True
    def on_win_key_press_event(self, widget, event):
        KlavyeButon = Gdk.keyval_name(event.keyval)
        if (KlavyeButon == 'Control_L'): 
            self.CtrL = True
            print event.button, 'ctrl'
    def on_button_press_event(self, IconView,  event, IconViewStore):
        try:
            if event.type == Gdk.EventType.BUTTON_PRESS:
                path = self.IconView.get_path_at_pos(event.x, event.y)
                if path != None and event.button == 1: 
                    selectitem.append(filedict[int(str(path))]['file'])
                    print ('select', selectitem, self.CtrL)
                elif event.button == 3:
                    self.IconView.select_path(path)
                    self.cb1()
        except:
            self.cb1()
    def haha(self, entrysearch):
        print  (self.entrysearch.get_text())
    def on_button_toggled(self, ToggleButton, IconViewStore, name):
        if self.ToggleButton.get_active():
            self.state = True
            self.IconViewStore.clear()
            self.Load(self.IconViewStore)
        else:
            self.state = False
            self.IconViewStore.clear()
            self.Load(self.IconViewStore)
    def connect_FileBack(self, IconView, path, IconViewStore):
        if self.CountNextBack > 1: self.CountNextBack = self.CountNextBack - 1
        if self.CountNextBack is 1 :             
            self.Geri.set_sensitive(False
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        if len(self.ArrayNextBack) > self.CountNextBack:
            self.Ileri.set_sensitive(True)
        self.IconViewStore.clear()
        self.Load(self.IconViewStore)
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
        self.IconViewStore.clear()
        self.Load(self.IconViewStore)
        self.Headerbar.props.title = self.Path
    def double_click(self, IconView, tree_path, IconViewStore):
        iter_ = self.IconViewStore.get_iter(tree_path)
        (path, is_dir) = self.IconViewStore.get(iter_, self.COL_PATH, self.COL_IS_DIRECTORY)
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
        self.IconViewStore.clear()
        self.Load(self.IconViewStore)
        self.runrun()
        #self.up_button.set_sensitive(True)
        if len(self.ArrayNextBack) > 1:
            self.Geri.set_sensitive(True
                )
    def Load(self, IconViewStore, indextest=0): 
        for enum, FileName in enumerate(os.listdir(self.Path),0):
            if FileName.startswith('.') is True and self.state is False:
                    indextest = indextest + 1
                    continue
            filedict[enum-indextest] = {'file':self.Path+'/'+FileName}
            self.IconViewStore.append(
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
