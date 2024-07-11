import ujson        
from bs4 import BeautifulSoup      
def get_information_live(html_string, trainNo=None, date=None, station=None):      
    soup = BeautifulSoup(html_string, 'html.parser')      
    station_divs = soup.find_all('div', class_='row rs__station-row flexy')
    information_live=[]     
    for div in station_divs: 
        station_name = has_passed = day = date = arrival = departure = delay = None  

        station_live={}     
        # print('_____________________________')  
        get_day_date = div.find_all('div', class_='col-xs-3')    
        if get_day_date:  
            info_div = get_day_date[0]  
            has_passed = info_div.find('svg') is not None  
            # print(f'Has Passed: {has_passed}')  
  
            # Get the station name from the first div      
            station_span = info_div.find('span')      
            if station_span is not None:  # Check if the span exists      
                station_name = station_span.text.strip()      
                # print(f"Station Name: {station_name}")      
  
            # Get the day and date from the second div      
            if len(get_day_date) > 1:      
                spans = get_day_date[1].find_all('span')      
                if len(spans) > 1:  # Check if there are at least 2 spans      
                    day = spans[0].text.strip()      
                    date = spans[1].text.strip()      
                    # print(f"Day: {day}")      
                    # print(f"Date: {date}")     
  
        # Get the time details from the divs with class 'col-xs-2'    
        time_span_2 = div.find_all('div', class_='col-xs-2')    
        if len(time_span_2) > 2:  # Check if there are at least 3 divs      
            arrival = time_span_2[0].find('span').text.strip()      
            departure = time_span_2[1].find('span').text.strip()      
            delay = time_span_2[2].text.strip()      
            # print(f"Arrival: {arrival}")    
            # print(f"Departure: {departure}")    
            # print(f"Delay: {delay}")
        station_live['Station']=station_name
        station_live['Has passed']=has_passed
        station_live['Day']=day
        station_live['Date']=date
        station_live['Arrival']=arrival
        station_live['Departure']=departure
        station_live['Delay']=delay
        information_live.append(station_live)          
     
    # with open(f"live_{trainNo}_{date}.json", 'w', encoding='utf-8') as jsn_w:  
    #     ujson.dump(information_live,jsn_w,indent=4)
    return(information_live)    