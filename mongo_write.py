import datetime

from pymongo import MongoClient
import pprint
import io
from PIL import Image
from PIL import ImageDraw

# Setup mongo connection
client = MongoClient("mongodb://utadmin:ee382v@zlotnik.mynetgear.com:27017")

# Databases on the server and tables in the database,
# can all be accessed using either the <element>.<subelement>
# OR element["subelement"] syntax


# EXAMPLE 1
db = client.testdb
my_collection = db.post
# for record in my_collection.find():
#    print(record["_id"])


# EXAMPLE 2
db = client["testdb"]
post_collection = db["post"]
# for record in  post_collection.find():
#    print(record["_id"])


# Creating a collection for users
user_collection = db["users"]

#
# Adding Data to the users table
#
# Data is created in JSON style dictionaries
user = {
    "name": "test_user123",
    "bio": "This is a bio string for a happy test user",
    "activation_date": datetime.datetime.utcnow()
}
user_insert = db.users.insert_one(user)# returns a mongo "ID" object
user_id = user_insert.inserted_id

# converting the image to a binary, which cn be stored in mongo
image_file = open("images/car0.png", "rb")
image_binary = image_file.read()

# Adding data to the post table
post = {
    "user_id": user_id,
    "image": image_binary,
    "comment": "I, the test user, saw and liked this car",
    "category": "Luxury"
}
post_insert = post_collection.insert_one(post)
post_id = post_insert.inserted_id

# Select the post we just inserted
selected_post = post_collection.find_one({"_id": post_id})

read_image_bytes = selected_post["image"]

image_file = open("images/car0.png", "rb")
image_binary = image_file.read()
stream = io.BytesIO(read_image_bytes)

img = Image.open(stream)
img.show()

# Deleting the records (documents) we created
user_collection.delete_one({"_id":user_id})
post_collection.delete_one({"_id":post_id})
