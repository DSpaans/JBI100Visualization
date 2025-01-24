# Here you can add any global configuations

column_options_1 = ["None", "Incident.year", "Provoked/unprovoked"]
column_options_heatmap = ["Shark.common.name", "Shark.scientific.name", "Injury.category", "Victim.injury", "State", "Site.category", 
                          "Provoked/unprovoked", "Victim.activity", "Injury.severity", "Month"]
column_options_barchart = ["Shark.common.name", "Shark.scientific.name", "Injury.category", "Victim.injury", "State", "Site.category", 
                          "Provoked/unprovoked", "Victim.activity", "Injury.severity", "Number_of_fatal_incidents", "Month"]

#Converts an integer to a month name
def int_to_month(int):
    if int == 1:
        return "January"
    elif int == 2:
        return "February"
    elif int == 3:
        return "March"
    elif int == 4:
        return "April"
    elif int == 5:
        return "May"
    elif int == 6:
        return "June"
    elif int == 7:
        return "July"
    elif int == 8:
        return "August"
    elif int == 9:
        return "September"
    elif int == 10:
        return "October"
    elif int == 11:
        return "November"
    elif int == 12:
        return "December"
    else:
        return "Unknown"