import re    
import ujson 
def get_information_current_station(html_string,trainNo=None, date=None, station=None):
    current_station={}
    data_match = re.search(r'var data = (\{.*?\});', html_string, re.DOTALL)  
    current_stn_code_match = re.search(r'var currentStnCode = ["\'](.*?)["\'];', html_string)  
    current_stn_name_match = re.search(r'var currentStnName = ["\'](.*?)["\'];', html_string)  
    json_obj = None  
    current_stn_code = None  
    current_stn_name = None  
    if data_match:  
        json_str = data_match.group(1).strip()  # This is the entire matched string  
        json_obj = ujson.loads(json_str)  # Load string to json object using ujson  
  
    if current_stn_code_match:  
        current_stn_code = current_stn_code_match.group(1).strip()  
  
    if current_stn_name_match:  
        current_stn_name = current_stn_name_match.group(1).strip()  

    # print(f"currentStnCode: {current_stn_code}")  
    # print(f"currentStnName: {current_stn_name}")  
    current_station['current station code']=current_stn_code
    current_station['current station name']=current_stn_name

    match = re.search(r'Last Updated:([^,]*)', html_string)  
    if match:  
        updated_at=match.group(1).replace('', '')  
        updated_at=updated_at.replace('&nbsp;','') 
        current_station['updated at']= updated_at
    
    # with open(f"station_{trainNo}_{date}.json", 'w', encoding='utf-8') as jsn_w:  
    #     ujson.dump(current_station,jsn_w,indent=4)
    return(current_station)     
