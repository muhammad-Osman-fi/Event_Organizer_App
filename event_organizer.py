#                                            EVENT ORGANIZER
#                                      Copyright 2024 Usman Aslam
#                              Licensed under the Apache License, Version 2.0

import tkinter as tk
import re
import sqlite3
import qrcode
import tempfile
import smtplib
import os
import cv2
from pyzbar.pyzbar import decode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import threading
from datetime import datetime

root = tk.Tk()
root.title("EVENT ORGANIZER")
root.configure(bg="gray")

global update_statistics

home=tk.Frame(root,bg='gray')
home.grid(row=1,column=0,sticky="nsew")

stats_frame=tk.Frame(home, bg="teal", padx=20, pady=10)
stats_frame.grid(row=0, column=1, sticky="nsew")

pre_listbox=tk.Listbox(home, borderwidth=2,width=10,bg="gray",fg="white", height=20, font=("Helvetica", 14))
pre_listbox.grid(row=3, column=1, padx=20, pady=10, sticky="w")

p_lbl=tk.Label(stats_frame, text=0, bg="teal", fg="white", font=("castellar", 14))
p_lbl.grid(row=2,column=0)

a_lbl=tk.Label(stats_frame, text=0, bg="teal", fg="white", font=("castellar", 14))
a_lbl.grid(row=3,column=0)

t_amount=tk.Label(stats_frame, text=0, bg="teal", fg="white", font=("castellar", 14))
t_amount.grid(row=4,column=0)

totall=tk.Label(stats_frame, text=0, bg="teal", fg="white", font=("castellar", 14))
totall.grid(row=0,column=0)

add_frame = tk.Frame(root, bg="gray", padx=20, pady=10)
add_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
add_frame.grid_forget()

def fill_dattetime_entry():
    current_datetime = datetime.now().strftime("%Y-%m-%d | %H:%M:%S %p")
    dattetime_entry.delete(0, tk.END)
    dattetime_entry.insert(0, current_datetime)

