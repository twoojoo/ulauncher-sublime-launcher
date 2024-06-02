from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from fuzzywuzzy import process

import glob
import os
import subprocess

class SublProjectsExtension(Extension):
    def __init__(self):
        super(SublProjectsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        sublime_paths = os.path.expanduser(extension.preferences['dirs']).split(",")
        home_dir = os.path.expanduser('~')
        items = []
        
        arg = event.get_argument()
        items = []
        
        for sublime_path in sublime_paths:
            explicit_path = sublime_path.replace('~', home_dir, 1)

            sub_folders = glob.glob(explicit_path + "/*/")

            if arg != None:
                matches = process.extract(arg, sub_folders, limit=10)
                print(matches)
                matches = [t[0] for t in process.extract(arg, sub_folders, limit=10)]
            else:
                matches = sub_folders

            for name in matches:
                item = ExtensionResultItem(
                    icon = 'images/icon.png',
                    name = name.split('/')[-2],
                    description = 'Path: %s' % name,
                    on_enter = ExtensionCustomAction(name)
                )
                items.append(item)

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        project_path = event.get_data()
        subl = extension.preferences['sublime_executable']
        subprocess.call([subl, project_path, "-n"])

if __name__ == '__main__':
    SublProjectsExtension().run()
