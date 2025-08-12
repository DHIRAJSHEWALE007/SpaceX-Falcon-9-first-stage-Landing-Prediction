from fastapi.responses import Response

import uvicorn
import os

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from SpaceXF9LandingPred.pipeline.prediction import PredictionPipeline
import pandas as pd

app = FastAPI()


templates = Jinja2Templates(directory="templates")

ORBIT_OPTIONS = ['LEO', 'ISS', 'PO', 'GTO', 'ES-L1', 'SSO', 'HEO', 'MEO', 'VLEO', 'SO', 'GEO']
LAUNCH_SITES = ['CCAFS SLC 40', 'VAFB SLC 4E', 'KSC LC 39A']
LANDING_PADS = ['nan', '5e9e3032383ecb761634e7cb', '5e9e3032383ecb6bb234e7ca', 
                '5e9e3032383ecb267a34e7c7', '5e9e3033383ecbb9e534e7cc',
                '5e9e3032383ecb554034e7c9']
SERIALS = ['B0003', 'B0005', 'B0007', 'B1003', 'B1004', 'B1005', 'B1006',
           'B1007', 'B1008', 'B1011', 'B1010', 'B1012', 'B1013', 'B1015',
           'B1016', 'B1018', 'B1019', 'B1017', 'B1020', 'B1021', 'B1022',
           'B1023', 'B1025', 'B1026', 'B1028', 'B1029', 'B1031', 'B1030',
           'B1032', 'B1034', 'B1035', 'B1036', 'B1037', 'B1039', 'B1038',
           'B1040', 'B1041', 'B1042', 'B1043', 'B1044', 'B1045', 'B1046',
           'B1047', 'B1048', 'B1049', 'B1050', 'B1054', 'B1051', 'B1056',
           'B1059', 'B1058', 'B1060', 'B1062']

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request,
        "orbits": ORBIT_OPTIONS,
        "launch_sites": LAUNCH_SITES,
        "landing_pads": LANDING_PADS,
        "serials": SERIALS
    })

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training Successful !!")
    
    except Exception as e:
        return Response(f"Error Occured! {e}")
    
@app.post("/inference")
async def predict_route(X):
    try:
        pipe =  PredictionPipeline()
        prediction = pipe.predict(X)[0]
        return prediction
    
    except Exception as e:
        raise e


@app.post("/predict/", response_class=HTMLResponse)
async def predict(
    request: Request,
    FlightNumber: int = Form(...),
    PayloadMass: float = Form(...),
    Orbit: str = Form(...),
    LaunchSite: str = Form(...),
    Flights: int = Form(...),
    GridFins: str = Form(...),
    Reused: str = Form(...),
    Legs: str = Form(...),
    LandingPad: str = Form(...),
    Block: int = Form(...),
    ReusedCount: int = Form(...),
    Serial: str = Form(...)):

    # Convert str to bool
    GridFins = GridFins == "True"
    Reused = Reused == "True"
    Legs = Legs == "True"

    input_df = pd.DataFrame([{
        "FlightNumber": FlightNumber,
        "PayloadMass": PayloadMass,
        "Orbit": Orbit,
        "LaunchSite": LaunchSite,
        "Flights": Flights,
        "GridFins": GridFins,
        "Reused": Reused,
        "Legs": Legs,
        "LandingPad": LandingPad,
        "Block": Block,
        "ReusedCount": ReusedCount,
        "Serial": Serial
    }])

    pipeline = PredictionPipeline()
    prediction = pipeline.predict(input_df)[0]

    return templates.TemplateResponse("form.html", {
        "request": request,
        "prediction": prediction,
        "orbits": ORBIT_OPTIONS,
        "launch_sites": LAUNCH_SITES,
        "landing_pads": LANDING_PADS,
        "serials": SERIALS
    })

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)