# David Gluckman
# CS 496 Section 400 Summer 2017
# Final Project - RESTful API Backend
# finalProject.py

import webapp2
import json
from google.appengine.ext import ndb
from google.net.proto.ProtocolBuffer import ProtocolBufferDecodeError

# Dog class based on Model
class Dog(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    breed = ndb.StringProperty()
    birthdate = ndb.StringProperty()
    adopted = ndb.BooleanProperty(required=True)
    fostered = ndb.BooleanProperty(required=True)
    foster_home = ndb.StringProperty()

# FosterHome class based on Model
class FosterHome(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    has_children = ndb.BooleanProperty(required=True)
    has_other_pets = ndb.BooleanProperty(required=True)

# Dog request handler
class DogHandler(webapp2.RequestHandler):
    # Add new Dog
    def post(self):
        # Get Dog JSON data
        dog_data = json.loads(self.request.body)
        
        # Check JSON data for wrong length
        if (len(dog_data) < 1 or len(dog_data) > 3):
            # If too few arguments
            if (len(dog_data) < 1):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not add Dog. Too few arguments.")
            # If too many arguments
            elif (len(dog_data) > 3):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not add Dog. Too many arguments.")
        # Else JSON is acceptable length
        else:
            # Attempt adding Dog
            try:
                # Create new Dog
                parent_key = ndb.Key(Dog, "parent_dog")
                newDog = Dog(name = dog_data['name'], parent = parent_key, adopted = False, fostered = False, foster_home = None)
                if (dog_data.has_key('breed')):
                    newDog.breed = dog_data['breed']
                if (dog_data.has_key('birthdate')):
                   newDog.birthdate = dog_data['birthdate']
                newDog.put()

                # Get ID and save to Dog
                newDog.id = str(newDog.key.urlsafe())
                newDog.put()

                # Return Dog info
                self.response.status = "201 created"
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(json.dumps({"name": newDog.name, "breed": newDog.breed, "birthdate": newDog.birthdate, "adopted": newDog.adopted, "fostered": newDog.fostered, "foster_home": newDog.foster_home, "id": newDog.id, "self": r"/dogs/" + newDog.id}))
            # If KeyError, bad arguments
            except KeyError:
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not add Dog. Incorrect arguments.")

    # Delete Dog
    def delete(self, id=None):
        # If an id was sent
        if (id):
            # Check that id is valid
            try:
                dogKey = ndb.Key(urlsafe=id)
            # If exception, display error
            except:
                self.response.status = "400 bad request"
                self.response.write("Error: Could not delete Dog. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Dog id
                if (dogKey.kind() == 'Dog'):
                    deleteDog = dogKey.get()
                    try:
                        # Delete Dog
                        dogKey.delete()
            
                        # Send response
                        self.response.status = "204 no content"
                        self.response.write("Dog successfully deleted.")
                    except AttributeError:
                        # Not a valid Boat ID
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not delete Dog. Not a valid Dog id.")
                else:
                    # Else not a valid Boat ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not delete Dog. Not a valid Dog id.")
        # Else no id was sent
        else:
            # Provide error message
            self.response.status = "400 bad request"
            self.response.write("Error: Could not delete Dog. No id provided.")

    # Modify Dog
    def patch(self, id=None):
        # If an id was sent
        if (id):
            # Check that id is valid
            try:
                dogKey = ndb.Key(urlsafe=id)
            except (TypeError, ProtocolBufferDecodeError, RuntimeError):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not modify Dog. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Dog id
                if (dogKey.kind() == 'Dog'):
                    # Get request body
                    modify_data = json.loads(self.request.body)
                    # Check for acceptable number of keys
                    if (len(modify_data) > 0 and len(modify_data) < 4):
                        # Modify Dog
                        try:
                            modifyDog = dogKey.get()
                            if (modify_data.has_key('name')):
                                modifyDog.name = modify_data['name']
                            if (modify_data.has_key('breed')):
                                modifyDog.breed = modify_data['breed']
                            if (modify_data.has_key('birthdate')):
                                modifyDog.birthdate = modify_data['birthdate']
                            modifyDog.put()
                        except KeyError:
                            self.response.status = "400 bad request"
                            self.response.write("Error: Could not modify Dog. Arguments required.")
                        else:
                            # Return Dog info
                            self.response.status = "200 ok"
                            self.response.headers['Content-Type'] = 'application/json'
                            self.response.write(json.dumps({"name": modifyDog.name, "breed": modifyDog.breed, "birthdate": modifyDog.birthdate, "adopted": modifyDog.adopted, "fostered": modifyDog.fostered, "foster_home": modifyDog.foster_home, "id": modifyDog.id, "self": r"/dogs/" + modifyDog.id}))
                    # If too few arguments
                    elif (len(modify_data) < 1):
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not modify Dog. Too few arguments.")
                    # If too many arguments
                    elif (len(modify_data) > 3):
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not modify Dog. Too many arguments.")
                else:
                    # Else not a valid Boat ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not modify Dog. Not a valid Dog id.")
        # Else no id was sent
        else:
            # Provide error message
            self.response.status = "400 bad request"
            self.response.write("Error: Could not modify Dog. No id provided.")
    
    # Adopt Dog
    def put(self, id=None):
        # If an id was sent
        if (id):
            # Check that id is valid
            try:
                dogKey = ndb.Key(urlsafe=id)
            except (TypeError, ProtocolBufferDecodeError):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not adopt Dog. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Dog id
                if (dogKey.kind() == 'Dog'):
                    adoptDog = dogKey.get()
                    # Check if fostered
                    if (adoptDog.fostered == True):
                        adoptDog.fostered = False
                        adoptDog.foster_home = None
                    # Set to adopted
                    adoptDog.adopted = True
                    adoptDog.put()
            
                    # Return Dog info
                    self.response.status = "200 ok"
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.write(json.dumps({"name": adoptDog.name, "breed": adoptDog.breed, "birthdate": adoptDog.birthdate, "adopted": adoptDog.adopted, "fostered": adoptDog.fostered, "foster_home": adoptDog.foster_home, "id": adoptDog.id, "self": r"/dogs/" + adoptDog.id}))
                else:
                    # Else not a valid Dog ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not adopt Dog. Not a valid Dog id.")
        # Else no id was sent
        else:
            # Provide error message
            self.response.status = "400 bad request"
            self.response.write("Error: Could not adopt Dog. No id provided.")

    # View a Dog or all Dogs
    def get(self, id=None):
        # If id was included
        if id:
            # Check that id is valid
            try:
                dogKey = ndb.Key(urlsafe=id)
            except (TypeError, ProtocolBufferDecodeError, RuntimeError):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not retrieve Dog. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Dog id
                if (dogKey.kind() == 'Dog'):
                    thisDog = dogKey.get()
                    # Try to access key/value
                    try:
                        thisName = thisDog.name
                        thisBreed = thisDog.breed
                        thisBirthdate = thisDog.birthdate
                        thisAdopted = thisDog.adopted
                        thisFostered = thisDog.fostered
                        thisFosterHome = thisDog.foster_home
                    except AttributeError:
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not retrieve Dog. Dog no longer exists.")
                    else:
                        # Return Dog info
                        self.response.headers['Content-Type'] = 'application/json'
                        self.response.write(json.dumps({"name": thisName, "breed": thisBreed, "birthdate": thisBirthdate, "adopted": thisAdopted, "fostered": thisFostered, "foster_home": thisFosterHome, "id": thisDog.id, "self": r"/dogs/" + thisDog.id}))
                else:
                    # Else not a valid Boat ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not retrieve Dog. Not a valid Dog id.")
        # Else no id included
        else:
            # Return all Dog info
            allDogs = [dog.to_dict() for dog in Dog.query()]
            # Add self key/value for each
            for dog in allDogs:
                dog['self'] = '/dogs/' + dog['id']
            # Send response
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(allDogs))


# Foster Home request handler
class FosterHomeHandler(webapp2.RequestHandler):
    # Add new Foster Home
    def post(self):
        # Get Foster Home JSON data
        foster_home_data = json.loads(self.request.body)
        # Check JSON data for wrong length
        if (len(foster_home_data) != 5):
            # If too few arguments
            if (len(foster_home_data) < 5):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not add Foster Home. Too few arguments.")
            # If too many arguments
            elif (len(foster_home_data) > 5):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not add Foster Home. Too many arguments.")
        # Else JSON is right length
        else:
            # Attempt adding Foster Home
            try:
                # Create new Foster Home
                parent_key = ndb.Key(FosterHome, "parent_foster_home")
                newFosterHome = FosterHome(name = foster_home_data['name'], parent = parent_key, address = foster_home_data['address'], phone = foster_home_data['phone'], has_children = foster_home_data['has_children'], has_other_pets = foster_home_data['has_other_pets'])
                newFosterHome.put()
                
                # Get ID and save to Foster Home
                newFosterHome.id = str(newFosterHome.key.urlsafe())
                newFosterHome.put()
                
                # Return Foster Home info
                self.response.status = "201 created"
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(json.dumps({"name": newFosterHome.name, "address": newFosterHome.address, "phone": newFosterHome.phone, "has_children": newFosterHome.has_children, "has_other_pets": newFosterHome.has_other_pets, "id": newFosterHome.id, "self": r"/foster_homes/" + newFosterHome.id}))
            # If KeyError, bad arguments
            except KeyError:
                self.response.status = "400 bad request"
                self.response.write("Error: Could not add Foster Home. Incorrect arguments.")

    # Delete Foster Home
    def delete(self, id=None):
        # If an id was sent
        if (id):
            # Check that id is valid
            try:
                fosterHomeKey = ndb.Key(urlsafe=id)
                # If exception, display error
            except (TypeError, ProtocolBufferDecodeError):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not delete Foster Home. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Foster Home id
                if (fosterHomeKey.kind() == 'FosterHome' and fosterHomeKey.get()):
                    # Check if any Dogs in this Foster Home
                    if (Dog.query(Dog.foster_home == id)):
                        # Set Dog to not fostered
                        self.response.write("A fostered animal needs to be updated.")
                    # Set Dog foster_home to None
                    
                    # Delete Foster Home
                    fosterHomeKey.delete()
                    
                    # Send response
                    self.response.status = "204 no content"
                    self.response.write("Foster Home successfully deleted.")
                else:
                    # Else not a valid Boat ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not delete Foster Home. Not a valid Foster Home id.")
        # Else no id was sent
        else:
            # Provide error message
            self.response.status = "400 bad request"
            self.response.write("Error: Could not delete Foster Home. No id provided.")

    # Modify Foster Home
    def patch(self, id=None):
        # If an id was sent
        if (id):
            # Check that id is valid
            try:
                fosterHomeKey = ndb.Key(urlsafe=id)
            except (TypeError, ProtocolBufferDecodeError, RuntimeError):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not modify Foster Home. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Foster Home id
                if (fosterHomeKey.kind() == 'FosterHome'):
                    # Get request body
                    modify_data = json.loads(self.request.body)
                    # Check for acceptable number of keys
                    if (len(modify_data) > 0 and len(modify_data) < 6):
                        # Modify Foster Home
                        try:
                            modifyFosterHome = fosterHomeKey.get()
                            if (modify_data.has_key('name')):
                                modifyFosterHome.name = modify_data['name']
                            if (modify_data.has_key('address')):
                                modifyFosterHome.address = modify_data['address']
                            if (modify_data.has_key('phone')):
                                modifyFosterHome.phone = modify_data['phone']
                            if (modify_data.has_key('has_children')):
                                modifyFosterHome.has_children = modify_data['has_children']
                            if (modify_data.has_key('has_other_pets')):
                                modifyFosterHome.has_other_pets = modify_data['has_other_pets']
                            modifyFosterHome.put()
                        except KeyError:
                            self.response.status = "400 bad request"
                            self.response.write("Error: Could not modify Foster Home. Arguments required.")
                        else:
                            # Return Foster Home info
                            self.response.status = "200 ok"
                            self.response.headers['Content-Type'] = 'application/json'
                            self.response.write(json.dumps({"name": modifyFosterHome.name, "address": modifyFosterHome.address, "phone": modifyFosterHome.phone, "has_children": modifyFosterHome.has_children, "has_other_pets": modifyFosterHome.has_other_pets, "id": modifyFosterHome.id, "self": r"/foster_homes/" + modifyFosterHome.id}))
                    # If too few arguments
                    elif (len(modify_data) < 1):
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not modify Foster Home. Too few arguments.")
                    # If too many arguments
                    elif (len(modify_data) > 5):
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not modify Foster Home. Too many arguments.")
                else:
                    # Else not a valid Foster Home ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not modify Foster Home. Not a valid Foster Home id.")
        # Else no id was sent
        else:
            # Provide error message
            self.response.status = "400 bad request"
            self.response.write("Error: Could not modify Foster Home. No id provided.")
    
    # View a Foster Home or all Foster Homes
    def get(self, id=None):
        # If id was included
        if id:
            # Check that id is valid
            try:
                fosterHomeKey = ndb.Key(urlsafe=id)
            except (TypeError, ProtocolBufferDecodeError):
                self.response.status = "400 bad request"
                self.response.write("Error: Could not retrieve Foster Home. Not a valid id.")
            # Else id is valid
            else:
                # Check that it is a Foster Home id
                if (fosterHomeKey.kind() == 'FosterHome'):
                    thisFosterHome = fosterHomeKey.get()
                    # Try to access key/value
                    try:
                        thisName = thisFosterHome.name
                        thisAddress = thisFosterHome.address
                        thisPhone = thisFosterHome.phone
                        thisHasChildren = thisFosterHome.has_children
                        thisHasOtherPets = thisFosterHome.has_other_pets
                        thisId = thisFosterHome.id
                    except AttributeError:
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not retrieve Foster Home. Foster Home no longer exists.")
                    else:
                        # Return Foster Home info
                        self.response.headers['Content-Type'] = 'application/json'
                        self.response.write(json.dumps({"name": thisName, "address": thisAddress, "phone": thisPhone, "has_children": thisHasChildren, "has_other_pets": thisHasOtherPets, "id": thisId, "self": r"/foster_homes/" + thisId}))
                else:
                    # Else not a valid Foster Home ID
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not retrieve Foster Home. Not a valid Foster Home id.")
        # Else no id included
        else:
            # Return all Foster Home info
            allFosterHomes = [foster_home.to_dict() for foster_home in FosterHome.query()]
            # Add self key/value for each
            for foster_home in allFosterHomes:
                foster_home['self'] = '/foster_homes/' + foster_home['id']
            # Send response
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(allFosterHomes))


# Dog-Foster Home interaction handler
class FosterStatusHandler(webapp2.RequestHandler):
    # Put Dog in Foster Home
    def put(self, id):
        # Check if Foster Home id is valid
        try:
            fosterHomeKey = ndb.Key(urlsafe=id)
        # If exception, display error
        except (TypeError, ProtocolBufferDecodeError):
            self.response.status = "400 bad request"
            self.response.write("Error: Could not place Foster Dog. Foster Home id not valid.")
        # Else id is valid
        else:
            # Check that it is a Foster Home id
            if (fosterHomeKey.kind() == 'FosterHome' and fosterHomeKey.get()):
                # Check arguments
                # Get request body
                dog_data = json.loads(self.request.body)
                # Check JSON data length
                if (len(dog_data) == 1):
                    # Attempt checking Dog id
                    try:
                        # Get Dog id
                        dogKey = ndb.Key(urlsafe=dog_data['foster_dog'])
                        thisDog = dogKey.get()
                        # Attempt placing Foster Dog
                        try:
                            thisDog.foster_home = r"/foster_homes/" + id
                            thisDog.fostered = True
                            thisDog.put()
                            # Return Dog info
                            self.response.status = "200 ok"
                            self.response.headers['Content-Type'] = 'application/json'
                            self.response.write(json.dumps({"name": thisDog.name, "breed": thisDog.breed, "birthdate": thisDog.birthdate, "adopted": thisDog.adopted, "fostered": thisDog.fostered, "foster_home": thisDog.foster_home, "id": thisDog.id, "self": r"/dogs/" + thisDog.id}))
                        # If TypeError, not a Dog
                        except (TypeError, AttributeError):
                            self.response.status = "400 bad request"
                            self.response.write("Error: Could not moor Boat. Boat id not valid.")
                    # If KeyError, bad arguments
                    except KeyError:
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not place Foster Dog. Incorrect arguments.")
                    except AttributeError:
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not place Foster Dog. Dog id not valid.")
                
                # Else if too few arguments
                elif (len(boat_data) < 1):
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not place Foster Dog. Too few arguments.")
                # Else if too many arguments
                elif (len(boat_data) > 1):
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not place Foster Dog. Too many arguments.")

            else:
                # Else not a valid Foster Home ID
                self.response.status = "400 bad request"
                self.response.write("Error: Could not place Foster Dog. Foster Home id not valid.")

    # Remove Dog from Foster Home
    def patch(self, id):
        # Check if Foster Home id is valid
        try:
            fosterHomeKey = ndb.Key(urlsafe=id)
        # If exception, display error
        except (TypeError, ProtocolBufferDecodeError):
            self.response.status = "400 bad request"
            self.response.write("Error: Could not remove Foster Dog. Foster Home id not valid.")
        # Else id is valid
        else:
            # Check that it is a Foster Home id
            if (fosterHomeKey.kind() == 'FosterHome' and fosterHomeKey.get()):
                # Get request body
                dog_data = json.loads(self.request.body)
                # Check JSON data length
                if (len(dog_data) == 1):
                    # Attempt checking Dog id
                    try:
                        # Get Dog id
                        dogKey = ndb.Key(urlsafe=dog_data['foster_dog'])
                        thisDog = dogKey.get()
                        # Check that Dog is in Foster Home
                        if (("/foster_homes/" + fosterHomeKey.get().id) == thisDog.foster_home):
                            
                            # Attempt removing Foster Dog
                            try:
                                thisDog.foster_home = None
                                thisDog.fostered = False
                                thisDog.put()
                                # Send response
                                self.response.status = "204 no content"
                            # If TypeError, not a Dog
                            except (TypeError, AttributeError):
                                self.response.status = "400 bad request"
                                self.response.write("Error: Could not remove Foster Dog. Dog id not valid.")
                        # Else Dog not in Foster Home
                        else:
                            self.response.status = "400 bad request"
                            self.response.write("Error: Could not remove Foster Dog. Dog not in specified Foster Home.")
                    # If KeyError, bad arguments
                    except KeyError:
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not place Foster Dog. Incorrect arguments.")
                    except AttributeError:
                        self.response.status = "400 bad request"
                        self.response.write("Error: Could not remove Foster Dog. Dog id not valid.")
                
                # Else if too few arguments
                elif (len(boat_data) < 1):
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not remove Foster Dog. Too few arguments.")
                # Else if too many arguments
                elif (len(boat_data) > 1):
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not remove Foster Dog. Too many arguments.")
            else:
                # Else not a valid Foster Home ID
                self.response.status = "400 bad request"
                self.response.write("Error: Could not place Foster Dog. Foster Home id not valid.")

    # View Dog(s) in Foster Home
    def get(self, id):
        # Check if Foster Home id is valid
        try:
            fosterHomeKey = ndb.Key(urlsafe=id)
        # If exception, display error
        except (TypeError, ProtocolBufferDecodeError):
            self.response.status = "400 bad request"
            self.response.write("Error: Could not retrieve Foster Dog(s). Foster Home id not valid.")
        # Else id is valid
        else:
            # Check that it is a Foster Home id
            if (fosterHomeKey.kind() == 'FosterHome' and fosterHomeKey.get()):
                # Check if any Dogs in Foster Home
                if (Dog.query(Dog.foster_home == id).get() != None):
                    query = Dog.query(Dog.foster_home == "/foster_homes/" + id)
                    fosterDogs = [dog.to_dict() for dog in query]
                    # Add self key/value for each
                    for dog in fosterDogs:
                        dog['self'] = '/dogs/' + dog['id']
                    # Send response
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.write(json.dumps(fosterDogs))
            
                # Else Foster Home not occupied
                else:
                    self.response.status = "400 bad request"
                    self.response.write("Error: Could not retrieve Foster Dog(s). Foster Home is empty.")
            else:
                # Else not a valid Foster Home ID
                self.response.status = "400 bad request"
                self.response.write("Error: Could not retrieve Foster Dog(s). Foster Home id not valid.")


# Main page handler
class NothingHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('This is a response about nothing.')

# Allow patch method
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# Create webapp2 app
app = webapp2.WSGIApplication([
                               ('/dogs/', DogHandler),
                               ('/dogs', DogHandler),
                               ('/dogs/(.*)/', DogHandler),
                               ('/dogs/(.*)', DogHandler),
                               ('/foster_homes/', FosterHomeHandler),
                               ('/foster_homes', FosterHomeHandler),
                               ('/foster_homes/(.*)/dog/', FosterStatusHandler),
                               ('/foster_homes/(.*)/dog', FosterStatusHandler),
                               ('/foster_homes/(.*)/', FosterHomeHandler),
                               ('/foster_homes/(.*)', FosterHomeHandler),
                               ('/', NothingHandler)
                               ])
