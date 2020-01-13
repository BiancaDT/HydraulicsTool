# import statement for GUI
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from fpdf import FPDF
import os
import fnmatch


#Window settings
window = Tk()
window.title("Hydraulics GUI")
window.geometry('800x500')
#window.configure(background='lightblue')

# Label texts
lbl = Label(window, text="Input engine number", font=("Arial Bold", 12))
lbl.grid(column=6, row=0)

# Input text
txt = Entry(window, width=10)
txt.grid(column=6, row=1)
txt.focus()

#List of answers
answers = []

#Buttons
def clicked():
    res = "Engine nr. " + txt.get()
    lbl.configure(text=res)

#Text input
btn = Button(window, text="Save", command=clicked)
btn.grid(column=6, row=2)

#Second label
lblTC = Label(window, text="Input T.C. number", font=("Arial Bold", 12))
lblTC.grid(column=6, row=3)

txtTC = Entry(window, width=10)
txtTC.grid(column=6, row=4)

def clickedTC():
    resTC = "TC nr. " + txtTC.get()
    lblTC.configure(text=resTC)

#Text input
btnTC = Button(window, text="Save", command=clickedTC)
btnTC.grid(column=6, row=5)


#For Filters
#To get input from filters
def clickRadioFilters():
    print(selectedFilters.get())


selectedFilters = StringVar()
lblFilters = Label(window, text="ME-Filter", font=("Arial Bold", 12))
lblFilters.grid(column=5, row=8)
radF1 = Radiobutton(window, text='Hydac', value='0001', command=clickRadioFilters, variable=selectedFilters)
radF2 = Radiobutton(window, text='Alfa Laval', value='0002', command=clickRadioFilters, variable=selectedFilters)
radF3 = Radiobutton(window, text='B&K', value='0003', command=clickRadioFilters, variable=selectedFilters)
radF4 = Radiobutton(window, text='Kanagawa', value='0004', command=clickRadioFilters, variable=selectedFilters)
#Add to list


#Arrangement of the radios
radF1.grid(column=7, row=8)
radF2.grid(column=8, row=8)
radF3.grid(column=9, row=8)
radF4.grid(column=10, row=8)

#Radio buttons section
def clickRadioPumps():
    print(selectedPumps.get())


#For pumps

selectedPumps = StringVar()
lblPumps = Label(window, text="HPS", font=("Arial Bold", 12))
lblPumps.grid(column=5, row=10)
radP1 = Radiobutton(window, text='Bosch Rexroth', value='0005', command=clickRadioPumps, variable=selectedPumps)
radP2 = Radiobutton(window, text='Eaton', value='0006', command=clickRadioPumps, variable=selectedPumps)
radP3 = Radiobutton(window, text='Parker', value='0007', command=clickRadioPumps, variable=selectedPumps)
radP4 = Radiobutton(window, text='EL-Bosch Rexroth', value='0008', command=clickRadioPumps, variable=selectedPumps)
radP5 = Radiobutton(window, text='EL-Eaton', value='0009', command=clickRadioPumps, variable=selectedPumps)
radP6 = Radiobutton(window, text='EL-Parker', value='0010', command=clickRadioPumps, variable=selectedPumps)
#Add to list


#Arrangement of the radios
radP1.grid(column=7, row=10)
radP2.grid(column=8, row=10)
radP3.grid(column=9, row=10)
radP4.grid(column=7, row=11)
radP5.grid(column=8, row=11)
radP6.grid(column=9, row=11)

#For Exh valves
#To get input from valves
def clickRadioValves():
    print(selectedValves.get())


selectedValves = StringVar()
lblValves = Label(window, text="Exhaust Valves", font=("Arial Bold", 12))
lblValves.grid(column=5, row=12)
radV1 = Radiobutton(window, text='Low Force', value='0011', command=clickRadioValves, variable=selectedValves)
radV2 = Radiobutton(window, text='TCEV', value='0012', command=clickRadioValves, variable=selectedValves)
#Add to list


