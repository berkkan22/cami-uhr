import pandas as pd
from enum import Enum
import json


class TurkishMonth(Enum):
    # Enum for Turkish months
    Ocak = 1
    Şubat = 2
    Mart = 3
    Nisan = 4
    Mayıs = 5
    Haziran = 6
    Temmuz = 7
    Ağustos = 8
    Eylül = 9
    Ekim = 10
    Kasım = 11
    Aralık = 12


# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'namaz.xlsx'

# Read the Excel file
df = pd.read_excel(file_path)

# Remove the header
df.columns = range(df.shape[1])

"""
format of json

{
    "2024-01-01": {
        "imsak": "time",
        "gunes": "time",
        "oglen": "time",
        "ikindi": "time",
        "aksam": "time",
        "yatsi": "time",
    },
    ...
}
"""
time_json = {}

"""
format of json

{
    "2024-01-01": {
        "day": 19,
        "month": "Cemaziyelahir",
        "year": 1445
    },
...
}
"""
date_json = {}

for i in range(2, len(df)):
    el = df.iloc[i]
    array = []
    for value in el:
        if pd.isna(value):
            print("Error: Nan value found")
            print(el)
            print(value)
            exit(1)

        array.append(value)

    for month in TurkishMonth:
        if month.name in array[0]:
            value = array[0].split(" ")
            day = value[0].zfill(2)
            month_num = str(month.value).zfill(2)
            date = f"{value[2]}-{month_num}-{day}"
            break

    hijri_date = array[1].split(" ")

    date_json[date] = {
        "day": hijri_date[0],
        "month": hijri_date[1],
        "year": hijri_date[2]
    }

    time_json[date] = {
        "Imsak": f"{date}T{array[2]}:00",
        "Güneş": f"{date}T{array[3]}:00",
        "Öğle": f"{date}T{array[4]}:00",
        "İkindi": f"{date}T{array[5]}:00",
        "Akşam": f"{date}T{array[6]}:00",
        "Yatsı": f"{date}T{array[7]}:00",
    }

with open('time_data.json', 'w', encoding='utf-8') as time_file:
    json.dump(time_json, time_file, ensure_ascii=False, indent=4)

with open('date_data.json', 'w', encoding='utf-8') as date_file:
    json.dump(date_json, date_file, ensure_ascii=False, indent=4)
