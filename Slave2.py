import random
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class All_functions:
    """this is the default object having all default row and column count, which is reusable """
    font_All = ('Arial', 10, 'bold')
    path_to_dataset = r"E:\mathan\Work\EasyMath\Dataset.xml"
    std_fg = 'blue'
    std_bg = 'white'
    items_valuelist = ['None', 'Transport', 'Recharges', 'savings', 'Home', 'other', 'Rent', 'Debit']
    additional_items_added = []
    widget_and_value_inUI = {}
    default_content_values = {"Indian": "112256", "SBI": "165", "Kotak": "8112", "None": "0"}
    _save_button = Widget
    _showgraph = Widget
    Income_value = Widget
    dropdown = Widget
    Entry1 = Widget
    Entry2 = Widget
    button = Widget

    def __init__(self, last_default_column, last_default_row, columncount, rowcount):
        self.last_default_column = last_default_column
        self.last_default_row = last_default_row
        self.rowcount = rowcount
        self.columncount = columncount
    @staticmethod
    def default_content(widget, main_object):
        widget.geometry("1075x400")
        """ALways visible and default content no hiding"""
        bank_name = main_object.Create_Label(widget, "choose your bank name:")
        bank_name.grid(row=0, column=0)
        # bank drop down list
        bank_dropdown = ttk.Combobox(
            widget,
            font=main_object.font_All,
            width=10
        )
        bank_dropdown['values'] = ("Indian", "SBI", "Kotak", "None")
        bank_dropdown.current(3)
        bank_dropdown.grid(row=0, column=1, sticky=W)
        # balance
        balance = main_object.Create_button(widget, "Show Balance")
        balance['command'] = lambda: main_object.update_balance_onclick(bank_dropdown, balance_value)
        balance.grid(row=1)
        # to show balance value
        balance_value = main_object.Create_Entry(widget)
        balance_value.grid(row=1, column=1, sticky=E)
        this_monthincome = main_object.Create_Label(widget, "Income")
        this_monthincome.grid(row=2)
        main_object.Income_value = main_object.Create_Entry(widget)
        main_object.Income_value.grid(row=2, column=1, sticky=E)
        Income_update = main_object.Create_button(widget, "Update")
        Income_update.grid(row=2, column=2, padx=10)
        Income_update['command'] = lambda: main_object.update_income_into_dictionary(main_object.Income_value)
        main_object.last_default_column = 2
        main_object.last_default_row = 2
        main_object.set_rowcolumn_width(widget, 50, 20)
        return main_object.onsave_add_to_xml(main_object.default_content_values)

    @staticmethod
    def update_income_into_dictionary(widget_toget_value):
        value_to_get = widget_toget_value.get()
        print("type of value from get function", type(value_to_get))
        All_functions.widget_and_value_inUI["Income"] = value_to_get
        print("valuies inside dict ", All_functions.widget_and_value_inUI.items())
        All_functions.onsave_add_to_xml(All_functions.widget_and_value_inUI)
    @staticmethod
    def create_app(widget, main_object):
        """Properties of window"""
        widget.geometry("1075x400")
        widget.title("Welcome")
        return All_functions.default_content(widget, main_object)

    @staticmethod
    def Create_Label(widget, text_to_display):
        """this will create a label tk widget for the argument passed"""
        Label1 = Label(
            widget,
            text=text_to_display,
            font=All_functions.font_All,
            fg=All_functions.std_fg
        )

        return Label1

    @staticmethod
    def Create_dropdown(widget, value_to_display):
        """this will create a drop down  tk widget for the argument passed"""
        dropdown = ttk.Combobox(
            widget,
            font=All_functions.font_All,
            width=10
        )
        dropdown['values'] = value_to_display
        return dropdown

    @staticmethod
    def Create_Entry(widget):
        """this will create a Entry  tk widget for the argument passed"""
        Label1 = Entry(
            widget,
            font=All_functions.font_All
        )
        return Label1
    @staticmethod
    def Create_button(widget, text_to_display):
        """this will create a button tk widget for the argument passed"""
        Label1 = Button(
            widget,
            text=text_to_display,
            font=All_functions.font_All,
            fg=All_functions.std_bg,
            bg=All_functions.std_fg
        )

        return Label1

    @staticmethod
    def add_button(widget, main_object):
        """"this is another button widget created """
        _add_button = All_functions.Create_button(widget, "Add Item")
        main_object.grid_manager(_add_button, 3, 0)
        _add_button['command'] = lambda: main_object.on_clickingadd_item(widget, main_object)

    @staticmethod
    def save_button_show_graph_button(widget, main_object):
        """"this is another button widget created """
        _save_button = main_object.Create_button(widget, "Save")
        main_object.grid_manager(widget, _save_button, main_object)
        _save_button['command'] = lambda: [
            graph.check_incomevalue_blank(main_object),
            main_object.Beat_bad_value(main_object.additional_items_added)]
        _showgraph = main_object.Create_button(widget, "Show Graph")
        main_object.grid_manager(_showgraph, 4, 1)
        _showgraph['command'] = lambda: graph.create_chart(widget, main_object, main_object.widget_and_value_inUI)
        main_object._save_button = _save_button
        main_object._showgraph = _showgraph

    @staticmethod
    def get_total_number_of_RC(widget, main_object):
        """will set the object row and column count within teh grid 
        note-> it won't consider 0, it will consider row and column number starting from 1"""
        TCR = Grid.grid_size(widget)
        main_object.rowcount = TCR[1] - 1
        main_object.columncount = TCR[0] - 1

    @staticmethod
    def on_clickingadd_item(widget, main_object, showvalue_object=None):
        """this will create a set of four widgets and store it in a list and returns the list"""
        dropdown = main_object.Create_dropdown(widget, main_object.items_valuelist)
        i = 0
        temp_value = None
        if (showvalue_object != None):
            for value0 in showvalue_object.list_namestopopulate:
                if value0 == 'Income':
                    _index = showvalue_object.list_namestopopulate.index('Income')
                    temp_value = showvalue_object.list_valuestopopulate[_index]
                    main_object.Income_value.delete(first=0, last=25)
                    try:
                        main_object.Income_value.insert(0, temp_value)
                    except:
                        pass
                    _indexoftag = showvalue_object.list_namestopopulate.index(value0)
                    showvalue_object.list_namestopopulate.pop(showvalue_object.list_namestopopulate.index(value0))
                    showvalue_object.list_valuestopopulate.pop(_indexoftag)
                    continue
                _index = main_object.items_valuelist.index(value0)
                dropdown.current(_index)
                _indexoftag = showvalue_object.list_namestopopulate.index(value0)
                temp_value = showvalue_object.list_valuestopopulate[_indexoftag]
                showvalue_object.list_namestopopulate.pop(showvalue_object.list_namestopopulate.index(value0))
                showvalue_object.list_valuestopopulate.pop(_indexoftag)
                break
        Entry1 = main_object.Create_Entry(widget)
        button = main_object.Create_button(widget, "Add")
        button['command'] = lambda: main_object.on_clicking_add(Entry1, Entry2, Entry2)
        Entry2 = main_object.Create_Entry(widget)
        if (showvalue_object != None):
            try:
                Entry2.insert(0, temp_value)
            except:
                pass
        list_of_items = []
        list_of_items.append(dropdown)
        list_of_items.append(Entry1)
        list_of_items.append(button)
        list_of_items.append(Entry2)
        main_object.grid_manager(widget, list_of_items, main_object)
        # to move the save button at last
        main_object._save_button.grid(row=main_object.rowcount + 2, column=0)
        main_object._showgraph.grid(row=main_object.rowcount + 2, column=1)

    @staticmethod
    def on_clicking_add(widget_entry1, widget_entry2, widget_toenter):
        """this will add entry 1 and entry2 and updtate in entry2 also throw warning shot for non numeric value"""
        try:
            try:
                text1 = int(widget_entry1.get())
            except:
                text1 = 0
                messagebox.showwarning('Bad Value', 'Please Enter numeric value!!!')
            try:
                text2 = int(widget_entry2.get())
            except:
                text2 = 0
                messagebox.showwarning('Bad Value', 'Please Enter numeric value!!!')
        except:
            text1 = 0
            text2 = 0
        added_value = text1 + text2
        widget_toenter.delete(first=0, last=25)
        widget_toenter.insert(0, added_value)

    @staticmethod
    def grid_manager(*param):
        if (type(param[1]) == int):
            """this will accept th widget and the row and column which can be given manually to the grid"""
            # def grid_manager(widget_to_arrange,row,column):
            param[0].grid(row=param[1], column=param[2])
        elif (type(param[1]) == list):
            """this will accept tk widget and will arrange the elements in grid automatically w.r.t last row and 
            column it will arrange only one set with four widgets in one row """
            All_functions.get_total_number_of_RC(param[0], param[2])
            # def grid_manager(widget,widget_to_arrange,object):
            row = param[2].rowcount + 1
            column = i = 0
            for x in param[1]:
                param[1][i].grid(row=row, column=column, pady=5)
                All_functions.additional_items_added.append(param[1][i])
                column += 1
                i += 1
        else:
            """this will arrange a single element in last row and column"""
            All_functions.get_total_number_of_RC(param[0], param[2])
            row = param[2].rowcount + 1
            column = 0
            param[1].grid(row=row, column=column)

    @staticmethod
    def get_xml_text(tagname):
        mytree = ET.parse(All_functions.path_to_dataset)
        myroot = mytree.getroot()
        value_in_tag = None
        try:
            for x in myroot.iter(tagname):
                value_in_tag = x.text
        except:
            print("the given tag name is not present in xml")
        return value_in_tag

        mytree.write(All_functions.path_to_dataset)

    @staticmethod
    def onsave_add_to_xml(dictionary):
        """"this will feed dictionary and add that to xml, if same value do nothing, if there is value difference update!!!"""
        mytree = ET.parse(All_functions.path_to_dataset)
        myroot = mytree.getroot()
        list_key = [key for key, value in dictionary.items()]
        list_value = [value for key, value in dictionary.items()]
        i = 0
        j = 0
        while (i < len(list_key)):
            try:

                text_in_xml = NONE
                for x in myroot.iter(list_key[i]):
                    if (x.tag == list_key[i]):
                        x.text = list_value[j]
                        mytree.write(All_functions.path_to_dataset)
                        text_in_xml = True
                        break
            except:
                text_in_xml = False
            if (text_in_xml == True):
                pass
            else:

                temp_element = ET.Element(list_key[i])
                temp_element.text = list_value[j]
                temp_element.tail = '\n'  # to get each tag in a new line
                myroot.append(temp_element)
                mytree.write(All_functions.path_to_dataset)
            i += 1
            j += 1

    @staticmethod
    def add_to_dictionary():
        """this will store the additional items added into key value pair on save"""
        temp_storage = []
        length_of_widgetsadded = len(All_functions.additional_items_added)
        if (length_of_widgetsadded > 0):
            for x in All_functions.additional_items_added:
                name_of_widget = x.widgetName
                widget_info = x.grid_info()
                if (name_of_widget == "ttk::combobox") | (name_of_widget == "entry"):
                    if (widget_info['column'] != 1):
                        value_in_widget = x.get()
                        print("the value inside widget is {}".format(value_in_widget))
                        temp_storage.append(value_in_widget)
        i = 0
        j = 1
        while (j + 1 <= len(temp_storage)):
            All_functions.widget_and_value_inUI[temp_storage[i]] = temp_storage[j]
            print("went in {0} {1}".format(temp_storage[i], temp_storage[j]))
            i += 2
            j += 2
            print(All_functions.widget_and_value_inUI.items())
        return All_functions.onsave_add_to_xml(All_functions.widget_and_value_inUI)

    @staticmethod
    def update_balance_onclick(from_widget, show_value_onwidget):
        """this will fetch teh value for matching tag and set the text for teh tag  into UI"""
        value_to_search = from_widget.get()
        text_to_bedisplayed = All_functions.get_xml_text(value_to_search)
        show_value_onwidget.delete(first=0, last=25)
        show_value_onwidget.insert(0, text_to_bedisplayed)

    @staticmethod
    def set_rowcolumn_width(widget, rowvalue, columnvalue):
        """this is to set the column and row width and also to set column 3 to have empty spaces"""
        col_count, row_count = widget.grid_size()
        for col in range(col_count):
            widget.grid_columnconfigure(col, minsize=columnvalue)
        for row in range(row_count):
            widget.grid_rowconfigure(row, minsize=rowvalue)
        # this is to set the third coulmn show even though its balnk
        widget.grid_columnconfigure(3, minsize=200)

    @staticmethod
    def Beat_bad_value(items_to_check):
        """this will check all entry boxes with only numeric values if not numeric show warning msg"""

        def check_badvalue(item):
            print(item)
            name = item.widgetName
            widget_info = item.grid_info()
            print(f"the widget inside beat bad value grid info is {widget_info}")
            if (name == "entry"):
                temp = item.get()
                if (temp != ''):
                    int(temp)

        try:
            list_dummy = list(map(check_badvalue, items_to_check))
        except:
            messagebox.showwarning('Bad Value', 'Please Enter numeric value!!!')
        else:
            All_functions.add_to_dictionary()


