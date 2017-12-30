#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, os, copy
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from gi.repository import GdkPixbuf, GLib
from gi.repository import Pango
import subprocess
HOME = os.environ['HOME']
PlacesSource = HOME+'/.config/_filemanager_py_mt_nr.places'
DefaultPlaces = HOME+'/.config/user-dirs.dirs'
LastSelect = HOME+'/.config/_filemanager_py_mt_nr.star'
filedict = {}
pdict = {}
pdict['Diskler'] = {'path':'/media', 'icon':'gtk-home', 'main':True}
pdict['Rash'] = {'path':HOME+'/.local/share/Trash/files/', 'icon':'gtk-quit', 'main':True}
pdict['Ev'] = {'path':HOME, 'icon':'gtk-home', 'main':True}
pdict['Root'] = {'path':'/', 'icon':'gtk-home', 'main':True}
def ConfigDeletePlaces(string, NewConfigData=''):
    with open(PlacesSource) as delete:
        test = delete.read()
    for j in test.splitlines():
        if j.startswith(string) is True:
            continue
        NewConfigData = NewConfigData + j + '\n'
    with open(PlacesSource, 'w') as places:
        places.write(NewConfigData)
def TempRead():
    with open(LastSelect) as temp:
        star = temp.read().replace('\n', '')
    return star
def TempWrite(path):
    with open(LastSelect, 'w') as temp:
        temp.write(path)
def ConfigAddPlaces(keys, value, icon, main):
    with open(PlacesSource) as oku:
        test = oku.read()
    if test.find(keys+',') is -1:
        with open(PlacesSource, 'a') as places:
            places.write(keys+','+value+','+icon+','+str(main)+'\n')
def LoadPlaces():
    with open(DefaultPlaces) as pla:
        places = pla.read().splitlines()
    places = [places.replace('"','').split('/')[-1] for places in places if places.startswith('#') is False]
    for add in places:
        ConfigAddPlaces(HOME+'/'+add, add, 'gtk-home', True)
    with open(PlacesSource) as pla:
        places = pla.read().splitlines()
    for add in places:
        pdict[add.split(',')[1]] = {'path':add.split(',')[0], 
        'icon':add.split(',')[2], 
                                    'main':add.split(',')[3]}
    return pdict
