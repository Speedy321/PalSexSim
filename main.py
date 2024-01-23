import csv
import PySimpleGUI as sg

import sys
import os
 
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#ui keys
WANT_CH = "wanted-child"
WANT_P1 = "wanted-parent1"
WANT_PS = "wanted-parents"
CHK_P1 = "check_parent1"
CHK_P2 = "check_parent2"
CHK_CH = "check_child"
POT_P1 = "potential-parent1"
POT_RES = "potential-results"

BTN_LOOK = "Look Up"

def load_data():
    data = []

    with open(resource_path("all_data.csv"), "r") as df:
        reader = csv.reader(df, delimiter=",")
        for row in reader:
            data.append(row)
        
    return data

def find_child(data: list[list[str]], parent1_name: str, parent2_name: str) -> str|None:
    x = None
    y = None
    
    if (not parent1_name) or (not parent2_name):
        return None

    for i in range(2, len(data[1])):
        if parent1_name in data[1][i]:
            x = i
            break
    
    for j in range(2, len(data)):
        if parent2_name in data[j][1]:
            y = j
            break
    
    if x and y:
        return data[y][x]
    
    return None

def find_parents(data: list[list[str]], child_name: str, filter_parent: str | None = None) -> list[tuple[str, str]] | None:
    parents = []

    if not child_name:
        return None

    for x in range(2, len(data[1])):
        for y in range(2, len(data)):
            if child_name in data[y][x]:
                ps = (data[1][x], data[y][1])
                
                duplicate = False
                for p in parents:
                    if (ps[0] in p[1]) and (ps[1] in p[0]):
                        duplicate = True
                
                if not duplicate:
                    if filter_parent:
                        if filter_parent in ps:
                            parents.append(ps)
                    else:
                        parents.append(ps)
    
    if parents:
        return parents
    
    return None

def find_potentials(parent_name: str) -> list[tuple[str, str]] | None:
    results = []

    if not parent_name:
        return None

    for x in range(2, len(data[1])):
        for y in range(2, len(data)):
            if parent_name in data[y][1]:
                results.append((data[y][x], data[1][x]))
    
    if results:
        results.sort()
        return results
    else:
        return None



if __name__ == "__main__":
    data = load_data()

    names = [name for name in data[1][2:]]
    names.sort()
    names.insert(0, "")

    child_layout = [
        [sg.Text("Find Parents:")],
        [sg.Text("Wanted Child:"), sg.DropDown(values=names, key=WANT_CH, enable_events=True)],
        [sg.Text("Filter parent (optional):"), sg.DropDown(values=names, key=WANT_P1, enable_events=True)],
        [sg.Text("Parents:")],
        [sg.Multiline("None", key=WANT_PS, disabled=True, size=(40, 10))]
    ]

    check_layout = [
        [sg.Text("Check Match:")],
        [sg.Text("Parent 1:"), sg.DropDown(values=names, key=CHK_P1, enable_events=True)],
        [sg.Text("Parent 2:"), sg.DropDown(values=names, key=CHK_P2, enable_events=True)],
        [sg.Text("Child:"), sg.InputText("None", key=CHK_CH, disabled=True, size=(25, 1))]
    ]

    potentials_layout = [
        [sg.Text("Potential Childs:")],
        [sg.Text("Parent 1:"), sg.DropDown(values=names, key=POT_P1, enable_events=True)],
        [sg.Text("Results:")],
        [sg.Multiline("None", key=POT_RES, disabled=True, size=(40, 12))]
    ]

    layout = [
        [sg.Column(child_layout, vertical_alignment="top"), sg.VerticalSeparator(), 
         sg.Column(check_layout, vertical_alignment="top"), sg.VerticalSeparator(), 
         sg.Column(potentials_layout, vertical_alignment="top")],
    ]
    
    window = sg.Window('Pal Sex Simulator', layout)

    while True:             # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif (event == WANT_CH) or (event == WANT_P1):
            parents = find_parents(data, values[WANT_CH], values[WANT_P1])

            if parents:
                result_str = ""
                for p in parents:
                    result_str = result_str + f"{p[0]} + {p[1]}\n"

                window[WANT_PS].update(result_str)
            else:
                window[WANT_PS].update("None")

        elif (event == CHK_P1) or (event == CHK_P2):
            child = find_child(data, values[CHK_P1], values[CHK_P2])

            if child:
                window[CHK_CH].update(child)
            else:
                window[CHK_CH].update("None")

        elif event == POT_P1:
            results = find_potentials(values[POT_P1])

            if results:
                res_str = ""

                for res in results:
                    child, parent = res
                    res_str = res_str + f"{child} with {parent}\n"

                window[POT_RES].update(res_str)
            else:
                window[POT_RES].update("None")

    window.close()
