import argparse
import urllib
import urllib.request
import logging
import datetime


def downloadData(url):
    """Downloads the data"""

    """this is the URL we are going to use"""
    # url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'

    """Open the URL"""
    response = urllib.request.urlopen(url)

    """Read the response and convert it to string characters if it was in binary"""
    file_content = response.read().decode('utf-8')
    return file_content

def processData(file_content):
    logger = logging.getLogger("assignment2")
    data_list = file_content.split('\n')

    personData = {}
    linenum = 0
    """Read each line"""
    for line in data_list:
        linenum = linenum + 1
        """Split string by each element"""
        info = line.split(',')
        if len(info) <3:
            continue
        """Create dictionary with id as key and tuple of name and birthday as the value"""
        try:
            id = info[0]
            name = info[1]
            birthday = datetime.datetime.strptime(info[2], "%d/%m/%Y")
            data_tuple = (name, birthday)
            personData[id] = data_tuple
            """Log message for invalid date"""
        except:
            logging.error("Error processing line #" + str(linenum) + " for ID #" + str(id))

    return personData


def displayPerson(id, personData):
    id = str(id)
    """Print name and birthday of a given id"""
    if id in personData.keys():
        data_tuple = personData[id]
        name = data_tuple[0]
        birthdate = datetime.datetime.strftime(data_tuple[1], "%Y/%m/%d")
        print('Person # {} is {} with a birthday of {}'.format(id, name, birthdate))
        """if no user with id found, print message"""
    else:
        print("No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    try:
        file_content = downloadData(url)
        personData = processData(file_content)
        """Keep asking for input until input <=0"""
        while True:
            val = int(input("Enter ID to lookup: "))
            if val <1:
                break
            displayPerson(val, personData)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    logger = logging.getLogger("assignment2")
    logging.basicConfig(filename='errors.log', encoding= 'utf-8',level=logging.ERROR)
    main(args.url)