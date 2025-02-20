from datetime import date

class User:
    def __init__(self, userId, name, age, gender, height_cm, weight):
        self.userId = userId
        self.name = name
        self.age = age
        self.gender = gender
        self.height = height_cm / 100  # Convert cm to meters
        self.weight = weight

    def calculateBMI(self):
        return self.weight / (self.height ** 2)

class BMIRecord:
    def __init__(self, recordId, user):
        self.recordId = recordId
        self.userId = user.userId
        self.date = date.today()
        self.bmiValue = user.calculateBMI()

    def getBMIStatus(self):
        return (
            "Underweight" if self.bmiValue < 18.5 else
            "Normal" if self.bmiValue < 24.9 else
            "Overweight" if self.bmiValue < 29.9 else
            "Obese"
        )

def get_user_input():
    userId = int(input("Enter user ID: "))
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    height_cm = float(input("Enter height in cm: "))  # Now asking for height in cm
    weight = float(input("Enter weight in kg: "))
    return User(userId, name, age, gender, height_cm, weight)

def main():
    user = get_user_input()
    record = BMIRecord(1, user)

    print(f"\n{user.name}'s BMI: {record.bmiValue:.2f}")
    print(f"BMI Status: {record.getBMIStatus()}")

if __name__ == "__main__":
    main()
