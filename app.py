from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data (in-memory storage)
pets = [
    {"id": 1, "name": "Bella", "type": "Dog", "age": 3},
    {"id": 2, "name": "Milo", "type": "Cat", "age": 2},
]

# Routes
@app.route("/")
def index():
    return render_template("index.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":
        new_pet = {
            "id": len(pets) + 1,
            "name": request.form["name"],
            "type": request.form["type"],
            "age": int(request.form["age"]),
        }
        pets.append(new_pet)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = next((p for p in pets if p["id"] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if request.method == "POST":
        pet["name"] = request.form["name"]
        pet["type"] = request.form["type"]
        pet["age"] = int(request.form["age"])
        return redirect(url_for("index"))

    return render_template("edit.html", pet=pet)

@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    global pets
    pets = [p for p in pets if p["id"] != pet_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("Starting Flask app...") 
    app.run(debug=True)
