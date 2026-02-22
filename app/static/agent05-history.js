(function () {
  const controls = document.getElementById("history-controls");
  const userInput = document.getElementById("user-id");
  const seedButton = document.getElementById("seed-summary");
  const list = document.getElementById("summary-list");
  const historyCount = document.getElementById("history-count");
  const avgAccuracy = document.getElementById("avg-accuracy");
  const totalLessons = document.getElementById("total-lessons");
  const topFocus = document.getElementById("top-focus");

  const dialog = document.getElementById("summary-dialog");
  const dialogClose = document.getElementById("dialog-close");
  const dialogTitle = document.getElementById("dialog-title");
  const dialogMeta = document.getElementById("dialog-meta");
  const topicTable = document.getElementById("topic-table");
  const recommendationList = document.getElementById("recommendations");
  const replayLink = document.getElementById("replay-link");

  let cache = [];

  function formatDate(value) {
    return new Date(value).toLocaleString();
  }

  function renderTopics(topics) {
    topicTable.innerHTML = "";
    const header = document.createElement("div");
    header.className = "topic-row";
    header.innerHTML = "<span>Topic</span><span>Correct</span><span>Incorrect</span><span>Accuracy</span>";
    topicTable.appendChild(header);

    topics.forEach(function (topic) {
      const row = document.createElement("div");
      row.className = "topic-row";
      row.innerHTML = "<span>" + topic.name + "</span><span>" + topic.correct + "</span><span>" + topic.incorrect + "</span><span>" + topic.accuracy + "%</span>";
      topicTable.appendChild(row);
    });
  }

  function updateMetrics(summaries) {
    totalLessons.textContent = String(summaries.length);
    historyCount.textContent = summaries.length + " records";
    if (summaries.length === 0) {
      avgAccuracy.textContent = "0%";
      topFocus.textContent = "None";
      return;
    }

    const avg =
      summaries.reduce(function (sum, item) {
        return sum + Number(item.accuracy || 0);
      }, 0) / summaries.length;
    avgAccuracy.textContent = avg.toFixed(1) + "%";

    const focusCount = {};
    summaries.forEach(function (summary) {
      (summary.focus_areas || []).forEach(function (focus) {
        focusCount[focus] = (focusCount[focus] || 0) + 1;
      });
    });
    const ranked = Object.entries(focusCount).sort(function (a, b) {
      return b[1] - a[1];
    });
    topFocus.textContent = ranked.length ? ranked[0][0] : "None";
  }

  function renderSummaries(summaries) {
    list.innerHTML = "";
    if (summaries.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No summaries found for this user.";
      list.appendChild(li);
      return;
    }

    summaries.forEach(function (summary) {
      const li = document.createElement("li");
      const chips = (summary.focus_areas || []).length
        ? summary.focus_areas.map(function (topic) {
            return '<span class="chip">' + topic + "</span>";
          }).join("")
        : '<span class="chip">No immediate focus area</span>';

      li.innerHTML =
        '<div class="summary-top"><div><h3>' +
        summary.lesson_title +
        "</h3><p>" +
        formatDate(summary.created_at) +
        "</p></div><p><strong>" +
        summary.accuracy +
        "%</strong></p></div>" +
        '<div class="chips">' +
        chips +
        "</div>" +
        '<div class="summary-actions">' +
        '<button data-id="' +
        summary.id +
        '" data-action="view" type="button">View Summary</button>' +
        '<a href="/replay/' +
        encodeURIComponent(summary.id) +
        '">Replay Lesson</a>' +
        "</div>";
      list.appendChild(li);
    });
  }

  function loadHistory(userId) {
    return fetch("/api/summaries?user_id=" + encodeURIComponent(userId))
      .then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok) {
            throw new Error(payload.error || "Unable to load summary history.");
          }
          return payload.summaries || [];
        });
      })
      .then(function (summaries) {
        cache = summaries;
        renderSummaries(summaries);
        updateMetrics(summaries);
      });
  }

  function openSummary(summaryId, userId) {
    fetch(
      "/api/summary/" +
        encodeURIComponent(summaryId) +
        "?user_id=" +
        encodeURIComponent(userId)
    )
      .then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok) {
            throw new Error(payload.error || "Unable to fetch summary detail.");
          }
          return payload.summary;
        });
      })
      .then(function (summary) {
        dialogTitle.textContent = summary.lesson_title;
        dialogMeta.textContent = "Completed " + formatDate(summary.created_at) + " • Accuracy " + summary.accuracy + "%";
        renderTopics(summary.topics || []);
        recommendationList.innerHTML = "";
        (summary.recommendations || []).forEach(function (recommendation) {
          const li = document.createElement("li");
          li.textContent = recommendation;
          recommendationList.appendChild(li);
        });
        replayLink.href = "/replay/" + encodeURIComponent(summary.id);
        dialog.showModal();
      })
      .catch(function (error) {
        window.alert(error.message);
      });
  }

  function createDemoSummary(userId) {
    const payload = {
      user_id: userId,
      lesson: {
        id: "lesson-linear-1",
        title: "Linear Equations and Graphs",
        estimated_duration: 32,
        modules: [
          { id: "m-1", title: "Slope Fundamentals", core_topics: ["Slope"] },
          { id: "m-2", title: "Intercepts", core_topics: ["Intercepts"] },
          { id: "m-3", title: "Applications", core_topics: ["Applications"] }
        ],
        media_assets: [
          { type: "video", label: "Slope Visual", url: "https://example.com/slope-video" },
          { type: "audio", label: "Applications Recap", url: "https://example.com/applications-audio" }
        ]
      },
      test_result: {
        feedback: {
          strong_topics: ["Slope", "Intercepts"],
          focus_topics: ["Applications", "Applications"]
        }
      },
      checkpoint_sessions: [
        {
          module_id: "m-1",
          qa_pairs: [{ question: "Explain slope", answer: "..." }]
        },
        {
          module_id: "m-3",
          qa_pairs: [
            { question: "When to model with line?", answer: "..." },
            { question: "Interpret intercept", answer: "..." }
          ]
        }
      ]
    };

    return fetch("/api/summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (response) {
      return response.json().then(function (body) {
        if (!response.ok) {
          throw new Error(body.error || "Could not create summary.");
        }
      });
    });
  }

  controls.addEventListener("submit", function (event) {
    event.preventDefault();
    const userId = userInput.value.trim();
    if (!userId) return;
    loadHistory(userId).catch(function (error) {
      window.alert(error.message);
    });
  });

  seedButton.addEventListener("click", function () {
    const userId = userInput.value.trim();
    if (!userId) return;
    createDemoSummary(userId)
      .then(function () {
        return loadHistory(userId);
      })
      .catch(function (error) {
        window.alert(error.message);
      });
  });

  list.addEventListener("click", function (event) {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    if (target.dataset.action !== "view") return;
    const summaryId = target.dataset.id;
    if (!summaryId) return;
    const summary = cache.find(function (item) {
      return item.id === summaryId;
    });
    openSummary(summaryId, summary ? summary.user_id : userInput.value.trim());
  });

  dialogClose.addEventListener("click", function () {
    dialog.close();
  });

  loadHistory(userInput.value.trim()).catch(function () {
    renderSummaries([]);
    updateMetrics([]);
  });
})();
