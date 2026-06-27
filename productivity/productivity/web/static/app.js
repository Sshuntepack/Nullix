"use strict";

const COLORS = {
  productive: "#34d399",
  distracting: "#f87171",
  neutral: "#94a3b8",
  accent: "#6d8bff",
};

let state = { range: "today" };
let charts = {};

function fmtDuration(seconds) {
  seconds = Math.round(seconds);
  if (seconds < 60) return `${seconds}s`;
  const m = Math.floor(seconds / 60);
  const h = Math.floor(m / 60);
  if (h) return `${h}h ${m % 60}m`;
  return `${m}m`;
}

function fmtClock(seconds) {
  seconds = Math.max(0, Math.round(seconds));
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

async function fetchDashboard() {
  const res = await fetch(`/api/dashboard?range=${state.range}`);
  if (!res.ok) return;
  const data = await res.json();
  render(data);
}

function render(data) {
  const summary = data.summary;
  const score = Math.round(summary.productivity_score * 100);
  document.getElementById("score").textContent = score;
  const ring = document.getElementById("score-ring");
  const circumference = 327;
  ring.style.strokeDashoffset = String(
    circumference - (circumference * score) / 100
  );
  ring.style.stroke =
    score >= 60 ? COLORS.productive : score >= 35 ? COLORS.accent : COLORS.distracting;

  document.getElementById("total-time").textContent =
    `${fmtDuration(summary.total_seconds)} tracked`;
  document.getElementById("generated-at").textContent =
    `Updated ${new Date(data.generated_at).toLocaleTimeString()}`;

  const byCat = summary.by_category || {};
  setStat("productive", byCat.productive || 0);
  setStat("distracting", byCat.distracting || 0);

  renderCategoryChart(byCat);
  renderAppsChart(data.by_app || []);
  renderHourlyChart(data.hourly || []);
  renderProjects(data.by_project || []);
  renderFocus(data.focus || { active: false });
}

function setStat(name, seconds) {
  document
    .querySelector(`[data-stat="${name}"]`)
    .textContent = fmtDuration(seconds);
}

function renderCategoryChart(byCat) {
  const labels = ["productive", "distracting", "neutral"];
  const values = labels.map((l) => byCat[l] || 0);
  const ctx = document.getElementById("category-chart");
  if (charts.category) {
    charts.category.data.datasets[0].data = values;
    charts.category.update();
    return;
  }
  charts.category = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels.map((l) => l[0].toUpperCase() + l.slice(1)),
      datasets: [
        {
          data: values,
          backgroundColor: labels.map((l) => COLORS[l]),
          borderWidth: 0,
        },
      ],
    },
    options: {
      cutout: "68%",
      plugins: {
        legend: { labels: { color: "#8b93a7" }, position: "bottom" },
        tooltip: { callbacks: { label: (c) => fmtDuration(c.raw) } },
      },
    },
  });
}

function renderAppsChart(apps) {
  const ctx = document.getElementById("apps-chart");
  const labels = apps.map((a) => a.app);
  const values = apps.map((a) => a.seconds);
  const colors = apps.map((a) => COLORS[a.category] || COLORS.neutral);
  if (charts.apps) {
    charts.apps.data.labels = labels;
    charts.apps.data.datasets[0].data = values;
    charts.apps.data.datasets[0].backgroundColor = colors;
    charts.apps.update();
    return;
  }
  charts.apps = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{ data: values, backgroundColor: colors, borderRadius: 6 }],
    },
    options: {
      indexAxis: "y",
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => fmtDuration(c.raw) } },
      },
      scales: {
        x: { ticks: { color: "#8b93a7" }, grid: { color: "#232a3a" } },
        y: { ticks: { color: "#e8ecf4" }, grid: { display: false } },
      },
    },
  });
}

function renderHourlyChart(hourly) {
  const ctx = document.getElementById("hourly-chart");
  const labels = hourly.map((h) => `${h.hour}`);
  const series = ["productive", "distracting", "neutral"].map((cat) => ({
    label: cat,
    data: hourly.map((h) => (h[cat] || 0) / 60),
    backgroundColor: COLORS[cat],
    borderRadius: 4,
    stack: "h",
  }));
  if (charts.hourly) {
    charts.hourly.data.datasets.forEach((ds, i) => {
      ds.data = series[i].data;
    });
    charts.hourly.update();
    return;
  }
  charts.hourly = new Chart(ctx, {
    type: "bar",
    data: { labels, datasets: series },
    options: {
      plugins: {
        legend: { labels: { color: "#8b93a7" } },
        tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${Math.round(c.raw)}m` } },
      },
      scales: {
        x: { stacked: true, ticks: { color: "#8b93a7" }, grid: { display: false } },
        y: { stacked: true, ticks: { color: "#8b93a7" }, grid: { color: "#232a3a" } },
      },
    },
  });
}

function renderProjects(projects) {
  const list = document.getElementById("project-list");
  const max = Math.max(1, ...projects.map((p) => p.seconds));
  list.innerHTML = projects
    .map(
      (p) => `
      <li>
        <span style="min-width:120px">${p.project}</span>
        <span class="bar"><span style="width:${(p.seconds / max) * 100}%"></span></span>
        <span class="val">${fmtDuration(p.seconds)}</span>
      </li>`
    )
    .join("");
  if (!projects.length) {
    list.innerHTML = `<li class="muted">No project activity yet</li>`;
  }
}

function renderFocus(focus) {
  const timer = document.getElementById("timer");
  const stateEl = document.getElementById("focus-state");
  const stopBtn = document.getElementById("stop-focus");
  const note = document.getElementById("blocklist-note");
  if (focus.active) {
    timer.textContent = fmtClock(focus.remaining);
    stateEl.textContent = `${focus.label} (${focus.kind}) in progress`;
    stopBtn.disabled = false;
    note.textContent =
      focus.kind === "focus" && focus.blocklist && focus.blocklist.length
        ? `Blocking: ${focus.blocklist.slice(0, 5).join(", ")}${
            focus.blocklist.length > 5 ? "\u2026" : ""
          }`
        : "";
  } else {
    timer.textContent = "--:--";
    stateEl.textContent = "No active session";
    stopBtn.disabled = true;
    note.textContent = "";
  }
}

async function postFocus(path, body) {
  await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  fetchDashboard();
}

function wireControls() {
  document.querySelectorAll(".range").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.range = btn.dataset.range;
      document
        .querySelectorAll(".range")
        .forEach((b) => b.setAttribute("aria-selected", String(b === btn)));
      fetchDashboard();
    });
  });
  document
    .getElementById("start-focus")
    .addEventListener("click", () =>
      postFocus("/api/focus/start", { kind: "focus", minutes: 25 })
    );
  document
    .getElementById("start-break")
    .addEventListener("click", () =>
      postFocus("/api/focus/start", { kind: "break", minutes: 5 })
    );
  document
    .getElementById("stop-focus")
    .addEventListener("click", () => postFocus("/api/focus/stop", {}));
}

document.addEventListener("DOMContentLoaded", () => {
  wireControls();
  fetchDashboard();
  setInterval(fetchDashboard, 5000);
});
