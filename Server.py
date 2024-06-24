from flask import Flask, request,redirect,url_for, render_template, send_from_directory
from flask_cors import CORS
from IDM import generate_html_tree, parse_xml
from werkzeug.utils import secure_filename
import os
from Extractor import Extract_Selected_Tags
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

file_path=["C:/Users\HHR6\PycharmProjects\TASK4-IDM\PINO_IDM_2024 (1).xml"]
@app.route('/')
def index():
    return (render_template('index.html'))

@app.route('/save_paths', methods=['POST'])
def save_paths():


    data = request.json
    paths = data['paths']
    with open('selected_paths.txt', 'w') as file:
        pass  # Do nothing, just open and close the file to truncate it

    # Now you can write new data to the file
    with open('selected_paths.txt', 'w') as f:
        for path in paths:
            f.write(path + '\n')

    print("saved the paths")
    print(file_path[-1])
    df= Extract_Selected_Tags(file_path[-1], "./selected_paths.txt")
    df.to_excel("./output.xlsx")
    html = df.to_html()

    with open('./templates/output.html', 'w') as file:
        pass  # Do nothing, just open and close the file to truncate it
    text_file = open("./templates/output.html", "w", encoding="utf-8")
    output_html = """<!DOCTYPE html>
<html>
<head>
    <title>Output Page</title>
</head>
<body>
    <h1>Data Output</h1>
    <div id="button-container">
        {{ button_html | safe }}
    </div>
    <div id="data-frame">
        {{ data_frame_html | safe }}
    </div>
    
</body>
</html>
"""
    text_file.write(output_html)

    # write html to file
    button_html = """
           <form action="http://127.0.0.1:5000/download" method="get">
               <button type="submit">Download</button>
           </form>"""
    text_file = open("./templates/output.html", "w",encoding="utf-8")
    text_file.write(render_template('output.html', data_frame_html=html, button_html=button_html))
    text_file.close()
    return redirect(url_for("new_route"))



@app.route('/results')
def new_route():
    # Render the desired template or perform some action for the new route
    return render_template("output.html")

@app.route('/download')
def new_routes():
    # Render the desired template or perform some action for the new route
    return send_from_directory("./","output.xlsx", as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure 'uploads' directory exists
    upload_folder = './uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.xml'):
        filename = secure_filename(file.filename)
        saved_path = os.path.join(upload_folder, filename)
        file.save(saved_path)

        # Process the XML file
        xml_root = parse_xml(saved_path)
        html_tree = generate_html_tree(xml_root)

        # Save the parsed HTML output
        with open('./templates/parsed.html', 'w', encoding="utf-8") as f:
            f.write(html_tree)

        return render_template("parsed.html")
    else:
        return "Invalid file type", 400


if __name__ == '__main__':
    app.run(debug=True,port=5000)