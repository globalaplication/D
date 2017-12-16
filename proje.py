import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from gi.repository.GdkPixbuf import Pixbuf
import os

HOME = os.environ['HOME']

nextback = []
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

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

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

        self.window.show_all()


    def item_activated(self, iconview, tree_path, liststore):
        index = self.iconview.get_selected_items()[0]
        gg = str(index)
        kk = int(gg)
        print -1,type(kk), fm[kk]['path']

        if os.path.isdir(fm[kk]['path']) is True:
            nextback.append(fm[kk]['path'])
            print nextback
            self.liststore.clear()
            folder(fm[kk]['path'])
            ic = [ic for ic in fm.keys()]
            for ic in ic:
                try:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(fm[ic]['icon'], 64, 0)
                    self.liststore.append([pixbuf, fm[ic]['label']])
                except:
                    pass
        else:
            eval(fm[kk]['path'])
     
                
def main(beta=None):
    IconViewWindow(beta)
    Gtk.main()

if __name__ == '__main__':
    main()

