import uvicorn  # ASGI
from fastapi import FastAPI
from Model import WaterQuality
import pickle

# 2. Create the app object
app = FastAPI()
pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'This is a Water Quality Tester'}


@app.post('/predict')
def predict_banknote(data: WaterQuality):
    data = data.dict()
    ph = data['ph']
    Hardness = data['Hardness']
    Solids = data['Solids']
    Chloramines = data['Chloramines']
    Sulfate = data['Sulfate']
    Conductivity = data['Conductivity']
    Organic_carbon = data['Organic_carbon']
    Trihalomethanes = data['Trihalomethanes']
    Turbidity = data['Turbidity']
    prediction = classifier.predict(
        [[ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]])
    if prediction[0] < 1:
        prediction = "Not Drinkable Water"
    else:
        prediction = "Drinkable Water"
    return {
        'prediction': prediction
    }


# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
