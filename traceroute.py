# this will allow this program to interpret JSON object. See example JSON:http://dazzlepod.com/ip/128.173.239.242.json
import json

# the tools needed to access a URL and get data.
import urllib.request

# allows operations such opening a default browser at a given URL
import webbrowser, os

# for pausing our requests to a web service that takes IP and returns latitude,longitude
import time

# scapy is an extensive networking library for python. We are going to be using its 'traceroute()'
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute

# this is to plot our lat/long data onto Google Maps  https://pypi.org/project/gmplot/
from gmplot import gmplot   

# adding for arguments
import sys 
import requests



diff_colors = ['blue','red', 'green', 'yellow', 'orange', 'pink', 'indigo', 'violet', 'white', 'cyan']


# creating arrays to hold coordinates
lat = []
long = []


# plots 3 coordinates onto Google Maps - hardcoded for in-class example
def plot_lat_long():
   
    # the initial lat long and the zoom levels for the map (3 is zoomed out)
    gmap = gmplot.GoogleMapPlotter(42.0167, 23.1000, 3)
    
    #Handle path issue for windows, so that marker images can optionally be found using gmplot
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"        
    
    # placing large dots on the lat longs
    # for your homework you will pass in coordinates retrieved from dazzlepod. 
    # for this in-class example, we will plot a hard-coded list of coordinates
    
    
    for i in range(len(lat)):
        
        # creating markers for each unique location and indexing through colors aray properly
        gmap.marker(lat[i], long[i],diff_colors[i % len(diff_colors)], title = str(i))
       
    
    gmap.plot(lat, long,'blue', 300)
    # get the currentdirectory
    cwd = os.getcwd()
    
    # saving the map as an HTML into the project directory
    gmap.draw("traceroute.html")
    
    # opening the HTML via default browser
    webbrowser.open("file:///" + cwd +"/traceroute.html")
    
  
# find the latitude and longitude 
def find_and_plot_coordinates():
    
    # plotting coordinates of each ip address
    for item in ips:
    
        # tool for finding latitutde and longitude of ip address
        url = "http://dazzlepod.com/ip/{}.json".format(item)
    
        # debugging the URLs
        print(url)
        
        response = requests.get(url)
        data = response.json()
        print(data)
        # making sure the wesbsite gave us lat and long
        if 'latitude' in data and 'longitude' in data:
            
            if (data['latitude'] not in lat) and (data['longitude'] not in long):
                lat.append( data['latitude'])
                long.append(data['longitude'])                
        
        # pausing for 2 seconds to make sure we don't get banned by 'dazzlepod.com'
        time.sleep(SLEEP_SECONDS)
            
    # filling array of labels with int 1 - amount of coordinates
    
    #calls function to plot the lats and longs
    
    print(lat,long)
    plot_lat_long()
    




#will need to slow down the request frequency from 'dazzlepod.com' to find latitude and longitude
SLEEP_SECONDS = 2;
#hostname to traceroute to, hardcoded for in-class example


if (len(sys.argv) != 0):
    hostname = sys.argv[1]
    print(hostname)
else:
    print("no valid argument")
# converting request hostname into IP address
print(hostname)
ip = socket.gethostbyname(hostname)
print(ip)

# a good explanation of how traceroute works: https://www.youtube.com/watch?v=G05y9UKT69s
# add maxttl=100 or more if you want to traceroute even deeper.
#'res' -- results from traceroute 
res, _ = traceroute(ip,maxttl=64,verbose = 0)

# will store retrieved IPs here.
ips = []

# going through the traceroute results and extracting IP addresses into the array
for item in res.get_trace()[ip]:
    ips.append(res.get_trace()[ip][item][0])
    
#find coordinates and plot them   
find_and_plot_coordinates()


