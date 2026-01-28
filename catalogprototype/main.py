from backend import read_items, save_items, validate_item

def show_items(items):
    print("\nCatalog Items:")
    for item in items:
        print(f"{item['id']}: {item['name']} - {item['description']}")

def add_item(items):
    name = input("Enter item name: ")
    description = input("Enter description: ")

    if not validate_item(name, description):
        print("Invalid input. Fields cannot be empty.")
        return

    new_id = str(len(items) + 1)
    items.append({
        "id": new_id,
        "name": name,
        "description": description
    })

    save_items(items)
    print("Item added successfully.")

def edit_item(items):
    item_id = input("Enter item ID to edit: ")

    for item in items:
        if item["id"] == item_id:
            name = input("New name: ")
            description = input("New description: ")

            if not validate_item(name, description):
                print("Invalid input.")
                return

            item["name"] = name
            item["description"] = description
            save_items(items)
            print("Item updated.")
            return

    print("Item not found.")

def main():
    items = read_items()

    while True:
        print("\n1. View items")
        print("2. Add item")
        print("3. Edit item")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_items(items)
        elif choice == "2":
            add_item(items)
            items = read_items()
        elif choice == "3":
            edit_item(items)
            items = read_items()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()