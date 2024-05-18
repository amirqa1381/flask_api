
from flask import make_response, abort

from config import db
from models import Person, people_schema, person_schema



def read_all():
    """
    This function is for returning the list of the all people in the database 
    and it's for retrinving the data in the get request 
    """
    people = Person.query.all()
    return people_schema.dump(people)


def create(person):
    """
    this function is for creating the instance of the people and here this function is for handling 
    the post http method and it get the fname and lname of the person and add it to the people 
    so this function is for posting and won't work in the get or update
    Args:
        person (_type_): person object
    """
    lname = person.get('lname')
    exisiting_person = Person.query.filter(Person.lname == lname).one_or_none()
    
    if exisiting_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"The person with lname {lname} is already exists.")
        


def read_one(lname):
    """
    this function is for retrinving single person and show it in api 
    so here this function is for the get request and handling the http get request 

    Args:
        lname (string): this arg is for retriving the person
    """
    person = Person.query.filter(Person.lname == lname).one_or_none()
    
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404 , f"The lname {lname} that you provided is not correct.")




def update(lname, person):
    """
    This function is for updating and rewrite the person and it's for 
    handling the put http method and when user want to update it's name or lastname
    can use put method for updating the pereson info
    Args:
        lname (string): it's used for retriving the person
        person (_type_): _description_
    """
    exsiting_person = Person.query.filter(Person.lname == lname).one_or_none()
    
    if exsiting_person is not None:
        updated_person = person_schema.load(person, session=db.session)
        exsiting_person.fname = updated_person.fname
        db.session.merge(exsiting_person)
        db.session.commit()
        return person_schema.dump(exsiting_person), 201
    else:
        abort(404, f"Person with last name {lname} not found.")        
    

def delete(lname):
    """
    this function is for deleting a person from our database and it's for handling the http delete request 
    and if a person should be removed we can use it .
    Args:
        lname (string): the arg that we get for retriving the object
    """
    exsiting_person = Person.query.filter(Person.lname == lname).one_or_none()
    
    if exsiting_person:
        db.session.delete(exsiting_person)
        db.session.commit()
        return make_response(f"The {lname} was successfully deleted.", 200)
    else:
        abort(404, f"The last name {lname} that you provided is successully deleted.")