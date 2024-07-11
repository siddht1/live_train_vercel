import re
import ujson
def get_information_train_route(html_string,trainNo=None, date=None, station=None):
    match = re.search(r'var data = (\{.*?\});', html_string, re.DOTALL)  
    if match:  
        json_str = match.group(1).strip()  # This is the entire matched string  
        json_obj = ujson.loads(json_str)  # Load string to json object using ujson  
  
    # with open(f"route_{trainNo}_{date}.json", 'w', encoding='utf-8') as jsn_w:  
    #     ujson.dump(json_obj, jsn_w,indent=4) 
    return(json_obj)