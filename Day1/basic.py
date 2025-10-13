def greet_user():
    name = input("Enter the name: ")
    age = int(input("Enter the age: "))
    print(f"Hello {name}, you are {age} years old!\n")


def Square_number():
    num = int(input("Enter the number: "))
    Square = num ** 2
    print(f"Square of {num} is: {Square}\n")


def reverse_text():
    text = input("Enter the text: ")
    reversed_text = text[::-1]
    print("Reversed text:", reversed_text)

    if text.lower() == reversed_text.lower():
        print(f"{text} is a palindrome\n")
    else:
        print(f"{text} is not a palindrome\n")


def cube_num():
    num = int(input("Enter the number: "))
    cube = num ** 3
    print(f"Cube of {num} is: {cube}\n")
    
def even_odd():
    num = int(input("enter the number"))
    if num % 2 == 0:
        print("number is even")
    else:
        print("number is odd")


def show_menu():
    print("----- Python Operations ------")
    print("1. Greet User")
    print("2. Square Number")
    print("3. Reverse Text / Palindrome Check")
    print("4. Cube Number")
    print("5. Even odd number")
    print("6.Exit")


def main():
    print("Welcome to Python Core Practice!\n")
    while True:
        show_menu()
        choice = input("Enter your choice (1 to 6):")

        if choice == "1":
            greet_user()
        elif choice == "2":
            Square_number()
        elif choice == "3":
            reverse_text()
        elif choice == "4":
            cube_num()
        elif choice == "5":
            even_odd()
        elif choice == "6":
            print("Thank you for practicing Python!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.\n")


if __name__ == "__main__":
    main()
