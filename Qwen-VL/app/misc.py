from fastapi import Request
from datetime import datetime
import uuid

def print_ascii_logo(flush: bool):
    print(""" _____         _             _____     _ _             
|   __|_ _ ___| |_ ___ _____|   __|___|_| |_ _ ___ ___ 
|__   | | |_ -|  _| -_|     |   __| .'| | | | |  _| -_|
|_____|_  |___|_| |___|_|_|_|__|  |__,|_|_|___|_| |___|
      |___|                                            """, flush=True)


hackaton = {
    "citizen's passport": "personal_passport",
    "driver license": "driver_license",
    "certificat d'immatriculation": "vehicle_certificate",
    "vehicle passport": "vehicle_passport"
}