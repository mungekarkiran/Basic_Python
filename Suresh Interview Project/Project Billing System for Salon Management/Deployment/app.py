import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pywhatkit

# Database setup
conn = sqlite3.connect("billing_system.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    position TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    product_id INTEGER,
    description TEXT,
    FOREIGN KEY(employee_id) REFERENCES employees(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

conn.commit()

# GUI setup
class BillingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Billing System")
        self.geometry("900x600")

        # Tabs
        self.tab_control = ttk.Notebook(self)
        self.add_product_tab = ttk.Frame(self.tab_control)
        self.add_employee_tab = ttk.Frame(self.tab_control)
        self.billing_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_product_tab, text="Manage Products")
        self.tab_control.add(self.add_employee_tab, text="Manage Employees")
        self.tab_control.add(self.billing_tab, text="Billing")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_product_tab()
        self.setup_employee_tab()
        self.setup_billing_tab()

    # Manage Products Tab
    def setup_product_tab(self):
        tk.Label(self.add_product_tab, text="Product Name").grid(row=0, column=0, padx=10, pady=10)
        self.product_name_var = tk.StringVar()
        tk.Entry(self.add_product_tab, textvariable=self.product_name_var).grid(row=0, column=1)

        tk.Label(self.add_product_tab, text="Price").grid(row=1, column=0, padx=10, pady=10)
        self.product_price_var = tk.DoubleVar()
        tk.Entry(self.add_product_tab, textvariable=self.product_price_var).grid(row=1, column=1)

        tk.Button(self.add_product_tab, text="Add Product", command=self.add_product).grid(row=2, column=0, columnspan=2, pady=10)

        self.product_tree = ttk.Treeview(self.add_product_tab, columns=("ID", "Name", "Price"), show="headings")
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.grid(row=3, column=0, columnspan=2, pady=10)
        self.load_products()

    def add_product(self):
        name = self.product_name_var.get()
        price = self.product_price_var.get()
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        self.load_products()

    def load_products(self):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            self.product_tree.insert("", "end", values=row)

    # Manage Employees Tab
    def setup_employee_tab(self):
        tk.Label(self.add_employee_tab, text="Employee Name").grid(row=0, column=0, padx=10, pady=10)
        self.employee_name_var = tk.StringVar()
        tk.Entry(self.add_employee_tab, textvariable=self.employee_name_var).grid(row=0, column=1)

        tk.Label(self.add_employee_tab, text="Position").grid(row=1, column=0, padx=10, pady=10)
        self.employee_position_var = tk.StringVar()
        tk.Entry(self.add_employee_tab, textvariable=self.employee_position_var).grid(row=1, column=1)

        tk.Button(self.add_employee_tab, text="Add Employee", command=self.add_employee).grid(row=2, column=0, columnspan=2, pady=10)

        self.employee_tree = ttk.Treeview(self.add_employee_tab, columns=("ID", "Name", "Position"), show="headings")
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Name", text="Name")
        self.employee_tree.heading("Position", text="Position")
        self.employee_tree.grid(row=3, column=0, columnspan=2, pady=10)
        self.load_employees()

    def add_employee(self):
        name = self.employee_name_var.get()
        position = self.employee_position_var.get()
        cursor.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully!")
        self.load_employees()

    def load_employees(self):
        for row in self.employee_tree.get_children():
            self.employee_tree.delete(row)
        cursor.execute("SELECT * FROM employees")
        for row in cursor.fetchall():
            self.employee_tree.insert("", "end", values=row)

    # Billing Tab
    def setup_billing_tab(self):
        tk.Label(self.billing_tab, text="Client Email").grid(row=0, column=0, padx=10, pady=10)
        self.client_email_var = tk.StringVar()
        tk.Entry(self.billing_tab, textvariable=self.client_email_var).grid(row=0, column=1)

        tk.Label(self.billing_tab, text="Client WhatsApp").grid(row=1, column=0, padx=10, pady=10)
        self.client_whatsapp_var = tk.StringVar()
        tk.Entry(self.billing_tab, textvariable=self.client_whatsapp_var).grid(row=1, column=1)

        tk.Button(self.billing_tab, text="Generate Bill", command=self.generate_bill).grid(row=2, column=0, columnspan=2, pady=10)

    def generate_bill(self):
        # Simulate bill generation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Billing System", ln=True, align="C")
        pdf.cell(200, 10, txt="Invoice Details", ln=True, align="C")
        file_name = "invoice.pdf"
        pdf.output(file_name)

        # Send email
        email = self.client_email_var.get()
        if email:
            self.send_email(email, file_name)

        # Send WhatsApp
        whatsapp = self.client_whatsapp_var.get()
        if whatsapp:
            self.send_whatsapp(whatsapp, "Your invoice has been generated.")

    def send_email(self, email, file_name):
        try:
            sender_email = "your_email@example.com"
            sender_password = "your_password"

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = "Invoice"
            body = "Please find attached your invoice."
            msg.attach(MIMEText(body, "plain"))

            with open(file_name, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={file_name}")
                msg.attach(part)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
            messagebox.showinfo("Success", "Invoice sent via email!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

    def send_whatsapp(self, number, message):
        try:
            pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
            messagebox.showinfo("Success", "Invoice sent via WhatsApp!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send WhatsApp message: {e}")


if __name__ == "__main__":
    app = BillingSystem()
    app.mainloop()
