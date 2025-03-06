from datetime import date

class User:
    def __init__(self, userId, name, age, gender, height, weight):
        self.userId = userId
        self.name = name
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight

    def calculateBMI(self):
        return self.weight / (self.height ** 2)

class BMIRecord:
    def __init__(self, recordId, userId, date, bmiValue):
        self.recordId = recordId
        self.userId = userId
        self.date = date
        self.bmiValue = bmiValue

    def getBMIStatus(self):
        if self.bmiValue < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmiValue < 24.9:
            return "Normal"
        elif 25 <= self.bmiValue < 29.9:
            return "Overweight"
        else:
            return "Obese"

class BMICalculator:
    @staticmethod
    def calculateBMI(height, weight):
        return weight / (height ** 2)

def get_user_input():
    userId = int(input("Enter user ID: "))
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    height = float(input("Enter height in meters: "))
    weight = float(input("Enter weight in kilograms: "))
    return User(userId, name, age, gender, height, weight)

def main():
    user = get_user_input()

    bmi_value = BMICalculator.calculateBMI(user.height, user.weight)
    record = BMIRecord(1, user.userId, date.today(), bmi_value)

    print(f"\n{user.name}'s BMI: {bmi_value:.2f}")
    print(f"BMI Status: {record.getBMIStatus()}")

if __name__ == "__main__":
    main()
