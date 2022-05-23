import PySimpleGUI as sg
import io
import os.path
from PIL import Image
import imageanalysis, time



#Debug################
debug = False
######################

#Define Layout for 3 columns

#Column for selecting file
file_list_column = [
    [   
        sg.Text('Please select an image to convert.'),
    ],
    [
        sg.Text('Selected Image folder: '),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [   
        sg.Text('Files in selected folder:'),
        sg.Listbox(
            values=[], default_values='Please select a folder', enable_events=True, size=(25, 30), key="-FILE LIST-"
        )
    ],
]

#Convert button column
convert_column = [
    [
    sg.Button(button_text="Convert")
    ],
]

#Image viewing column
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# Keycodes for selecting buttons with keyboard
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'

#Define windows layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(convert_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

#Make Window object
window = sg.Window("Sensi Vibrotactile Image Converter", layout, icon='icon.ico')

# Run Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Populate list of files in selected folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", '.jpg','.jpeg'))
        ]
        window["-FILE LIST-"].update(fnames)
    
    # Check for ENTER key
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):         
        # go find element with Focus
        elem = window.find_element_with_focus()
         # if it's a button element, click it
        if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:      
            elem.Click()

    #Identify file chosen from list
    elif event == "-FILE LIST-": 
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)

            pil_image = Image.open(filename)
            png_bio = io.BytesIO()
            pil_image.save(png_bio, format="PNG")
            png_data = png_bio.getvalue()
            window["-IMAGE-"].update(data=png_data)
            sg.Popup(values["-FILE LIST-"][0], ' selected!')
        except:
            pass

    #Convert image when convert button pressed
    elif event == 'Convert':
        try:
            print(filename)
            start = time.time()
            result = imageanalysis.convertimage(filename,debug)
            end = time.time()
            elapsed = end-start
            print('Time: ',elapsed,' seconds')
            if result == True:
                sg.Popup('Conversion Succesful!')
            if result == False:
                sg.Popup('USB Error')
        except:
            sg.Popup('Conversion Failed')

window.close()