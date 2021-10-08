from tkinter import *
import tkinter.ttk as ttk
import urllib.request
import datetime
import xml.dom.minidom
import matplotlib
import matplotlib.pyplot as plt

d = datetime.datetime.today()
dt = d.strftime("%d/%m/%Y")

names = []
values = []
nominals = []
response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req={}".format(dt))
dom = xml.dom.minidom.parse(response)
dom.normalize()
nodeArray = dom.getElementsByTagName("Valute")
for node in nodeArray:
    childList=node.childNodes
    for child in childList:
        # print("{} - {}".format(child.nodeName, child.childNodes[0].nodeValue))
        if child.nodeName == "Name":
            names.append(child.childNodes[0].nodeValue)
        if child.nodeName == "Value":
            values.append(child.childNodes[0].nodeValue)
        if child.nodeName == "Nominal":
            nominals.append(child.childNodes[0].nodeValue)

valute_dict = {}
names.append('Рубль')
values.append('1,0')
nominals.append('1')
for index in range(0, len(names)):
    valute_dict[names[index]] = [values[index], nominals[index]]

# print(valute_dict)
# print(names)
# print(values)
# print(nominals)


def to_float(a, b):
    lil = a.split(",")
    a = "{}.{}".format(lil[0], lil[1])
    a = float(a) / float(b)
    return a


def clicked():
    ins = (float(txt.get()) * to_float(valute_dict[currency1.get()][0], valute_dict[currency1.get()][1]))\
          / to_float(valute_dict[currency2.get()][0], valute_dict[currency2.get()][1])
    lbl = ttk.Label(tab1, text=ins, width=42)
    lbl.grid(column=1, row=1, padx=10, pady=0)


# вторая вкладка
dates = {'Январь 2019': [31, '01/2019'], 'Февраль 2019': [28, '02/2019'], 'Март 2019': [31, '03/2019'],
         'Апрель 2019': [30, '04/2019'], 'Май 2019': [31, '05/2019'], 'Июнь 2019': [30, '06/2019'],
         'Июль 2019': [31, '07/2019'], 'Август 2019': [31, '08/2019'], 'Сентябрь 2019': [30, '09/2019'],
         'Октябрь 2019': [31, '10/2019'], 'Ноябрь 2019': [30, '11/2019'], 'Декабрь 2019': [31, '12/2019']}
tilt = ["Январь 2019", "Февраль 2019", "Март 2019", "Апрель 2019", "Май 2019", "Июнь 2019",
        "Июль 2019", "Август 2019", "Сентябрь 2019", "Октябрь 2019", "Ноябрь 2019", "Декабрь 2019"]


def plot():
    walk = []
    x_list = []
    for ind in range(0, dates[currency3.get()][0]):
        x_list.append(ind + 1)
        names2 = []
        values2 = []
        nominals2 = []
        if ind < 9:
            strat = "0" + str(ind + 1)
        else:
            strat = str(ind + 1)
        response2 = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req={}/{}"
                                           .format(strat, dates[currency3.get()][1]))
        dom2 = xml.dom.minidom.parse(response2)
        dom2.normalize()
        node_array = dom2.getElementsByTagName("Valute")
        for node2 in node_array:
            child_list = node2.childNodes
            for child2 in child_list:
                if child2.nodeName == "Name":
                    names2.append(child2.childNodes[0].nodeValue)
                if child2.nodeName == "Value":
                    values2.append(child2.childNodes[0].nodeValue)
                if child2.nodeName == "Nominal":
                    nominals2.append(child2.childNodes[0].nodeValue)
        valute_dict2 = {}
        for ind2 in range(0, len(names2)):
            valute_dict2[names2[ind2]] = [values2[ind2], nominals2[ind2]]

        walk.append(to_float(valute_dict2[currency4.get()][0], valute_dict2[currency4.get()][1]))
    matplotlib.use('TkAgg')
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
    plot_widget = canvas.get_tk_widget()
    fig.clear()
    plt.plot(x_list, walk)
    plt.grid()
    plot_widget.grid(column=1, row=2)


window = Tk()
window.title("Конвертер валют")
window.geometry("900x600")

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="курсы валют")
tab_control.add(tab2, text="график")

currency1 = ttk.Combobox(tab1, values=names, width=42)
currency1.grid(column=0, row=0, padx=10, pady=10)
currency2 = ttk.Combobox(tab1, values=names, width=42)
currency2.grid(column=1, row=0, padx=10, pady=10)
txt = ttk.Entry(tab1)
txt.grid(column=0, row=1, padx=10, pady=0)
txt.insert(0, 1)
btn = ttk.Button(tab1, text="Конвертировать", command=clicked)
btn.grid(column=2, row=0, padx=10, pady=0)

currency3 = ttk.Combobox(tab2, values=tilt, width=42)
currency3.grid(column=0, row=0, padx=10, pady=10)
currency4 = ttk.Combobox(tab2, values=names, width=42)
currency4.grid(column=0, row=1, padx=10, pady=10)
btn = ttk.Button(tab2, text="График", command=plot)
btn.grid(column=0, row=2, padx=10, pady=0)

tab_control.pack(expand=True, fill=BOTH)
window.mainloop()
