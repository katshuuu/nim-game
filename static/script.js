let piles = [];

async function startGame(mode) {
    const k = document.getElementById("k").value;

    const res = await fetch("/start", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mode, k})
    });

    const data = await res.json();
    piles = data.piles;
    updateTurn(data.turn);
    render(piles, data.nim_sum);
}

async function playerMove(i) {
    const take = parseInt(prompt("Сколько камней взять?"));
    if (!take) return;

    await fetch("/player_move", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({pile: i, remove: take})
    });

    updateTurn("computer");

    setTimeout(async () => {
        const res = await fetch("/computer_move", {method: "POST"});
        const data = await res.json();

        if (data.message)
            document.getElementById("message").innerText = data.message;

        piles = data.piles;
        updateTurn(data.turn);
        render(piles, data.nim_sum);

        if (data.winner)
            alert(`🏆 Победил: ${data.winner}`);
    }, 800);
}

function updateTurn(turn) {
    const el = document.getElementById("turn");
    el.textContent = turn === "player" ? "🧑 Ваш ход" : "🤖 Ход компьютера";
    el.className = turn;
}

function render(piles, nimSum) {
    document.getElementById("nim").innerHTML = `Ним-сумма: <b>${nimSum}</b>`;
    const board = document.getElementById("board");
    board.innerHTML = "";

    piles.forEach((count, i) => {
        const pile = document.createElement("div");
        pile.className = "pile";
        pile.innerHTML = `<h3>Кучка ${i + 1}</h3>`;

        const stones = document.createElement("div");
        stones.className = "stones";

        for (let s = 0; s < count; s++) {
            stones.appendChild(document.createElement("div")).className = "stone";
        }

        const btn = document.createElement("button");
        btn.textContent = "Ход";
        btn.onclick = () => playerMove(i);

        pile.append(stones, btn);
        board.appendChild(pile);
    });
}
