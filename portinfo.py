#!/usr/bin/python3
import requests
import sys
import random
from bs4 import BeautifulSoup

#a functon that checks that a valid argument was provided (port number)
def checkarg(arg):
    #a help text to display if argument is not valid
    helptxt = """Usage: portinfo [PORT_NUMBER]
Fetches network port information from SANS Internet Storm Center.
A valid port number in the range of 1 and 65535 number must be provided as argument.."""
    
    #checks that only 1 argument is provided (argument 1 is the name of the script, 2 is the port number) 
    if len(arg) ==2:

        port = str(arg[1])
        #check is argunment string contains digits
        if str.isdigit(port):
            #checks if the portnumber is within a valid range
            if int(port) in range(1,65535):
                return port

    #prints helptext and returns false if argument is invalid
    print(helptxt)
    return False
    
def fetchwebpage(port):
#a function that fetches port information ics.sans.edu
    #URL to lookup port information
    url = "https://isc.sans.edu/port.html?port="
    
    #faking header som we are not blocked
    headers = randomHeader()
    #fetcing webpage
    res = requests.get(url + port,headers=headers)
    
    #checking the status code, only continue if a page was returned
    if res.status_code == 200:

        #making the html more structured 
        soup = BeautifulSoup(res.text, "html.parser")
        #fetching table class "threadList" containing port info
        table_element = soup.find("table", class_="threadList")
        #fetching all rows in the table
        td_element = table_element.find_all('td')
        if len(td_element)>0: 
            return td_element
        else: 
            return False
    else:
        return False

def fetchportinfo(td_element):
        #checks any values was found
        if len(td_element)>0: 
            counter = 0
            row = []
            #loops throuh results
            for item in td_element:
                #print(item) 
                counter+=1
                #table on page has 3 rows
                if counter <=3:
                    output = item.get_text()
                    row.append(output.strip())
                    if counter == 3: 
                        #prints rows as we have them
                        yield row
                        #Removes content from row to fetch next row. 
                        row =[]
                        counter = 0;
        #else: 
            #returns false if no rows was found
        #    return False
    #else:
        #returns false if no we were unable to fetch information from isc.sans.edu
    #    return False

#a function that picks a random header
def randomHeader():
    headers =[
        #Firefox 82 Mac
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
            'Accept-Encoding': 'identity', 
            'Accept-Language': 'en-US,en;q=0.5', 
            'Dnt': '1', 
            'Host': 'isc.sans.edu',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1',
            'Usaer-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:82.0) Gecko/20100101 Firefox/82.0',
            'X-Amzn-Trace-Id': 'Root=1-5fac6727-6fe31dd620d457511f8f2ac8'
        },
        #Firefox 82 Windows
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Dnt': '1', 'Host': 'isc.sans.edu', 
            'Referer': 'https://www.google.com/', 
            'Upgrade-Insecure-Requests': '1', 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0', 
            'X-Amzn-Trace-Id': 'Root=1-5fac6727-6d02163a69ed4e8934bf2662'
        },

        #Chrome 86 Mac
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Dnt': '1',
            'Host': 'isc.sans.edu',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
            'X-Amzn-Trace-Id': 'Root=1-5fac6728-1d917774256a595f37667999'
        },
        #Chrome 86 Windows
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'isc.sans.edu',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
            'X-Amzn-Trace-Id': 'Root=1-5fac6728-01598a3e18492ae403adbdc5'
        }
    ]

    return random.choice(headers)

def main(): 
    #fetching port number provided as argument
    port = sys.argv
    
    #checking that a valid port number was provided as argument
    port = checkarg(port)
    
    #moves on only if argument was valid
    if port: 
        #fetcing <td>-elements containing port information from isc.sans.edu
        td_element = fetchwebpage(port) 
        #returning an error message to the users if no we could not reach the page or no information was found
        if not td_element: 
            print("Error: Could not fetch port information from SANS Internet Storm Center!")
        else: 
            #fetcing content of table from html
            portinfo = fetchportinfo(td_element)
            #printig a table heading with correct space
            print ("{:<10} {:<20} {:<20}".format('Protocol','Service','Name'))
        
            #printing port information 
            for line in portinfo: 
                print ("{:<10} {:<20} {:<20}".format(line[0],line[1],line[2]))
    

#calling main function
if __name__ == "__main__":
        main()
