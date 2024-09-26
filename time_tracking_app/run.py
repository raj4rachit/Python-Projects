import PySimpleGUI as sg
import bcrypt

# Function to hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# Function to check the hashed password
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Define the theme for the design
sg.theme('BlueMono')  # Add a touch of color

# Define the layout for the login window
layout = [
    [sg.Text('Welcome to the Employee Management System', font=('Any', 15), justification='center', expand_x=True)],
    [sg.Frame(layout=[
        [sg.Text('Username', size=(10, 1)), sg.InputText(key='username')],
        [sg.Text('Password', size=(10, 1)), sg.InputText(key='password', password_char='*')]
    ], title='Login Details', relief=sg.RELIEF_SUNKEN)],
    [sg.Button('Login', bind_return_key=True), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Employee Management System', layout, size=(800, 600))

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Login':
        username = values['username']
        password = values['password']
        # Here you would retrieve the hashed password from your database
        # For demonstration, we'll use a pre-hashed password
        hashed_pw_from_db = b'$2y$12$n68BTs4zh.0cdm0xFuugqeo1Hfvf9JhjR.017mzaF/C25g.6pD9zq'
        if check_password(hashed_pw_from_db, password):
            sg.popup('Login Successful!', title='Success')
        else:
            sg.popup('Invalid username or password.', title='Error')

window.close()
