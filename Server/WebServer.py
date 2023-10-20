from flask import Flask, request, render_template
from Classifier import classifyItem, calculateCal
from MQTT import connectMQTT
import os
import threading
# Create the Flask object
app = Flask(__name__)

image_dir = "Picture"
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".ico"]


@app.route('/', methods = ['GET'])
def root():
    return 'CS3237 Sample Site', 200

# Examples of how to render a template. Also note
# how we use requests.args.get to extract GET parameters
@app.route('/index', methods = ['GET'])
def index():
    """ Demo routine to show how to pass parameters through GET """

    # Extract GET parameters from request object
    name = request.args.get('name')

    if name is None:
        name = 'Bob Jones'

    return render_template('index.html', info = {"title":"Hello World", "name":name}), 200

@app.route('/classify')
def identify():
    try:
        # check if image have been received and saved
        files = os.listdir(image_dir)
        image_found = False
        image_file = ""
        for file in files:
            if os.path.isfile(os.path.join(image_dir, file)):
                file_extension = os.path.splitext(file)[1].lower()  # Get the file extension in lowercase
                if file_extension in image_extensions:
                    image_found = True
                    image_file = os.path.join(image_dir, file)
                    break
        if image_found:
            item = classifyItem(image_file)
            calories = calculateCal(image_file, item)
            return render_template('index.html', info = {"title":"Item: ", "name":str(item)+" "+calories}), 200
        else:
            return render_template('index.html', info = {"title":"No item found", "name":" no item found"}), 200
        
    except Exception as e:
        return render_template('index.html', info = {"title":"No item found ", "name":e}), 200

def main():
    global client, db, col, app
    thread = threading.Thread(target=connectMQTT)
    thread.start()
    app.run(port = 3237)

if __name__ == '__main__':
    main()

