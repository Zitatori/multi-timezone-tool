import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="World Time Cards",
    page_icon="🌍",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #1e3a8a 0, transparent 28%),
                linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1200px; }
</style>
""", unsafe_allow_html=True)

APP_HTML = r"""
<div class="wtc-app">
  <section class="hero">
    <div>
      <p class="eyebrow">World Time Converter</p>
      <h1>Global Time Cards</h1>
      <p class="subtitle">Change one country’s date and time. All other countries update instantly.</p>
    </div>
    <div class="hero-badge">Live JS Sync</div>
  </section>

  <section class="control-panel">
    <div class="field">
      <label for="base-country">Base country</label>
      <select id="base-country"></select>
    </div>
    <div class="field">
      <label for="base-datetime">Date & time</label>
      <input id="base-datetime" type="datetime-local" />
    </div>
    <button id="now-btn" type="button">Use current time</button>
  </section>

  <section id="cards" class="cards"></section>
</div>

<style>
.wtc-app {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #e5e7eb;
}
.hero {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
  padding: 28px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 28px;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.72));
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(18px);
}
.eyebrow {
  margin: 0 0 8px;
  color: #93c5fd;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
h1 {
  margin: 0;
  font-size: clamp(36px, 6vw, 64px);
  line-height: 0.95;
  letter-spacing: -0.06em;
}
.subtitle {
  margin: 16px 0 0;
  color: #cbd5e1;
  font-size: 17px;
}
.hero-badge {
  flex: 0 0 auto;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(59, 130, 246, 0.16);
  color: #bfdbfe;
  border: 1px solid rgba(96, 165, 250, 0.35);
  font-weight: 700;
}
.control-panel {
  margin-top: 22px;
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 16px;
  padding: 18px;
  border-radius: 24px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.18);
}
.field label {
  display: block;
  margin-bottom: 8px;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 700;
}
select, input, button {
  width: 100%;
  box-sizing: border-box;
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  background: rgba(2, 6, 23, 0.8);
  color: #f8fafc;
  padding: 14px 15px;
  font-size: 15px;
  outline: none;
}
button {
  align-self: end;
  cursor: pointer;
  font-weight: 800;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border: none;
  box-shadow: 0 14px 30px rgba(37, 99, 235, 0.35);
}
.cards {
  margin-top: 22px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}
.card {
  position: relative;
  overflow: hidden;
  padding: 22px;
  border-radius: 26px;
  background: linear-gradient(160deg, rgba(30, 41, 59, 0.96), rgba(15, 23, 42, 0.86));
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 0 20px 54px rgba(0, 0, 0, 0.28);
}
.card::before {
  content: "";
  position: absolute;
  inset: -80px -60px auto auto;
  width: 180px;
  height: 180px;
  background: rgba(59, 130, 246, 0.18);
  border-radius: 999px;
}
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  position: relative;
}
.flag { font-size: 34px; }
.country { margin: 0; font-size: 22px; font-weight: 850; }
.city { margin-top: 4px; color: #94a3b8; font-size: 14px; }
.time {
  margin-top: 26px;
  font-size: 38px;
  font-weight: 900;
  letter-spacing: -0.04em;
}
.date {
  margin-top: 4px;
  color: #cbd5e1;
  font-size: 15px;
}
.offset {
  margin-top: 18px;
  display: inline-flex;
  padding: 8px 10px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.78);
  color: #93c5fd;
  font-size: 13px;
  font-weight: 800;
}
.active {
  border-color: rgba(96, 165, 250, 0.65);
  box-shadow: 0 0 0 1px rgba(96, 165, 250, 0.3), 0 22px 60px rgba(37, 99, 235, 0.22);
}
@media (max-width: 900px) {
  .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .control-panel { grid-template-columns: 1fr; }
  .hero { align-items: flex-start; flex-direction: column; }
}
@media (max-width: 620px) {
  .cards { grid-template-columns: 1fr; }
  .time { font-size: 34px; }
}
</style>

