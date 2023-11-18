import requests
import json
import aiogram
import BusClass
with open("db.json", "r") as db:
    ras = json.load(db)
bus = BusClass.Bus(ras, 'Tomsk', 'Novosobornaya', 'left_side', '32lsk')
bus.print_table()