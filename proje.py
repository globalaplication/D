import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
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
        pdict[add] = {'path':HOME+'/'+add, 'icon':'edit-copy'}
    return pdict

folder('/home')

class IconViewWindow(Gtk.Window):

    def __init__(self, beta):

        self.window = Gtk.Window()
        self.window.set_border_width(1)
        self.window.set_title('Dosya Yoneticisi')
        self.window.set_default_size(650, 400)
        self.window.connect('destroy', Gtk.main_quit)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        self.window.set_titlebar(hb)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        self.BAck = Gtk.Button()
        self.BAck.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(self.BAck)

        self.NExt = Gtk.Button()
        self.NExt.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(self.NExt)


        self.NExt.set_sensitive(False)
        self.BAck.set_sensitive(False)

        hb.pack_start(box)

        self.hbox = Gtk.HBox(spacing=11, homogeneous=False)
        self.window.add(self.hbox)


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
                pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 64, 0)
                self.liststore.append([pixbuf, fm[ic]['label']])
            except:
                pass

        self.iconview.connect('item-activated', self.item_activated, self.liststore) #button-press-event
        self.iconview.grab_focus()

        self.NExt.connect('button-press-event', self.connect_NExt, self.liststore) 
        self.BAck.connect('button-press-event', self.connect_BAck, self.liststore) 

        self.window.show_all()

    def item_activated(self, iconview, tree_path, liststore):
        global select_item_value
        index = self.iconview.get_selected_items()[0]
        gg = str(index)
        kk = int(gg)
        self.liststore.clear()
        if os.path.isdir(fm[kk]['path']) is True:
            
            if fm[kk]['path'] not in nextback:
                nextback.append(fm[kk]['path'])

            print nextback

            select_item_value = fm[kk]['path']

            if len(nextback) > 0 : self.BAck.set_sensitive(True)

            folder(fm[kk]['path'])

            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 64, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
        else:
            #eval(fm[kk]['path'])
            print ('ha ne oluyor')

    def connect_NExt(self, iconview, tree_path, liststore):
        global select_item_value
        if os.path.isdir(nextback[nextback.index(select_item_value)+1]) is True:
            self.liststore.clear()
            folder(nextback[nextback.index(select_item_value)+1])
            select_item_value = nextback[nextback.index(select_item_value)+1]
            if nextback.index(select_item_value) is 0: self.BAck.set_sensitive(False)
            if nextback.index(select_item_value) is len(nextback)-1: 
                self.NExt.set_sensitive(False)
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 64, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
    def connect_BAck(self, iconview, tree_path, liststore):
        global select_item_value
        if os.path.isdir(nextback[nextback.index(select_item_value)-1]) is True:
            self.liststore.clear()
            folder(nextback[nextback.index(select_item_value)-1])
            select_item_value = nextback[nextback.index(select_item_value)-1]
            if nextback.index(select_item_value) is 0: self.BAck.set_sensitive(False)
            if nextback.index(select_item_value) < len(nextback)-1: 
                self.NExt.set_sensitive(True)
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 64, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
def main(beta=None):
    IconViewWindow(beta)
    Gtk.main()
if __name__ == '__main__':
    main()
