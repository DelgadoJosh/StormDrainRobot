try:
  # Python 3.x
  import tkinter as tk 
  from tkinter import ttk 
except importError: 
  import Tkinter as tk 
  import ttk 

from tkcalendar import Calendar, DateEntry 

def example1():
  def print_sel():
    print(cal.selection_get()) 
  
  top = tk.Toplevel(root)

  cal = Calendar(top,
                  font = "Arial 14", selectmode="day",
                  cursor="hand1", year=2018, month=2, day=5)
  cal.pack(fill="both", expand=True)
  ttk.Button(top, text="ok", command=print_sel).pack() 

def example2():
  top = tk.Toplevel(root)

  cal = Calendar(top, selectmode="none")
  date = cal.datetime.today() + cal.timedelta(days=2)
  cal.calevent_create(date, "Hello world!", "message")
  cal.calevent_create(date, "Reminder 2", "reminder")
  cal.calevent_create(date + cal.timedelta(days=-2), "Reminder 1", "reminder")
  cal.calevent_create(date + cal.timedelta(days=3), "Message", "Message")

  cal.tag_config("reminder", background="red", foreground="yellow")

  cal.pack(fill="both", expand=True)
  ttk.Label(top, text="Hover over the events.").pack()



def example3():
  def print_sel():
    print(cal.get())
  top = tk.Toplevel(root) 

  ttk.Label(top, text="Choose date").pack(padx=10, pady=10)

  cal = DateEntry(top, width=12, background="darkblue",
                  foreground="white", borderwidth=2, firstweekday="sunday")
  cal.pack(padx=10, pady=10)

  ttk.Button(top, text="ok", command=print_sel).pack()


root = tk.Tk()
s = ttk.Style(root)
s.theme_use("clam")

ttk.Button(root, text="Calendar", command=example1).pack(padx=10, pady=10)
ttk.Button(root, text="Calendar with events", command=example2).pack(padx=10, pady=10)
ttk.Button(root, text="DateEntry", command=example3).pack(padx=10, pady=10)

root.mainloop()
