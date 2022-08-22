# This is importing the Flask library and other libraries that we need to build our web application.
from flask import Flask, render_template, json, request
import requests 

app = Flask(__name__)

# Making a request to the API and getting the data.

#url = 'https://pataa.in:5052/gt-usr-cnt-st'              ## testing 
url = "https://adminapiv1.pataa.com/gt-pc-cnt-st"         ## Production   
payload = json.dumps({"type": "1", "country_id": "4"})
response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=payload, verify=False)
count_data = response.json()
count_data = count_data['result']

for j in count_data:
    if (j['state_id']) == 157:
        j['state_name'] = 'Andaman & Nicobar Island'
    elif (j['state_id']) == 53:
        j['state_name'] = 'Arunanchal Pradesh'
    elif (j['state_id']) == 33:
        j['state_name'] = 'Dadara & Nagar Havelli'
    elif (j['state_id']) == 165:
        j['state_name'] = 'Daman & Diu'
    elif (j['state_id']) == 128:
        j['state_name'] = 'Jammu & Kashmir'
    elif (j['state_id']) == 69:
        j['state_name'] = 'NCT of Delhi'



"""
    It renders the index1.html file.
    :return: the index1.html file.
"""
@app.route("/", methods=["GET"])
def hello():
    return render_template("index1.html")


"""
    It takes a state name as input, and returns the number of counties in that state
    :return: The count of the state name.
"""
@app.route('/state', methods=['POST'])
def state():
    if request.method == 'POST':
        d = request.get_json()  # parse as JSON
        fi = d['state_name']
        for i in count_data:
            if i['state_name'] == fi:
                c = i['count']
        return c,200


"""
    It takes a JSON object from the client, extracts the state name and district name from it, then uses
    those values to query a database and return the count of the district
    :return: The value of c is being returned.
"""
@app.route('/dis', methods=['POST'])
def dis():
    if request.method == 'POST':
        d = request.get_json()  # parse as JSON
        sn = d['state_name']
        dn = d['district']
        print("//////////////////////////")
        print(dn)    
        for i in count_data:
            if i['state_name'] == sn:
                sid = i['state_id']
                print(sid)
                url = "https://pataa.in:5052/gt-pc-cnt-dst"
                payload = json.dumps({"type": "1", "country_id": "4" , "state_id" : sid})
                response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=payload, verify=False)
                result = response.json()
                result = result['result']
                c = ""
                for i in result:
                    if i['district_name'] == dn:
                        c = i['count']

                print(c)
        
        return c , 200


"""
    It takes a state name and a city name as input, and returns the number of people in that city
    :return: The count of the city.
"""
@app.route('/city', methods=['POST'])
def city_count():
    if request.method == 'POST':
        d = request.get_json()  # parse as JSON
        sn = d['state_name']
        cn = d['city']

        for i in count_data:
            if i['state_name'] == sn:
                sid = i['state_id']
                print(sid)
                
                url = "https://adminapiv1.pataa.com/gt-pc-cnt-st"  ## production api
                response = requests.request("POST", url, headers={'Content-Type': 'application/json'},
                           data=json.dumps({"type": "1", "country_id": "4", "state_id": sid}), verify=False)

                r = response.json()
                a = r['result']
                c = ""
                for i in a:
                    if i['city_name'] == cn:
                        c = i['count']
                if(c == ""):
                    c = "No Data Found"
        return c,200



# This is a special Python construct that allows the file to be run directly by the Python
# interpreter, e.g. python app.py. It only runs if the module is executed as the main script, e.g.
# python app.py, and not if it is imported by another module, e.g. import app.
if __name__ == "__main__":
    app.run(port=4000,debug=True)
