#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import os

HOME = os.environ['HOME']

nextback = ['/home']
fm = {}
pdict = {}

def file_info(path):
    f = Gio.file_new_for_path(path)
    info = f.query_info(Gio.FILE_ATTRIBUTE_STANDARD_ICON,
                        Gio.FileQueryInfoFlags.NONE,
                        None)
    gicon = info.get_icon()
    return gicon.get_names()[0]

def folder(u=HOME, h=False):
    fm.clear()
    f = [f for f in os.listdir(u) if f.startswith('.') is h]
    for isdir in f:
        fm[f.index(isdir)] = {'path':u+'/'+isdir, 'icon':file_info(u+'/'+isdir), 'label':isdir}
    return fm

def scanf(t='folder'):
    keys = [keys for keys in fm if fm[keys]['type'] == t]
    return keys

def places():
    with open(HOME+'/.config/user-dirs.dirs') as pla:
        places = pla.read().splitlines()
    places = [places.replace('"','').split('/')[-1] for places in places if places.startswith('#') is False]
    for add in places:
        pdict[add] = {'path':HOME+'/'+add, 'icon':'folder-music'}
    return pdict

folder('/home')

#XDG_DESKTOP_DIR="$HOME/Masaüstü"  --> user-desktop
#XDG_DOWNLOAD_DIR="$HOME/İndirilenler" folder-download
#XDG_TEMPLATES_DIR="$HOME/Şablonlar"
#XDG_PUBLICSHARE_DIR="$HOME/Genel"
#XDG_DOCUMENTS_DIR="$HOME/Belgeler"
#XDG_MUSIC_DIR="$HOME/Müzik"
#XDG_PICTURES_DIR="$HOME/Resimler"
#XDG_VIDEOS_DIR="$HOME/Videolar"


print places()

class IconViewWindow(Gtk.Window):

    def __init__(self, beta):

        self.window = Gtk.Window()
        self.window.set_border_width(0)
        self.window.set_title('Dosya Yoneticisi')
        self.window.set_default_size(750, 600)
        self.window.connect('destroy', Gtk.main_quit)

        #Gtk HeaderBar
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        #self.hb.props.title = "HeaderBar example"
        self.window.set_titlebar(self.hb)

        #Sağ taraftaki butonlar
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-save-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.hb.pack_end(button)

        
        self.entrysearch = Gtk.Entry()
        self.entrysearch.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            'system-search-symbolic')
        self.entrysearch.connect("changed", self.haha)
        self.hb.pack_end(self.entrysearch)
        
        #Sol tarfataki butonlar
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        self.Geri = Gtk.Button()
        self.Geri.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(self.Geri)
        self.Ileri = Gtk.Button()
        self.Ileri.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(self.Ileri)
        #self.Ev = Gtk.Button()
        #self.Ev.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        #box.add(self.Ev)
        self.hb.pack_start(box)

        #iler ve geri butonları başlangıçta disabled
        self.Ileri.set_sensitive(False)
        self.Geri.set_sensitive(False)

        self.hbox = Gtk.Box(spacing=0, homogeneous=False)
        self.window.add(self.hbox)

        self.placesstore = Gtk.ListStore(str, str)
        self.placestitle = Gtk.TreeViewColumn('Places                                                ')
        self.placestreeview = Gtk.TreeView(self.placesstore)
        for addplaces in places().keys():
            self.placesstore.append([addplaces, Gtk.STOCK_OPEN])
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
        self.hbox.add(self.placestreeview)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.hbox.pack_start(sw, True, True, 1)


        self.liststore = Gtk.ListStore(Pixbuf, str)
        self.iconview = Gtk.IconView(model=self.liststore)

        self.iconview.set_pixbuf_column(0)
        self.iconview.set_text_column(1)
        self.iconview.set_item_width(70)

        self.iconview.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        sw.add(self.iconview)

        ic = [ic for ic in fm.keys()]
        for ic in ic:
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 48, 0)
                self.liststore.append([pixbuf, fm[ic]['label']])
            except:
                pass

        self.iconview.connect('button-press-event', self.press, self.liststore)
        self.iconview.connect('item-activated', self.item_activated, self.liststore)
        self.iconview.grab_focus()

        self.Ileri.connect('button-press-event', self.connect_NExt, self.liststore) 
        self.Geri.connect('button-press-event', self.connect_BAck, self.liststore) 

        self.window.show_all()

    def haha(self, entrysearch):
        self.liststore.clear()
        dict = {}
        index = [index for index in fm.keys() if fm[index]['icon'].find('text') is not -1]
        for enum, test in enumerate(index, 0):
            with open(fm[test]['path']) as search:
                search = search.read()
            if search.find(self.entrysearch.get_text()) is not -1:
                dict[enum] = {'path':fm[test]['path'], 'icon':fm[test]['icon'], 'label':fm[test]['label']}
        if len(self.entrysearch.get_text()) is 0:
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 48, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
        ic = [ic for ic in dict.keys()]
        for ic in ic:
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(dict[ic]['icon'], 48, 0)
                self.liststore.append([pixbuf, dict[ic]['label']])
            except:
                pass
    def press(self, iconview, tree_path, liststore):
        index = self.iconview.get_selected_items()[0]
        print index, 'press'

    def item_activated(self, iconview, tree_path, liststore):
        global select_item_value
        index = self.iconview.get_selected_items()[0]
        gg = str(index)
        kk = int(gg)
        self.liststore.clear()
        if os.path.isdir(fm[kk]['path']) is True:
            #if fm[kk]['path'] not in nextback:
            nextback.append(fm[kk]['path'])
            print nextback
            select_item_value = fm[kk]['path']
            self.hb.props.title = select_item_value
            if len(nextback) > 0 : self.Geri.set_sensitive(True)
            folder(fm[kk]['path'])
            print fm
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 48, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pixbuf = Gtk.IconTheme.get_default().load_icon('error', 48, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
        else:
            print ('ha ne oluyor')

    def connect_NExt(self, iconview, tree_path, liststore):
        global select_item_value
        if os.path.isdir(nextback[nextback.index(select_item_value)+1]) is True:
            self.liststore.clear()
            folder(nextback[nextback.index(select_item_value)+1])
            select_item_value = nextback[nextback.index(select_item_value)+1]
            self.hb.props.title = select_item_value
            if nextback.index(select_item_value) is 0: self.Geri.set_sensitive(False)
            if nextback.index(select_item_value) is len(nextback)-1: 
                self.Ileri.set_sensitive(False)
            if nextback.index(select_item_value) > 0: 
                self.Geri.set_sensitive(True)
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 48, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
    def connect_BAck(self, iconview, tree_path, liststore):
        global select_item_value
        if os.path.isdir(nextback[nextback.index(select_item_value)-1]) is True:
            self.liststore.clear()
            folder(nextback[nextback.index(select_item_value)-1])
            select_item_value = nextback[nextback.index(select_item_value)-1]
            self.hb.props.title = select_item_value
            if nextback.index(select_item_value) is 0: self.Geri.set_sensitive(False)
            if nextback.index(select_item_value) < len(nextback)-1: 
                self.Ileri.set_sensitive(True)
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 48, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
def main(beta=None):
    IconViewWindow(beta)
    Gtk.main()

if __name__ == '__main__':
    main()
