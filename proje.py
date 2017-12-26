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
pdict['Ev'] = {'path':HOME, 'icon':'gtk-quit', 'main':True}
pdict['Root'] = {'path':'/', 'icon':'gtk-quit', 'main':True}
pdict['Diskler'] = {'path':'/media', 'icon':'gtk-quit', 'main':True}

def ConfigDeletePlaces(string, NewConfigData=''):
    with open(HOME+'/.config/_filemanager_py_mt_nr.places') as delete:
        test = delete.read()
    for j in test.splitlines():
        if j.startswith(string) is True:
            continue
        NewConfigData = NewConfigData + j + '\n'
    with open(HOME+'/.config/_filemanager_py_mt_nr.places', 'w') as places:
        places.write(NewConfigData)
def TempRead():
    with open(HOME+'/.config/_filemanager_py_mt_nr.star') as temp:
        star = temp.read().replace('\n', '')
    return star
def TempWrite(path):
    with open(HOME+'/.config/_filemanager_py_mt_nr.star', 'w') as temp:
        temp.write(path)
def ConfigAddPlaces(keys, value, icon, main):
    with open(HOME+'/.config/_filemanager_py_mt_nr.places') as oku:
        test = oku.read()
    if test.find(keys+',') is -1:
        with open(HOME+'/.config/_filemanager_py_mt_nr.places', 'a') as places:
            places.write(keys+','+value+','+icon+','+str(main)+'\n')
def LoadPlaces():
    with open(HOME+'/.config/user-dirs.dirs') as pla:
        places = pla.read().splitlines()
    places = [places.replace('"','').split('/')[-1] for places in places if places.startswith('#') is False]
    for add in places:
        ConfigAddPlaces(HOME+'/'+add, add, 'gtk-home', True)
    with open(HOME+'/.config/_filemanager_py_mt_nr.places') as pla:
        places = pla.read().splitlines()
    for add in places:
        pdict[add.split(',')[1]] = {'path':add.split(',')[0], 'icon':add.split(',')[2], 'main':add.split(',')[3]}
    print pdict
    return pdict

