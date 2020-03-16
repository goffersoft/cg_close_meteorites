import requests
import math

meteor_data_url = 'https://data.nasa.gov/resource/gh4g-9sfh.json'
my_location = {'reclat': 1.302880, 'reclong': 103.861572}

def get_data(url):
    resp = requests.get(url)
    if (resp.ok): return resp.json()
    raise ConnectionError

def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

   
def compute_distance(mdata):
    for m in mdata:
        if (not ('reclat' in m or 'reclong' in m)): continue
        m['distance'] = calc_dist(\
                          float(m['reclat']), float(m['reclong']),\
                          my_location['reclat'], \
                          my_location['reclong'])

def get_key(m):
    if 'distance' not in m: return math.inf   
    return m['distance']

def print_closest(mdata, max):
    for i in range(0,max):
        if ('distance' not in mdata[i]): continue
        print("name={0}, dist={1}".\
               format(mdata[i]['name'],\
                      mdata[i]['distance']))

def main_loop():
    meteor_data = get_data(meteor_data_url)
    compute_distance(meteor_data)
    meteor_data.sort(key=get_key)
    print_closest(meteor_data, 10)

main_loop()

    

