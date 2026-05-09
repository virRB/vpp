import tkinter as tk
from tkinter import filedialog
import subprocess
import time
import keyboard
import atexit
loaded_file = None
root = tk.Tk()
root.geometry('75x110+100+100')
vars = []
varvals = []
labels = []
text_labels = []
functions = []
nest_level = 0
in_func = False
main_win_name = ""
entry = tk.Entry(root)
entry.pack()
in_if = False
output = ""
default_imports = 'import os\nimport pyautogui\nimport time\nimport tkinter as tk\nfrom tkinter import messagebox'

def get_text_label(label):
    for tl in text_labels:
        if tl == label:
            return tl
def clear():
    global labels
    for label in labels:
        label.destroy()
    with open("runitme.py", "w") as f:
        f.write(default_imports)
    entry.delete(0, tk.END)

clear()

his = tk.Toplevel()
his.geometry('400x500+700+100')

def get_val(var):
    if var in vars:
        return varvals[vars.index(var)]
    
def edit_val(var, num, type):
    if var in vars:
        index = vars.index(var)
        current_val = int(varvals[index])
        
        if type == 'plus':
            varvals[index] = current_val + num
        elif type == 'minus':
            varvals[index] = current_val - num
        elif type == 'equal':
            varvals[index] = num
        print(varvals[index])

