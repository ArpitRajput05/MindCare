(() => {
  "use strict";

  const API_BASE = (window.location.protocol === "file:" || !window.location.origin || window.location.origin === "null")
    ? "http://127.0.0.1:8000"
    : window.location.origin;

  // DOM Elements - Tabs
  const tabAnalytics = document.getElementById("tab-analytics");
  const tabChat = document.getElementById("tab-chat");
  const viewAnalytics = document.getElementById("view-analytics");
  const viewChat = document.getElementById("view-chat");

  // DOM Elements - Form & Result
  const form = document.getElementById("predict-form");
  const submitBtn = document.getElementById("submit-btn");
  const resetBtn = document.getElementById("reset-btn");
  const errorRetryBtn = document.getElementById("error-retry-btn");

  const stateIdle = document.getElementById("state-idle");
  const stateLoading = document.getElementById("state-loading");
  const stateResult = document.getElementById("state-result");
  const stateError = document.getElementById("state-error");

  const scoreNumberEl = document.getElementById("score-number");
  const scoreBandEl = document.getElementById("score-band");
  const scoreContextEl = document.getElementById("score-context");
  const gaugeFill = document.getElementById("gauge-fill");
  const errorLabelEl = document.getElementById("error-label");
  const errorCopyEl = document.getElementById("error-copy");

  // DOM Elements - SHAP & Plan
  const shapCardsContainer = document.getElementById("shap-cards");
  const generatePlanBtn = document.getElementById("generate-plan-btn");
  const planResultBox = document.getElementById("plan-result-box");
  const planHeadlineEl = document.getElementById("plan-headline");
  const planProviderBadge = document.getElementById("plan-provider-badge");
  const planStepsContainer = document.getElementById("plan-steps-container");
  const ragSourcesList = document.getElementById("rag-sources-list");

  // DOM Elements - Chatbot
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatMessages = document.getElementById("chat-messages");
  const promptChips = document.querySelectorAll(".chip-btn");

  // DOM Elements - Helpline Modal
  const helplineModal = document.getElementById("helpline-modal");
  const openHelplineModalBtn = document.getElementById("open-helpline-modal");
  const closeHelplineModalBtn = document.getElementById("close-helpline-modal");

  const GAUGE_ARC_LENGTH = 314; // approx pi * r(100)
  let lastStudentPayload = null;

  // ---------------------------------------------------------
  // Tab Switching
  // ---------------------------------------------------------
  function switchTab(target) {
    if (target === "analytics") {
      tabAnalytics.classList.add("active");
      tabAnalytics.setAttribute("aria-selected", "true");
      tabChat.classList.remove("active");
      tabChat.setAttribute("aria-selected", "false");
      viewAnalytics.classList.add("active");
      viewAnalytics.hidden = false;
      viewChat.classList.remove("active");
      viewChat.hidden = true;
    } else {
      tabChat.classList.add("active");
      tabChat.setAttribute("aria-selected", "true");
      tabAnalytics.classList.remove("active");
      tabAnalytics.setAttribute("aria-selected", "false");
      viewChat.classList.add("active");
      viewChat.hidden = false;
      viewAnalytics.classList.remove("active");
      viewAnalytics.hidden = true;
      chatInput.focus();
    }
  }

  tabAnalytics.addEventListener("click", () => switchTab("analytics"));
  tabChat.addEventListener("click", () => switchTab("chat"));

  // ---------------------------------------------------------
  // Helpline Modal Handlers
  // ---------------------------------------------------------
  openHelplineModalBtn.addEventListener("click", () => helplineModal.showModal());
  closeHelplineModalBtn.addEventListener("click", () => helplineModal.close());
  helplineModal.addEventListener("click", (e) => {
    if (e.target === helplineModal) helplineModal.close();
  });

  // ---------------------------------------------------------
  // Gauge Ticks Drawing
  // ---------------------------------------------------------
  function drawTicks() {
    document.querySelectorAll(".gauge-ticks").forEach((g) => {
      g.innerHTML = "";
      const cx = 120, cy = 140, rOuter = 100, rInner = 90;
      for (let i = 0; i <= 10; i += 2) {
        const angle = Math.PI - (i / 10) * Math.PI;
        const x1 = cx + rOuter * Math.cos(angle);
        const y1 = cy - rOuter * Math.sin(angle);
        const x2 = cx + rInner * Math.cos(angle);
        const y2 = cy - rInner * Math.sin(angle);
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", x1.toFixed(1));
        line.setAttribute("y1", y1.toFixed(1));
        line.setAttribute("x2", x2.toFixed(1));
        line.setAttribute("y2", y2.toFixed(1));
        g.appendChild(line);
      }
    });
  }
  drawTicks();

  // ---------------------------------------------------------
  // Segmented Control (stress_level)
  // ---------------------------------------------------------
  const segGroup = document.getElementById("stress_level_group");
  const stressHiddenInput = document.getElementById("stress_level");
  segGroup.querySelectorAll(".seg-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      segGroup.querySelectorAll(".seg-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      stressHiddenInput.value = btn.dataset.value;
      clearFieldError(stressHiddenInput);
    });
  });

  // ---------------------------------------------------------
  // Field-level Error Helpers
  // ---------------------------------------------------------
  function fieldWrapper(input) {
    return input.closest(".field");
  }

  function setFieldError(input, message) {
    const wrap = fieldWrapper(input);
    if (!wrap) return;
    wrap.classList.add("field-error");
    const msgEl = wrap.querySelector(".error-msg");
    if (msgEl) msgEl.textContent = message;
  }

  function clearFieldError(input) {
    const wrap = fieldWrapper(input);
    if (!wrap) return;
    wrap.classList.remove("field-error");
    const msgEl = wrap.querySelector(".error-msg");
    if (msgEl) msgEl.textContent = "";
  }

  function clearAllErrors() {
    form.querySelectorAll(".field").forEach((f) => f.classList.remove("field-error"));
    form.querySelectorAll(".error-msg").forEach((m) => (m.textContent = ""));
  }

  // ---------------------------------------------------------
  // Collect & Validate Payload
  // ---------------------------------------------------------
  function collectPayload() {
    return {
      age: Number(document.getElementById("age").value),
      gender: document.getElementById("gender").value,
      country: document.getElementById("country").value.trim(),
      academic_level: document.getElementById("academic_level").value,
      most_used_platform: document.getElementById("most_used_platform").value,
      purpose_of_use: document.getElementById("purpose_of_use").value,
      avg_daily_usage_hours: Number(document.getElementById("avg_daily_usage_hours").value),
      daily_unlocks: Number(document.getElementById("daily_unlocks").value),
      study_hours: Number(document.getElementById("study_hours").value),
      physical_activity_hours: Number(document.getElementById("physical_activity_hours").value),
      sleep_hours_per_night: Number(document.getElementById("sleep_hours_per_night").value),
      stress_level: stressHiddenInput.value,
    };
  }

  function validate(payload) {
    const errors = [];
    if (!payload.age || payload.age < 10 || payload.age > 100) errors.push([document.getElementById("age"), "Enter an age between 10 and 100."]);
    if (!payload.gender) errors.push([document.getElementById("gender"), "Please select gender."]);
    if (!payload.country) errors.push([document.getElementById("country"), "Country is required."]);
    if (!payload.academic_level) errors.push([document.getElementById("academic_level"), "Please select academic level."]);
    if (!payload.most_used_platform) errors.push([document.getElementById("most_used_platform"), "Please select platform."]);
    if (!payload.purpose_of_use) errors.push([document.getElementById("purpose_of_use"), "Please select primary purpose."]);
    if (isNaN(payload.avg_daily_usage_hours) || payload.avg_daily_usage_hours < 0 || payload.avg_daily_usage_hours > 24) {
      errors.push([document.getElementById("avg_daily_usage_hours"), "0 to 24 hrs."]);
    }
    if (isNaN(payload.daily_unlocks) || payload.daily_unlocks < 0) {
      errors.push([document.getElementById("daily_unlocks"), "Enter 0 or greater."]);
    }
    if (isNaN(payload.study_hours) || payload.study_hours < 0 || payload.study_hours > 24) {
      errors.push([document.getElementById("study_hours"), "0 to 24 hrs."]);
    }
    if (isNaN(payload.physical_activity_hours) || payload.physical_activity_hours < 0 || payload.physical_activity_hours > 24) {
      errors.push([document.getElementById("physical_activity_hours"), "0 to 24 hrs."]);
    }
    if (isNaN(payload.sleep_hours_per_night) || payload.sleep_hours_per_night < 0 || payload.sleep_hours_per_night > 24) {
      errors.push([document.getElementById("sleep_hours_per_night"), "0 to 24 hrs."]);
    }
    if (!payload.stress_level) {
      errors.push([stressHiddenInput, "Select your perceived stress level."]);
    }
    return errors;
  }

  // ---------------------------------------------------------
  // UI State Switching
  // ---------------------------------------------------------
  function showState(name) {
    [stateIdle, stateLoading, stateResult, stateError].forEach((el) => (el.hidden = true));
    ({ idle: stateIdle, loading: stateLoading, result: stateResult, error: stateError }[name]).hidden = false;
  }

  function renderResult(predData, explainData) {
    const score = predData.predicted_mental_health_score;
    const clamped = Math.max(0, Math.min(10, score));

    scoreNumberEl.textContent = score.toFixed(2);
    scoreBandEl.textContent = `Signal: ${predData.band.toLowerCase()}`;
    scoreContextEl.textContent = predData.summary;

    // Animate Gauge Arc
    gaugeFill.style.transition = "none";
    gaugeFill.style.strokeDashoffset = String(GAUGE_ARC_LENGTH);
    requestAnimationFrame(() => {
      gaugeFill.style.transition = "";
      const offset = GAUGE_ARC_LENGTH * (1 - clamped / 10);
      gaugeFill.style.strokeDashoffset = String(offset);
    });

    // Render SHAP Driver Cards
    renderShapCards(explainData);

    // Reset Plan Box
    planResultBox.hidden = true;
    generatePlanBtn.disabled = false;
    generatePlanBtn.querySelector("span:first-child").textContent = "✨ Generate 3-Step Action Plan (RAG + LLM)";

    showState("result");
  }

  function renderShapCards(explainData) {
    shapCardsContainer.innerHTML = "";
    if (!explainData || !explainData.risk_factors) return;

    // Show top 2 risk drivers and top 1 protective factor
    const topRisks = explainData.risk_factors.slice(0, 2);
    const topProtective = (explainData.protective_factors || []).slice(0, 1);
    const combined = [...topRisks, ...topProtective];

    combined.forEach((item) => {
      const card = document.createElement("div");
      card.className = "shap-card";

      const sign = item.impact > 0 ? "+" : "";
      const badgeClass = item.impact < 0 ? "negative" : "positive";

      card.innerHTML = `
        <div class="shap-card-info">
          <span class="shap-label">${item.label}: <strong>${item.user_value}</strong></span>
          <span class="shap-desc">${item.description}</span>
        </div>
        <span class="shap-badge ${badgeClass}">${sign}${item.impact.toFixed(2)} pts</span>
      `;
      shapCardsContainer.appendChild(card);
    });
  }

  // ---------------------------------------------------------
  // Form Submit Handler (ML + SHAP)
  // ---------------------------------------------------------
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAllErrors();

    const payload = collectPayload();
    const clientErrors = validate(payload);
    if (clientErrors.length > 0) {
      clientErrors.forEach(([input, msg]) => input && setFieldError(input, msg));
      clientErrors[0][0]?.focus?.();
      return;
    }

    lastStudentPayload = payload;
    submitBtn.disabled = true;
    submitBtn.classList.add("loading");
    showState("loading");

    try {
      // Parallel fetch for ML prediction and SHAP explanation
      const [predRes, explainRes] = await Promise.all([
        fetch(`${API_BASE}/predict`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }),
        fetch(`${API_BASE}/explain`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        })
      ]);

      if (!predRes.ok || !explainRes.ok) {
        throw new Error("Failed to process prediction or SHAP analysis.");
      }

      const predData = await predRes.json();
      const explainData = await explainRes.json();

      renderResult(predData, explainData);
    } catch (err) {
      errorLabelEl.textContent = "Analysis Error";
      errorCopyEl.textContent = err.message || "Failed to reach backend server.";
      showState("error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.classList.remove("loading");
    }
  });

  resetBtn.addEventListener("click", () => showState("idle"));
  errorRetryBtn.addEventListener("click", () => showState("idle"));

  // ---------------------------------------------------------
  // Generate 3-Step Plan Handler (RAG + LLM)
  // ---------------------------------------------------------
  generatePlanBtn.addEventListener("click", async () => {
    if (!lastStudentPayload) return;

    generatePlanBtn.disabled = true;
    const btnLabel = generatePlanBtn.querySelector("span:first-child");
    const originalText = btnLabel.textContent;
    btnLabel.textContent = "Retrieving Guidelines & Synthesizing Plan…";

    try {
      const res = await fetch(`${API_BASE}/generate-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_data: lastStudentPayload })
      });

      if (!res.ok) throw new Error("Plan generation failed.");
      const planData = await res.json();

      // Render Plan
      planHeadlineEl.textContent = planData.headline;
      planProviderBadge.textContent = planData.provider_used;

      planStepsContainer.innerHTML = "";
      planData.steps.forEach((step) => {
        const stepEl = document.createElement("div");
        stepEl.className = "plan-step";
        stepEl.innerHTML = `
          <div class="step-top">
            <span class="step-num">${step.step_number}</span>
            <span class="step-title">${step.title}</span>
          </div>
          <p class="step-action">${step.action}</p>
          <span class="step-source">📖 Source: ${step.source}</span>
        `;
        planStepsContainer.appendChild(stepEl);
      });

      // Render RAG Knowledge Base Sources
      ragSourcesList.innerHTML = "";
      (planData.retrieved_sources || []).forEach((src) => {
        const item = document.createElement("div");
        item.className = "rag-source-item";
        item.innerHTML = `
          <strong>${src.source}</strong> — <em>${src.title}</em> (${src.category})
          <p style="margin: 4px 0 0; opacity: 0.85;">${src.snippet}</p>
        `;
        ragSourcesList.appendChild(item);
      });

      planResultBox.hidden = false;
      btnLabel.textContent = "✓ Plan Generated";
    } catch (err) {
      alert("Error generating action plan: " + err.message);
      btnLabel.textContent = originalText;
      generatePlanBtn.disabled = false;
    }
  });

  // ---------------------------------------------------------
  // Grounded Chatbot Interaction
  // ---------------------------------------------------------
  function appendChatMessage(role, text, sources = [], isCrisis = false) {
    const msgEl = document.createElement("div");
    msgEl.className = `chat-msg msg-${role} ${isCrisis ? "msg-crisis" : ""}`;

    const avatar = role === "user" ? "👤" : (isCrisis ? "🚨" : "🌱");
    let sourcesHtml = "";
    if (sources && sources.length > 0) {
      const sourceBadges = sources.map((s) => `• ${s.source}`).join(" ");
      sourcesHtml = `<span class="msg-meta">📚 Sources: ${sourceBadges}</span>`;
    }

    msgEl.innerHTML = `
      <div class="msg-avatar">${avatar}</div>
      <div class="msg-body">
        <p>${text.replace(/\n/g, "<br>")}</p>
        ${sourcesHtml}
      </div>
    `;

    chatMessages.appendChild(msgEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function handleUserChatMessage(userQuery) {
    if (!userQuery.trim()) return;

    appendChatMessage("user", userQuery);
    chatInput.value = "";
    chatInput.disabled = true;

    // Typing indicator
    const typingId = "typing-" + Date.now();
    const typingEl = document.createElement("div");
    typingEl.className = "chat-msg msg-assistant";
    typingEl.id = typingId;
    typingEl.innerHTML = `
      <div class="msg-avatar">🌱</div>
      <div class="msg-body"><p><em>Searching wellness guidelines & formulating answer…</em></p></div>
    `;
    chatMessages.appendChild(typingEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userQuery,
          student_context: lastStudentPayload || null
        })
      });

      document.getElementById(typingId)?.remove();

      if (!res.ok) throw new Error("Failed to receive response from assistant.");
      const chatData = await res.json();

      if (chatData.is_crisis) {
        appendChatMessage("assistant", chatData.reply, [], true);
        helplineModal.showModal();
      } else {
        appendChatMessage("assistant", chatData.reply, chatData.sources || []);
      }
    } catch (err) {
      document.getElementById(typingId)?.remove();
      appendChatMessage("assistant", "Sorry, I had trouble connecting to the wellness knowledge base. Please try again.");
    } finally {
      chatInput.disabled = false;
      chatInput.focus();
    }
  }

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleUserChatMessage(chatInput.value);
  });

  promptChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const promptText = chip.dataset.prompt;
      if (promptText) {
        handleUserChatMessage(promptText);
      }
    });
  });

})();
