'''
A CLI Program to Track and Calculate Study Progress
⚠️ Warning: This code is experimental and for personal/educational use.
Author : zen
'''

import time
import csv 
import os

def menu():
    os.system('clear')
    print("""
🌟 Welcome to Zen's Study Progress Tracker 🌟

📚 1 - ➕ Add New Objective
🗑️ 2 - ❌ Remove Objective
⏱️ 3 - ▶️ Start Study Session
📊 4 - 📖 Show Progress Table
🚪 5 - 🔚 Exit Program
           """)


def csv_write(rows):
    with open('csvdatabase.csv','a', newline='', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(rows)


def csv_remove(name):
    with open('csvdatabase.csv', 'r') as inp, open('csvdatabase2.csv', 'w') as out:
        csv_writer = csv.writer(out)
        for row in csv.reader(inp):
            if row[0] != name:
                csv_writer.writerow(row)
    os.replace('csvdatabase2.csv', 'csvdatabase.csv')
        
def if_exist_csv():
    if os.path.exists('csvdatabase.csv'):
        return True
    else:
        print('⚠️ Please create some courses first!')
        return
     

def csv_reader():
    if if_exist_csv():
        print("\n📖 Your Current Courses:\n")
        with open('csvdatabase.csv', 'r', newline='', encoding='utf-8') as input_file:
            for row in csv.reader(input_file):
                print(f'📘 Name: {row[0]}  |  🎯 Goal Hours: {row[1]}h ')
        print()
        return True
    else:
        return False
     
def csv_reader_table():
    if if_exist_csv():
        print('\n' + '='*60)
        print('📊  Your Study Progress Table')
        print('='*60)
        print('🔹 Name | 🎯 Total Hours | ⏱️ Studied Hours | 🕒 Studied Minutes')
        print('-'*60)
        with open('csvdatabase.csv', 'r', newline='', encoding='utf-8') as input_file:
            for row in csv.reader(input_file):
                print(f'📘 {row[0]} | {row[1]}h | {row[2]}h | {row[3]}m')
        print('='*60 + '\n')
        return True
    else:
        return False



def csv_change_hours(course_name,studied_time_now):
    with open('csvdatabase.csv', 'r', newline='', encoding='utf-8') as input_file:
        with open('csvdatabasenew.csv', 'w', newline='', encoding='utf-8') as ouput_file:
            reader = csv.reader(input_file)
            writer = csv.writer(ouput_file)
            all = []
            for row in reader:
                name = row[0]
                if name.lower() == course_name.lower():
                    if not studied_time_now:
                        print('⚠️ Please study at least 1 minute to save progress.')
                        return
                    current_studied_hours = int(row[2]) 
                    current_studied_minutes = int(row[3])
                    
                    total_minute = int(studied_time_now) + current_studied_minutes
                    row.pop()
                    row.pop()
                    total_hour = total_minute // 60 + current_studied_hours
                    row.append(total_hour)
                    row.append(total_minute)
                    all.append(row)
                else:
                    all.append(row)               
            writer.writerows(all)
            os.replace('csvdatabasenew.csv','csvdatabase.csv')

def check_if_exist(course_name):
    if if_exist_csv():
        with open('csvdatabase.csv', 'r', newline='', encoding='utf-8') as input_file:
            reader = csv.reader(input_file)
            check = False
            for row in reader:
                name = row[0]
                if course_name.lower() == name.lower():
                    check = True
        return check

def timer():
    start = time.time()
    print('⏳ Press Ctrl+C to stop studying.')
    try:
        while KeyboardInterrupt:
            elapsed = time.time() - start
            elapsed_str = str(elapsed)
            elapsed_splited = elapsed_str.split('.')
            print(f'\r🕒 Studying... {elapsed_splited[0]} sec', end="")
            time.sleep(1)
    except KeyboardInterrupt:
        end = time.time()
        string_num = str(end-start)
        num = string_num.split('.')
        int_num = int(num[0])
        os.system('clear')
        if int_num > 3600:
            min_num = int_num // 60
            hour_num = min_num // 60
            print(f'\n\n✅ Great Job! You studied for {hour_num} hours. Progress saved! 💾')
            time.sleep(5)
            return min_num
        elif int_num > 60:
            min_num = int_num // 60
            print(f'\n\n✅ Well done! You studied {min_num} minutes. Progress saved! 💾')
            time.sleep(3)
            return min_num
        else:
            print('\n⚠️ Less than a minute studied. No progress saved.')
            time.sleep(2)
            return 0
                    

def main():
    os.system('clear')
    input_user = 0
    while True:
        menu()
        input_user = str(input('👉 Please Enter Your Choice: ')).strip()
        if input_user == '5':
            os.system('clear')
            print('👋 Exiting program... See you next time')
            return
        if input_user == '1':
            os.system('clear')
            name = str(input('✏️ Enter the name of your study objective: ')).strip()
            hours = str(input('⏳ Enter total study hours goal: ')).strip()
            if hours.isdigit():
                rows = [name.lower(), hours, 0, 0]
                csv_write(rows)
                print('✅ Objective added successfully!')
                time.sleep(1.5)
            else:
                print('❌ Please Enter an number For Goal Study Hour of this Object!')
                time.sleep(1.5)
        if input_user == '2':
            if os.path.exists('csvdatabase.csv'):
                name = str(input('🗑️ Enter name of the objective to remove: ')).strip()
                csv_remove(name.lower())
                print('✅ Objective removed.')
                time.sleep(1.5)
                os.system('clear')
            else:
                print('⚠️ Please create a subject first.')
                time.sleep(2)
                    
        if input_user == '3':
            os.system('clear')
            print('🎯 Please select a course:')
            if csv_reader():
                user_input = input('📘 Enter course name: ').strip()
                if check_if_exist(user_input):
                    os.system('clear')
                    print(f'🚀 Study session for "{user_input.lower()}" started!')
                    csv_change_hours(user_input.lower(), timer())
                else:
                    print('❌ No such course found. Try again.')
                    time.sleep(2)
            else:
                print('⚠️ No courses found. Add one first.')
                time.sleep(2)
            
        if input_user == '4':
            os.system('clear')
            if csv_reader_table():
                user = input('↩️ Press Enter to go back...')
            else:
                print('⚠️ Please add some objectives first.')
                time.sleep(2) 

if __name__ == '__main__':
    main()