class graph():
    """this class deals with all graph objects"""
    canvas = None
    income_value = None

    # constructor
    def __init__(self, Lables, Sizes, Color, Explode):
        self.Lables = Lables
        self.Sizes = Sizes
        self.Color = Color
        self.Explode = Explode

    @staticmethod
    def create_chart(widget, main_object, dictionary):
        """this will create chart as per newly added values and adjust graph height as per  newly added rows"""
        graph.check_incomevalue_blank(main_object)
        my_graph = graph(Lables=0, Sizes=0, Color=0, Explode=0)
        graph.income_value = dictionary["Income"]
        graph.modify_graph_input(All_functions.widget_and_value_inUI, my_graph)
        fig = Figure(figsize=(5, 2), dpi=100, frameon=True)
        a = fig.add_axes([0, 0, 1, 1])
        a.axis('equal')
        lables = my_graph.Lables
        sizes = my_graph.Sizes
        color = my_graph.Color
        print("the label is {} the sizes are {} and color is {}".format(lables, sizes, color))
        explode = [int(x) - int(x) for x in dictionary.values()]
        explode.insert(0, 0.1)
        explode.pop(-1)
        explode_tup = tuple(explode)
        a.pie(sizes, labels=lables, colors=color, autopct='%1.1f%%', shadow=True, startangle=140, explode=explode_tup)
        graph.canvas = FigureCanvasTkAgg(fig, widget)
        All_functions.get_total_number_of_RC(widget, main_object)
        row = main_object.rowcount + 1
        graph.canvas.get_tk_widget().grid(row=0, column=4, rowspan=row, sticky=NSEW)

    @staticmethod
    def modify_graph_input(dictionary, graph_object):
        """this will take ad hoc input from dict and give input to create chart func"""
        color = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'coral', 'red']
        list_labels = [key for key in dictionary.keys()]
        list_values = [value for value in dictionary.values()]
        print(f"the list values are {list_values}")
        list_values_tofeed = list(map(graph.reducing_incomevalue, dictionary.values()))
        print(f"The updated list is{list_values_tofeed}")
        list_values.pop(0)
        # this is to fetch the last value in lits values to feed beczo in last only updated values will be updated
        list_values.insert(0, list_values_tofeed[-1])
        print(f"the list values after upodate are {list_values}")

        graph_object.Lables = list_labels
        graph_object.Sizes = list_values
        random.shuffle(color)
        counter = random.randint(0, len(color) - 1)
        graph_object.Color = color

    @staticmethod
    def reducing_incomevalue(to_reduce):
        """this is to reduce the income with consecutive values added newly in order to get correct grapg split"""
        try:
            if not (to_reduce == graph.income_value):
                temp = graph.income_value
                temp = int(temp)
                temp = temp - int(to_reduce)
                graph.income_value = temp
                print(f"the totola reduced value is {temp} and the reducing value is {to_reduce}")
                return temp
        except:
            print("exception throen inside reducing income value")

    @staticmethod
    def check_incomevalue_blank(main_object):
        """this is to check whether income value is balnk and tell users to update if blank"""
        temp = main_object.Income_value.get()
        print("the value is {0} and it stype is {1}".format(temp, type(temp)))
        if (temp.isnumeric() == False) or (temp == '0'):
            messagebox.showwarning('Update Income Value', 'Please update income value and click on update!!!')
            graph.canvas.get_tk_widget().grid_remove()


