import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
from fpdf import FPDF
import pandas as pd
from tkinter import *
import tkinter as tk
from tkinter import ttk
import subprocess
import csv
from pandas import DataFrame

#Read the file


df = pd.read_excel(r'C:/Users/BIDN/PycharmProjects/Hydraulics.xlsx', sheet_name='Third proposal', skipinitialspace=True)

#Drop all NaN values
df = df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False)
df.reset_index(drop=False)

PartnoList = df['Part no']
MakersList = df['Maker choice']
GroupList = df['Group']

listGRoupmakers = df['Maker choice'].groupby(df['Group']).apply(list).reset_index(name='Brands')
listMakers = listGRoupmakers['Brands'].tolist()


#---------GUI-----------
root = tk.Tk()
root.resizable(False, False)
root.title("Hydraulics GUI")

root.iconbitmap('C:/Users/BIDN/PycharmProjects/Hydraulics/LogoMAN.ico')

categories = df['Category'].unique().tolist()
groups = df['Group'].unique().tolist()

#Dictionary to dynamically declare variables

d={}
dInt={}
listIndexVariables = []
listVariables = []
listIntVariables =  []
XVariables = []
for x in range(len(listMakers)):
        d["Var{0}".format(x)] = tk.StringVar()
        dInt["NumVar{0}".format(x)] = tk.StringVar()
        XVariables.append(d)
        listIndexVariables.append(dInt)


   ###### Name and variable in dictionary

for key, value in d.items():
        temp = [key, value]
        listVariables.append(temp[1])

r = 0
answers = []
list_of_widgets = []

def clearComboBox():
    for widget in list_of_widgets:
        widget.set('')

for c in categories:
    ttk.Label(text=c, relief=tk.RIDGE, width=15).grid(row=r,column=0)
    categoriesParts = ttk.Combobox(root, textvariable = listVariables[r], values=listMakers[r],width=10, state="readonly")
    categoriesParts.grid(row=r,column=1)
    list_of_widgets.append(categoriesParts)
    r = r + 1

list_of_Stuffwidgets = []

partNoList = []

# Label texts
lbl = Label(root, text="Input T.C. number", font=("Arial Bold", 12))
lbl.grid(column=4, row=0)

# Input text
txt = Entry(root, width=10)
txt.grid(column=4, row=1)
txt.focus()

#Buttons
def clickedTC():
    res = "T.C. nr. " + txt.get()
    lbl.configure(text=res)
    print("res:", res)

    #Title file for PDF

    pdf = FPDF('L')
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=20)

    pdf.cell(200, 30, txt=res,
            ln=3, align='C')

    pdf.cell(200, 30, txt="Input from TC field",
            ln=5, align='C')

    pdf.output("FrontPage.pdf")

    #PDF merge
paths = []
maker =df['Maker choice']
answersInt = []
answersCat = []
indexMakerChoice = []
listGroup  = []

#LIstMakers are already grouped in the proper groups of Excel

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def merge_pdfs(paths, output):
    for x in range(len(listMakers)):
        answers.append(listVariables[x].get())
        answersCat.append(categories[x])
    ######
    for x in range(len(answers)):
        set1 = df.index[df['Maker choice'].isin([answers[x]])].tolist()
        set2 = df.index[df['Category'].isin([answersCat[x]])].tolist()
        setInt = intersection(set1, set2)
        for sublist in setInt:
                indexMakerChoice.append(sublist)
    #######
    print("indexMakerChoice", indexMakerChoice)
    print("answers", answers)
    listPartNo = df.loc[indexMakerChoice, 'Part no'].tolist()
    print("listPartNo", listPartNo)
    listGroup = df.loc[indexMakerChoice, 'Group'].tolist()
    print("listGroup", listGroup)

    patterns = [s + '.pdf' for s in listPartNo]
    paths.append("FrontPage.pdf")
    for pattern in patterns:
        for fn in glob.glob(pattern):
            paths.append(fn)
    print("paths", paths)

    ####CSV
    Qty_csv = list();
    for i in range(len(listGroup)):
        Qty_csv.append(1)

    csvHeader = ['Find_No', 'pos','Part', 'Qty']

    TC_nr = str(txt.get())

    lst2bat = ['kit',TC_nr]
    firstRow = pd.DataFrame(columns=lst2bat)

    dfcsv = pd.DataFrame(columns=csvHeader)

    dfcsv['Find_No'] = [int(x) * 10 for x in listGroup]
    dfcsv['pos'] = [int(y) * 10 for y in listGroup]
    dfcsv['Part'] = listPartNo
    dfcsv['Qty'] = Qty_csv

    print(dfcsv)
    nameCSV = str(txt.get()) + '.csv'
    firstRow.to_csv(nameCSV, sep=';', index=False, header=lst2bat, encoding='utf-8', mode='a')
    dfcsv.to_csv(nameCSV, sep=';', index=False, header=csvHeader, encoding='utf-8', mode='a')

    indexMakerChoice.clear()
    answers.clear()
    answersInt.clear()

    ##############PDFS
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))
    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
    # Clear the files list after configuring
    paths.clear()
    res = txt.get()

def clearComboBox():
    for widget in list_of_widgets:
        widget.set('')

def start_batch():
    subprocess.call([r'C:/Users/BIDN/Desktop/MBD_create_BOM_from_file/MBD_create_BOM_from_file.bat'])
#To be called in button

browseButton_Excel = tk.Button(text='Print Config', command=lambda : [clickedTC(), merge_pdfs(paths, output= str(txt.get()) + '.pdf')], bg='green', fg='white')

browseButton_Excel.grid(column=1, row=50)
browseButton_Clear = tk.Button(text='Clear Config', command=clearComboBox, bg='green', fg='white')
browseButton_Clear.grid(column=4, row=50)
answers.clear()

mainloop()
