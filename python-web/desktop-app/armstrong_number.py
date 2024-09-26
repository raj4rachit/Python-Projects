def armstrongNumber(number):
    if not isinstance(number, int) or number < 100 or number > 999:
        return "Enter Number is not a valid 3 digit number"

    digit1 = number // 100
    digit2 = (number // 10) % 10
    digit3 = number % 10

    sum_of_cubes = (digit1 ** 3) + (digit2 ** 3) + (digit3 ** 3)

    if sum_of_cubes == number:
        return "Yes"
    else:
        return "No"


# Example usage
input_number = int(input("Enter a 3-digit number: "))
result = armstrongNumber(input_number)
print(result)