class ShowValue():
    tostore_value = {}

    def __init__(self, list_namestopopulate, list_valuestopopulate):
        self.list_namestopopulate = list_namestopopulate
        self.list_valuestopopulate = list_valuestopopulate

    @staticmethod
    def pullvalues_fromxml(widget, sv_object, main_object):
        """this will pull all values from dataset and store it in two different list only if they are not default
        values """
        mytree = ET.parse(All_functions.path_to_dataset)
        myroot = mytree.getroot()
        sv_object.list_namestopopulate = [keys.tag for keys in myroot.iter() if
                                          keys.tag != 'items' and keys.tag not in All_functions.default_content_values]
        sv_object.list_valuestopopulate = [keys.text for keys in myroot.iter() if
                                           keys.tag != 'items' and keys.tag not in All_functions.default_content_values]
        print(f"the valueinside names to populate is {sv_object.list_namestopopulate}")
        print(f"the valueinside value to populate is {sv_object.list_valuestopopulate}")
        return ShowValue.add_number_of_newly_added_items(widget, main_object, sv_object)

    @staticmethod
    def add_number_of_newly_added_items(widget, main_object, sv_object):
        i = 0
        while len(sv_object.list_namestopopulate) != 0:
            main_object.on_clickingadd_item(widget, main_object, sv_object)
            i += 1
        main_object.update_income_into_dictionary(main_object.Income_value)
        main_object.add_to_dictionary()
