# example_textinput_cursor.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import sys
sys.path.append(__file__.rsplit("/src/",1)[0] + "/src/")
from text_input_cursor import TextInputCursor

class TextInputCursorExample(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        textinput = TextInput(multiline=True)
        cursor = TextInputCursor(textinput)
        layout.add_widget(textinput)
        return layout

if __name__ == '__main__':
    TextInputCursorExample().run()