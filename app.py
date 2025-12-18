# app.py
from flask import Flask, render_template, request, jsonify
from backend import (
    calculate_nim_sum,
    computer_move,
    is_game_over,
    initialize_game
)

app = Flask(__name__)

game = {
    "piles": [],
    "turn": "player"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    game["piles"] = initialize_game(data["mode"], int(data["k"]))
    game["turn"] = "player"
    return jsonify({
        "piles": game["piles"],
        "turn": game["turn"],
        "nim_sum": calculate_nim_sum(game["piles"])
    })

@app.route("/player_move", methods=["POST"])
def player_move():
    data = request.json
    i, take = data["pile"], data["remove"]
    game["piles"][i] -= take

    if is_game_over(game["piles"]):
        return jsonify({"winner": "player", "piles": game["piles"]})

    game["turn"] = "computer"
    return jsonify({"piles": game["piles"], "turn": game["turn"]})

@app.route("/computer_move", methods=["POST"])
def comp_move():
    piles, msg = computer_move(game["piles"])

    if is_game_over(piles):
        return jsonify({"winner": "computer", "piles": piles, "message": msg})

    game["turn"] = "player"
    return jsonify({
        "piles": piles,
        "turn": game["turn"],
        "message": msg,
        "nim_sum": calculate_nim_sum(piles)
    })

if __name__ == "__main__":
    app.run(debug=True)
