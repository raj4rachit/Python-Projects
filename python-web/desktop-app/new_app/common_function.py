from tkinter import messagebox


def checkToken(token):
    if token == '':
        messagebox.showerror("Error", "Token Mismatch.")
        return False
    else:
        return True