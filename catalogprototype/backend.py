#read file


def get_catalog_data():
    return [line.strip() for line in data]

def read_items():
    with open("catalog.csv", "r") as file:
        data = []
        for line in file:
            id, name, description = line.strip().split(",", 2)
            data.append({
                "id": id,
                "name": name,
                "description": description
            })
    return data

def save_items(items):
    with open("catalog.csv", "w") as file:
        for item in items:
            line = f"{item['id']},{item['name']},{item['description']}\n"
            file.write(line)


def validate_item(name, description):
    return bool(name.strip()) and bool(description.strip())