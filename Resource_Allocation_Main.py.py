import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry, Calendar
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",  
            database="CollegeResourceSystem"
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

current_user = None
db = create_connection()
cursor = db.cursor() if db else None

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()

    if cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            current_user = user
            login_window.destroy()
            if user[3] == "Faculty":
                open_faculty_dashboard()
            elif user[3] == "Admin":
                open_admin_dashboard()
            else:
                open_hod_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Database connection not established.")

# Configure common styles
def configure_styles():
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure common styles
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabelframe", background="#f0f0f0")
    style.configure("TLabelframe.Label", font=("Arial", 12, "bold"), background="#f0f0f0")
    
    # Button styles
    style.configure("TButton", font=("Arial", 12), background="#4b8a9c", foreground="white", padding=5)
    style.map("TButton", background=[("active", "#3a6d7a")])
    
    # Create a special style for the primary action buttons
    style.configure("Primary.TButton", font=("Arial", 12, "bold"), background="#4b8a9c", foreground="white", padding=5)
    style.map("Primary.TButton", background=[("active", "#3a6d7a")])
    
    # Create a special style for danger buttons (reject)
    style.configure("Danger.TButton", font=("Arial", 12), background="#d9534f", foreground="white", padding=5)
    style.map("Danger.TButton", background=[("active", "#c9302c")])
    
    # Create a special style for success buttons (approve)
    style.configure("Success.TButton", font=("Arial", 12), background="#5cb85c", foreground="white", padding=5)
    style.map("Success.TButton", background=[("active", "#4cae4c")])
    
    # Header style
    style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#4b8a9c", foreground="white", padding=10)
    
    # Treeview styling
    style.configure("Treeview", 
                   font=("Arial", 11),
                   rowheight=25,
                   background="#ffffff",
                   fieldbackground="#ffffff")
    style.configure("Treeview.Heading", 
                   font=("Arial", 12, "bold"),
                   background="#4b8a9c",
                   foreground="white")
    style.map("Treeview", background=[("selected", "#d1e0e5")])

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the frame background
        self.configure(style="TFrame")

        # Create the canvas for scrolling
        self.canvas = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")

        # Allow dynamic resizing of scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window inside the canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack canvas to fill frame
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind mouse wheel events for scrolling
        self.bind_mousewheel(self.canvas)

    def bind_mousewheel(self, widget):
        # Windows & MacOS
        widget.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Linux (Scroll up/down)
        widget.bind_all("<Button-4>", self._on_mousewheel)
        widget.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.canvas.yview_scroll(1, "units")

