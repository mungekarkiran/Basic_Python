# Variable's
students = {
    'Ram' : 100,
    'John' : 74,
    'Guru' : 82
}

# Functions
'''
Add 
Update
Delete
View
exit
'''

def show_all_students():
    print(f"student | \t gread | \t")
    for student, gread in students.items():
        print(f"{student} | \t {gread} | \t")
    print("\n")

def add_student(name:str, gread:int):
    if name not in students.keys():
        students[name] = gread
        print(f"New student added !!! \n")
    else:
        print(f"Student alreay exist. \n")

def update_gread(name:str, gread:int):
    if name in students.keys():
        students[name] = gread
        print(f"Student gread updated !!! \n")
    else:
        print(f"Student not found. \n")

def delete_student(name:str):
    if name in students.keys():
        del students[name] 
        print(f"Student deleted !!! \n")
    else:
        print(f"Student not found. \n")

def exit_code():
    exit(1)

if __name__ == "__main__":
    print(f"Welcome To Student Grade Management System. \n\n")
    while 1:
        print(f"1. View students gread. \n2. Add new student and gread. \n3. Update student gread. \n4. Delete student. \n5. exit. \n")
        choice = int(input("Enter your choice : "))

        if choice == 1:
            show_all_students()
        elif choice == 2:
            name = input("Enter student name : ")
            gread = int(input("Enter student gread : "))
            add_student(name, gread)
        elif choice == 3:
            name = input("Enter student name : ")
            gread = int(input("Enter student gread : "))
            update_gread(name, gread)
        elif choice == 4:
            name = input("Enter student name : ")
            delete_student(name)
        elif choice == 5:
            exit_code()
        else:
            print(f"Wrong choice. Please try again !!! \n")
        








