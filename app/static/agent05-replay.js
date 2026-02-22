(function () {
  const titleEl = document.getElementById("replay-title");
  const metaEl = document.getElementById("replay-meta");
  const moduleIndexEl = document.getElementById("module-index");
  const moduleCardEl = document.getElementById("module-card");
  const assetListEl = document.getElementById("asset-list");
  const prevButton = document.getElementById("prev-module");
  const nextButton = document.getElementById("next-module");
  const summaryId = window.AGENT05_SUMMARY_ID;

  let replay = { modules: [], media_assets: [] };
  let moduleIndex = 0;

  function renderModule() {
    const modules = replay.modules || [];
    if (modules.length === 0) {
      moduleCardEl.innerHTML = "<p>No modules available for replay.</p>";
      moduleIndexEl.textContent = "Module 0 / 0";
      prevButton.disabled = true;
      nextButton.disabled = true;
      return;
    }

    const current = modules[moduleIndex];
    moduleCardEl.innerHTML =
      "<h3>" +
      (current.title || current.id || "Module") +
      "</h3>" +
      "<p>" +
      ((current.core_topics || []).join(", ") || current.topic || "No topic metadata") +
      "</p>";
    moduleIndexEl.textContent = "Module " + (moduleIndex + 1) + " / " + modules.length;
    prevButton.disabled = moduleIndex === 0;
    nextButton.disabled = moduleIndex >= modules.length - 1;
  }

  function renderAssets() {
    const assets = replay.media_assets || [];
    assetListEl.innerHTML = "";
    if (assets.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No media assets available.";
      assetListEl.appendChild(li);
      return;
    }

    assets.forEach(function (asset) {
      const li = document.createElement("li");
      if (asset.url) {
        li.innerHTML =
          "<strong>" +
          (asset.label || asset.type || "Asset") +
          '</strong> • <a href="' +
          asset.url +
          '" target="_blank" rel="noreferrer">Open</a>';
      } else {
        li.innerHTML = "<strong>" + (asset.label || asset.type || "Asset") + "</strong>";
      }
      assetListEl.appendChild(li);
    });
  }

  function loadReplay() {
    fetch("/api/summary/" + encodeURIComponent(summaryId))
      .then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok) {
            throw new Error(payload.error || "Unable to load replay.");
          }
          return payload.summary;
        });
      })
      .then(function (summary) {
        replay = summary.replay || replay;
        titleEl.textContent = summary.lesson_title;
        metaEl.textContent =
          "Accuracy " + summary.accuracy + "% • " + (replay.estimated_duration || "?") + " min";
        moduleIndex = 0;
        renderModule();
        renderAssets();
      })
      .catch(function (error) {
        titleEl.textContent = "Replay unavailable";
        metaEl.textContent = error.message;
        renderModule();
        renderAssets();
      });
  }

  prevButton.addEventListener("click", function () {
    if (moduleIndex <= 0) return;
    moduleIndex -= 1;
    renderModule();
  });

  nextButton.addEventListener("click", function () {
    if (moduleIndex >= (replay.modules || []).length - 1) return;
    moduleIndex += 1;
    renderModule();
  });

  loadReplay();
})();
