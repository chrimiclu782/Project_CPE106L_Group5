import flet as ft
import sqlite3
import datetime
import random

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        age INTEGER,
                        gender TEXT,
                        weight REAL,
                        height REAL,
                        vices TEXT,
                        workout_style TEXT,
                        login_days INTEGER DEFAULT 0,
                        last_login TEXT)''')
    conn.commit()
    conn.close()

def calculate_bmi(weight, height):
    height_m = height / 100  # Convert cm to meters
    return round(weight / (height_m ** 2), 2)

def get_today_plan():
    weekday = datetime.datetime.today().weekday()
    workout_plans = random.sample([
        "Light cardio and stretching", "Full-body strength training", "Yoga and flexibility exercises",
        "Cardio and endurance training", "Upper body strength", "Lower body strength", "HIIT workout",
        "Pilates session", "Core and abs training", "Endurance running"
    ], 7)
    
    meal_plans = random.sample([
        "Oatmeal and fruits", "Grilled chicken with quinoa", "Vegetable stir-fry with tofu",
        "Salmon with brown rice", "Lean beef with steamed vegetables", "Chicken and sweet potatoes", 
        "Balanced light meals", "Avocado toast with eggs", "Smoothie bowl with nuts", "Protein-packed salad"
    ], 7)
    
    return workout_plans[weekday], meal_plans[weekday]

def register_user(e, page, reg_username_field, reg_password_field, reg_age_field, reg_gender_field, reg_weight_field, reg_height_field, reg_vices_field, reg_workout_field, register_status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, age, gender, weight, height, vices, workout_style, last_login) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (reg_username_field.value, reg_password_field.value, reg_age_field.value, reg_gender_field.value, reg_weight_field.value, reg_height_field.value, reg_vices_field.value, reg_workout_field.value, "Never"))
        conn.commit()
        register_status.value = "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
        register_status.value = "Username already exists!"
    conn.close()
    page.update()
    show_login_screen(page)

def show_registration(page):
    reg_username_field = ft.TextField(label="Username")
    reg_password_field = ft.TextField(label="Password", password=True)
    reg_age_field = ft.TextField(label="Age", keyboard_type=ft.KeyboardType.NUMBER)
    reg_gender_field = ft.TextField(label="Gender")
    reg_weight_field = ft.TextField(label="Weight (kg)", keyboard_type=ft.KeyboardType.NUMBER)
    reg_height_field = ft.TextField(label="Height (cm)", keyboard_type=ft.KeyboardType.NUMBER)
    reg_vices_field = ft.TextField(label="Vices (if any)")
    reg_workout_field = ft.TextField(label="Workout Style")
    register_status = ft.Text(value="")
    register_button = ft.ElevatedButton(text="Register", on_click=lambda e: register_user(e, page, reg_username_field, reg_password_field, reg_age_field, reg_gender_field, reg_weight_field, reg_height_field, reg_vices_field, reg_workout_field, register_status))
    back_to_login_button = ft.ElevatedButton(text="Back to Login", on_click=lambda e: show_login_screen(page))
    page.clean()
    page.add(
        ft.Text("Register for Healthy Habits App", size=20, weight=ft.FontWeight.BOLD),
        reg_username_field, reg_password_field, reg_age_field, reg_gender_field, reg_weight_field, reg_height_field, reg_vices_field, reg_workout_field,
        register_button, back_to_login_button, register_status
    )

def show_login_screen(page):
    page.clean()
    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    login_status = ft.Text(value="")
    login_button = ft.ElevatedButton(text="Login", on_click=lambda e: login(e, page, username_field, password_field, login_status))
    register_button = ft.ElevatedButton(text="Register", on_click=lambda e: show_registration(page))
    page.add(username_field, password_field, login_button, register_button, login_status)

def login(e, page, username_field, password_field, login_status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username_field.value, password_field.value))
    user = cursor.fetchone()
    if user:
        weight_field = ft.TextField(label="Enter your current weight (kg)", keyboard_type=ft.KeyboardType.NUMBER)
        height_field = ft.TextField(label="Enter your current height (cm)", keyboard_type=ft.KeyboardType.NUMBER)
        update_button = ft.ElevatedButton(text="Update BMI", on_click=lambda e: update_bmi(e, page, user, weight_field, height_field))
        page.clean()
        page.add(ft.Text("Update your BMI"), weight_field, height_field, update_button)
    else:
        login_status.value = "Invalid credentials."
        conn.close()
        page.update()

def update_bmi(e, page, user, weight_field, height_field):
    new_weight = float(weight_field.value)
    new_height = float(height_field.value)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET weight=?, height=?, login_days = login_days + 1, last_login = ? WHERE username=?", (new_weight, new_height, datetime.date.today().strftime("%Y-%m-%d"), user[1]))
    conn.commit()
    conn.close()
    show_main_app(page, user, new_weight, new_height)

def show_main_app(page, user, weight, height):
    username, age, gender, vices, workout_style, login_days, last_login = user[1], user[3], user[4], user[7], user[8], user[9], user[10]
    bmi = calculate_bmi(weight, height)
    workout_plan, meal_plan = get_today_plan()
    page.clean()
    page.add(
        ft.Text(f"Welcome {username}!", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(f"BMI: {bmi}"),
        ft.Text(f"Today's Workout Plan: {workout_plan}"),
        ft.Text(f"Today's Meal Plan: {meal_plan}"),
        ft.Text(f"Login Days: {login_days}"),
        ft.ElevatedButton(text="Logout", on_click=lambda e: show_login_screen(page))
    )

def main(page: ft.Page):
    page.title = "Healthy Habits Tracker"
    init_db()
    show_login_screen(page)

ft.app(target=main)
