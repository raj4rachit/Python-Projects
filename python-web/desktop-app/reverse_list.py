class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

def reverseList(head):
    prev = None
    current = head

    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev

# Helper function to print linked list
def print_linked_list(head):
    current = head
    while current is not None:
        print(current.value, end=" -> ")
        current = current.next
    print("None")

# Taking input from the user to create the linked list
input_list = list(map(int, input("Enter elements of the linked list separated by spaces: ").split()))
head = None
prev_node = None

for val in input_list:
    new_node = ListNode(val)
    if head is None:
        head = new_node
    if prev_node is not None:
        prev_node.next = new_node
    prev_node = new_node

print("\nOriginal linked list:")
print_linked_list(head)

reversed_head = reverseList(head)

print("\nReversed linked list:")
print_linked_list(reversed_head)
