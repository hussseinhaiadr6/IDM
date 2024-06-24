import xml.etree.ElementTree as ET

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def xml_to_html(element, path=""):
    current_path = f"{path}/{element.tag}"
    if len(element) > 0:
        html = f'<li class="tree-node"><span class="expand-arrow">▶</span> <input type="checkbox" class="node-checkbox" value="{current_path}"> {element.tag}: {element.text}'
    else:
        html = f'<li class="tree-node"> <input type="checkbox" class="node-checkbox" value="{current_path}"> {element.tag}: {element.text}'
    if element.attrib:
        html += ' <div class="attributes">Attributes:'
        for attr, value in element.attrib.items():
            attr_path = f"{current_path}-{attr}-]"
            html += f' <label><input type="checkbox" class="attribute-checkbox" value="{attr_path}"> {attr}="{value}"</label>'
        html += '</div>'

    if len(element) > 0:
        html += '<ul class="nested">'
        for child in element:
            html += xml_to_html(child, current_path)
        html += '</ul>'

    html += '</li>'
    return html


def generate_html_tree(xml_root):
    html_content = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                
               
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
                font-size: 24px;
                color: #333;
            }
            ul {
                padding: 20px;
                width: 95%;
                
            }
            .tree-node, .tree-leaf {
                list-style-type: none;
                margin: 5px 0;
                padding: 5px;
                border: 1px solid #ddd;
                background-color: #fff;
                border-radius: 5px;
            }
            .tree-leaf{
            padding-left: 30px;
            }
            .tree-node {
                cursor: pointer;
            }
            .tree-leaf:hover {
                background-color: #e6e6e6;
            }
            .expand-arrow {
                cursor: pointer;
                display: inline-block;
                width: 20px;
                font-size: 14px;
                transform: rotate(0deg);
                transition: transform 0.2s;
            }
            .expanded > .expand-arrow {
                transform: rotate(90deg);
            }
            .attributes {
                font-style: italic;
                color: gray;
            }
            .nested {
                display: none;
                padding-left: 20px;
            }
            .active {
                display: block;
            }
            #extractButton {
                display: block;
                margin: 20px 0;
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            #extractButton:hover {
                background-color: #0056b3;
            }
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                document.querySelectorAll('.expand-arrow').forEach(arrow => {
                    arrow.addEventListener('click', (event) => {
                        event.stopPropagation();
                        let parentNode = arrow.parentElement;
                        let childUl = parentNode.querySelector('.nested');
                        if (childUl) {
                            childUl.classList.toggle('active');
                            parentNode.classList.toggle('expanded');
                        }
                    });
                });

                document.getElementById('extractButton').addEventListener('click', () => {
                    let selectedCheckboxes = document.querySelectorAll('.node-checkbox:checked, .attribute-checkbox:checked');
                    let selectedPaths = Array.from(selectedCheckboxes).map(checkbox => checkbox.value);
                    if (selectedPaths.length > 0) {
                        console.log('Selected Paths:', selectedPaths);
                        // Save selected paths to a text file
                        fetch('http://localhost:5000//save_paths', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ paths: selectedPaths })
                        }).then(response => {
            if (response.ok) {
                // Redirect to new_route
                window.location.href = 'http://localhost:5000/results';
            } else {
                return response.text().then(text => { throw new Error(text) });
            }
        })
                          .catch(error => console.error('Error:', error));
                    } else {
                        alert('No tags selected.');
                    }
                });
            });
        </script>
    </head>
    <body>
        <h1>IDM Explorer</h1>
        <ul>
    """
    html_content += xml_to_html(xml_root)
    html_content += """
        </ul>
        <button id="extractButton">Extract Selected Tags</button>
    </body>
    </html>
    """
    return html_content

