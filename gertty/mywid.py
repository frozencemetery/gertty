# Copyright 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import urwid

class TextButton(urwid.Button):
    def selectable(self):
        return True

    def __init__(self, text, on_press=None, user_data=None):
        super(TextButton, self).__init__('', on_press=on_press, user_data=user_data)
        text = urwid.Text(text)
        self._w = urwid.AttrMap(text, None, focus_map='reversed')

class FixedButton(urwid.Button):
    def sizing(self):
        return frozenset([urwid.FIXED])

    def pack(self, size, focus=False):
        return (len(self.get_label())+4, 1)

class TableColumn(urwid.Pile):
    def pack(self, size, focus=False):
        mx = max([len(i[0].text) for i in self.contents])
        return (mx+2, len(self.contents))

class Table(urwid.WidgetWrap):
    def __init__(self, headers=[]):
        super(Table, self).__init__(
            urwid.Columns([('pack', TableColumn([('pack', w)])) for w in headers]))

    def addRow(self, cells=[]):
        for i, widget in enumerate(cells):
            self._w.contents[i][0].contents.append((widget, ('pack', None)))

class MessageDialog(urwid.WidgetWrap):
    signals = ['close']
    def __init__(self, title, message):
        ok_button = FixedButton(u'OK')
        urwid.connect_signal(ok_button, 'click',
            lambda button:self._emit('close'))
        buttons = urwid.Columns([('pack', ok_button)],
                                dividechars=2)
        rows = []
        rows.append(urwid.Text(message))
        rows.append(urwid.Divider())
        rows.append(buttons)
        pile = urwid.Pile(rows)
        fill = urwid.Filler(pile, valign='top')
        super(MessageDialog, self).__init__(urwid.LineBox(fill, title))