#Arrangement of the radios
radV1.grid(column=7, row=12)
radV2.grid(column=9, row=12)

separator = ttk.Separator(window).place(x=0, y=225, relwidth=2)

#######OPTIONALS

#For LPS
#To get input from LPS
def clickCheckLPS():
    print(chkLPS_state.get())


varLPS = StringVar()
lblLPS = Label(window, text="LPS booster", font=("Arial Bold", 12))
lblLPS.grid(column=5, row=18)

chkLPS_state = BooleanVar()

chkLPS_state.set(False)  # set check state

chkLPS = Checkbutton(window, var=chkLPS_state, onvalue="True", command=clickCheckLPS)

#Arrangement of the radios
chkLPS.grid(column=7, row=18)

##################

#For THS
#To get input from THS
def clickCheckTHS():
    print(chkTHS_state.get())

varTHS = StringVar()
lblTHS = Label(window, text="THS 2", font=("Arial Bold", 12))
lblTHS.grid(column=5, row=20)

chkTHS_state = BooleanVar()

chkTHS_state.set(False)  # set check state

chkTHS = Checkbutton(window, var=chkTHS_state, onvalue="True", command=clickCheckTHS)

#Arrangement of the radios
chkTHS.grid(column=7, row=20)

##########
#Button print PDFs
################################################################

####PDF

def merge_pdfs(paths, output):
    answers.append(selectedFilters.get())
    answers.append(selectedPumps.get())
    answers.append(selectedValves.get())
    if chkLPS_state.get() == True:
        answers.append('0013')
    if chkTHS_state.get() == True:
        answers.append('0014')
    print("ME-Filter: ", answers[0], ", HPS: ", answers[1], ", Exhaust valves: ", answers[2])
    print(answers)
    #Check content of answers list
    if '0001' in answers:
        print("Yes, 0001")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0001-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0002' in answers:
        print("Yes, '0002")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0002-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0003' in answers:
        print("Yes, '3")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0003-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0004' in answers:
        print("Yes, 4")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0004-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0005' in answers:
        print("Yes, 0005")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0005-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0006' in answers:
        print("Yes, '0006")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0006-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0007' in answers:
        print("Yes, '7")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0007-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0008' in answers:
        print("Yes, 8")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0008-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0009' in answers:
        print("Yes, '9")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0009-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0010' in answers:
        print("Yes, 10")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0010-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0011' in answers:
        print("Yes, 0011")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0011-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0012' in answers:
        print("Yes, '0012")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0012-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0013' in answers:
        print("Yes, '13")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0013-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)
    if '0014' in answers:
        print("Yes, 14")
        for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
            if fnmatch.fnmatch(file_name, '*0014-*.pdf'):
                print('File name: ', file_name)
                paths.append(file_name)

    #Clear the list for next config
    answers.clear()
    ##############PDFS
    pdf_writer = PdfFileWriter()
    #pdf_writer.addPage('')

    for path in paths:
        pdf_reader = PdfFileReader(path)
        #pdf_reader.addBlankPage()
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

    # Clear the files list after configuring
    paths.clear()

if __name__ == '__main__':
#  entries = os.listdir('C:/Users/BIDN/PycharmProjects')
#  print('Files in directory: ',entries)
#   for entry in entries:
#        print(entry)
    for file_name in os.listdir('C:/Users/BIDN/PycharmProjects'):
        if fnmatch.fnmatch(file_name, '*0001-*.pdf'):
            print('File name: ',file_name)
    paths = []
    #merge_pdfs(paths, output='mergedPDF.pdf')

btn = Button(window, text="Print Config", command=lambda : merge_pdfs(paths, output='HydraulicPartsMerged.pdf'))

btn.grid(column=8, row=50)

#Put all changes above this line
#Show GUI, must be the final statement
window.mainloop()