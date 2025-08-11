import requests
import pandas as pd
import numpy as np
import datetime

from SpaceXF9LandingPred.logging import logger

from SpaceXF9LandingPred.entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config=config

    def getBoosterVersion(self,data):
        for x in data['rocket']:
            if x:
                response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
                self.BoosterVersion.append(response['name'])

    def getLaunchSite(self,data):
        for x in data['launchpad']:
            if x:
                response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
                self.Longitude.append(response['longitude'])
                self.Latitude.append(response['latitude'])
                self.LaunchSite.append(response['name'])

    def getPayloadData(self,data):
        for load in data['payloads']:
            if load:
                response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
                self.PayloadMass.append(response['mass_kg'])
                self.Orbit.append(response['orbit'])


    def getCoreData(self,data):
        for core in data['cores']:
                if core['core'] != None:
                    response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                    self.Block.append(response['block'])
                    self.ReusedCount.append(response['reuse_count'])
                    self.Serial.append(response['serial'])
                else:
                    self.Block.append(None)
                    self.ReusedCount.append(None)
                    self.Serial.append(None)
                self.Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
                self.Flights.append(core['flight'])
                self.GridFins.append(core['gridfins'])
                self.Reused.append(core['reused'])
                self.Legs.append(core['legs'])
                self.LandingPad.append(core['landpad'])
   

    def fetch_data(self):
        response=requests.get(self.config.data_url)

        data = pd.json_normalize(response.json())
        
        data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

        data = data[data['cores'].map(len)==1]
        data = data[data['payloads'].map(len)==1]

        data['cores'] = data['cores'].map(lambda x : x[0])
        data['payloads'] = data['payloads'].map(lambda x : x[0])

        data['date'] = pd.to_datetime(data['date_utc']).dt.date

        data = data[data['date'] <= datetime.date(2025, 7, 7)]

        self.BoosterVersion = []
        self.PayloadMass = []
        self.Orbit = []
        self.LaunchSite = []
        self.Outcome = []
        self.Flights = []
        self.GridFins = []
        self.Reused = []
        self.Legs = []
        self.LandingPad = []
        self.Block = []
        self.ReusedCount = []
        self.Serial = []
        self.Longitude = []
        self.Latitude = []

        self.getBoosterVersion(data)
        logger.info("Booster Version fetched Successfully")
        self.getLaunchSite(data)
        logger.info("Launch Sites fetched Successfully")
        self.getPayloadData(data)
        logger.info("Payload Data Fetched Successfully")
        self.getCoreData(data)
        logger.info("Core Data fetched Successfully")

        launch_dict = {'FlightNumber': list(data['flight_number']),
        'Date': list(data['date']),
        'BoosterVersion':self.BoosterVersion,
        'PayloadMass':self.PayloadMass,
        'Orbit':self.Orbit,
        'LaunchSite':self.LaunchSite,
        'Outcome':self.Outcome,
        'Flights':self.Flights,
        'GridFins':self.GridFins,
        'Reused':self.Reused,
        'Legs':self.Legs,
        'LandingPad':self.LandingPad,
        'Block':self.Block,
        'ReusedCount':self.ReusedCount,
        'Serial':self.Serial,
        'Longitude': self.Longitude,
        'Latitude': self.Latitude}

        data_falcon= pd.DataFrame(launch_dict)

        data_falcon9 = data_falcon[data_falcon["BoosterVersion"] != "Falcon 1"]

        data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))

        logger.info(f"Total {len(data_falcon9)} records extracted from the API")

        data_falcon9.to_csv(self.config.data_path, index=False)
        logger.info("Data file has been created in artifacts")