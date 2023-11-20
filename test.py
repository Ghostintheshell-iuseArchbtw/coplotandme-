import subprocess
import tkinter as tk
from tkinter import filedialog

def burn_iso_to_usb(iso_file, usb_drive):
    try:
        # Run the dd command to burn the ISO to the USB drive
        subprocess.run(['dd', 'if=' + iso_file, 'of=' + usb_drive, 'bs=4M'])
        print('ISO burned to USB successfully!')
    except Exception as e:
        print('Error burning ISO to USB:', str(e))

def select_iso_file():
    # Open a file dialog to select the ISO file
    iso_file = filedialog.askopenfilename(filetypes=[('ISO Files', '*.iso')])
    iso_file_entry.delete(0, tk.END)
    iso_file_entry.insert(0, iso_file)

def select_usb_drive():
    # Open a file dialog to select the USB drive
    usb_drive = filedialog.askdirectory()
    usb_drive_entry.delete(0, tk.END)
    usb_drive_entry.insert(0, usb_drive)

def burn_iso():
    # Get the ISO file path and USB drive path from the user
    iso_file = iso_file_entry.get()
    usb_drive = usb_drive_entry.get()

    # Call the burn_iso_to_usb function
    burn_iso_to_usb(iso_file, usb_drive)

# Create the main window
window = tk.Tk()
window.title('ISO Burner')

# Create the ISO file selection label and entry
iso_file_label = tk.Label(window, text='ISO File:')
iso_file_label.pack()
iso_file_entry = tk.Entry(window)
iso_file_entry.pack()
iso_file_button = tk.Button(window, text='Select', command=select_iso_file)
iso_file_button.pack()

# Create the USB drive selection label and entry
usb_drive_label = tk.Label(window, text='USB Drive:')
usb_drive_label.pack()
usb_drive_entry = tk.Entry(window)
usb_drive_entry.pack()
usb_drive_button = tk.Button(window, text='Select', command=select_usb_drive)
usb_drive_button.pack()

# Create the burn button
burn_button = tk.Button(window, text='Burn ISO', command=burn_iso)
burn_button.pack()

# Start the main loop
window.mainloop()
