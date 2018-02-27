#!/usr/bin/env python3

from DB_Connection import DB_Connection
from User import User

from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty, ObjectProperty

# -*- coding utf-8 -*-

class MessageBox(Popup):
    dbc = DB_Connection()
    def popup_dismiss(self, user,cup):
        self.dismiss()
        self.dbc._open()
        if cup == 1:
            query = ("UPDATE user SET anz = anz+1 WHERE kuerzel = '{0}';").format(user[10:])
        elif cup == 0:
            query = ("UPDATE user SET anz = anz+4 WHERE kuerzel = '{0}';").format(user[10:])
        self.dbc.executeNonQuery(query)
        self.dbc._close()


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')

    def getInfo(self,id):
        return id


        #hier werden die aktuellen Daten nachgeladen

class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_press(self):
        self.parent.selected_value = 'Selected: {}'.format(self.parent.getInfo(self.id))


    def on_release(self):
        pop = MessageBox()
        pop.open()

    def test(self):
        return 'a'

class RV(RecycleView):
    rv_layout = ObjectProperty(None)
    dbc = DB_Connection()
    userList = ListProperty([])

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.getUserList()

    def getUserList(self):
        query = "SELECT kuerzel from user"
        table = self.dbc.executeQuery("SELECT kuerzel FROM user")
        x = []
        i = 0
        for i in range(0,25):
            x.append({'text':table[0+i][0].upper(), 'id':table[0+i][0]})
            x.append({'text':table[25+i][0].upper(), 'id':table[25+i][0]})
            x.append({'text':table[50+i][0].upper(), 'id':table[50+i][0]})
            i=i+1

        self.data=x

    def getName(self,user):
        query = "SELECT kuerzel, nachname, vorname, anz FROM user WHERE kuerzel = '{0}'".format(user[10:])
        table=self.dbc.executeQuery(query)
        self.user = User(table[0][0],table[0][1],table[0][2],table[0][3])
        name = self.user.vorname[0].upper()+self.user.vorname[1:] + ' ' +self.user.nachname[0].upper()+self.user.nachname[1:]
        return name

    def getTasse(self):
        return str(self.user.anz)


class TestApp(App):
    title = "kaffee@bk-tm.de"

    def build(self):
        return RV()


if __name__ == "__main__":
    TestApp().run()
