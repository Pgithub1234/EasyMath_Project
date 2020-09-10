from tkinter import Tk

import Slave2


def main():
    """This is to call functions from slave and act accordingly and update"""
    main_object = Slave2.All_functions(2, 2, 3, 3)
    show_value = Slave2.ShowValue(0, 0)
    _widget = Tk()
    main_object.create_app(_widget, main_object)
    main_object.add_button(_widget, main_object)
    main_object.save_button_show_graph_button(_widget, main_object)
    main_object.onsave_add_to_xml(Slave2.All_functions.widget_and_value_inUI)
    show_value.pullvalues_fromxml(_widget, show_value, main_object)
    _widget.mainloop()


class Myapp1:

    if __name__ == "__main__":
        main()