class Child(Gtk.Window):
    def __init__(self):
        self.window2 = Gtk.Window()
        self.window2.set_default_size(200, 300)
        self.window2.show_all()
    def fflist(self, path):
        dir = [path]
        for j in dir:
            yield [j]
            if os.path.isdir(j) is True:
                for k in os.listdir(j):
                    dir.extend([j+'/'+k])
    def CopyCutF(self, hedef, path):
        for enum, file in enumerate (self.fflist(path), 0):
            copyfile = ''
            if (enum is 0):
                p = copy.copy(file[0].split('/')[-1])
            test = hedef+'/'+str(file[0][file[0].find(p):])
            for split in test.split('/')[0:-1]:
                copyfile = copyfile + split + '/'
            os.system('cp -avr ' + file[0] + ' ' + copyfile)
        yield None
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
    DefaultFolder = 'Klasör'
    IconViewSelectedItem = []
    CountFolder = 0
    CountText = 0
    CountHideFile = 0
    SelectIconViewIsdir = False
    ExtendSelectIconViewIndex = []
    RashPath = '~/.local/share/Trash/files/'
    def __init__(self, BetaApp):
        self.window = Gtk.Window()
        self.window.set_default_size(960, 600)
        self.window.connect('destroy', Gtk.main_quit)

        self.menu = Gtk.Menu()
        MenuKonumlarSil = Gtk.MenuItem("Sil")
        MenuKonumlarSil.connect("activate", self.PlacesTreeViewFonksiyon, 'Sil')
        MenuKonumlarDegistir = Gtk.MenuItem("Yeniden Adlandır")
        MenuKonumlarDegistir.connect("activate", self.PlacesTreeViewFonksiyon, 'Yeniden Adlandır')
        self.menu.append(MenuKonumlarDegistir)
        self.menu.append(MenuKonumlarSil)
        self.menu.show_all()
        self.MenuIconView = Gtk.Menu()

        self.MenuIconViewCopy = Gtk.MenuItem("Kopyala")
        self.MenuIconViewCopy.connect("activate", self.IconViewFonksiyon, 'Kopyala')
        #self.MenuIconViewCopy.connect("activate", self.on_folder_clicked)

        self.MenuIconViewCut = Gtk.MenuItem("Taşı")
        self.MenuIconViewCut.connect("activate", self.IconViewFonksiyon, 'Taşı')
        self.MenuIconViewPaste = Gtk.MenuItem("Yapıştır")
        self.MenuIconViewPaste.connect("activate", self.IconViewFonksiyon, 'Yapıştır')
        self.MenuIconViewYeniKlasor = Gtk.MenuItem("Yeni Klasör")
        self.MenuIconViewYeniKlasor.connect("activate", self.IconViewFonksiyon, 'Yeni Klasör')
        self.MenuIconViewDelete = Gtk.MenuItem("Sil")
        self.MenuIconViewDelete.connect("activate", self.IconViewFonksiyon, 'Sil')
        self.MenuIconViewCopeTasi = Gtk.MenuItem("Çöp Kutusuna Taşı")
        self.MenuIconViewCopeTasi.connect("activate", self.IconViewFonksiyon, 'Çöp Kutusuna Taşı')
        self.MenuIconViewFolderAddPlaces = Gtk.MenuItem("Konuma Ekle ")
        self.MenuIconViewFolderAddPlaces.connect("activate", self.IconViewFonksiyon, 'Konuma Ekle')
        self.MenuIconViewChanged = Gtk.MenuItem("Yeniden Adlandır")
        self.MenuIconViewChanged.connect("activate", self.IconViewFonksiyon, 'Yeniden Adlandır')
        self.MenuIconView.append(self.MenuIconViewCopy)
        self.MenuIconView.append(self.MenuIconViewCut)
        self.MenuIconView.append(self.MenuIconViewPaste)
        self.MenuIconView.append(self.MenuIconViewFolderAddPlaces)
        self.MenuIconView.append(self.MenuIconViewYeniKlasor)
        self.MenuIconView.append(self.MenuIconViewDelete)
        self.MenuIconView.append(self.MenuIconViewCopeTasi)
        self.MenuIconView.append(self.MenuIconViewChanged)
        self.MenuIconView.show_all()
        #Gtk HeaderBar
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        #self.Headerbar.props.title = self.Path
        self.window.set_titlebar(self.Headerbar)

        #sağ taraf buton
        self.BlueToothButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-floppy")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.BlueToothButton.add(image)
        self.BlueToothButton.connect('clicked', self.test)
        self.Headerbar.pack_end(self.BlueToothButton)

        self.ToggleButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-stop")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.ToggleButton.add(image)
        self.Headerbar.pack_end(self.ToggleButton)

        #self.ButtonAdd = Gtk.Button()
        #icon = Gio.ThemedIcon(name="gtk-home")
        #image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        #self.ButtonAdd.add(image)
        #self.Headerbar.pack_end(self.ButtonAdd)
        #Sol tarfataki butonlar

        self.HeaderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.HeaderBox.get_style_context(), "linked")
        self.spinner = Gtk.Spinner()
        self.HeaderBox.add(self.spinner)
        self.Geri = Gtk.Button()
        self.Geri.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.HeaderBox.add(self.Geri)
        self.Ileri = Gtk.Button()
        self.Ileri.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.HeaderBox.add(self.Ileri)
        self.Headerbar.pack_start(self.HeaderBox)
        #sağ taraftaki butonlar
        self.GoEntry = Gtk.Entry()
        self.GoEntry.set_width_chars(50)
        self.GoEntry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,'gtk-apply')
        self.GoEntry.connect("changed", self.ChangedGoEntry)
        #self.Headerbar.pack_end(self.GoEntry)
        self.FormBox = Gtk.Box(homogeneous=False, spacing=0)
        self.window.add(self.FormBox)
        self.PlacesStore = Gtk.ListStore(str, str)
        for addplaces in LoadPlaces().keys():
            self.PlacesStore.append([addplaces, pdict[addplaces]['icon']])
        self.PlacesTreeView = Gtk.TreeView(self.PlacesStore)
        self.PlacesColumn = Gtk.TreeViewColumn('Konumlar'+' '*25)
        self.PlacesTreeView.append_column(self.PlacesColumn)
        self.CellIcon = Gtk.CellRendererPixbuf()
        self.CellText = Gtk.CellRendererText()
        self.PlacesTreeView.set_property("enable-search", True)
        self.CellText.set_fixed_size(24,24)
        #self.PlacesColumn.set_alignment(10.0)
        #self.CellText.set_property('xalign', 100)
        #self.CellText.set_property('yalign', 0)
        #self.CellText.set_property('wrap-width', 1660)
        #self.CellIcon.set_property('yalign', 100)
        #self.CellText.set_property('editable', True)
        #self.PlacesColumn.set_property('clickable', True)
        #self.CellIcon.set_property('xalign', 0.1)
        #self.CellText.set_property('xalign', 1.0)
        #self.CellText.props.weight_set = True
        #self.CellText.props.weight = Pango.WEIGHT_NORMAL=545 #WEIGHT_BOLD=700
        #self.CellText.props.weight = Pango.Weight.BOLD
        #self.CellText.props.wrap_width = 70  
        #self.CellText.set_property("editable", True)
        self.PlacesColumn.pack_start(self.CellIcon, False)
        self.PlacesColumn.pack_start(self.CellText, True)
        self.PlacesColumn.set_attributes(self.CellIcon, stock_id=1)
        self.PlacesColumn.set_attributes(self.CellText, text=0)
        self.PlacesTreeView.set_activate_on_single_click(True) 
        self.FormBox.add(self.PlacesTreeView)
