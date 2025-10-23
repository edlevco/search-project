## Binary Sorting Algorithm


## Array that will be searched
arr = [1, 6, 8, 10, 14, 17, 22, 23, 24, 25, 29, 30, 32, 34]

def find_index(array, target):
    left = 0 ## left pointer
    right = len(array) - 1 ## right pointer 

    while left <= right: ## While the left pointer is less or equal to the right pointer
        ## each loop find the new middle pos
        mid = left + (right - left) // 2

        if array[mid] == target:
            return mid ## return index of target
        elif array[mid] < target:
            left = mid + 1  ## move the left pointer to the right of the middle
        else:
            right = mid - 1 ## move the right pointer to the left of the middle

    return -1  # Not found


# --- Handle user input ---
try:
    user_input = input("Enter a number to search for: ").strip()

    # Check if input is empty
    if user_input == "":
        print("You must enter a number.")
    else:
        target = int(user_input)
        result = find_index(arr, target)

        if result != -1:
            print(f"{target} at index {result} of the array.")
        else:
            print(f"{target} is not in the array.")

except ValueError:
    print("Invalid input. Please enter an integer.")


