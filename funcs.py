

import os

global addressbartext

HOME = os.environ['HOME']

fm = {}
pdict = {}

def folder(u=HOME, h=False):
	f = [f for f in os.listdir(u) if f.startswith('.') is h]
	for isdir in f:
		if os.path.isdir(u+'/'+isdir) is False:
			fm[u+'/'+isdir] = {'dir':False, 'type':os.path.splitext(u+isdir)[1], 'label':isdir}
 		else: fm[u+'/'+isdir] = {'dir':True, 'type':'folder', 'label':isdir}
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

def oclick():
	return 0

def dclick():
	return 0
  
print folder()
print places()


