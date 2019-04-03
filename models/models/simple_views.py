#Helper method
#Convert rides queryset into dict & filters by depart time

#The param """""""is_after""""""""""""
# if it's 1, it means it's after this date
# date = 2020/20/02/10 & is_after = True then,
# It's gonna fetch all rides after 2020/20/02/10

def convertTime(date):
    date = date[11:]
    am_or_pm = 'am'
    time = int(date)
    if(time>12):
        time = time - 12
        am_or_pm = 'pm'
    return str(time)+am_or_pm

def convertToDate(date):
    day = date[8:11]
    month = date[5:7]
    year = date[:4]
    return str(day+month+'/'+year)

def convertRidesToDict(rides,driver_id = -1):
    rides_as_dict = []
    for ride in rides:
        passengers_ids = [user.id for user in model_to_dict(ride)['passengers']]
        seats_filled = len(passengers_ids)
        seats_left = ride.seats_offered - seats_filled
        
        rides_as_dict.append({
            'special_time_fmt': ride.depart_time,
            'ride_id': ride.id,
            'vehicle': ride.vehicle.id,
            'passengers': passengers_ids,
            'destination': ride.destination,
            'start': ride.start,
           'hr': convertTime(ride.depart_time),
            'date': convertToDate(ride.depart_time),
            'seats_offered':ride.seats_offered,
            'price':ride.price,
            'seats_left': seats_left,
            'seats_filled': seats_filled,
            'driver_id': driver_id,
        }) 
    return {"rides":rides_as_dict}

#returns true if time is greater or equal
# Format is YYYY-MM-DD as strings
def compareTime(old_time, new_time):
    old_time = old_time.split("-")
    new_time = new_time.split("-")

    for i in range(3):
        prev = int(old_time[i])
        new = int(new_time[i])

        if(prev > new):
            return False

        elif(prev < new):
            return True

        else:
            pass

    return True