def update_statistics():
    total_guests = home_listbox.size()
    present_guests = pre_listbox.size()
    absent_guests = total_guests - present_guests

    total_amount = 0

    try:
        with sqlite3.connect("guests.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT payment FROM guests')
            payments = cursor.fetchall()

            for payment in payments:
                total_amount += float(payment[0])

    except sqlite3.Error as e:
        print("SQLite error:", e)

    totall.config(text=f"Total Guests: {total_guests}")
    p_lbl.config(text=f"Present: {present_guests}")
    a_lbl.config(text=f"Absent: {absent_guests}")
    t_amount.config(text=f"Total Amount: {total_amount}€")

def validate_email(event):
    email = Email_entry.get()
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    result_label = tk.Label(add_frame, text="", font=("Arial", 14))
    result_label.grid(row=4, column=2, sticky="w")
    result_label.after(3000,result_label.destroy)
    

    if re.match(email_pattern, email):
        result_label.config(text="Valid Email", fg="green")

    else:
        result_label.config(text="Invalid Email", fg="red")

def validate_payment(P):
    return re.match(r'^\d*\.?\d*$', P) is not None


conn = sqlite3.connect("guests.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS guests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    event_name TEXT,
                    email TEXT,
                    payment TEXT,
                    payment_type TEXT,
                    dattetime TEXT,
                    male_or_female TEXT
                )''')
conn.commit()

entry_widgets = []    
    
def update_home_list():
    home_listbox.delete(0, "end")
    try:
        with sqlite3.connect("guests.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, event_name, email, payment, payment_type, dattetime, male_or_female FROM guests')
            guest_data = cursor.fetchall()
            for guest_info in guest_data:
                name, event_name, email, payment, payment_type, dattetime, male_or_female = guest_info
                home_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                                          f"||, {payment} ||, {payment_type} "
                                          f"||, {dattetime} ||, {male_or_female}")
    except sqlite3.Error as e:
        print("SQLite error:", e)
    update_statistics()
    

def add_fun():
    home.grid_forget()
    add_frame.grid()
    

def back_func():
    add_frame.grid_forget()
    home.grid()

def add_guest():
    global email
    name = name_entry.get()
    event_name = Event_entry.get()
    email = Email_entry.get()
    payment = payment_entry.get()
    payment_type = payment_type_entry.get()
    dattetime = dattetime_entry.get()
    
    if ggender_var.get() == 1:
        male_or_female = "Male"
    else:
        ggender_var.get()==2
        male_or_female ="Female"

    try:
        with sqlite3.connect("guests.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO guests (name, event_name, email, payment, payment_type, dattetime, male_or_female)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, event_name, email, payment, payment_type, dattetime, male_or_female))
            conn.commit()
            

    except sqlite3.Error as e:
        print("SQLite error:", e)
        
    update_home_list()
    name_entry.delete(0, tk.END)
    Event_entry.delete(0, tk.END)
    Email_entry.delete(0, tk.END)
    payment_entry.delete(0, tk.END)
    payment_type_entry.delete(0, tk.END)
    dattetime_entry.delete(0, tk.END)
    ggender_var.set(0)
    
    update_statistics()

enttry_var = tk.StringVar()
save_btn=tk.Button(add_frame, text=" ADD ",command=add_guest, font=("castellar", 16))
save_btn.grid(row=9, column=1, sticky="nsew")
            
Email_entry = tk.Entry(add_frame, borderwidth=2.5, font=("Helvetica", 16))
Email_entry.grid(row=4, column=1, sticky="ew")
email=Email_entry.get()
home_listbox = tk.Listbox(home, borderwidth=2,width=80,bg="gray",fg="white", height=20, font=("Helvetica", 14))
home_listbox.grid(row=3, column=0, padx=20, pady=10, sticky="w")
update_home_list()
update_statistics()

side_bar = tk.Frame(home, bg="teal", padx=20, pady=10)
side_bar.grid(row=0, column=0, sticky="ne")

def filtering():
    male_selected = gender_var.get() == 1
    female_selected = gender_var.get() == 2
    min_payment = pay_ent.get()
    max_payment = pay2_ent.get()
    
    home_listbox.delete(0, "end") 

    try:
        with sqlite3.connect("guests.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, event_name, email, payment, payment_type, dattetime, male_or_female FROM guests')
            guest_data = cursor.fetchall()
            
            for guest_info in guest_data:
                name, event_name, email, payment, payment_type, dattetime, male_or_female = guest_info

                if (male_selected and male_or_female == "Male") or (female_selected and male_or_female == "Female"):
                    if min_payment and max_payment:
                        if float(min_payment) <= float(payment) <= float(max_payment):
                            home_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                                                    f"||, {payment} ||, {payment_type} "
                                                    f"||, {dattetime} ||, {male_or_female}")
                            
                    else:
                        home_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                                                f"||, {payment} ||, {payment_type} "
                                                f"||, {dattetime} ||, {male_or_female}")
                        
    except sqlite3.Error as e:
        print("SQLite error:", e)
    update_statistics()

def clear_filters():
    gender_var.set(0)  
    pay_ent.delete(0, "end")  
    pay2_ent.delete(0, "end")
    update_home_list()

def update_and_clear():
    update_home_list()
    clear_filters()

def search_guests():
    conn = sqlite3.connect("guests.db")
    cursor = conn.cursor()
    search_name = sear_ent.get()
    
    cursor.execute("SELECT name, event_name, email, payment, payment_type, dattetime, male_or_female FROM guests")
    guest_data = cursor.fetchall()

    home_listbox.delete(0, "end")

    for guest_info in guest_data:
        name, event_name, email, payment, payment_type, dattetime, male_or_female = guest_info

        if search_name.lower() in name.lower():

            home_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                                      f"||, {payment} ||, {payment_type} "
                                      f"||, {dattetime} ||, {male_or_female}")
    update_statistics()
    
        
pathh="C:/Users/adminpc/Desktop/search_symbol.png"
texxt= tk.PhotoImage(file=pathh)

sear_ent=tk.Entry(side_bar,font=("Arial", 20))
sear_ent.grid_remove()

sear_btn=tk.Button(side_bar,image=texxt,bg="white",command=search_guests)
sear_btn.grid_remove()

def search_widgets():

    if sear_ent.winfo_viewable():  
        sear_ent.grid_remove()  
        sear_btn.grid_remove()  
    else:
        sear_ent.grid(row=1, column=3)  
        sear_btn.grid(row=1, column=4)  
        


gender_var = tk.IntVar()
global m_ch, f_ch, pay_lbl, pay2_lbl, pay2_ent, pay_ent

m_ch=tk.Radiobutton(side_bar, text="Male", font=("Arial", 12), variable=gender_var, value=1)
m_ch.grid_forget()

f_ch=tk.Radiobutton(side_bar, text="Female", font=("Arial", 12), variable=gender_var, value=2)
f_ch.grid_forget()

pay_lbl=tk.Label(side_bar,text="From",font=("Arial", 12))
pay_lbl.grid_forget()

pay_ent=tk.Entry(side_bar,font=("Arial", 12))
pay_ent.grid_forget()

pay2_lbl=tk.Label(side_bar,text="To",font=("Arial", 12))
pay2_lbl.grid_forget()

pay2_ent=tk.Entry(side_bar,font=("Arial", 12))
pay2_ent.grid_forget()

ok_btn=tk.Button(side_bar,text="  OK  ",command=filtering,font=("Arial", 12))
ok_btn.grid_forget()

clear_btn=tk.Button(side_bar,text="  CLEAR  ",command=update_and_clear,font=("Arial", 12))
clear_btn.grid_forget()

def filter_it():

    m_ch.grid(row=1,column=5)
    f_ch.grid(row=1,column=6)

    pay_lbl.grid(row=2,column=5)
    pay_ent.grid(row=2,column=6)

    pay2_lbl.grid(row=3,column=5)
    pay2_ent.grid(row=3,column=6)

    ok_btn.grid(row=4, column=6)
    clear_btn.grid(row=4, column=5)
    
def hide_widgets(event):

    if event.widget == home:
        m_ch.grid_remove()
        f_ch.grid_remove()

        pay_lbl.grid_remove()
        pay_ent.grid_remove()

        pay2_lbl.grid_remove()
        pay2_ent.grid_remove()

        ok_btn.grid_remove()
        clear_btn.grid_remove()
        
        sear_ent.grid_remove()
        sear_btn.grid_remove()    

save_btn.config(state="disabled")
def check_entry_contents():
    if enttry_var.get():
        save_btn.config(state="normal")
    else:
        save_btn.config(state="disabled")

home_lbl=tk.Label(home,text="GUEST LIST", bg="gray", fg="white", font=("Helvetica", 20))
home_lbl.grid(row=2, column=0, sticky="nsew")

home_lbl1=tk.Label(home,text="Present Guests", bg="gray", fg="white", font=("Helvetica", 20))
home_lbl1.grid(row=2, column=1, sticky="nsew")

space_lbl = tk.Label(side_bar, bg="teal", text=" " * 75)
space_lbl.grid(row=0, column=0, sticky="nsew")

space_lbl = tk.Label(side_bar, bg="teal", text=" " * 75)
space_lbl.grid(row=0, column=6, sticky="nsew")

space_lbl = tk.Label(side_bar, bg="teal", text="  ")
space_lbl.grid(row=0, column=2, sticky="nsew")

space_lbl2 = tk.Label(side_bar, bg="teal", text="  ")
space_lbl2.grid(row=0, column=4, sticky="nsew")

add_lbl = tk.Label(add_frame, text="ADD YOUR GUESTS' INFORMATION", bg="gray", fg="white", font=("Helvetica", 20))
add_lbl.grid(row=0, column=1, sticky="nsew")

home_btn=tk.Button(add_frame,text=" <  ",borderwidth=2,command=back_func, font=("Arial",15))
home_btn.grid(row=0, column=0, sticky="nw")

name_lbl = tk.Label(add_frame, text="NAME: ", bg="teal", fg="white", font=("castellar", 16))
name_lbl.grid(row=2, column=0, sticky="w")

Event_lbl = tk.Label(add_frame, text="EVENT NAME: ", bg="teal", fg="white", font=("castellar", 16))
Event_lbl.grid(row=3, column=0, sticky="w")

Email_lbl = tk.Label(add_frame, text="EMAIL ADDRESS: ", bg="teal", fg="white", font=("castellar", 16))
Email_lbl.grid(row=4, column=0, sticky="w")

ggender_var = tk.IntVar()
checkbox1 = tk.Radiobutton(add_frame, text="Male", font=("castellar", 16), variable=ggender_var,value=1)
checkbox1.grid(row=8, column=0, sticky="w")

checkbox2 = tk.Radiobutton(add_frame, text="Female", font=("castellar", 16), variable=ggender_var,value=2)
checkbox2.grid(row=8, column=1, sticky="w")

additional_labels = ["PAYMENT:", "PAYMENT TYPE:", "DATE AND TIME:"]

for i, label_text in enumerate(additional_labels):

    label = tk.Label(add_frame, text=label_text, bg="teal", fg="white", font=("castellar", 16))
    label.grid(row=i + 5, column=0, sticky="w")

name_entry = tk.Entry(add_frame, borderwidth=2.5, font=("Helvetica", 16))
name_entry.grid(row=2, column=1, sticky="ew")

Event_entry = tk.Entry(add_frame, borderwidth=2.5, font=("Helvetica", 16))
Event_entry.grid(row=3, column=1, sticky="ew")

payment_validation = root.register(validate_payment)

payment_entry = tk.Entry(add_frame, borderwidth=2.5, validate="key",textvariable=enttry_var, validatecommand=(payment_validation, "%P"),font=("Helvetica", 16))
payment_entry.grid(row=5, column=1, sticky="ew")

payment_type_entry = tk.Entry(add_frame, borderwidth=2.5, font=("Helvetica", 16))
payment_type_entry.grid(row=6, column=1, sticky="ew")

dattetime_entry = tk.Entry(add_frame, borderwidth=2.5, font=("Helvetica", 16))
dattetime_entry.grid(row=7, column=1, sticky="ew")

auto_dt=tk.Button(add_frame,text=" FILL ",bg="green",fg="white",command=fill_dattetime_entry, font=("Arial",15))
auto_dt.grid(row=7,column=2)

add_btn=tk.Button(side_bar,text=" ADD ",bg="gray",fg="white",command=add_fun, font=("Arial",15))
add_btn.grid(row=0,column=1)

def empty_database():
    conn = sqlite3.connect("guests.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guests")
    conn.commit()
    conn.close()
    home_listbox.delete(0, tk.END)
    update_statistics()

del_btn=tk.Button(side_bar,text="EMPTY GUEST LIST",bg="red",fg="white",command=empty_database, font=("Arial",15))
del_btn.grid(row=0,column=0)

search_btn=tk.Button(side_bar,text=" SEARCH ",bg="gray",fg="white",command=search_widgets, font=("Arial",15))
search_btn.grid(row=0,column=3,sticky="nsew")

filter_btn=tk.Button(side_bar,text="   FILTER   ",bg="gray",fg="white", font=("Arial",15), command=filter_it)
filter_btn.grid(row=0,column=5,sticky="w")

selected_item = None 
def show_btn(event=None): 
    global selected_item
    selected_indices = home_listbox.curselection()
    if len(selected_indices) == 1:
        global show_qrbtn
        global selected_item
        selected_item = home_listbox.get(selected_indices[0])
        show_qrbtn=tk.Button(side_bar, text=" Show QR ", bg="green", fg="white", command= gen_qr, font=("Arial", 15))
        show_qrbtn.grid(row=1, column=0, sticky="e")
        send_qrbtn.grid()

        def del_one():  
            try:
                conn = sqlite3.connect("guests.db")
                cursor = conn.cursor()
                cursor.execute(f"DELETE {selected_indices} FROM guests")
                conn.commit()
                conn.close()

                home_listbox.delete(selected_indices)
            except sqlite3.Error as e:
                print("SQLite error:", e)
        
        del_one_btn=tk.Button(side_bar, text=" Delete Guest ", bg="red", fg="white", command= del_one, font=("Arial", 15))
        del_one_btn.grid(row=1, column=1)

    else:
        print("No item selected")
    update_statistics()

def info_prompt():
    global email_
    global password_
    if not os.path.exists('config.txt'):
        prompt_info= tk.Toplevel(root)
        prompt_info.title("Communication Method")
        prompt_info.configure(bg="gray")
        email_label = tk.Label(prompt_info, text="Your Email:",bg="teal", fg="white", font=("castellar", 16))
        email_label.grid(row=0, column=0)
        email_entry = tk.Entry(prompt_info,borderwidth=2.5, font=("Helvetica", 16))
        email_entry.grid(row=0, column=1)
        password_label = tk.Label(prompt_info, text="Email Password:",bg="teal", fg="white", font=("castellar", 16))
        password_label.grid(row=1, column=0)
        password_entry = tk.Entry(prompt_info, show="*",borderwidth=2.5, font=("Helvetica", 16))
        password_entry.grid(row=1, column=1)
        email_ = email_entry.get()
        password_ = password_entry.get()
        def save_config():
            global email_
            global password_
            with open('config.txt', 'w') as config_file:
                config_file.write(f"Email: {email_}\n")
                config_file.write(f"Password: {password_}\n")
                prompt_info.destroy()
        save_button = tk.Button(prompt_info, text=" Save ", command=save_config,bg="teal", fg="white", font=("Arial", 16))
        save_button.grid(row=2, column=1)
    else:
        pass

        
info_prompt()
    
tmp_file = None

def getcred():
    global email_
    global password_
    if not os.path.exists('config.txt'):
        info_prompt()
        return "", ""
    else:
        with open('config.txt', 'r') as config_file:
            cont = config_file.read()
            em_i = cont.find("Email: ")
            pa_i = cont.find("Password: ")
            if em_i != -1:
                em_v = cont[em_i + 7:].split('\n')[0]
                pa_v = cont[pa_i + 9:].split('\n')[0].strip()
                bp = pa_v
                ae = em_v
            else:
                info_prompt()
                return "", ""
    email_ = ae
    password_ = bp
    return email_, password_

email_,password_=getcred()

def remove_it():
    qr_wndw.destroy()
    show_qrbtn.destroy()
    
  
def redo_it():
        global qr_wndw
        global okqr_btn
        qr_wndw=tk.Toplevel(root)
        qr_wndw.title("QR CODE")
        okqr_btn=tk.Button(qr_wndw,text=" Done ", bg="gray", fg="white", command=remove_it, font=("Arial", 15)) 
        okqr_btn.pack()
        show_qrbtn.configure(state="disabled") 
        

def gen_qr():
    redo_it()
    global tmp_file
    global qr_code_photo  
    if selected_item:

        global qr_code_canvas
        g_info = selected_item
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(g_info)
        qr.make(fit=True)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        qr.make_image(fill_color="black", back_color="white").save(tmp_file.name, "PNG")
        qr_code_photo = tk.PhotoImage(file=tmp_file.name)
        qr_code_canvas = tk.Canvas(qr_wndw, width=qr_code_photo.width(), height=qr_code_photo.height())
        qr_code_canvas.create_image(0, 0, anchor=tk.NW, image=qr_code_photo)
        qr_code_canvas.pack()
        


if '@gmail.com' in email_:
    email_server = 'smtp.gmail.com'
    email_port = 587
    
elif '@yahoo.com' in email_:
    email_server = 'smtp.mail.yahoo.com'
    email_port = 587
    
elif '@outlook.com' in email_ or '@hotmail.com' in email_:
    email_server = 'smtp.office365.com'
    email_port = 587
    
elif '@aol.com' in email_:
    email_server = 'smtp.aol.com'
    email_port = 587
    
elif '@icloud.com' in email_:
    email_server = 'smtp.mail.me.com'
    email_port = 587
     
else:
    email_server = 'smtp.default_server.com'
    email_port = 587

email_server = email_server
email_port = email_port
email_username = email_
email_password = password_

def send_email():
    global guest_email
    if selected_item:
        guest_info = selected_item.split(" ||, ")
        if len(guest_info) >= 3:
            guest_email = guest_info[2]
            email_subject = 'Your Invitation'
            email_message = 'Use the following QR code as Invitation: '
            qr_code_path = tmp_file  
            
    server = smtplib.SMTP(email_server, email_port)
    server.starttls()
    server.login(email_username, email_password)

    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = guest_email
    msg['Subject'] = email_subject
    msg.attach(MIMEText(message, 'plain'))
    with open(qr_code_path, 'rb') as qr_file:
        qr_image = MIMEImage(qr_file.read(), name='qr_code.png')
        msg.attach(qr_image)
    server.sendmail(email_username, guest_email, msg.as_string())
    server.quit()
    
send_qrbtn=tk.Button(home, text=" Send QR ", bg="green", fg="white", command= send_email, font=("Arial", 15))
send_qrbtn.grid(row=1, column=2, sticky="w")
send_qrbtn.grid_forget()

def scanQR():
    def scan():
        global g_data
        cv2.namedWindow("QR Code Scanner", cv2.WINDOW_NORMAL)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        present_conn = sqlite3.connect("present_guests.db")
        present_cursor = present_conn.cursor()
        present_cursor.execute('''CREATE TABLE IF NOT EXISTS present_guests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        event_name TEXT,
                        email TEXT,
                        payment TEXT,
                        payment_type TEXT,
                        dattetime TEXT,
                        male_or_female TEXT
                    )''')
        present_conn.commit()
        while True:
            ret, frame = cap.read()
            D_obj = decode(frame)
            for obj in D_obj:
                g_data = obj.data.decode('utf-8')
                cv2.imshow("QR Code Scanner", frame)
                found = False
                for item in home_listbox.get(0, tk.END):
                    if g_data == item:
                        found = True
                        break
                if found:
                    guest_info = item.split(" ||, ")
                    if len(guest_info) >= 7:
                        name, event_name, email, payment, payment_type, dattetime, male_or_female = guest_info
                        inv_lbl = tk.Label(root, text="This Is Our Guest", bg="white", fg="green",
                                           font=("Helvetica", 16))
                        inv_lbl.grid(row=3, column=0, sticky='nsew')
                        inv_lbl.after(4000, inv_lbl.destroy)
                        i_to_m = home_listbox.get(0, tk.END).index(g_data)
                        home_listbox.selection_set(i_to_m)
                        present_cursor.execute('''
                            INSERT INTO present_guests (name, event_name, email, payment, payment_type, dattetime, male_or_female)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (name, event_name, email, payment, payment_type, dattetime, male_or_female))
                        present_conn.commit()
                        pre_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                                                  f"||, {payment} ||, {payment_type} "
                                                  f"||, {dattetime} ||, {male_or_female}")
                        pre_listbox.delete(0, "end")
                        try:
                            with sqlite3.connect("present_guests.db") as conn:
                                cursor = conn.cursor()
                                cursor.execute('SELECT name, event_name, email, payment, payment_type, dattetime, male_or_female FROM present_guests')
                                guest_data = cursor.fetchall()
                                for guest_info in guest_data:
                                    name, event_name, email, payment, payment_type, dattetime, male_or_female = guest_info
                                    pre_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                                                f"||, {payment} ||, {payment_type} "
                                                f"||, {dattetime} ||, {male_or_female}")
                                    break
                                if os.path.exists("present_guests.db") and guest_info in "present_guests.db":
                                    break
                                
                        except sqlite3.Error as e:
                            print("SQLite error:", e)
                elif not cap.isOpened():
                    print("Error: Could not open camera.")
                    return
                elif not found:
                    ninv_lbl = tk.Label(root, text="Not In Our List", bg="white", fg="red",
                                        font=("Helvetica", 16))
                    ninv_lbl.grid(row=3, column=0, sticky='nsew')
                    ninv_lbl.after(4000, ninv_lbl.destroy)
                else:
                    einv_lbl = tk.Label(root, text="ERROR!!! TRY AGAIN", bg="red", fg="white",
                                        font=("Helvetica", 16))
                    einv_lbl.grid(row=3, column=0, sticky='nsew')
                    einv_lbl.after(4000, ninv_lbl.destroy)

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    update_statistics()
        
    scanning_thread = threading.Thread(target=scan)
    scanning_thread.start()

