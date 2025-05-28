from fastapi import FastAPI, Path, HTTPException, Query
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
    raise HTTPException(status_code = 404,  detail =  ' patient not found')

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




# python -m venv myenv
#  myenv\Scripts\activate 
#  pip install fastapi pydantic uvicorn
#  uvicorn main:app  --reload 