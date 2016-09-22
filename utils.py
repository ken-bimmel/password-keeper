import logging

from google.appengine.ext import ndb

from models import AccountInfo, MyObjectClassName


# TODO: Implement




# Potentially helpful (or not) NDB Snippets - For reference only
def get_parent_key_for_email(email):
    """ Gets the parent key (the key that is the parent to all Datastore data for this user) from the user's email. """
    return ndb.Key("Entity", email.lower())

 
def get_account_info_for_email(email, create_if_none=False):
    """ Gets the one and only AccountInfo object for this email. Returns None if AccountInfo object doesn't exist. """
    email = email.lower()  # Just in case.
    parent_key = get_parent_key_for_email(email)
    account_info = AccountInfo.get_by_id(email, parent=parent_key)
    
    if create_if_none and not account_info:
        parent_key = get_parent_key_for_email(email)
        logging.info("Creating a new AccountInfo for user " + email)
        account_info = AccountInfo(parent=parent_key, id=email)
        account_info.put()
  
    return account_info
 
 
def get_query_for_all_OBJECTS_for_email(email):
    """ Returns a query for all OBJECTS for this user. """
    parent_key = get_parent_key_for_email(email)
    return MyObjectClassName.query(ancestor=parent_key).order(MyObjectClassName.someProperty)
 
 
def get_query_for_OBJECTS_for_FIELD(somePropertyValue):
    """ Returns a query for all OBJECTS the FIELD is in. """
    return MyObjectClassName.query(MyObjectClassName.someProperty == somePropertyValue)
 
 
def get_complex_query_example1(email, someFieldValue):
    """ Shows an example of modifying an existing query and the ndb.AND syntax (ndb.OR is just as easy). """
    query = get_query_for_all_OBJECTS_for_email(email)
    return query.filter(ndb.AND(MyObjectClassName.boolean == False, MyObjectClassName.someNumericfieldName >= someFieldValue))
 
 
def get_complex_query_example2(email, someFieldValue):
    """ Example of a complex query, shows looking for a value within a repeated field.  A bit ugly. """
    parent_key = get_parent_key_for_email(email)
    return MyObjectClassName.query(ancestor=parent_key).order(MyObjectClassName.someProperty, MyObjectClassName.key).filter(MyObjectClassName.repeatedField.IN([someFieldValue]))
  
