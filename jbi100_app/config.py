# Here you can add any global configuations
import pandas as pd

column_options_1 = ["None", "Incident.year", "Provoked/unprovoked"]
column_options_heatmap = ["Shark.common.name", "Shark.scientific.name", "Injury.category", "Victim.injury", "State", "Site.category", 
                          "Provoked/unprovoked", "Victim.activity", "Injury.severity"]
column_options_barchart = ["Shark.common.name", "Shark.scientific.name", "Injury.category", "Victim.injury", "State", "Site.category", 
                          "Provoked/unprovoked", "Victim.activity", "Injury.severity", "Number_of_fatal_incidents"]

AU_CITIES = pd.DataFrame({
    'City': [
        'Sydney',
        'Melbourne',
        'Brisbane',
        'Perth',
        'Adelaide',
        'Canberra',
        'Hobart',
        'Darwin'
    ],
    'Latitude': [
        -33.8688,
        -37.8136,
        -27.4698,
        -31.9505,
        -34.9285,
        -35.2809,
        -42.8821,
        -12.4634
    ],
    'Longitude': [
        151.2093,
        144.9631,
        153.0251,
        115.8605,
        138.6007,
        149.1300,
        147.3272,
        130.8456
    ]
})