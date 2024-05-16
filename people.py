from datetime import datetime
from flask import abort, make_response



def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


PEOPLE = {
    "Fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "Ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "Bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    }
}

def read_all():
    """
    This function is for returning the list of the all people in the database 
    and it's for retrinving the data in the get request 
    """
    return list(PEOPLE.values())


def create(person):
    """
    this function is for creating the instance of the people and here this function is for handling 
    the post http method and it get the fname and lname of the person and add it to the people 
    so this function is for posting and won't work in the get or update
    Args:
        person (_type_): person object
    """
    fname = person.get("fname")
    lname = person.get("lname")
    if lname and lname not in PEOPLE:
        PEOPLE[lname] = {
            "fname" : fname,
            "lname" : lname,
            "timestamp" : get_timestamp()
        }
        return PEOPLE[lname], 201
    else:
        abort(406, f"this lanme {lname} is already exists.")



def read_one(lname):
    """
    this function is for retrinving single person and show it in api 
    so here this function is for the get request and handling the http get request 

    Args:
        lname (string): this arg is for retriving the person
    """
    if lname in PEOPLE:
        return PEOPLE[lname], 200
    else:
        abort(404, f"The lname {lname} is not provided.")


def update(lname, person):
    """
    This function is for updating and rewrite the person and it's for 
    handling the put http method and when user want to update it's name or lastname
    can use put method for updating the pereson info
    Args:
        lname (string): it's used for retriving the person
        person (_type_): _description_
    """
    if lname in PEOPLE:
        PEOPLE[lname]['fname'] = person.get('fname', PEOPLE[lname]['fname'])
        PEOPLE[lname]['lname'] = person.get("lname", PEOPLE[lname]['lname'])
        PEOPLE[lname]['timestamp'] = get_timestamp()
        return PEOPLE[lname], 200
    else:
        abort(404, f"the lname {lname} that you provided is not found.")
        
    

def delete(lname):
    """
    this function is for deleting a person from our database and it's for handling the http delete request 
    and if a person should be removed we can use it .
    Args:
        lname (string): the arg that we get for retriving the object
    """
    if lname in PEOPLE:
        PEOPLE.pop(lname)
        return make_response(f"The {lname} is successfully deleted", 200)
    else:
        abort(404, f"The lastname {lname} that you provided is not found!")