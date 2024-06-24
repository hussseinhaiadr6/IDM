import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file

def Extract_Selected_Tags(IDM_path,Selected_path):
    tree = ET.parse(IDM_path)
    root = tree.getroot()

    file_path = Selected_path
    # Initialize an empty list to store the rows
    paths = []
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read each row in the file
        for row in file:
            # Strip newline characters from the row and add it to the list
            paths.append(row)

    Dict={}

    for path in paths:
        if "-"in path:
            name = path.split('-')[1]
            Dict[path] = "Attribte: " + name
        else:
            name=path.split('/')[-1]
            Dict[path]="Tag: " + name




    # Print the list to verify the result

    # Define paths


    # Initialize dictionary to store extracted data
    data = {path: [] for path in Dict.values()}

    # Iterate over each ITEM tag
    for item in root.findall(".//ITEM"):
        for path in paths:

            # Determine if the path is pointing to an element or an attribute
            if '-' in path:
                # It's an attribute

                element_path, attribute_name = path.rsplit('-', 2)[0], path.rsplit('-', 2)[1]
                parentPath=element_path[element_path.find("ITEMS/ITEM")+10:len(element_path)]
                if len(parentPath)>0:
                    elements = item.findall("./"+parentPath)

                    if elements is not None:
                        attribute_value=""
                        for element in elements:

                            if len(attribute_value)>0:
                                attribute_value += ", "+element.get(attribute_name)
                            else:
                                attribute_value += element.get(attribute_name)
                            print(attribute_value)
                        data[Dict[path]].append(attribute_value)
                    else:
                        attribute_value = None
                        data[Dict[path]].append("attribute_value")
                else:
                    attribute_value = item.get(attribute_name)

                    data[Dict[path]].append(attribute_value)
            else:
                # It's an element
                var=path[path.find("ITEMS/ITEM")+11:len(path)]
                elements = item.findall(str(var).strip())

                element_text=""
                for element in elements:

                    if element is not None:
                        if len(element_text)>0:
                            element_text +=", "+ element.text
                        else:
                            element_text +=element.text
                    else:
                        element_text += None
                data[Dict[path]].append(element_text)
    # Create a DataFrame

    df = pd.DataFrame(data)

    # Save to Excel file
    return df


