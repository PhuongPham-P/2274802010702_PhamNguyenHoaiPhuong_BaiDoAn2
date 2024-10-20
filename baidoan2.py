import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Kết nối cơ sở dữ liệu PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
        host="localhost",  
        database="baiktr",
        user="postgres",
        password="1"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", str(e))
        return None

# Các hàm thao tác với cơ sở dữ liệu
def fetch_students():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

def insert_student(name, age, gender, major):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)",
            (name, age, gender, major)
        )
        conn.commit()
        conn.close()

def update_student(student_id, name, age, gender, major):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s",
            (name, age, gender, major, student_id)
        )
        conn.commit()
        conn.close()

def delete_student(student_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        conn.commit()
        conn.close()

# Lớp ứng dụng chính
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh Viên")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f4f7")

        # Biến lưu trữ thông tin nhập liệu
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.major_var = tk.StringVar()

        # Form nhập liệu
        form_frame = tk.Frame(self.root, bg="#f0f4f7")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Tên:", bg="#f0f4f7", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.name_var, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Tuổi:", bg="#f0f4f7", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.age_var, font=("Arial", 12), width=10).grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Giới tính:", bg="#f0f4f7", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.gender_var, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Ngành học:", bg="#f0f4f7", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.major_var, font=("Arial", 12), width=20).grid(row=1, column=3, padx=10)

        # Các nút chức năng
        button_frame = tk.Frame(self.root, bg="#f0f4f7")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Thêm sinh viên", command=self.add_student, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Cập nhật", command=self.update_student, bg="#2196F3", fg="white", font=("Arial", 12), padx=10).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Xóa", command=self.delete_student, bg="#f44336", fg="white", font=("Arial", 12), padx=10).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(button_frame, text="Tải lại", command=self.load_students, bg="#FFC107", fg="white", font=("Arial", 12), padx=10).grid(row=0, column=3, padx=10, pady=5)

        # Bảng hiển thị danh sách sinh viên
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Age", "Gender", "Major"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Tên")
        self.tree.heading("Age", text="Tuổi")
        self.tree.heading("Gender", text="Giới tính")
        self.tree.heading("Major", text="Ngành học")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150, anchor="center")
        self.tree.column("Age", width=50, anchor="center")
        self.tree.column("Gender", width=100, anchor="center")
        self.tree.column("Major", width=150, anchor="center")
        self.tree.pack(pady=20)

        self.load_students()

    def add_student(self):
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        major = self.major_var.get()

        if name and age.isdigit() and gender and major:
            insert_student(name, int(age), gender, major)
            self.load_students()
        else:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập dữ liệu hợp lệ.")

    def update_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            student_id = self.tree.item(selected_item, "values")[0]
            name = self.name_var.get()
            age = self.age_var.get()
            gender = self.gender_var.get()
            major = self.major_var.get()

            if name and age.isdigit() and gender and major:
                update_student(student_id, name, int(age), gender, major)
                self.load_students()
            else:
                messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập dữ liệu hợp lệ.")
        else:
            messagebox.showwarning("Lỗi chọn sinh viên", "Vui lòng chọn sinh viên.")

    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            student_id = self.tree.item(selected_item, "values")[0]
            delete_student(student_id)
            self.load_students()
        else:
            messagebox.showwarning("Lỗi chọn sinh viên", "Vui lòng chọn sinh viên.")

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = fetch_students()
        for student in students:
            self.tree.insert("", "end", values=student)

# Khởi tạo ứng dụng Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