#
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.FormBox.pack_start(self.box2, 1, 1, 0)

        #self.HeaderBar2 = Gtk.HeaderBar()
        #self.box2.add(self.HeaderBar2)

        mb = Gtk.MenuBar()
        filemenu = Gtk.Menu()
        self.filem = Gtk.MenuItem()
        mb.append(self.filem)
        self.box2.add(mb)

        #self.ToggleButton = Gtk.ToggleButton()
        #icon = Gio.ThemedIcon(name="gtk-stop")
        #image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        #self.ToggleButton.add(image)
        #self.HeaderBar2.pack_start(self.ToggleButton)

        self.ScrolledWindow = Gtk.ScrolledWindow()
        self.ScrolledWindow.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.ScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.box2.pack_end(self.ScrolledWindow, 1, 1, 0)

        self.IconViewStore = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, bool)
        self.LoadIconView(self.IconViewStore)
        self.IconView = Gtk.IconView(model=self.IconViewStore)
        self.IconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.IconView.set_text_column(self.FILENAME)
        self.IconView.set_pixbuf_column(self.FILEICON)
        self.IconView.set_item_width(self.IconWidth)
        self.IconView.set_margin(5)
        #self.IconView.set_markup_column(5)
        #self.IconView.set_reorderable(100)
        self.IconView.set_row_spacing(0)
        #self.IconView.set_spacing(100)
        #self.IconView.set_border_width(10)
        self.IconView.set_margin_left(0)
        self.IconView.set_margin_right(0)
        self.IconView.set_margin_start(0)
        self.IconView.set_margin_top(0)
        self.IconView.set_opacity(1.0)
        #self.IconView.set_valign(1)
        #self.IconView.set_visible(1)
        self.ScrolledWindow.add(self.IconView)