<script>
const countries = [
  { name: "Switzerland", city: "Zurich", flag: "🇨🇭", tz: "Europe/Zurich" },
  { name: "Japan", city: "Tokyo", flag: "🇯🇵", tz: "Asia/Tokyo" },
  { name: "France", city: "Paris", flag: "🇫🇷", tz: "Europe/Paris" },
{ name: "Ecuador", city: "Quito", flag: "🇪🇨", tz: "America/Guayaquil" },
  { name: "New Zealand", city: "Auckland", flag: "🇳🇿", tz: "Pacific/Auckland" },
  { name: "Vietnam", city: "Ho Chi Minh City", flag: "🇻🇳", tz: "Asia/Ho_Chi_Minh" }
];

const select = document.getElementById("base-country");
const input = document.getElementById("base-datetime");
const cards = document.getElementById("cards");
const nowBtn = document.getElementById("now-btn");

countries.forEach((c, i) => {
  const opt = document.createElement("option");
  opt.value = i;
  opt.textContent = `${c.flag} ${c.name} / ${c.city}`;
  select.appendChild(opt);
});
select.value = "0";

function getParts(date, timeZone) {
  const formatter = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false
  });
  const parts = Object.fromEntries(formatter.formatToParts(date).map(p => [p.type, p.value]));
  return {
    year: Number(parts.year), month: Number(parts.month), day: Number(parts.day),
    hour: Number(parts.hour), minute: Number(parts.minute), second: Number(parts.second)
  };
}

function zonedTimeToUtc(localDateTime, timeZone) {
  const [datePart, timePart] = localDateTime.split("T");
  const [year, month, day] = datePart.split("-").map(Number);
  const [hour, minute] = timePart.split(":").map(Number);
  const guess = new Date(Date.UTC(year, month - 1, day, hour, minute));
  const actual = getParts(guess, timeZone);
  const actualUtc = Date.UTC(actual.year, actual.month - 1, actual.day, actual.hour, actual.minute, actual.second);
  const targetUtc = Date.UTC(year, month - 1, day, hour, minute, 0);
  return new Date(guess.getTime() + (targetUtc - actualUtc));
}

function formatForInput(date, timeZone) {
  const p = getParts(date, timeZone);
  return `${p.year}-${String(p.month).padStart(2, "0")}-${String(p.day).padStart(2, "0")}T${String(p.hour).padStart(2, "0")}:${String(p.minute).padStart(2, "0")}`;
}

function formatCard(date, timeZone) {
  const time = new Intl.DateTimeFormat("en-GB", { timeZone, hour: "2-digit", minute: "2-digit", hour12: false }).format(date);
  const dateText = new Intl.DateTimeFormat("en-GB", { timeZone, weekday: "short", day: "2-digit", month: "short", year: "numeric" }).format(date);
  const offset = new Intl.DateTimeFormat("en", { timeZone, timeZoneName: "shortOffset" })
    .formatToParts(date).find(p => p.type === "timeZoneName")?.value || "";
  return { time, dateText, offset };
}

function render() {
  const base = countries[Number(select.value)];
  const utcDate = zonedTimeToUtc(input.value, base.tz);
  cards.innerHTML = "";
  countries.forEach((c, i) => {
    const f = formatCard(utcDate, c.tz);
    const card = document.createElement("article");
    card.className = `card ${i === Number(select.value) ? "active" : ""}`;
    card.innerHTML = `
      <div class="card-top">
        <div>
          <h2 class="country">${c.name}</h2>
          <div class="city">${c.city}</div>
        </div>
        <div class="flag">${c.flag}</div>
      </div>
      <div class="time">${f.time}</div>
      <div class="date">${f.dateText}</div>
      <div class="offset">${f.offset} · ${c.tz}</div>
    `;
    cards.appendChild(card);
  });
}

nowBtn.addEventListener("click", () => {
  const base = countries[Number(select.value)];
  input.value = formatForInput(new Date(), base.tz);
  render();
});
select.addEventListener("change", () => {
  const oldUtc = zonedTimeToUtc(input.value, countries[0].tz);
  input.value = formatForInput(new Date(), countries[Number(select.value)].tz);
  render();
});
input.addEventListener("input", render);

input.value = formatForInput(new Date(), countries[0].tz);
render();
</script>
"""

html(APP_HTML, height=1000, scrolling=True)
