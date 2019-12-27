from tkinter import *
import pandas as pd
from datetime import datetime
import smtplib

entry = pd.read_csv("Entry.csv")
df = pd.DataFrame(entry)
e = 0
entry_status = False
time = 0
def check_entry():
    global entry_status
    global e
    guest_id = e.get()
    guest_id = int(guest_id)
    print(guest_id)
    for id in df['id']:
        if id == guest_id:
            entry_status = True
            break
        else:
            entry_status = False
    print(entry_status)
    if entry_status == False :
        checkin()
    else:
        checkout()

def checkin():
    global e  
    def store_details():
        def send_mail():
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('your_email', 'your_password')
            subject = "Checkin"
            body = f"{name} checked in, phone no- {phone} and email - {email} at {time}"
            msg = f"Subject: {subject}\n\n{body}"
            server.sendmail(
            'from',
            'to',
            msg
            )
            print("Email has been sent")

            server.quit()

        global df,time
        user_id = e.get()
        user_id = int(user_id)
        name = e_2.get()
        name = str(name)
        email = e_4.get()
        email = str(email)
        phone = e_3.get()
        phone = str(phone)
        time = datetime.now()
        time = str(time)
        checkin = True
        checkin = str(checkin)
        print(name, email, phone, time)
        new_row = {'id': user_id, 'Name': name, 'email': email, 'phone': phone, 'time': time, 'checkin': checkin}
        print(new_row)
        send_mail()
        df = df.append(new_row, ignore_index = True)
        print(df)
        df.set_index('id', inplace = True)
        df.to_csv('Entry.csv')
        root.destroy()

    top = Toplevel()
    label_2 = Label(top, text = "Enter your name")
    label_2.pack()
    e_2 = Entry(top)
    e_2.focus()
    e_2.pack()
    label_3 = Label(top, text = "Enter your phone no")
    label_3.pack()
    e_3 = Entry(top)
    e_3.pack()
    label_4 = Label(top, text = "Enter your email")
    label_4.pack()
    e_4 = Entry(top)
    e_4.pack()
    button_2 = Button(top, text = "Checkin", command = store_details)
    button_2.pack()

def checkout():
    def delete_details():
        def send_checkout_mail():
            global time
            checkout_time = datetime.now()
            checkout_time = str(checkout_time)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('your_email', 'your_password')
            subject = "Check out"
            body = f"You visited 221B Bakers Street at {time} and checked out at {checkout_time}"
            msg = f"Subject: {subject}\n\n{body}"
            server.sendmail(
            'from',
            email,
            msg
            )
            print("Email has been sent")
            server.quit()

        global e, df, time
        guest_id = e.get()
        guest_id = int(guest_id)
        email = df['email'][df['id'] == guest_id].astype(str)
        i = df.index[df['id'] == guest_id]
        email = email[i[0]]
        print(email)
        print(i[0])
        df = df[df['id'] != guest_id]
        print(df)
        df.set_index('id', inplace = True)
        df.to_csv('Entry.csv')
        root.destroy()
        send_checkout_mail()

    down = Toplevel()
    button_3 = Button(down, text = "Check out", command = delete_details)
    button_3.pack()

root = Tk()
label = Label(root, text = "Enter your id")
label.pack()
e = Entry(root)
e.focus()
e.pack()
button_1 = Button(root, text = "Click", command = check_entry) 
button_1.pack()
root.mainloop()