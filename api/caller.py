from concurrent.futures import ThreadPoolExecutor  
import requests  
import ujson
import json  
import current_station  
import live_train  
import url_builder  
import train_route  
  
entire_list = {}  
  
def call_site(trainNo, date=None, station=None):    
    try:  
        response = requests.get(url_builder.url_builder(trainNo, date))    
        if response.status_code == 200:    
            # with open(f"{trainNo}_{date}.html", "w", encoding='utf-8') as fw:    
            #     fw.write(response.text)    
  
            with ThreadPoolExecutor(max_workers=3) as executor:  
                route_future = executor.submit(train_route.get_information_train_route, response.text, trainNo, date)  
                live_future = executor.submit(live_train.get_information_live, response.text, trainNo, date)  
                current_future = executor.submit(current_station.get_information_current_station, response.text, trainNo, date)  
                  
                entire_list['route'] = route_future.result()  
                entire_list['live status'] = live_future.result()  
                entire_list['current'] = current_future.result()  
  
            # with open(f"all_{trainNo}_{date}.json", 'w', encoding='utf-8') as jsn_w:    
            #     ujson.dump(entire_list, jsn_w, indent=4)

            print(json.dumps(entire_list, indent=4))  
            return(entire_list)
  
        else:    
            print(f"Error: Request failed with status code {response.status_code}")  
  
    except requests.exceptions.RequestException as e:    
        print(f"Request failed: {e}")  