# Faculty Dashboard
def open_faculty_dashboard():
    faculty_window = tk.Tk()
    faculty_window.title("Faculty Dashboard - SK Somaiya College")
    center_window(faculty_window, 900, 700)
    faculty_window.configure(bg="#f0f0f0")
    
    # Configure styles
    configure_styles()

    # Create a scrollable frame
    scrollable_frame = ScrollableFrame(faculty_window)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Header Frame
    header_frame = ttk.Frame(scrollable_frame.scrollable_frame, style="TFrame")
    header_frame.pack(pady=10, fill="x")
    
    header_label = ttk.Label(header_frame, text="Faculty Dashboard", style="Header.TLabel")
    header_label.pack(fill="x")

    # Logout Button at the top right
    logout_button = ttk.Button(header_frame, text="Logout", command=lambda: logout(faculty_window))
    logout_button.place(relx=0.95, rely=0.5, anchor="e")

    # User Info Frame
    user_info_frame = ttk.LabelFrame(scrollable_frame.scrollable_frame, text="Faculty Information", padding=15)
    user_info_frame.pack(pady=10, fill="x")
    
    info_grid = ttk.Frame(user_info_frame)
    info_grid.pack(fill="x", expand=True)
    
    ttk.Label(info_grid, text="Faculty ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[0]}").grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(info_grid, text="Name:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[4]}").grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(info_grid, text="Department:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[5]}").grid(row=2, column=1, sticky="w", padx=5, pady=5)

    # Request Resource Frame
    request_frame = ttk.LabelFrame(scrollable_frame.scrollable_frame, text="Request Classroom/Resource", padding=15)
    request_frame.pack(pady=10, fill="x")

    request_form = ttk.Frame(request_frame)
    request_form.pack(fill="x", expand=True)

    # Resource Type
    ttk.Label(request_form, text="Resource Type:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=8, sticky="w")
    resource_type_var = tk.StringVar(value="Classroom")
    resource_types = ["Classroom", "Laboratory", "Auditorium", "Projector", "Other"]
    resource_type_combo = ttk.Combobox(request_form, textvariable=resource_type_var, values=resource_types, state="readonly", width=25)
    resource_type_combo.grid(row=0, column=1, padx=5, pady=8, sticky="w")

    # Date
    ttk.Label(request_form, text="Date:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=8, sticky="w")
    date_entry = DateEntry(request_form, date_pattern="yyyy-mm-dd", background="#4b8a9c", foreground="white", width=20)
    date_entry.grid(row=1, column=1, padx=5, pady=8, sticky="w")

    # Time Slot
    ttk.Label(request_form, text="Time Slot:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=8, sticky="w")
    time_slot_var = tk.StringVar(value="09:00-11:00")
    time_slots = ["08:00-09:00", "09:00-11:00", "11:00-13:00", "14:00-16:00", "16:00-18:00"]
    time_slot_combo = ttk.Combobox(request_form, textvariable=time_slot_var, values=time_slots, state="readonly", width=25)
    time_slot_combo.grid(row=2, column=1, padx=5, pady=8, sticky="w")

    # Purpose
    ttk.Label(request_form, text="Purpose:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=8, sticky="nw")
    purpose_text = tk.Text(request_form, height=4, width=30, font=("Arial", 11), wrap="word")
    purpose_text.grid(row=3, column=1, padx=5, pady=8, sticky="w")

    # Add keyboard-based scrolling to the text widget
    purpose_text.bind("<Key>", lambda e: scrollable_frame.scrollable_frame.update_idletasks())

    request_button = ttk.Button(
        request_form, 
        text="Submit Resource Request", 
        command=lambda: request_resource(
            resource_type_var.get(), 
            date_entry.get(), 
            time_slot_var.get(), 
            purpose_text.get("1.0", "end-1c")
        ),
        style="Primary.TButton"
    )
    request_button.grid(row=4, column=0, columnspan=2, pady=15)

    # View Requests Status Frame
    status_frame = ttk.LabelFrame(scrollable_frame.scrollable_frame, text="My Resource Requests", padding=15)
    status_frame.pack(pady=10, fill="both", expand=True)

    # Create Treeview
    columns = ("Resource Type", "Date", "Time Slot", "Purpose", "Status", "Approved Resource")
    tree = ttk.Treeview(status_frame, columns=columns, show="headings", selectmode="browse")
    
    # Define column headings and widths
    tree.heading("Resource Type", text="Resource Type")
    tree.heading("Date", text="Date")
    tree.heading("Time Slot", text="Time Slot")
    tree.heading("Purpose", text="Purpose")
    tree.heading("Status", text="Status")
    tree.heading("Approved Resource", text="Approved Resource")
    
    # Set column widths
    tree.column("Resource Type", width=120, minwidth=100)
    tree.column("Date", width=100, minwidth=100)
    tree.column("Time Slot", width=100, minwidth=100)
    tree.column("Purpose", width=200, minwidth=150)
    tree.column("Status", width=100, minwidth=80)
    tree.column("Approved Resource", width=150, minwidth=120)
    
    # Make the tree scrollable
    tree.configure(height=8)
    tree.pack(fill="both", expand=True, pady=5)
    
    # Bind the tree to the mousewheel events for the scrollable frame
    scrollable_frame.bind_mousewheel(tree)
    
    # Refresh button
    refresh_button = ttk.Button(
        status_frame, 
        text="Refresh", 
        command=lambda: view_resource_requests(tree)
    )
    refresh_button.pack(pady=10, anchor="e")
    
    # Configure tags for color-coding status
    tree.tag_configure("pending", background="#FFF9C4")  # Light yellow for pending
    tree.tag_configure("approved", background="#E8F5E9")  # Light green for approved
    tree.tag_configure("rejected", background="#FFEBEE")  # Light red for rejected
    
    # Load resource requests data
    view_resource_requests(tree)

    # View Available Resources Button
    view_resources_button = ttk.Button(
        scrollable_frame.scrollable_frame,
        text="View Available Resources",
        command=view_available_resources,
        style="Primary.TButton"
    )
    view_resources_button.pack(pady=10)

    # Bind key events for keyboard navigation
    faculty_window.bind("<Up>", lambda e: scrollable_frame.canvas.yview_scroll(-1, "units"))
    faculty_window.bind("<Down>", lambda e: scrollable_frame.canvas.yview_scroll(1, "units"))
    faculty_window.bind("<Prior>", lambda e: scrollable_frame.canvas.yview_scroll(-5, "units"))  # Page Up
    faculty_window.bind("<Next>", lambda e: scrollable_frame.canvas.yview_scroll(5, "units"))    # Page Down

    faculty_window.mainloop()

# HOD Dashboard
def open_hod_dashboard():
    hod_window = tk.Tk()
    hod_window.title("HOD Dashboard - SK Somaiya College")
    center_window(hod_window, 1200, 700)
    hod_window.configure(bg="#f0f0f0")
    
    # Configure styles
    configure_styles()

    # Create a main frame with padding
    main_frame = ttk.Frame(hod_window, style="TFrame", padding=10)
    main_frame.pack(fill="both", expand=True)

    # Header Frame
    header_frame = ttk.Frame(main_frame, style="TFrame")
    header_frame.pack(fill="x", pady=5)
    
    header_label = ttk.Label(header_frame, text=f"HOD Dashboard - {current_user[5]} Department", style="Header.TLabel")
    header_label.pack(fill="x")

    # Logout Button
    logout_button = ttk.Button(header_frame, text="Logout", command=lambda: logout(hod_window))
    logout_button.place(relx=0.95, rely=0.5, anchor="e")

    # User Info Frame
    user_info_frame = ttk.LabelFrame(main_frame, text="HOD Information", padding=15)
    user_info_frame.pack(fill="x", pady=10)
    
    info_grid = ttk.Frame(user_info_frame)
    info_grid.pack(fill="x", expand=True)
    
    ttk.Label(info_grid, text="HOD ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[0]}").grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(info_grid, text="Name:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[4]}").grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(info_grid, text="Department:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[5]}").grid(row=2, column=1, sticky="w", padx=5, pady=5)

    # Resource Requests Frame
    requests_frame = ttk.LabelFrame(main_frame, text="Resource Requests", padding=15)
    requests_frame.pack(fill="both", expand=True, pady=10)

    # Create a frame for the treeview and scrollbars
    tree_container = ttk.Frame(requests_frame)
    tree_container.pack(fill="both", expand=True, pady=5)
    
    # Define columns
    columns = ("Request ID", "Faculty ID", "Name", "Resource Type", "Date", "Time Slot", "Purpose", "Status")
    tree = ttk.Treeview(tree_container, columns=columns, show="headings", selectmode="browse")
    
    # Configure column headings
    for col in columns:
        tree.heading(col, text=col)
        if col in ["Request ID", "Faculty ID"]:
            tree.column(col, width=80, minwidth=80)
        elif col in ["Name", "Resource Type"]:
            tree.column(col, width=120, minwidth=100)
        elif col in ["Date", "Time Slot"]:
            tree.column(col, width=100, minwidth=90)
        elif col == "Purpose":
            tree.column(col, width=250, minwidth=150)
        else:  # Status
            tree.column(col, width=100, minwidth=80)
    
    # Add vertical and horizontal scrollbars
    y_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
    x_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
    
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Grid layout for tree and scrollbars
    tree.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    tree_container.grid_rowconfigure(0, weight=1)
    tree_container.grid_columnconfigure(0, weight=1)
    
    # Load resource requests data
    view_hod_requests(tree)
    
    # Action buttons container
    action_container = ttk.Frame(requests_frame)
    action_container.pack(fill="x", pady=10)
    
    # Approve button (left)
    approve_button = ttk.Button(
        action_container,
        text="Approve Selected Request",
        style="Success.TButton",
        command=lambda: approve_reject_resource(tree, "Approved")
    )
    approve_button.pack(side="left", padx=5)
    
    # Reject button (left, next to approve)
    reject_button = ttk.Button(
        action_container,
        text="Reject Selected Request",
        style="Danger.TButton",
        command=lambda: approve_reject_resource(tree, "Rejected")
    )
    reject_button.pack(side="left", padx=5)
    
    # Refresh button (right)
    refresh_button = ttk.Button(
        action_container,
        text="Refresh",
        command=lambda: view_hod_requests(tree)
    )
    refresh_button.pack(side="right", padx=5)
    
    # Status label for feedback
    status_label = ttk.Label(requests_frame, text="Select a request to approve or reject", font=("Arial", 10, "italic"))
    status_label.pack(pady=5, anchor="w")
    
    # Add a tag to highlight pending requests
    tree.tag_configure("pending", background="#FFF9C4")  # Light yellow for pending
    tree.tag_configure("approved", background="#E8F5E9")  # Light green for approved
    tree.tag_configure("rejected", background="#FFEBEE")  # Light red for rejected

    # View Department Resources Button
    view_dept_resources_button = ttk.Button(
        main_frame,
        text="View Department Resources",
        command=lambda: view_department_resources(current_user[5]),
        style="Primary.TButton"
    )
    view_dept_resources_button.pack(pady=10)

    hod_window.mainloop()

# Admin Dashboard
def open_admin_dashboard():
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard - SK Somaiya College")
    center_window(admin_window, 1200, 700)
    admin_window.configure(bg="#f0f0f0")
    
    # Configure styles
    configure_styles()

    # Create a main frame with padding
    main_frame = ttk.Frame(admin_window, style="TFrame", padding=10)
    main_frame.pack(fill="both", expand=True)

    # Header Frame
    header_frame = ttk.Frame(main_frame, style="TFrame")
    header_frame.pack(fill="x", pady=5)
    
    header_label = ttk.Label(header_frame, text="Admin Dashboard", style="Header.TLabel")
    header_label.pack(fill="x")

    # Logout Button
    logout_button = ttk.Button(header_frame, text="Logout", command=lambda: logout(admin_window))
    logout_button.place(relx=0.95, rely=0.5, anchor="e")

    # User Info Frame
    user_info_frame = ttk.LabelFrame(main_frame, text="Admin Information", padding=15)
    user_info_frame.pack(fill="x", pady=10)
    
    info_grid = ttk.Frame(user_info_frame)
    info_grid.pack(fill="x", expand=True)
    
    ttk.Label(info_grid, text="Admin ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[0]}").grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(info_grid, text="Name:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(info_grid, text=f"{current_user[4]}").grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # Create Notebook for tabs
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True, pady=10)

    # Tab 1: Resource Management
    resource_tab = ttk.Frame(notebook)
    notebook.add(resource_tab, text="Resource Management")

    # Resource Management Frame
    resource_frame = ttk.LabelFrame(resource_tab, text="College Resources", padding=15)
    resource_frame.pack(fill="both", expand=True, pady=10)

    # Create Treeview for resources
    resource_columns = ("Resource ID", "Resource Name", "Resource Type", "Capacity", "Department", "Status")
    resource_tree = ttk.Treeview(resource_frame, columns=resource_columns, show="headings", selectmode="browse")
    
    # Configure column headings
    for col in resource_columns:
        resource_tree.heading(col, text=col)
        if col in ["Resource ID"]:
            resource_tree.column(col, width=80, minwidth=80)
        elif col in ["Resource Type", "Department"]:
            resource_tree.column(col, width=120, minwidth=100)
        elif col in ["Resource Name"]:
            resource_tree.column(col, width=200, minwidth=150)
        elif col in ["Capacity"]:
            resource_tree.column(col, width=80, minwidth=60)
        else:  # Status
            resource_tree.column(col, width=100, minwidth=80)
    
    # Add scrollbars
    y_scrollbar = ttk.Scrollbar(resource_frame, orient="vertical", command=resource_tree.yview)
    x_scrollbar = ttk.Scrollbar(resource_frame, orient="horizontal", command=resource_tree.xview)
    
    resource_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Grid layout
    resource_tree.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    resource_frame.grid_rowconfigure(0, weight=1)
    resource_frame.grid_columnconfigure(0, weight=1)
    
    # Load resources data
    view_all_resources(resource_tree)
    
    # Action buttons container
    resource_action_container = ttk.Frame(resource_frame)
    resource_action_container.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
    
    # Add Resource button
    add_resource_button = ttk.Button(
        resource_action_container,
        text="Add New Resource",
        style="Success.TButton",
        command=add_new_resource
    )
    add_resource_button.pack(side="left", padx=5)
    
    # Edit Resource button
    edit_resource_button = ttk.Button(
        resource_action_container,
        text="Edit Selected Resource",
        command=lambda: edit_resource(resource_tree)
    )
    edit_resource_button.pack(side="left", padx=5)
    
    # Delete Resource button
    delete_resource_button = ttk.Button(
        resource_action_container,
        text="Delete Selected Resource",
        style="Danger.TButton",
        command=lambda: delete_resource(resource_tree)
    )
    delete_resource_button.pack(side="left", padx=5)
    
    # Refresh button
    refresh_button = ttk.Button(
        resource_action_container,
        text="Refresh",
        command=lambda: view_all_resources(resource_tree)
    )
    refresh_button.pack(side="right", padx=5)

    # Tab 2: User Management
    user_tab = ttk.Frame(notebook)
    notebook.add(user_tab, text="User Management")

    # User Management Frame
    user_frame = ttk.LabelFrame(user_tab, text="College Users", padding=15)
    user_frame.pack(fill="both", expand=True, pady=10)

    # Create Treeview for users
    user_columns = ("User ID", "Username", "Name", "Role", "Department", "Email")
    user_tree = ttk.Treeview(user_frame, columns=user_columns, show="headings", selectmode="browse")
    
    # Configure column headings
    for col in user_columns:
        user_tree.heading(col, text=col)
        if col in ["User ID"]:
            user_tree.column(col, width=80, minwidth=80)
        elif col in ["Role", "Department"]:
            user_tree.column(col, width=120, minwidth=100)
        elif col in ["Username", "Name", "Email"]:
            user_tree.column(col, width=150, minwidth=120)
    
    # Add scrollbars
    y_scrollbar = ttk.Scrollbar(user_frame, orient="vertical", command=user_tree.yview)
    x_scrollbar = ttk.Scrollbar(user_frame, orient="horizontal", command=user_tree.xview)
    
    user_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Grid layout
    user_tree.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    user_frame.grid_rowconfigure(0, weight=1)
    user_frame.grid_columnconfigure(0, weight=1)
    
    # Load users data
    view_all_users(user_tree)
    
    # Action buttons container
    user_action_container = ttk.Frame(user_frame)
    user_action_container.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
    
    # Add User button
    add_user_button = ttk.Button(
        user_action_container,
        text="Add New User",
        style="Success.TButton",
        command=add_new_user
    )
    add_user_button.pack(side="left", padx=5)
    
    # Edit User button
    edit_user_button = ttk.Button(
        user_action_container,
        text="Edit Selected User",
        command=lambda: edit_user(user_tree)
    )
    edit_user_button.pack(side="left", padx=5)
    
    # Delete User button
    delete_user_button = ttk.Button(
        user_action_container,
        text="Delete Selected User",
        style="Danger.TButton",
        command=lambda: delete_user(user_tree)
    )
    delete_user_button.pack(side="left", padx=5)
    
    # Refresh button
    refresh_button = ttk.Button(
        user_action_container,
        text="Refresh",
        command=lambda: view_all_users(user_tree)
    )
    refresh_button.pack(side="right", padx=5)

    # Tab 3: Reports
    reports_tab = ttk.Frame(notebook)
    notebook.add(reports_tab, text="Reports")

    # Reports Frame
    reports_frame = ttk.LabelFrame(reports_tab, text="Generate Reports", padding=15)
    reports_frame.pack(fill="both", expand=True, pady=10)

    # Report options
    report_options = ttk.Frame(reports_frame)
    report_options.pack(fill="x", pady=10)

    ttk.Label(report_options, text="Report Type:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    report_type_var = tk.StringVar(value="Resource Utilization")
    report_types = ["Resource Utilization", "Department-wise Allocation", "Faculty-wise Requests"]
    report_type_combo = ttk.Combobox(report_options, textvariable=report_type_var, values=report_types, state="readonly", width=25)
    report_type_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(report_options, text="Date Range:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    date_range_frame = ttk.Frame(report_options)
    date_range_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(date_range_frame, text="From:").grid(row=0, column=0, padx=2)
    from_date_entry = DateEntry(date_range_frame, date_pattern="yyyy-mm-dd", width=12)
    from_date_entry.grid(row=0, column=1, padx=2)

    ttk.Label(date_range_frame, text="To:").grid(row=0, column=2, padx=2)
    to_date_entry = DateEntry(date_range_frame, date_pattern="yyyy-mm-dd", width=12)
    to_date_entry.grid(row=0, column=3, padx=2)

    # Generate Report button
    generate_button = ttk.Button(
        reports_frame,
        text="Generate Report",
        style="Primary.TButton",
        command=lambda: generate_report(report_type_var.get(), from_date_entry.get(), to_date_entry.get())
    )
    generate_button.pack(pady=15)

    # Report display area
    report_display = tk.Text(reports_frame, height=15, width=100, wrap="word", state="disabled", font=("Arial", 11))
    report_display.pack(fill="both", expand=True, pady=10)

    admin_window.mainloop()

# Request Resource Function
def request_resource(resource_type, date, time_slot, purpose):
    # Validate inputs
    if not resource_type or not date or not time_slot or not purpose.strip():
        messagebox.showerror("Error", "All fields are required")
        return
        
    if cursor:
        try:
            cursor.execute("""
                INSERT INTO resource_requests 
                (user_id, resource_type, date, time_slot, purpose, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (current_user[0], resource_type, date, time_slot, purpose, "Pending"))
            db.commit()
            messagebox.showinfo("Success", "Resource request submitted successfully.")
        except Error as e:
            messagebox.showerror("Database Error", f"Error submitting resource request: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

# View Resource Requests Function (for Faculty)
def view_resource_requests(tree):
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
        
    if cursor:
        try:
            cursor.execute("""
                SELECT resource_type, date, time_slot, purpose, status, approved_resource 
                FROM resource_requests 
                WHERE user_id = %s 
                ORDER BY date DESC, time_slot
            """, (current_user[0],))
            requests = cursor.fetchall()
            
            if not requests:
                # Add a dummy row if no requests found
                tree.insert("", "end", values=("No resource requests found", "", "", "", "", ""))
                return
                
            for request in requests:
                status = request[4]
                if status == "Pending":
                    tree.insert("", "end", values=request, tags=("pending",))
                elif status == "Approved":
                    tree.insert("", "end", values=request, tags=("approved",))
                elif status == "Rejected":
                    tree.insert("", "end", values=request, tags=("rejected",))
                else:
                    tree.insert("", "end", values=request)
                    
            # Configure tag appearance
            tree.tag_configure("pending", background="#FFF9C4")  # Light yellow
            tree.tag_configure("approved", background="#E8F5E9")  # Light green
            tree.tag_configure("rejected", background="#FFEBEE")  # Light red
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving resource requests: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

# View HOD Requests Function
def view_hod_requests(tree):
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
        
    if cursor:
        try:
            cursor.execute("""
                SELECT r.request_id, r.user_id, u.name, r.resource_type, r.date, 
                       r.time_slot, r.purpose, r.status 
                FROM resource_requests r
                JOIN users u ON r.user_id = u.user_id
                WHERE u.department = %s AND r.status = 'Pending'
                ORDER BY r.date, r.time_slot
            """, (current_user[5],))
            requests = cursor.fetchall()
            
            if not requests:
                # Add a dummy row if no requests found
                tree.insert("", "end", values=("", "", "No pending requests in your department", "", "", "", "", ""))
                return
                
            for request in requests:
                status = request[7]  # Status is at index 7
                if status == "Pending":
                    tree.insert("", "end", values=request, tags=("pending",))
                elif status == "Approved":
                    tree.insert("", "end", values=request, tags=("approved",))
                elif status == "Rejected":
                    tree.insert("", "end", values=request, tags=("rejected",))
                else:
                    tree.insert("", "end", values=request)
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving resource requests: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

# Approve/Reject Resource Function
def approve_reject_resource(tree, status):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No resource request selected. Please select a request first.")
        return
        
    request_id = tree.item(selected_item[0])['values'][0]  # Get the request_id from the selected row
    current_status = tree.item(selected_item[0])['values'][7]  # Get the current status
    
    if current_status != "Pending":
        messagebox.showerror("Error", f"Cannot modify request that is already {current_status.lower()}.")
        return
    
    # For approval, we need to select a specific resource
    approved_resource = None
    if status == "Approved":
        # Show dialog to select available resource
        approved_resource = select_available_resource(request_id)
        if not approved_resource:
            return  # User canceled or no resource available
    
    # Confirm action
    if not messagebox.askyesno("Confirm Action", f"Are you sure you want to {status.lower()} this resource request?"):
        return
        
    if cursor:
        try:
            if status == "Approved":
                cursor.execute("""
                    UPDATE resource_requests 
                    SET status = %s, approved_resource = %s 
                    WHERE request_id = %s
                """, (status, approved_resource, request_id))
            else:
                cursor.execute("""
                    UPDATE resource_requests 
                    SET status = %s 
                    WHERE request_id = %s
                """, (status, request_id))
                
            db.commit()
            messagebox.showinfo("Success", f"Resource request {status.lower()} successfully.")
            view_hod_requests(tree)  # Refresh the Treeview
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating request status: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def select_available_resource(request_id):
    # Get the request details
    if cursor:
        try:
            cursor.execute("""
                SELECT resource_type, date, time_slot 
                FROM resource_requests 
                WHERE request_id = %s
            """, (request_id,))
            request = cursor.fetchone()
            
            if not request:
                messagebox.showerror("Error", "Request not found.")
                return None
                
            resource_type, date, time_slot = request
            
            # Find available resources of the requested type that are not allocated
            cursor.execute("""
                SELECT r.resource_id, r.resource_name 
                FROM resources r
                LEFT JOIN resource_requests rr ON (
                    r.resource_id = rr.approved_resource 
                    AND rr.date = %s 
                    AND rr.time_slot = %s 
                    AND rr.status = 'Approved'
                )
                WHERE r.resource_type = %s AND rr.request_id IS NULL
            """, (date, time_slot, resource_type))
            available_resources = cursor.fetchall()
            
            if not available_resources:
                messagebox.showerror("Error", f"No available {resource_type} resources for the selected time slot.")
                return None
                
            # Create a dialog to select resource
            select_window = tk.Toplevel()
            select_window.title("Select Resource")
            center_window(select_window, 400, 200)
            
            ttk.Label(select_window, text=f"Select {resource_type}:").pack(pady=10)
            
            resource_var = tk.StringVar()
            resource_combo = ttk.Combobox(
                select_window, 
                textvariable=resource_var,
                values=[f"{res[0]} - {res[1]}" for res in available_resources],
                state="readonly"
            )
            resource_combo.pack(pady=10)
            
            selected_resource = None
            
            def on_select():
                nonlocal selected_resource
                selected = resource_var.get()
                if selected:
                    selected_resource = selected.split(" - ")[0]
                    select_window.destroy()
            
            ttk.Button(select_window, text="Select", command=on_select).pack(pady=10)
            
            select_window.grab_set()
            select_window.wait_window()
            
            return selected_resource
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error finding available resources: {e}")
            return None
    else:
        messagebox.showerror("Error", "Database connection not established.")
        return None

def view_available_resources():
    # Create a new window to display available resources
    resources_window = tk.Toplevel()
    resources_window.title("Available Resources")
    center_window(resources_window, 800, 500)
    
    # Configure styles
    configure_styles()
    
    # Create a frame for the treeview
    tree_frame = ttk.Frame(resources_window)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create Treeview
    columns = ("Resource ID", "Resource Name", "Resource Type", "Capacity", "Department", "Status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    
    # Define column headings and widths
    tree.heading("Resource ID", text="Resource ID")
    tree.heading("Resource Name", text="Resource Name")
    tree.heading("Resource Type", text="Resource Type")
    tree.heading("Capacity", text="Capacity")
    tree.heading("Department", text="Department")
    tree.heading("Status", text="Status")
    
    # Set column widths
    tree.column("Resource ID", width=80, minwidth=80)
    tree.column("Resource Name", width=150, minwidth=120)
    tree.column("Resource Type", width=120, minwidth=100)
    tree.column("Capacity", width=80, minwidth=60)
    tree.column("Department", width=120, minwidth=100)
    tree.column("Status", width=100, minwidth=80)
    
    # Add scrollbars
    y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Grid layout
    tree.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    # Filter options
    filter_frame = ttk.Frame(resources_window)
    filter_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(filter_frame, text="Filter by:").pack(side="left", padx=5)
    
    resource_type_var = tk.StringVar(value="All")
    resource_types = ["All", "Classroom", "Laboratory", "Auditorium", "Projector", "Other"]
    resource_type_combo = ttk.Combobox(filter_frame, textvariable=resource_type_var, values=resource_types, state="readonly", width=15)
    resource_type_combo.pack(side="left", padx=5)
    
    department_var = tk.StringVar(value="All")
    if cursor:
        cursor.execute("SELECT DISTINCT department FROM resources")
        departments = ["All"] + [dept[0] for dept in cursor.fetchall()]
        department_combo = ttk.Combobox(filter_frame, textvariable=department_var, values=departments, state="readonly", width=15)
        department_combo.pack(side="left", padx=5)
    
    def apply_filters():
        resource_type = resource_type_var.get()
        department = department_var.get()
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        if cursor:
            try:
                query = "SELECT * FROM resources WHERE 1=1"
                params = []
                
                if resource_type != "All":
                    query += " AND resource_type = %s"
                    params.append(resource_type)
                
                if department != "All":
                    query += " AND department = %s"
                    params.append(department)
                
                cursor.execute(query, tuple(params))
                resources = cursor.fetchall()
                
                for resource in resources:
                    tree.insert("", "end", values=resource)
                    
            except Error as e:
                messagebox.showerror("Database Error", f"Error retrieving resources: {e}")
    
    filter_button = ttk.Button(filter_frame, text="Apply Filters", command=apply_filters)
    filter_button.pack(side="left", padx=5)
    
    # Load all resources initially
    apply_filters()
    
    resources_window.mainloop()

def view_department_resources(department):
    # Create a new window to display department resources
    dept_window = tk.Toplevel()
    dept_window.title(f"{department} Department Resources")
    center_window(dept_window, 800, 500)
    
    # Configure styles
    configure_styles()
    
    # Create a frame for the treeview
    tree_frame = ttk.Frame(dept_window)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create Treeview
    columns = ("Resource ID", "Resource Name", "Resource Type", "Capacity", "Status")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    
    # Define column headings and widths
    tree.heading("Resource ID", text="Resource ID")
    tree.heading("Resource Name", text="Resource Name")
    tree.heading("Resource Type", text="Resource Type")
    tree.heading("Capacity", text="Capacity")
    tree.heading("Status", text="Status")
    
    # Set column widths
    tree.column("Resource ID", width=80, minwidth=80)
    tree.column("Resource Name", width=200, minwidth=150)
    tree.column("Resource Type", width=120, minwidth=100)
    tree.column("Capacity", width=80, minwidth=60)
    tree.column("Status", width=100, minwidth=80)
    
    # Add scrollbars
    y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
    
    # Grid layout
    tree.grid(row=0, column=0, sticky="nsew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # Configure grid weights
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    # Load department resources
    if cursor:
        try:
            cursor.execute("""
                SELECT resource_id, resource_name, resource_type, capacity, status 
                FROM resources 
                WHERE department = %s
                ORDER BY resource_type, resource_name
            """, (department,))
            resources = cursor.fetchall()
            
            for resource in resources:
                tree.insert("", "end", values=resource)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving department resources: {e}")
    
    dept_window.mainloop()

def view_all_resources(tree):
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
        
    if cursor:
        try:
            cursor.execute("SELECT * FROM resources ORDER BY resource_type, department, resource_name")
            resources = cursor.fetchall()
            
            for resource in resources:
                tree.insert("", "end", values=resource)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving resources: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def view_all_users(tree):
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
        
    if cursor:
        try:
            cursor.execute("SELECT user_id, username, name, role, department, email FROM users ORDER BY role, department, name")
            users = cursor.fetchall()
            
            for user in users:
                tree.insert("", "end", values=user)
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving users: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def add_new_resource():
    # Create a dialog to add new resource
    add_window = tk.Toplevel()
    add_window.title("Add New Resource")
    center_window(add_window, 400, 400)
    
    # Form fields
    form_frame = ttk.Frame(add_window, padding=15)
    form_frame.pack(fill="both", expand=True)
    
    ttk.Label(form_frame, text="Resource Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(form_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Resource Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    type_var = tk.StringVar(value="Classroom")
    type_combo = ttk.Combobox(form_frame, textvariable=type_var, values=["Classroom", "Laboratory", "Auditorium", "Projector", "Other"], state="readonly")
    type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Capacity:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    capacity_entry = ttk.Entry(form_frame)
    capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Department:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    dept_var = tk.StringVar()
    if cursor:
        cursor.execute("SELECT DISTINCT department FROM resources")
        departments = [dept[0] for dept in cursor.fetchall()]
        dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, values=departments)
        dept_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    status_var = tk.StringVar(value="Available")
    status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=["Available", "Maintenance", "Unavailable"], state="readonly")
    status_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    
    def save_resource():
        name = name_entry.get()
        resource_type = type_var.get()
        capacity = capacity_entry.get()
        department = dept_var.get()
        status = status_var.get()
        
        if not name or not resource_type or not capacity or not department or not status:
            messagebox.showerror("Error", "All fields are required")
            return
            
        try:
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a number")
            return
            
        if cursor:
            try:
                cursor.execute("""
                    INSERT INTO resources 
                    (resource_name, resource_type, capacity, department, status) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, resource_type, capacity, department, status))
                db.commit()
                messagebox.showinfo("Success", "Resource added successfully.")
                add_window.destroy()
            except Error as e:
                messagebox.showerror("Database Error", f"Error adding resource: {e}")
        else:
            messagebox.showerror("Error", "Database connection not established.")
    
    button_frame = ttk.Frame(form_frame)
    button_frame.grid(row=5, column=0, columnspan=2, pady=10)
    
    ttk.Button(button_frame, text="Save", style="Success.TButton", command=save_resource).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side="left", padx=5)
    
    add_window.mainloop()

def edit_resource(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No resource selected. Please select a resource first.")
        return
        
    resource_id = tree.item(selected_item[0])['values'][0]  # Get the resource_id from the selected row
    
    # Get current resource details
    if cursor:
        try:
            cursor.execute("SELECT * FROM resources WHERE resource_id = %s", (resource_id,))
            resource = cursor.fetchone()
            
            if not resource:
                messagebox.showerror("Error", "Resource not found.")
                return
                
            # Create a dialog to edit resource
            edit_window = tk.Toplevel()
            edit_window.title("Edit Resource")
            center_window(edit_window, 400, 400)
            
            # Form fields
            form_frame = ttk.Frame(edit_window, padding=15)
            form_frame.pack(fill="both", expand=True)
            
            ttk.Label(form_frame, text="Resource Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            name_entry = ttk.Entry(form_frame)
            name_entry.insert(0, resource[1])
            name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Resource Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            type_var = tk.StringVar(value=resource[2])
            type_combo = ttk.Combobox(form_frame, textvariable=type_var, values=["Classroom", "Laboratory", "Auditorium", "Projector", "Other"], state="readonly")
            type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Capacity:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            capacity_entry = ttk.Entry(form_frame)
            capacity_entry.insert(0, str(resource[3]))
            capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Department:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            dept_var = tk.StringVar(value=resource[4])
            if cursor:
                cursor.execute("SELECT DISTINCT department FROM resources")
                departments = [dept[0] for dept in cursor.fetchall()]
                dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, values=departments)
                dept_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
            status_var = tk.StringVar(value=resource[5])
            status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=["Available", "Maintenance", "Unavailable"], state="readonly")
            status_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
            
            def update_resource():
                name = name_entry.get()
                resource_type = type_var.get()
                capacity = capacity_entry.get()
                department = dept_var.get()
                status = status_var.get()
                
                if not name or not resource_type or not capacity or not department or not status:
                    messagebox.showerror("Error", "All fields are required")
                    return
                    
                try:
                    capacity = int(capacity)
                except ValueError:
                    messagebox.showerror("Error", "Capacity must be a number")
                    return
                    
                if cursor:
                    try:
                        cursor.execute("""
                            UPDATE resources 
                            SET resource_name = %s, resource_type = %s, capacity = %s, 
                                department = %s, status = %s 
                            WHERE resource_id = %s
                        """, (name, resource_type, capacity, department, status, resource_id))
                        db.commit()
                        messagebox.showinfo("Success", "Resource updated successfully.")
                        edit_window.destroy()
                        view_all_resources(tree)  # Refresh the treeview
                    except Error as e:
                        messagebox.showerror("Database Error", f"Error updating resource: {e}")
                else:
                    messagebox.showerror("Error", "Database connection not established.")
            
            button_frame = ttk.Frame(form_frame)
            button_frame.grid(row=5, column=0, columnspan=2, pady=10)
            
            ttk.Button(button_frame, text="Update", style="Success.TButton", command=update_resource).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="left", padx=5)
            
            edit_window.mainloop()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving resource: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def delete_resource(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No resource selected. Please select a resource first.")
        return
        
    resource_id = tree.item(selected_item[0])['values'][0]  # Get the resource_id from the selected row
    resource_name = tree.item(selected_item[0])['values'][1]
    
    # Confirm deletion
    if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {resource_name}? This action cannot be undone."):
        return
        
    if cursor:
        try:
            # First check if the resource is allocated in any approved requests
            cursor.execute("""
                SELECT COUNT(*) FROM resource_requests 
                WHERE approved_resource = %s AND status = 'Approved'
            """, (resource_id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                messagebox.showerror("Error", "Cannot delete resource that is currently allocated in approved requests.")
                return
                
            # Delete the resource
            cursor.execute("DELETE FROM resources WHERE resource_id = %s", (resource_id,))
            db.commit()
            messagebox.showinfo("Success", "Resource deleted successfully.")
            view_all_resources(tree)  # Refresh the treeview
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting resource: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def add_new_user():
    # Create a dialog to add new user
    add_window = tk.Toplevel()
    add_window.title("Add New User")
    center_window(add_window, 400, 450)
    
    # Form fields
    form_frame = ttk.Frame(add_window, padding=15)
    form_frame.pack(fill="both", expand=True)
    
    ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    username_entry = ttk.Entry(form_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    password_entry = ttk.Entry(form_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(form_frame)
    name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    role_var = tk.StringVar(value="Faculty")
    role_combo = ttk.Combobox(form_frame, textvariable=role_var, values=["Admin", "HOD", "Faculty"], state="readonly")
    role_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Department:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    dept_var = tk.StringVar()
    if cursor:
        cursor.execute("SELECT DISTINCT department FROM resources")
        departments = [dept[0] for dept in cursor.fetchall()]
        dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, values=departments)
        dept_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    
    ttk.Label(form_frame, text="Email:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    email_entry = ttk.Entry(form_frame)
    email_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
    
    def save_user():
        username = username_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        role = role_var.get()
        department = dept_var.get()
        email = email_entry.get()
        
        if not username or not password or not name or not role or not email:
            messagebox.showerror("Error", "All fields except department are required")
            return
            
        if role in ["HOD", "Faculty"] and not department:
            messagebox.showerror("Error", "Department is required for HOD and Faculty")
            return
            
        if cursor:
            try:
                cursor.execute("""
                    INSERT INTO users 
                    (username, password, role, name, department, email) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (username, password, role, name, department, email))
                db.commit()
                messagebox.showinfo("Success", "User added successfully.")
                add_window.destroy()
            except Error as e:
                messagebox.showerror("Database Error", f"Error adding user: {e}")
        else:
            messagebox.showerror("Error", "Database connection not established.")
    
    button_frame = ttk.Frame(form_frame)
    button_frame.grid(row=6, column=0, columnspan=2, pady=10)
    
    ttk.Button(button_frame, text="Save", style="Success.TButton", command=save_user).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side="left", padx=5)
    
    add_window.mainloop()

def edit_user(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No user selected. Please select a user first.")
        return
        
    user_id = tree.item(selected_item[0])['values'][0]  # Get the user_id from the selected row
    
    # Get current user details
    if cursor:
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                messagebox.showerror("Error", "User not found.")
                return
                
            # Create a dialog to edit user
            edit_window = tk.Toplevel()
            edit_window.title("Edit User")
            center_window(edit_window, 400, 450)
            
            # Form fields
            form_frame = ttk.Frame(edit_window, padding=15)
            form_frame.pack(fill="both", expand=True)
            
            ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            username_entry = ttk.Entry(form_frame)
            username_entry.insert(0, user[1])
            username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            password_entry = ttk.Entry(form_frame, show="*")
            password_entry.insert(0, user[2])
            password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            name_entry = ttk.Entry(form_frame)
            name_entry.insert(0, user[4])
            name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            role_var = tk.StringVar(value=user[3])
            role_combo = ttk.Combobox(form_frame, textvariable=role_var, values=["Admin", "HOD", "Faculty"], state="readonly")
            role_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Department:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
            dept_var = tk.StringVar(value=user[5] if user[5] else "")
            if cursor:
                cursor.execute("SELECT DISTINCT department FROM resources")
                departments = [dept[0] for dept in cursor.fetchall()]
                dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, values=departments)
                dept_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
            
            ttk.Label(form_frame, text="Email:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
            email_entry = ttk.Entry(form_frame)
            email_entry.insert(0, user[6])
            email_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
            
            def update_user():
                username = username_entry.get()
                password = password_entry.get()
                name = name_entry.get()
                role = role_var.get()
                department = dept_var.get()
                email = email_entry.get()
                
                if not username or not password or not name or not role or not email:
                    messagebox.showerror("Error", "All fields except department are required")
                    return
                    
                if role in ["HOD", "Faculty"] and not department:
                    messagebox.showerror("Error", "Department is required for HOD and Faculty")
                    return
                    
                if cursor:
                    try:
                        cursor.execute("""
                            UPDATE users 
                            SET username = %s, password = %s, role = %s, 
                                name = %s, department = %s, email = %s 
                            WHERE user_id = %s
                        """, (username, password, role, name, department, email, user_id))
                        db.commit()
                        messagebox.showinfo("Success", "User updated successfully.")
                        edit_window.destroy()
                        view_all_users(tree)  # Refresh the treeview
                    except Error as e:
                        messagebox.showerror("Database Error", f"Error updating user: {e}")
                else:
                    messagebox.showerror("Error", "Database connection not established.")
            
            button_frame = ttk.Frame(form_frame)
            button_frame.grid(row=6, column=0, columnspan=2, pady=10)
            
            ttk.Button(button_frame, text="Update", style="Success.TButton", command=update_user).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="left", padx=5)
            
            edit_window.mainloop()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error retrieving user: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def delete_user(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No user selected. Please select a user first.")
        return
        
    user_id = tree.item(selected_item[0])['values'][0]  # Get the user_id from the selected row
    username = tree.item(selected_item[0])['values'][1]
    
    # Prevent deletion of current user
    if user_id == current_user[0]:
        messagebox.showerror("Error", "You cannot delete your own account while logged in.")
        return
        
    # Confirm deletion
    if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {username}? This action cannot be undone."):
        return
        
    if cursor:
        try:
            # First check if the user has any pending or approved requests
            cursor.execute("""
                SELECT COUNT(*) FROM resource_requests 
                WHERE user_id = %s AND status IN ('Pending', 'Approved')
            """, (user_id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                messagebox.showerror("Error", "Cannot delete user with pending or approved resource requests.")
                return
                
            # Delete the user
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            db.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            view_all_users(tree)  # Refresh the treeview
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting user: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

def generate_report(report_type, from_date, to_date):
    # Validate dates
    try:
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
        
        if from_date_obj > to_date_obj:
            messagebox.showerror("Error", "From date cannot be after To date")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
        return
        
    if cursor:
        try:
            report_content = ""
            
            if report_type == "Resource Utilization":
                cursor.execute("""
                    SELECT r.resource_name, r.resource_type, r.department, 
                           COUNT(rr.request_id) as allocations,
                           SUM(CASE WHEN rr.status = 'Approved' THEN 1 ELSE 0 END) as approved,
                           SUM(CASE WHEN rr.status = 'Rejected' THEN 1 ELSE 0 END) as rejected
                    FROM resources r
                    LEFT JOIN resource_requests rr ON r.resource_id = rr.approved_resource
                        AND rr.date BETWEEN %s AND %s
                    GROUP BY r.resource_id
                    ORDER BY r.resource_type, r.department, r.resource_name
                """, (from_date, to_date))
                
                report_content += "RESOURCE UTILIZATION REPORT\n"
                report_content += f"Date Range: {from_date} to {to_date}\n"
                report_content += "-" * 80 + "\n"
                report_content += "Resource Name".ljust(25) + "Type".ljust(15) + "Department".ljust(15) + "Allocations".center(12) + "Approved".center(10) + "Rejected".center(10) + "\n"
                report_content += "-" * 80 + "\n"
                
                for row in cursor.fetchall():
                    report_content += f"{row[0][:24].ljust(25)}{row[1][:14].ljust(15)}{row[2][:14].ljust(15)}{str(row[3]).center(12)}{str(row[4]).center(10)}{str(row[5]).center(10)}\n"
                    
            elif report_type == "Department-wise Allocation":
                cursor.execute("""
                    SELECT u.department, 
                           COUNT(rr.request_id) as total_requests,
                           SUM(CASE WHEN rr.status = 'Approved' THEN 1 ELSE 0 END) as approved,
                           SUM(CASE WHEN rr.status = 'Rejected' THEN 1 ELSE 0 END) as rejected,
                           SUM(CASE WHEN rr.status = 'Pending' THEN 1 ELSE 0 END) as pending
                    FROM users u
                    LEFT JOIN resource_requests rr ON u.user_id = rr.user_id
                        AND rr.date BETWEEN %s AND %s
                    WHERE u.department IS NOT NULL
                    GROUP BY u.department
                    ORDER BY u.department
                """, (from_date, to_date))
                
                report_content += "DEPARTMENT-WISE ALLOCATION REPORT\n"
                report_content += f"Date Range: {from_date} to {to_date}\n"
                report_content += "-" * 80 + "\n"
                report_content += "Department".ljust(20) + "Total".center(10) + "Approved".center(10) + "Rejected".center(10) + "Pending".center(10) + "\n"
                report_content += "-" * 80 + "\n"
                
                for row in cursor.fetchall():
                    report_content += f"{row[0][:19].ljust(20)}{str(row[1]).center(10)}{str(row[2]).center(10)}{str(row[3]).center(10)}{str(row[4]).center(10)}\n"
                    
            elif report_type == "Faculty-wise Requests":
                cursor.execute("""
                    SELECT u.name, u.department, 
                           COUNT(rr.request_id) as total_requests,
                           SUM(CASE WHEN rr.status = 'Approved' THEN 1 ELSE 0 END) as approved,
                           SUM(CASE WHEN rr.status = 'Rejected' THEN 1 ELSE 0 END) as rejected,
                           SUM(CASE WHEN rr.status = 'Pending' THEN 1 ELSE 0 END) as pending
                    FROM users u
                    LEFT JOIN resource_requests rr ON u.user_id = rr.user_id
                        AND rr.date BETWEEN %s AND %s
                    WHERE u.role = 'Faculty'
                    GROUP BY u.user_id
                    ORDER BY u.department, u.name
                """, (from_date, to_date))
                
                report_content += "FACULTY-WISE REQUESTS REPORT\n"
                report_content += f"Date Range: {from_date} to {to_date}\n"
                report_content += "-" * 80 + "\n"
                report_content += "Faculty Name".ljust(25) + "Department".ljust(15) + "Total".center(10) + "Approved".center(10) + "Rejected".center(10) + "Pending".center(10) + "\n"
                report_content += "-" * 80 + "\n"
                
                for row in cursor.fetchall():
                    report_content += f"{row[0][:24].ljust(25)}{row[1][:14].ljust(15)}{str(row[2]).center(10)}{str(row[3]).center(10)}{str(row[4]).center(10)}{str(row[5]).center(10)}\n"
            
            # Display the report in the text widget
            report_display = tk.Toplevel()
            report_display.title(f"{report_type} Report")
            center_window(report_display, 800, 600)
            
            text_widget = tk.Text(report_display, wrap="word", font=("Courier", 10))
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
            text_widget.insert("1.0", report_content)
            text_widget.config(state="disabled")
            
            # Add a button to save the report
            def save_report():
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                    title="Save Report As"
                )
                if file_path:
                    with open(file_path, "w") as f:
                        f.write(report_content)
                    messagebox.showinfo("Success", "Report saved successfully.")
            
            save_button = ttk.Button(report_display, text="Save Report", command=save_report)
            save_button.pack(pady=10)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error generating report: {e}")
    else:
        messagebox.showerror("Error", "Database connection not established.")

# Logout Function
def logout(window):
    global current_user
    current_user = None
    window.destroy()
    open_login_window()

# Open Login Window
def open_login_window():
    global login_window, username_entry, password_entry
    login_window = tk.Tk()
    login_window.title("SK Somaiya College - Resource Management System")
    center_window(login_window, 400, 400)
    login_window.configure(bg="#f0f0f0")

    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TButton", font=("Arial", 12), background="#4b8a9c", foreground="white", padding=5)
    style.map("TButton", background=[("active", "#3a6d7a")])
    style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#4b8a9c", foreground="white", padding=10)

    # Create a main frame with padding
    main_frame = ttk.Frame(login_window, padding=20, style="TFrame")
    main_frame.pack(fill="both", expand=True)

    # Header Frame
    header_frame = ttk.Frame(main_frame, style="TFrame")
    header_frame.pack(fill="x", pady=(0, 20))
    
    header_label = ttk.Label(header_frame, text="SK Somaiya College", style="Header.TLabel")
    header_label.pack(fill="x")
    
    subheader_label = ttk.Label(header_frame, text="Resource Management System", font=("Arial", 12), background="#4b8a9c", foreground="white")
    subheader_label.pack(fill="x")

    # Login Form Frame
    login_form = ttk.Frame(main_frame, style="TFrame")
    login_form.pack(fill="x", pady=10)

    # Username Field
    username_frame = ttk.Frame(login_form, style="TFrame")
    username_frame.pack(fill="x", pady=10)
    
    ttk.Label(username_frame, text="Username:", font=("Arial", 12)).pack(anchor="w")
    username_entry = ttk.Entry(username_frame, font=("Arial", 12), width=30)
    username_entry.pack(fill="x", pady=(5, 0))

    # Password Field
    password_frame = ttk.Frame(login_form, style="TFrame")
    password_frame.pack(fill="x", pady=10)
    
    ttk.Label(password_frame, text="Password:", font=("Arial", 12)).pack(anchor="w")
    password_entry = ttk.Entry(password_frame, show="*", font=("Arial", 12), width=30)
    password_entry.pack(fill="x", pady=(5, 0))

    # Login Button
    login_button = ttk.Button(login_form, text="Login", command=login, style="Primary.TButton")
    login_button.pack(pady=20)
    
    # Bind Enter key to login
    login_window.bind("<Return>", lambda event: login())

    login_window.mainloop()

# Start the application
open_login_window()

# Close the database connection when the application exits
if db:
    db.close()