def upload():
    global loaded_file

    clear()

    file = filedialog.askopenfilename(
        filetypes=[("VPP files", "*.vpp")]
    )

    if file:
        loaded_file = file
        lab(f"Loaded: {file}")

        with open(loaded_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            if line:
                send(line)

        his.update()

def lab(m):
    label = tk.Label(his, text=m)
    label.pack()
    labels.append(label)

def do():
    time.sleep(2)
    subprocess.run("python runitme.py", shell=True)

def run(cmd):
    with open("runitme.py", "a") as f:
        f.write("\n" + cmd)

def send(thingy):
    global main_win_name
    global in_if
    global text_labels
    global functions
    global in_func
    global nest_level
    global output
    result = thingy.strip()
    if ':' in result:
        command = result.split(':')
        cmd = command[0].strip()
        msg = command[1].strip()
        
        output = ""
        if cmd == 'mouse':
            coords = [c.strip() for c in msg.split(',')]
            x = int(coords[0])
            y = int(coords[1])
            output = f'pyautogui.moveTo({x}, {y})'
        elif cmd == 'click':
            cc = [c.strip() for c in msg.split(',')]
            x = int(cc[0])
            y = int(cc[1])
            output = f'pyautogui.click({x}, {y})'
        elif cmd == 'wait':
            output = f'time.sleep({int(msg)})'
        elif cmd == 'int':
            things = msg.split('=')
            name = things[0]
            val = things[1]
            vars.append(name)
            varvals.append(int(val))
            print(get_val(name))
            output = f'{name} = {int(val)}'
        elif cmd == 'str':
            things = msg.split('=')
            name = things[0]
            val = things[1]
            vars.append(name)
            varvals.append(str(val))
            print(get_val(name))
            output = f"{name} = '{str(val)}'"
        elif cmd == 'print_var':
            output = f'print({msg})'
        elif cmd == 'print_str':
            output = f"print('{msg}')"
        elif cmd == 'main_win':
            if ', ' in msg:
                stuffy = msg.split(', ')
                namey = stuffy[0]
                geometry = stuffy[1]
                output = f"{namey} = tk.Tk()\n{namey}.geometry('{geometry}')"
                main_win_name = namey
            else:
                print('Undefined win properties')
        elif cmd == 'end':
            if main_win_name and msg == main_win_name:
                output = f'{main_win_name}.mainloop()'
        elif cmd == 'text':
            if main_win_name:
                if ', ' in msg:
                    stuffy2 = msg.split(', ')
                    var = stuffy2[0]
                    text_labels.append(var)
                    text = stuffy2[1]
                    output = f"{var} = tk.Label({main_win_name}, text='{text}')"
        elif cmd == 'configurate':
            if ', ' in msg:
                stuffy7 = msg.split(', ')
                tl = stuffy7[0]
                newtext = stuffy7[1]
                output = f"{tl}.config(text='{newtext}')"
        elif cmd == 'adjust':
            if '+=' in msg:
                stuffy3 = msg.split('+=')
                varname = stuffy3[0]
                edit = stuffy3[1]
                edit_val(str(varname), int(edit), 'plus')
                output = f'{varname} += {edit}'
            elif '-=' in msg:
                stuffy4 = msg.split('-=')
                varname = stuffy4[0]
                edit = stuffy4[1]
                edit_val(str(varname), int(edit), 'minus')
                output = f'{varname} -= {edit}'
            elif '=' in msg:
                stuffy6 = msg.split('=')
                var = stuffy6[0]
                eqvl = stuffy6[1]
                edit_val(var, int(eqvl), 'equal')
                output = f'{var} = {eqvl}'
        elif cmd == 'if':
            stuffy5 = msg.split('==')
            var = stuffy5[0]
            tst = stuffy5[1]
            output = f"if {var} == {tst}:"
            nest_level += 1
            print(nest_level)
            in_if = True
        elif cmd == 'endif':
            if in_if:
                in_if = False
                nest_level -= 1
                print(nest_level)
            else:
                print('Cannot call endif outside of an if statement')
            output = "#end if statement"
        elif cmd == 'func':
            if msg:
                functions.append(msg)
                in_func = True
                output = f'def {msg}():'
                nest_level += 1
                print(nest_level)
        elif cmd == 'endfunc':
            if in_func:
                in_func = False
                nest_level -= 1
                print(nest_level)
                output = "#end of function"
            else:
                print('cannot call endfunc while not inside a function')
        elif cmd == 'call':
            if msg in functions:
                output = f"{msg}()"
            else:
                print('function not recognised')
        elif cmd == 'button':
            stuffy8 = msg.split(', ')
            varname = stuffy8[0]
            text = stuffy8[1]
            cmnd = stuffy8[2]
            output = f"{varname} = tk.Button({main_win_name}, text='{text}', command={cmnd})"
        elif cmd == 'msg':
            stuff = msg.split(';')
            typ = stuff[0]
            val = stuff[1]
            if typ == 'str':
                output = f"messagebox.showinfo('Message', '{val}')"
            elif typ == 'var':
                output = f"messagebox.showinfo('Message', str({val}))"
        elif cmd == 'globalify':
            output = f"global {msg}"
        elif cmd == 'chaos':
            output = f"nevergon = tk.Label({main_win_name}, text='-. . ...- . .-. / --. --- -. -. .- / --. .. ...- . / -.-- --- ..- / ..- .--.')\nnevergon.pack()"
        elif cmd == '$':
            output = f"#{msg}"
        elif cmd == 'append':
            output = f"{msg}.pack()"
            
    if output:
        if cmd == 'if' and not in_func:
            run(output)

        elif cmd == 'func':
            run(output)

        elif cmd == 'endif':
            run(output)

        elif cmd == 'endfunc':
            run(output)

        else:
            if cmd == 'if' and in_func:
                nest_level -=1
                indent = "    " * nest_level
                run(indent + output)
                nest_level += 1
            else:
                indent = "    " * nest_level
                run(indent + output)
        lab(thingy)
    else:
        print('Invalid syntax')
    entry.delete(0, tk.END)



def parse(msg):
    if '; ' in msg:
        msgs = msg.split('; ')
        for thing in msgs:
            send(thing)
    else:
        send(msg)

def pl(*args):
    parse(entry.get())

sendb = tk.Button(root, text='Run', command=do)
sendb.pack()

cl = tk.Button(root, text='Clear', command=clear)
cl.pack()

uploadb = tk.Button(root, text='Upload', command=upload)
uploadb.pack()

def cleanup():
    with open("runitme.py", "w") as f:
        f.write(default_imports)

atexit.register(cleanup)

keyboard.on_press_key('enter', lambda e: pl())
root.mainloop()