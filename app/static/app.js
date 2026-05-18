const els = {
  form: document.getElementById("chat-form"),
  input: document.getElementById("message-input"),
  log: document.getElementById("chat-log"),
  send: document.getElementById("send-button"),
  traceToggle: document.getElementById("trace-toggle"),
  traceOutput: document.getElementById("trace-output"),
  missingList: document.getElementById("missing-list"),
  intent: document.getElementById("metric-intent"),
  score: document.getElementById("metric-score"),
  llm: document.getElementById("metric-llm"),
  statusPill: document.getElementById("status-pill"),
  statusText: document.getElementById("status-text"),
};

function addMessage(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "user" ? "고객" : "AI 상담";

  const body = document.createElement("div");
  body.className = "message-body";
  body.textContent = text;

  article.append(meta, body);
  els.log.appendChild(article);
  els.log.scrollTop = els.log.scrollHeight;
}

function setLoading(isLoading) {
  els.send.disabled = isLoading;
  els.send.textContent = isLoading ? "생성 중" : "전송";
}

function renderMissing(fields) {
  els.missingList.innerHTML = "";
  if (!fields.length) {
    const li = document.createElement("li");
    li.textContent = "추가 필수 정보 없음";
    els.missingList.appendChild(li);
    return;
  }
  fields.forEach((field) => {
    const li = document.createElement("li");
    li.textContent = field;
    els.missingList.appendChild(li);
  });
}

function compactTrace(data) {
  if (!data.trace) {
    return "Trace 옵션이 꺼져 있습니다.";
  }
  const trace = data.trace;
  return JSON.stringify(
    {
      intent: trace.intent,
      intent_confidence: trace.intent_confidence,
      retrieved_contexts: trace.retrieved_contexts,
      risk_flags: trace.risk_flags,
      critic_score: trace.critic_score,
      critic_issues: trace.critic_issues,
      model: trace.model,
      llm_enabled: trace.llm_enabled,
      latency_seconds: trace.latency_seconds,
    },
    null,
    2,
  );
}

async function refreshHealth() {
  try {
    const res = await fetch("/health");
    const data = await res.json();
    els.statusPill.classList.add("ok");
    els.statusText.textContent = "API 연결됨";
    els.llm.textContent = data.llm_enabled ? data.model : "fallback";
  } catch {
    els.statusPill.classList.remove("ok");
    els.statusText.textContent = "API 대기";
    els.llm.textContent = "-";
  }
}

async function sendMessage(message) {
  addMessage("user", message);
  setLoading(true);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        include_trace: els.traceToggle.checked,
      }),
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();
    addMessage("agent", data.answer);
    els.intent.textContent = data.intent;
    els.score.textContent = `${data.critic_score}/5`;
    renderMissing(data.missing_fields || []);
    els.traceOutput.textContent = compactTrace(data);
  } catch {
    addMessage("agent", "상담 서버 응답을 받지 못했습니다. 서버 상태를 확인해 주세요.");
  } finally {
    setLoading(false);
  }
}

els.form.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = els.input.value.trim();
  if (!message) return;
  els.input.value = "";
  sendMessage(message);
});

document.querySelectorAll(".example-button").forEach((button) => {
  button.addEventListener("click", () => {
    els.input.value = button.dataset.query;
    els.input.focus();
  });
});

refreshHealth();
