from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Configure MongoDB URI
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Routes
@app.route("/")
def index():
    pets = mongo.db.pets.find()
    return render_template("index.html", pets=pets)


@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":
        new_pet = {
            "name": request.form["name"],
            "type": request.form["type"],
            "age": int(request.form["age"]),
        }
        mongo.db.pets.insert_one(new_pet)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<string:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = mongo.db.pets.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        return "Pet not found", 404

    if request.method == "POST":
        updated_pet = {
            "name": request.form["name"],
            "type": request.form["type"],
            "age": int(request.form["age"]),
        }
        mongo.db.pets.update_one({"_id": ObjectId(pet_id)}, {"$set": updated_pet})
        return redirect(url_for("index"))

    return render_template("edit.html", pet=pet)

@app.route("/delete/<string:pet_id>",  methods=["POST"])
def delete_pet(pet_id):
    mongo.db.pets.delete_one({"_id": ObjectId(pet_id)})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
