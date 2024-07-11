import os  


LIVE_TRAIN_BASE_URL= 'https://www.confirmtkt.com/train-running-status'

def url_builder(trainNo, date=None, station=None):  
    if not trainNo.isdigit() or len(trainNo) != 5:  
        raise ValueError("Invalid train number. Train number must be a 5-digit number.")  
    url = f"{LIVE_TRAIN_BASE_URL}/{trainNo}"  
    if date:  
        url += f"?Date={date}"  
    if station:  
        url += f"&StationName={station}"  
  
    return url