pre_listbox.delete(0, "end")
try:
    with sqlite3.connect("present_guests.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, event_name, email, payment, payment_type, dattetime, male_or_female FROM present_guests')
        guest_data = cursor.fetchall()
        for guest_info in guest_data:
            name, event_name, email, payment, payment_type, dattetime, male_or_female = guest_info
            pre_listbox.insert("end", f"{name} ||, {event_name} ||, {email} "
                            f"||, {payment} ||, {payment_type} "
                            f"||, {dattetime} ||, {male_or_female}")
            
except sqlite3.Error as e:
    print("SQLite error:", e)
    
def empty_present_guests_db():
    try:
        conn = sqlite3.connect("present_guests.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM present_guests")
        conn.commit()
        conn.close()

        pre_listbox.delete(0, tk.END)
    except sqlite3.Error as e:
        print("SQLite error:", e)

empty_db_btn = tk.Button(side_bar, text="Empty P.Guests List", bg="red", fg="white", command=empty_present_guests_db, font=("Arial", 15))
empty_db_btn.grid(row=0, column=6)

scan_qrbtn=tk.Button(side_bar, text=" Scan QR ", bg="gray", fg="white", command= scanQR, font=("Arial", 15))
scan_qrbtn.grid(row=2, column=3, sticky="w")
        
Email_entry.bind("<FocusOut>", validate_email)

home_listbox.bind("<ButtonRelease-1>", show_btn)

root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(1, weight=3)
root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))
enttry_var.trace("w", lambda *args: check_entry_contents())

root.bind("<Button-1>", hide_widgets)
root.mainloop()