#
        self.IconView.grab_focus()
        self.ToggleButton.connect("toggled", self.HideFileShow, self.IconViewStore, '1')
        self.PlacesTreeView.connect('button_press_event', self.PlacesTreeViewSelect, self.PlacesTreeView)
        self.PlacesTreeView.connect('button_press_event', self.LoadPlacesTreeViewSelect, self.IconViewStore)
        self.CellText.connect("edited", self.ChangePlaces)
        self.IconView.connect('selection-changed', self.IconViewSelect, self.IconView) 
        self.IconView.connect('button_press_event', self.IconViewSelectPressEvent, self.IconView)
        self.IconView.connect('item-activated', self.IconViewDoubleClick, self.IconViewStore)
        self.Geri.connect('button-press-event', self.FileBack, self.IconViewStore) 
        self.Ileri.connect('button-press-event', self.FileNext, self.IconViewStore) 
        self.Geri.set_sensitive(False)
        self.Ileri.set_sensitive(False)
        self.window.show_all()

    def test(self, BlueToothButton):
        c = Child()
        for j in self.ExtendSelectIconViewIndex:
            for test in c.fflist(filedict[int(str(j))]['file']):
                print test

    def ChangedGoEntry(self, GoEntry, say=0):
        print ('test')
    def ConTextMenuIconView(self):
        self.MenuIconView.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def IconViewSelectPressEvent(self, IconView,  event, IconViewStore):
        try:
            if event.type == Gdk.EventType.BUTTON_PRESS:
                self.path = self.IconView.get_path_at_pos(event.x, event.y)
                if self.path != None and event.button == 1: 
                    print (self.path, 'self')
                elif (event.button == 3):
                    isdir = os.path.isdir(os.path.join(self.Path, filedict [ int(str(self.path)) ]['file']))
                    self.SelectIconViewIsdir = isdir
                    self.IconView.select_path(self.path)
                    self.ConTextMenuIconView()
                    if (self.IconViewSelectedItem > 0):
                        self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, True), 
                        (self.MenuIconViewDelete, True),(self.MenuIconViewCopeTasi, True), 
                        (self.MenuIconViewCut, True),(self.MenuIconViewPaste, False),
                        (self.MenuIconViewCopy,True), (self.MenuIconViewYeniKlasor,False), 
                        (self.MenuIconViewFolderAddPlaces,True)])
                    else:
                        self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, True), 
                        (self.MenuIconViewDelete, True),(self.MenuIconViewCopeTasi, True),
                        (self.MenuIconViewCut, True),
                        (self.MenuIconViewCopy,True), (self.MenuIconViewPaste, False)
                        (self.MenuIconViewYeniKlasor,False), 
                        (self.MenuIconViewFolderAddPlaces,False)])
        except:
            self.ConTextMenuIconView()
            if (len(self.ExtendSelectIconViewIndex) is 0):
                self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, False), 
                (self.MenuIconViewDelete, False),
                (self.MenuIconViewCopeTasi, False),
                (self.MenuIconViewCut, False),
                (self.MenuIconViewCopy,False), 
                (self.MenuIconViewPaste, False),
                (self.MenuIconViewYeniKlasor,True),
                (self.MenuIconViewFolderAddPlaces,False)])
            else:
                self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, False), 
                (self.MenuIconViewDelete, False),
                (self.MenuIconViewCopeTasi, False),
                (self.MenuIconViewCut, False),
                (self.MenuIconViewCopy,False), 
                (self.MenuIconViewPaste, True),
                (self.MenuIconViewYeniKlasor,True),
                (self.MenuIconViewFolderAddPlaces,False)])
    def IconViewContextMenuEnabled(self, menuitem):
        for enabled in menuitem:
            enabled[0].set_sensitive(enabled[1])
    def IconViewSelect(self, IconView, event, model=None):
        self.IconViewSelectedItem = IconView.get_selected_items()
        if (len(self.IconViewSelectedItem) is 0):
            info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
            self.StatusBarInfo(info) 
        else:
            string = str(len(self.IconViewSelectedItem)) + ' Dosya seçildi'
            self.StatusBarInfo(string)
    def IconViewFonksiyon(self, PlacesTreeView, data = None):
        selection = self.PlacesTreeView.get_selection()
        (model, iter) = selection.get_selected()
        if (data == 'Yeni Klasör'):
            for id in range(1, 111):
                Error = os.path.isdir(self.Path +'/'+ self.DefaultFolder + str(id))
                if (Error is True):
                    continue
                if (Error is False):

                    self.DefaultFolder = self.DefaultFolder + str(id)
                    os.makedirs(self.Path +'/'+ self.DefaultFolder)
                    self.IconViewStore.append((os.path.join(self.Path, 
                        self.DefaultFolder),self.DefaultFolder, 
                        self.FileIcon(os.path.join(self.Path, 
                            self.DefaultFolder)),
                    os.path.isdir(os.path.join(self.Path, 
                        self.DefaultFolder))
                        )
                    )
                    NewFolder = self.DefaultFolder
                    isdir = os.path.isdir(os.path.join(self.Path, NewFolder))
                    filedict[len(filedict)] = {'isdir':isdir, 'file':self.Path+'/'+NewFolder}
                    break
        if (data == 'Konuma Ekle'):
            keys = os.path.split ( filedict [ int(str(self.path)) ]['file'] )[1]
            path = filedict [ int(str(self.path)) ]['file']
            #icon = filedict [ int(str(self.path)) ]['icon']
            self.PlacesStore.append([keys, 'gtk-home'])
            pdict[keys] = {'path':path, 'icon':'gtk-home', 'main':'False'}
            ConfigAddPlaces(path,keys,'gtk-home','False')
        if (data == 'Sil'):
            for delete in self.IconViewSelectedItem:
                self.spinner.start()
                if filedict[int(str(delete))]['isdir'] is True:
                    self.Info = os.system('rm -r '+filedict[int(str(delete))]['file'].replace(' ', '\ ')) #klasor
                    self.CountFolder = self.CountFolder -1
                else: 
                    self.Info = os.system('rm -f '+filedict[int(str(delete))]['file'].replace(' ', '\ '))
                    self.CountText = self.CountText -1
                self.IconViewStore.remove(self.IconViewStore.get_iter(delete))
                for test in range(int(str(delete)), len(filedict)):
                    if test is not len(filedict)-1:
                        filedict[test] = filedict[test+1]
                    else:
                        filedict.pop(test)
            info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
            self.StatusBarInfo(info) 
            self.spinner.stop()
        if (data == 'Çöp Kutusuna Taşı'):
            print ('ok rash')
        if (data == 'Kopyala'):
            print ('kopyalama işlemi', self.IconViewSelectedItem)
            self.ExtendSelectIconViewIndex = []
            for test in self.IconViewSelectedItem:
                print self.ExtendSelectIconViewIndex.extend(test)
        if (data == 'Taşı'):
            print ('taşıma işlemi', self.IconViewSelectedItem)
            self.ExtendSelectIconViewIndex = []
            for test in self.IconViewSelectedItem:
                print self.ExtendSelectIconViewIndex.extend(test)
        if (data == 'Yapıştır'):
            c = Child()
            for j in self.ExtendSelectIconViewIndex:
                for test in c.CopyCutF(self.Path, filedict[int(str(j))]['file']):
                    print test
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
        with open(PlacesSource) as read:
            source = read.read()
        source = source.replace(pdict[self.PlacesStore[path][0]]['path']+','+self.PlacesStore[path][0], 
            pdict[self.PlacesStore[path][0]]['path']+','+text)
        with open(PlacesSource, 'w') as change:
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
        elif (data == 'Yeniden Adlandır'):
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
            #self.Headerbar.props.title = self.Path
            TempWrite(self.Path)
            self.Geri.set_sensitive(True)
            self.ArrayNextBack.append(self.Path)
            self.CountNextBack = self.CountNextBack + 1
            #print (self.ArrayNextBack)
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
            if (self.Path == HOME+'/.local/share/Trash/files/'):
                self.GoEntry.set_text('Rash://')
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
        #self.Headerbar.props.title = self.Path
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
        #self.Headerbar.props.title = self.Path
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
        #self.Headerbar.props.title = self.Path
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
        if len(self.ArrayNextBack) > 1:
            self.Geri.set_sensitive(True
                )
    def LoadIconView(self, IconViewStore, indextest=0): 
        #self.Headerbar.props.title = self.Path
        self.CountFolder, self.CountText, self.CountHideFile = 0, 0, 0
        self.GoEntry.set_text(self.Path)
        try:
            if (self.Path == HOME+'/.local/share/Trash/files/'):
                self.GoEntry.set_text('Rash://')
            for enum, FileName in enumerate(os.listdir(self.Path),0):
                if FileName.startswith('.') is True and self.state is False:
                        indextest = indextest + 1
                        self.CountHideFile = self.CountHideFile + 1
                        continue
                filedict[enum-indextest] = {'file':self.Path+'/'+FileName, 
                        'isdir':os.path.isdir(os.path.join(self.Path, FileName))}
                if os.path.isdir(os.path.join(self.Path, FileName)) is True:
                    self.CountFolder = self.CountFolder + 1
                else:
                    self.CountText = self.CountText + 1
                self.IconViewStore.append(
                (os.path.join(self.Path, FileName), 
                    FileName, 
                    self.FileIcon(os.path.join(self.Path, FileName)
                        ),
                    os.path.isdir(os.path.join(self.Path, FileName)
                        )
                    )
                )
            if (self.CountFolder is 0 and self.CountText is 0):
                self.StatusBarInfo(str('Dizin boş'))
            else:
                info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
                self.StatusBarInfo(info) 
        except:
            self.StatusBarInfo(str('Böyle bir dizin yok'))   
    def StatusBarInfo(self, String):
        StatusBarInfo = String
        self.filem.set_label(str(String))
        self.filem.select()
        self.filem.activate()
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
