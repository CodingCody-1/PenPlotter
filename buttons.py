from vex import *

class ButtonUi:
    class Button:
        def __init__(self):
            self.index = 0
            self.xpos = 0
            self.ypos = 0
            self.width = 80
            self.height = 80
            self.color = Color.WHITE
            self.text = ''
            self.alttext = ''
            self.state = False
            self.toggle = False
            self.callback = None

        def set_toggle(self, toggle, text):
            self.toggle = toggle
            if text is not None:
                self.alttext = text
            else:
                self.alttext = self.text
            return self

        def set_size(self, width, height):
            self.width = width
            self.height = height
            return self

        def set_color(self, color):
            self.color = color
            return self

    def __init__(self):
        self.brain = Brain()
        self._buttons = []
        self._enabled = True
        self.brain.screen.pressed(self._screen_press)
        self.brain.screen.released(self._screen_release)

    @staticmethod
    def _find_button(b, xpos, ypos):
        if xpos < b.xpos or xpos > (b.xpos + b.width):
            return False

        if ypos < b.ypos or ypos > (b.ypos + b.height):
            return False

        return True

    def _draw_button(self, b, bHighlight):
        if bHighlight:
            self.brain.screen.draw_rectangle(
                b.xpos, b.ypos, b.width, b.height, Color(0x808080))
        else:
            self.brain.screen.draw_rectangle(
                b.xpos, b.ypos, b.width, b.height, b.color)

        self.brain.screen.draw_rectangle(
            b.xpos, b.ypos, b.width, b.height, Color.TRANSPARENT)
        self.brain.screen.set_fill_color(Color.BLACK)
        self.brain.screen.set_pen_color(Color.WHITE)
        self.brain.screen.set_font(FontType.MONO20)

        if b.toggle and b.state:
            text = b.alttext
        else:
            text = b.text
        # we need to add twxt width to python VM, this will do for now
        textwidth = len(text) * 10
        self.brain.screen.print_at(
            text, opaque=False, x=b.xpos + (b.width-textwidth)/2, y=b.ypos + b.height/2 + 10)

    def _draw_buttons(self):
        for b in self._buttons:
            self._draw_button(b, False)

    def _screen_press(self):
        if not self._enabled:
            return

        xpos = self.brain.screen.x_position()
        ypos = self.brain.screen.y_position()

        for b in self._buttons:
            if self._find_button(b, xpos, ypos):
                if b.toggle is True:
                    b.state = not b.state
                else:
                    b.state = True

                self._draw_button(b, True)
                if b.callback is not None:
                    b.callback(b.index, b.state)
                return

    def _screen_release(self):
        if not self._enabled:
            return

        for b in self._buttons:
            if not b.toggle:
                if b.state:
                    b.state = False
                    if b.callback is not None:
                        b.callback(b.index, b.state)

        self._draw_buttons()

    def add_button(self, x, y, text, callback):
        b = ButtonUi.Button()
        b.index = len(self._buttons)
        b.xpos = x
        b.ypos = y
        b.text = text
        b.callback = callback
        self._buttons.append(b)
        return b

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def display(self, bClearScreen=False):
        if bClearScreen:
            self.brain.screen.clear_screen()
        self._draw_buttons()

# ----------------------------------------------------------

def userTouchAction(index, state):
    if index == 0 and not state:
        brain.screen.print_at("Button 1 pressed ", x=150, y=150)

    if index == 1 and not state:
        brain.screen.print_at("Button 2 pressed ", x=150, y=150)

    if index == 2 and not state:
        brain.screen.print_at("Button 3 pressed ", x=150, y=150)

    if index == 3 and not state:
        brain.screen.print_at("Button 4 pressed ", x=150, y=150)

# ----------------------------------------------------------

'''
# create ui object
ui = ButtonUi()

# add some buttons
ui.add_button(50, 20, "PLAY", userTouchAction).set_color(Color.RED)
ui.add_button(150, 20, "STOP", userTouchAction).set_color(Color.BLUE)
ui.add_button(250, 20, "FWD", userTouchAction).set_color(Color(0x208020))
ui.add_button(350, 20, "REV", userTouchAction).set_color(Color(0x404040))

ui.add_button(50, 120, "OFF", userTouchAction).set_color(Color(0x804040)).set_toggle(True, "ON")

ui.display()
'''