"use strict";

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#39;");

function table(headers, rows) {
  if (!rows.length) return '<div class="empty">No records</div>';
  return `<table><thead><tr>${headers.map(([label]) => `<th>${escapeHtml(label)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) =>
    `<tr>${headers.map(([, key, render]) => `<td>${render ? render(row[key]) : escapeHtml(row[key])}</td>`).join("")}</tr>`
  ).join("")}</tbody></table>`;
}

async function load() {
  const [summary, devices, incidents, telemetry] = await Promise.all([
    getJson("/api/summary"), getJson("/api/devices"),
    getJson("/api/incidents"), getJson("/api/telemetry?limit=12"),
  ]);
  const metrics = [
    ["Registered devices", summary.devices],
    ["Telemetry readings", summary.telemetry],
    ["Open incidents", summary.open_incidents],
    ["Critical incidents", summary.critical_incidents],
  ];
  document.querySelector("#metrics").innerHTML = metrics.map(([label, value]) =>
    `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`
  ).join("");
  document.querySelector("#device-count").textContent = `${devices.devices.length} registered`;
  document.querySelector("#incident-count").textContent = `${incidents.incidents.length} open`;
  document.querySelector("#devices").innerHTML = table([
    ["Device", "name"], ["Kind", "kind"], ["Status", "status", (v) => `<span class="status">${escapeHtml(v)}</span>`], ["Last seen", "last_seen"],
  ], devices.devices);
  document.querySelector("#incidents").innerHTML = table([
    ["Severity", "severity", (v) => `<span class="severity ${escapeHtml(v)}">${escapeHtml(v)}</span>`],
    ["Device", "device_id"], ["Incident", "title"], ["Count", "occurrences"],
    ["Detail", "id", (id) => `<button data-incident="${escapeHtml(id)}">View</button>`],
  ], incidents.incidents);
  document.querySelector("#telemetry").innerHTML = table([
    ["Device", "device_id"], ["Metric", "metric"], ["Value", "value"], ["Unit", "unit"], ["Recorded", "recorded_at"],
  ], telemetry.telemetry);
  await loadEventFilters();
  await loadEvents();
}

async function getJson(url) {
  const response = await fetch(url);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `Request failed (${response.status})`);
  return body;
}

let eventParams = new URLSearchParams();
let eventCursors = [null];
let eventPage = 0;
let eventNext = null;
let eventRequest = 0;

async function loadEventFilters() {
  const filters = await getJson("/api/events/filters");
  for (const [name, values] of [["severity", filters.severities], ["service", filters.services], ["device_id", filters.devices]]) {
    const select = document.querySelector(`[name="${name}"]`);
    for (const value of values) select.add(new Option(value, value));
  }
}

async function loadEvents() {
  const request = ++eventRequest;
  const params = new URLSearchParams(eventParams);
  params.set("limit", "20");
  if (eventCursors[eventPage]) params.set("cursor", eventCursors[eventPage]);
  document.querySelector("#events-prev").disabled = true;
  document.querySelector("#events-next").disabled = true;
  document.querySelector("#event-error").hidden = true;
  try {
    const result = await getJson(`/api/events?${params}`);
    if (request !== eventRequest) return;
    eventNext = result.next_cursor;
    document.querySelector("#event-count").textContent = `${result.events.length} on this page`;
    document.querySelector("#event-page").textContent = `Page ${eventPage + 1}`;
    document.querySelector("#events").innerHTML = table([
      ["Severity", "severity", (v) => `<span class="severity ${escapeHtml(v)}">${escapeHtml(v)}</span>`],
      ["Time", "recorded_at"], ["Service", "service"], ["Device", "device_id"],
      ["Message", "message", (v) => `<span class="event-message">${escapeHtml(v)}</span>`],
      ["Source", "source"], ["Line", "physical_line"], ["Byte offset", "byte_offset"],
    ], result.events);
    document.querySelector("#events-prev").disabled = eventPage === 0;
    document.querySelector("#events-next").disabled = !eventNext;
  } catch (error) {
    if (request !== eventRequest) return;
    const target = document.querySelector("#event-error");
    target.textContent = error.message;
    target.hidden = false;
    document.querySelector("#events").replaceChildren();
    document.querySelector("#event-count").textContent = "Unable to load events";
    document.querySelector("#event-page").textContent = "";
  }
}

document.querySelector("#event-filters").addEventListener("submit", (event) => {
  event.preventDefault();
  eventParams = new URLSearchParams();
  for (const [key, raw] of new FormData(event.currentTarget)) {
    if (raw.trim()) eventParams.set(key, ["since", "until"].includes(key) ? new Date(raw).toISOString() : raw.trim());
  }
  eventCursors = [null]; eventPage = 0;
  loadEvents();
});
document.querySelector("#event-filters").addEventListener("reset", () => {
  eventParams = new URLSearchParams(); eventCursors = [null]; eventPage = 0;
  loadEvents();
});
document.querySelector("#events-next").addEventListener("click", () => {
  eventCursors[++eventPage] = eventNext;
  loadEvents();
});
document.querySelector("#events-prev").addEventListener("click", () => {
  eventPage--; loadEvents();
});

document.querySelector("#incidents").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-incident]");
  if (!button) return;
  const detail = document.querySelector("#incident-detail");
  detail.hidden = false;
  document.querySelector("#detail-body").textContent = "Loading incident…";
  detail.focus();
  try {
    const result = await getJson(`/api/incidents/${button.dataset.incident}`);
    const incident = result.incident;
    document.querySelector("#detail-title").textContent = incident.title;
    document.querySelector("#detail-body").innerHTML =
      `<p class="detail-summary">${escapeHtml(incident.device_id)} · ${escapeHtml(incident.severity)} · ${escapeHtml(incident.occurrences)} occurrences<br>First: ${escapeHtml(incident.first_seen)}<br>Last: ${escapeHtml(incident.last_seen)}</p>` +
      `<h3>Latest readings for this metric</h3><div class="table-wrap">${table([
        ["Metric", "metric"], ["Value", "value"], ["Unit", "unit"], ["Recorded", "recorded_at"],
      ], result.telemetry)}</div><h3>Latest events for this device</h3><div class="table-wrap">${table([
        ["Severity", "severity"], ["Time", "recorded_at"], ["Message", "message"],
      ], result.events)}</div>`;
  } catch (error) {
    document.querySelector("#detail-body").textContent = error.message;
  }
});
document.querySelector("#close-detail").addEventListener("click", () => {
  document.querySelector("#incident-detail").hidden = true;
  document.querySelector("[data-incident]")?.focus();
});

load().catch((error) => {
  document.querySelector("main").innerHTML = `<div class="error">Unable to load dashboard: ${escapeHtml(error.message)}</div>`;
});
