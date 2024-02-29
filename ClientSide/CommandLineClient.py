import requests
import json
import zipfile
import io

def get_image_path():
    return input("Please enter the location of the image you want to modify: ")

def get_operations():
    operations = []
    while True:
        print("\nHere are the available operations:")
        print("1: Rotate")
        print("2: Flip")
        print("3: Grayscale")
        print("4: Resize")
        print("5: Thumbnail")
        print("6: Rotate Left (90 degrees CCW)")
        print("7: Rotate Right (90 degrees CW)")
        print("8: Done with operations")
        operation_choice = input("Please select an operation (1-8): ")
        
        if operation_choice == '8':
            break
        else:
            operation = create_operation(operation_choice)
            if operation:
                operations.append(operation)
            more_operations = input("Do you want to add more operations? (yes/no): ").lower()
            if more_operations != 'yes':
                break
    return operations
            
    
def create_operation(choice):
    if choice == '1':
        degrees = input("Enter degrees to rotate (int only): ")
        return {"operation": "rotate", "degrees": degrees}
    elif choice == '2':
        direction = input("Enter flip direction (horizontal, vertical, both): ")
        return {"operation": "flip", "direction": direction}
    elif choice == '3':
        return {"operation": "grayscale"}
    elif choice == '4':
        percentage = input("Enter resize percentage (int only): ")
        return {"operation": "resize", "percentage": percentage}
    elif choice == '5':
        return {"operation": "thumbnail"}
    elif choice == '6':
        return {"operation": "rotateLeft"}
    elif choice == '7':
        return {"operation": "rotateRight"}
    else:
        print("Invalid operation selected.")
        return None


def confirm_and_process(image_path, operations):
    print(f"\nYou have chosen to apply the following operations to the image located at {image_path}:")
    for op in operations:
        print(f"- {op['operation']} with parameters: {op}")
    
    confirmation = input("\nDo you want to proceed with these operations? (yes/no): ").lower()
    
    if confirmation == 'yes':
        url = 'http://localhost:5000/process_image_sequence'
        operations_json = json.dumps(operations)
        
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            data = {'operations': operations_json}
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                zip_in_memory = io.BytesIO(response.content)
                with zipfile.ZipFile(zip_in_memory) as zf:
                    zf.extractall(path="./processed_images/")
                print("The processed images are saved in './processed_images/'.")
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
    else:
        print("Operation canceled.")

if __name__ == "__main__":
    image_path = get_image_path()
    operations = get_operations()
    confirm_and_process(image_path, operations)

    
    