class BetaFileManager(Gtk.Window):

    (COL_PATH, FILENAME, FILEICON, COL_IS_DIRECTORY,
        NUM_COLS) = range(5)
    Path = TempRead()
    IconWidth = 60
    ArrayNextBack, CountNextBack = [Path], 1
    state = False
    SelectPlacesItem = 0
    CtrL = False
    SelectPlacesItemIter = 0
    SelectPlacesItemChangePdict = {}

    def __init__(self, BetaApp):
        self.window = Gtk.Window()
        self.window.set_default_size(750, 700)
        self.window.connect('destroy', Gtk.main_quit)

        self.menu = Gtk.Menu()
        MenuKonumlarSil = Gtk.MenuItem("Sil")
        MenuKonumlarSil.connect("activate", self.PlacesTreeViewFonksiyon, 'Sil')
        MenuKonumlarDegistir = Gtk.MenuItem("Değiştir")
        MenuKonumlarDegistir.connect("activate", self.PlacesTreeViewFonksiyon, 'Değiştir')
        self.menu.append(MenuKonumlarDegistir)
        self.menu.append(MenuKonumlarSil)
        self.menu.show_all()

        #Gtk HeaderBar
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        #self.Headerbar.props.title = self.Path
        self.window.set_titlebar(self.Headerbar)

        #sağ taraf buton
        self.ToggleButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-stop")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.ToggleButton.add(image)
        self.Headerbar.pack_end(self.ToggleButton)

        self.ButtonAdd = Gtk.Button()
        icon = Gio.ThemedIcon(name="gtk-home")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.ButtonAdd.add(image)
        self.Headerbar.pack_end(self.ButtonAdd)

        #sağ taraf dosya arama
        self.entrysearch = Gtk.Entry()
        self.entrysearch.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            'system-search-symbolic')
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
    
        self.FormBox = Gtk.Box(homogeneous=False, spacing=3)
        self.window.add(self.FormBox)


        self.PlacesStore = Gtk.ListStore(str, str)
        for addplaces in LoadPlaces().keys():
            self.PlacesStore.append([addplaces, pdict[addplaces]['icon']])
        self.PlacesTreeView = Gtk.TreeView(self.PlacesStore)
        self.PlacesColumn = Gtk.TreeViewColumn('Konumlar'+' '*40)
        self.PlacesTreeView.append_column(self.PlacesColumn)
        self.CellIcon = Gtk.CellRendererPixbuf()
        self.CellText = Gtk.CellRendererText()
        #self.CellText.set_property("editable", True)
        self.PlacesColumn.pack_start(self.CellIcon, False)
        self.PlacesColumn.pack_start(self.CellText, True)
        self.PlacesColumn.set_attributes(self.CellIcon, stock_id=1)
        self.PlacesColumn.set_attributes(self.CellText, text=0)
        self.PlacesTreeView.set_activate_on_single_click(True) 
        self.FormBox.add(self.PlacesTreeView)



        self.ScrolledWindow = Gtk.ScrolledWindow()
        self.ScrolledWindow.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.ScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.FormBox.pack_start(self.ScrolledWindow, True, True, 1)

        self.IconViewStore = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, bool)
        self.LoadIconView(self.IconViewStore)
        self.IconView = Gtk.IconView(model=self.IconViewStore)
        self.IconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.IconView.set_text_column(self.FILENAME)
        self.IconView.set_pixbuf_column(self.FILEICON)
        self.IconView.set_item_width(self.IconWidth)
        self.ScrolledWindow.add(self.IconView)




        self.ToggleButton.connect("toggled", self.HideFileShow, self.IconViewStore, '1')

        self.PlacesTreeView.connect('button_press_event', self.PlacesTreeViewSelect, self.PlacesTreeView)
        self.PlacesTreeView.connect('button_press_event', self.LoadPlacesTreeViewSelect, self.IconViewStore)
        self.CellText.connect("edited", self.ChangePlaces)

        self.IconView.connect('item-activated', self.IconViewDoubleClick, self.IconViewStore)

        self.Geri.connect('button-press-event', self.FileBack, self.IconViewStore) 
        self.Ileri.connect('button-press-event', self.FileNext, self.IconViewStore) 

        self.Geri.set_sensitive(False)
        self.Ileri.set_sensitive(False)

        self.window.show_all()

    def HideFileShow(self, ToggleButton, IconViewStore, name):
        if self.ToggleButton.get_active():
            self.state = True
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
        else:
            self.state = False
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
    def ChangePlaces(self, widget, path, text):
        with open(HOME+'/.config/_filemanager_py_mt_nr.places') as read:
            source = read.read()
        source = source.replace(pdict[self.PlacesStore[path][0]]['path']+','+self.PlacesStore[path][0], 
            pdict[self.PlacesStore[path][0]]['path']+','+text)
        with open(HOME+'/.config/_filemanager_py_mt_nr.places', 'w') as change:
            change.write(source)
        self.PlacesStore[path][0] = text
        self.CellText.set_property("editable", False)
        pdict[text] = self.SelectPlacesItemChangePdict
    def PlacesTreeViewFonksiyon(self, PlacesTreeView, data = None):
        selection = self.PlacesTreeView.get_selection()
        (model, iter) = selection.get_selected()
        if (data == 'Sil'):
            ConfigDeletePlaces(pdict[model[self.SelectPlacesItemIter][0]]['path']+','+model[self.SelectPlacesItemIter][0])
            model.remove(self.SelectPlacesItemIter)
        elif (data == 'Değiştir'):
            self.CellText.set_property("editable", True)
            self.SelectPlacesItemChangePdict = pdict[model[iter][0]]
    def PlacesTreeViewSelect(self, PlacesTreeView, Event, PlacesStore):
        if Event.button == 3:
            pthinfo = self.PlacesTreeView.get_path_at_pos(Event.x, Event.y)
            if pthinfo != None:
                (path,col,cellx,celly) = pthinfo
                self.PlacesTreeView.grab_focus()
                self.PlacesTreeView.set_cursor(path,col,0)
            selection = self.PlacesTreeView.get_selection()
            (model, iter) = selection.get_selected()
            self.SelectPlacesItemIter = iter
            if (pdict[model[iter][0]]['main'] == 'False'): 
                self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def LoadPlacesTreeViewSelect(self, PlacesTreeView, Event, IconViewStore):  
        if Event.button == 1:
            pthinfo = self.PlacesTreeView.get_path_at_pos(Event.x, Event.y)
            if pthinfo != None:
                (path,col,cellx,celly) = pthinfo
                self.PlacesTreeView.grab_focus()
                self.PlacesTreeView.set_cursor(path,col,0)
            selection = self.PlacesTreeView.get_selection()
            (model, iter) = selection.get_selected()
            self.SelectPlacesItem = pdict[model[iter][0]]['path']
            self.Path = self.SelectPlacesItem
            self.Headerbar.props.title = self.Path
            TempWrite(self.Path)
            self.Geri.set_sensitive(True)
            self.ArrayNextBack.append(self.Path)
            self.CountNextBack = self.CountNextBack + 1
            print self.ArrayNextBack
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
    def FileBack(self, IconView, path, IconViewStore):
        if self.CountNextBack > 1: self.CountNextBack = self.CountNextBack - 1
        if self.CountNextBack is 1 :             
            self.Geri.set_sensitive(False
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        if len(self.ArrayNextBack) > self.CountNextBack:
            self.Ileri.set_sensitive(True)
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
        self.Headerbar.props.title = self.Path
        TempWrite(self.Path)
    def FileNext(self, IconView, path, IconViewStore):
        self.CountNextBack = self.CountNextBack + 1
        if self.CountNextBack is len(self.ArrayNextBack) :             
            self.Ileri.set_sensitive(False
                )
        if self.CountNextBack > 1 :             
            self.Geri.set_sensitive(True
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
        self.Headerbar.props.title = self.Path
        TempWrite(self.Path)
    def IconViewDoubleClick(self, IconView, tree_path, IconViewStore):
        iter_ = self.IconViewStore.get_iter(tree_path)
        (path, is_dir) = self.IconViewStore.get(iter_, self.COL_PATH, self.COL_IS_DIRECTORY)
        if (is_dir is True) : 
            TempWrite(path)
            self.ArrayNextBack.insert(self.CountNextBack, path)
            self.CountNextBack = self.CountNextBack + 1
        else:
            subprocess.call(('xdg-open', path))
        if not is_dir:
            return
        self.Path = path
        self.Headerbar.props.title = self.Path
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
   
        if len(self.ArrayNextBack) > 1:
            self.Geri.set_sensitive(True
                )
    def LoadIconView(self, IconViewStore, indextest=0): 
        self.Headerbar.props.title = self.Path
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
