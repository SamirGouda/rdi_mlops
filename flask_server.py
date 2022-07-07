import torch
from torchvision import transforms
from flask import Flask, request, jsonify
from PIL import Image
import torch.nn.functional as F
import os

img_transforms = transforms.Compose([
                                transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                                ])
model_path = 'model/model.ts'

# create flask instance
app = Flask(__name__)
model = None

def load_model():
    global model
    # model variable refers to the global variable
    model = torch.jit.load(model_path)

def preprocess_image(image):
    try:
        with open(image, 'rb') as fd:
            img = Image.open(fd)
            img = img.convert('RGB')
    except TypeError:
        img = Image.open(image)
        img = img.convert('RGB')
    return img_transforms(img)

def feedforward(batch):
    with torch.no_grad():
        # runs globally loaded model on the data
        model.eval()
        pred = model(batch)
        probabilities = F.softmax(pred, dim=-1).squeeze()
    out = {'COVID19': probabilities[0].item(), 'NORMAL': probabilities[1].item()}
    return out

@app.route('/')
def home_endpoint():
    return 'Hello Tester!'

@app.route("/alive", methods=["GET"])
def alive_view():
    """
    This function is attached to the /alive route.

    Returns
    ========
        flask.wrappers.Response
            A json response contains a message key:
                {"message": "alive"}

    """
    return jsonify({"message": "alive"})

# We expect a form submission (HTTP POST) at the “/predict” endpoint
@app.route('/predict', methods=['POST'])
def get_prediction():
    # Works only for a single sample
    if request.method == 'POST':
        # Our request will have one file called img
        # image = json.load(request.data)
        data = {**request.files, **request.form}
        image = data['image']
        batch = preprocess_image(image).unsqueeze(0)  # converts shape from (c, w, h) to (1, c, w, h)
        out = feedforward(batch)
    # Encodes our response content as JSON
    return jsonify(out), 200

if __name__ == "__main__":
    load_model()  # load model at the beginning once only
    app.run(debug=False, #int(os.getenv("FLASK_DEBUG", 0)) == 1,
            host='0.0.0.0', port=8000,
            threaded=True)
