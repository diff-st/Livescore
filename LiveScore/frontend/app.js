const ws = new WebSocket("ws://localhost:8888/ws");

const matchesDiv = document.getElementById("matches");
const eventsUl = document.getElementById("events");

const urlParams = new URLSearchParams(window.location.search);
const matchId = urlParams.get("id");

  // FETCH INIZIALE

if (matchesDiv) {
  fetch("/api/matches")
    .then(r => r.json())
    .then(renderMatches);
}

if (matchId) {
  fetch(`/api/matches/${matchId}`)
    .then(r => r.json())
    .then(renderMatchDetail);
}

  // WEBSOCKET

ws.onmessage = (msg) => {
  const data = JSON.parse(msg.data);

  if (data.type !== "match_update") return;

  if (matchesDiv) {
    updateMatchCard(data.data);
  }

  if (matchId && data.data._id === matchId) {
    updateMatchDetail(data.data);
  }
};


   // RENDER MATCH

function renderMatches(matches) {
  matchesDiv.innerHTML = "";
  matches.forEach(createMatchCard);
}

function createMatchCard(match) {
  const div = document.createElement("div");
  div.id = match._id;
  div.className = `match ${match.status}`;

  div.onclick = () => {
    window.location = `match.html?id=${match._id}`;
  };

  updateCardContent(div, match);
  matchesDiv.appendChild(div);
}

function updateMatchCard(match) {
  let div = document.getElementById(match._id);
  if (!div) {
    createMatchCard(match);
    return;
  }
  updateCardContent(div, match);
}

function updateCardContent(div, match) {
  div.className = `match ${match.status}`;
  div.innerHTML = `
    <div class="score">
      ${match.home_team} ${match.score.home}
      -
      ${match.score.away} ${match.away_team}
    </div>
    <div class="minute">
      ${match.status === "live" ? "🔴 LIVE" : ""}
      ⏱️ ${match.minute}'
    </div>
  `;
}

  // MATCH

function renderMatchDetail(data) {
  document.getElementById("title").innerText =
    `${data.match.home_team} vs ${data.match.away_team}`;

  updateMatchDetail(data.match);

  data.events.forEach(addEvent);
}

function updateMatchDetail(match) {
  document.getElementById("info").innerHTML = `
    <div class="score">
      ${match.home_team} ${match.score.home}
      -
      ${match.score.away} ${match.away_team}
    </div>
    <div>
      ${match.status === "live" ? "🔴 LIVE" : "⏹️ FINITO"} |
      ⏱️ ${match.minute}'
    </div>
  `;
}

function addEvent(event) {
  const li = document.createElement("li");
  li.className = "event";
  li.innerText = `${icon(event.type)} ${event.minute}' - ${event.description}`;
  eventsUl.appendChild(li);
}

function icon(type) {
  return {
    try: "🏉",
    penalty: "🎯",
    yellow: "🟨",
    red: "🟥"
  }[type] || "ℹ️";
}
