from flask import abort, make_response
from models import Note, note_schema, Person

from config import db


def read_one(note_id):
    """
    this function is for retriving the single note that we get the note_id as parameter
    Args:
        note_id (int): this is the id of the note
    """
    note = Note.query.get(note_id)
    if note is not None:
        return note_schema.dump(note), 200
    else:
        abort(404, f"the note_id {note_id} that you provided is not exists")



def update(note_id, note):
    """
    this function is for updating a note and we can retrive a note and 
    change some part of it and make changes on it
    Args:
        note_id (int): id of the note that we pass in the url parameter
        note (note object): note object that we have
    """
    exisiting_note = Note.query.get(note_id)
    if exisiting_note is not None:
        updated_note = note_schema.load(note, session=db.session)
        exisiting_note.content = updated_note.content
        db.session.merge(exisiting_note)
        db.session.commit()
        return note_schema.dump(exisiting_note), 201
    else:
        abort(404, f"The note_id {note_id} that you've provided is not exists!")
    
    
def delete(note_id):
    """
    this function is for retriving the note and deleting the note if exists , and if it does not have
    exists we should show an error message that we don't have any note that has id like you provided
    Args:
        note_id (int): id that we can use for retriving the note
    """
    note = Note.query.get(note_id)
    if note is not None:
        db.session.delete(note)
        db.session.commit()
        return make_response(f"Note id {note_id} was successfully deleted!", 204)
    else:
        abort(404, f"The note id {note_id} that you've provided is not exists!")
        
        


def create(note):
    """
    this function is for creating an exiciting note 
    Args:
        note (note object): note object that we want to create
    """
    person_id = note.get("person_id")
    person = Person.query.get(person_id)
    
    if person:
        new_note = note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(404, f"person id not found {person_id}")


    