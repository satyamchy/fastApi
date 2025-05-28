from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(...,  gt = 0, lt = 120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(...,gt = 0,  description='height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt = 0,  description='weight of the patient in kgs')]
    

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi      

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data  = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f) 
       

@app.get('/')
def hello():
    return {'messgae': 'Patient Management System Api'}

@app.get('/about')
def about():
    return {'message': ' A fully functional api to manage patients records'}
  
@app.get('/view')
def view_data():
    return load_data()

# path params
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404,  detail =  ' patient not found')

# query params
@app.get('/sort')  # sort?sort_by=height&order=desc
def sort_patients(sort_by: str = Query(..., description= 'Sort on the basis of height, weight or bmi'), order: str = Query('asc', description ='sort in asc or desc order' )):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in  valid_fields:
        raise HTTPException(status_code = 400, detail=f'Invalid field select form {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail='INvalid order select between asc and desc')
    
    data = load_data()
    sort_order = True if order == 'desc' else  False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse = sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()
    print(patient)
    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude = ['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code = 201, content={'message': 'patient created successfully'})










# python -m venv myenv
#  myenv\Scripts\activate 
#  pip install fastapi pydantic uvicorn
#  uvicorn main:app  --reload 