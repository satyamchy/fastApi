from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data   = json.load(f)

    return data
    

@app.get('/')
def hello():
    return {'messgae': 'Patient Management System Api'}

@app.get('/about')
def about():
    return {'message': ' A fully functional api to manage patients records'}

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException{ status_code = 404,  detail =  ' patient not found'}






# python -m venv myenv
#  myenv\Scripts\activate 
#  pip install fastapi pydantic uvicorn
#  uvicorn main:app  --reload 