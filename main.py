"""3 STAGES
1) Get up-to-date data from API
2) Statistical calculations
3) Data visualisation
"""


import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt


# GOV.UK covid data API url:  https://api.coronavirus.data.gov.uk/v1/data

def data_request(url):
    # API request
    requested = requests.get(url).text
    # converting JSON to python dictionary
    pydata = json.loads(requested)
    # parsing python dictionary
    data_frame = pydata["data"]
    # open a csv file named "data_file" to write
    csv_data_file = open('data_file.csv', 'w')
    # creating the csv converted object
    csv_converted = csv.writer(csv_data_file)
    # counter used for writing headers

    count = 0
    for datas in data_frame:
        if count == 0:
            # Writing headers to CSV file
            header = datas.keys()
            csv_converted.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_converted.writerow(datas.values())

    csv_data_file.close()


API = "https://api.coronavirus.data.gov.uk/v1/data"
# API request function to create up-to-date data file
data_request(API)

# reading csv file and putting datas into a dataframe called data
data_f = pd.read_csv("data_file.csv")

# converting date columns type object to datetime
data_f["date"] = pd.to_datetime(data_f["date"])

# assigning date variable as an index, with this assignment we will be able to call data giving the date as an index
data_f.index = data_f["date"]



# creating multiple charts in one window to see the relevancy between each other
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,figsize=(20,8))


# title for graphs
fig.suptitle("new death(red), death rate (blue), total confirmed cases (green), total death(yellow)")


# assigning the x-axis,y-axis of each graph and defining the arguments of them
ax1.scatter(data_f.index, data_f["deathNew"], s=0.2, c="r")
ax2.plot(data_f.index, data_f["deathRate"], c="b")
ax3.plot(data_f.index, data_f["confirmed"], c="g")
ax4.plot(data_f.index, data_f["death"], c="y")


plt.show()

