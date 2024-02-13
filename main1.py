import xml.etree.ElementTree as ET

def convert_xml_to_txt(xml_file, txt_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open the .txt file for writing
    with open(txt_file, 'w') as file:
        # Iterate over the XML elements
        for element in root.iter():
            # Write the element tag and text to the .txt file
            file.write(f"{element.tag}: {element.text}\n")

# Example usage
xml_file = 'resource/example_input.xml'
txt_file = 'data.txt'
convert_xml_to_txt(xml_file, txt_file)