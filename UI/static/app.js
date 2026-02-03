document.addEventListener("DOMContentLoaded", () => {
  const promptEl = document.getElementById("prompt");
  const runBtn = document.getElementById("runBtn");
  const runStatus = document.getElementById("runStatus");
  const runIdEl = document.getElementById("runId");
  const downloadLink = document.getElementById("downloadLink");

  const previewFrame = document.getElementById("previewFrame");
  const codeBlock = document.getElementById("codeBlock");

  const siteManifestEl = document.getElementById("siteManifest");
  const assetsManifestEl = document.getElementById("assetsManifest");
  const finalResponseEl = document.getElementById("finalResponse");

  const tabs = Array.from(document.querySelectorAll(".tab"));

  const assetInput = document.getElementById("assetInput");
  const assetList = document.getElementById("assetList");
  const dropzone = document.getElementById("dropzone");
  const browseBtn = document.getElementById("browseBtn");

  const clearBtn = document.getElementById("clearBtn");
  const openPreviewBtn = document.getElementById("openPreviewBtn");

  const historyBtn = document.getElementById("historyBtn");
  const historyModal = document.getElementById("historyModal");
  const closeHistory = document.getElementById("closeHistory");
  const historyList = document.getElementById("historyList");

  let current = { html: "", css: "", js: "" };
  let selectedTab = "html";
  let assetsState = []; // [{file, desc}]
  let currentPreviewUrl = "";

  function setStatus(msg, isError = false) {
    runStatus.textContent = msg || "";
    runStatus.classList.toggle("error", !!isError);
  }

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes)) return "";
    const units = ["B", "KB", "MB", "GB"];
    let i = 0;
    let v = bytes;
    while (v >= 1024 && i < units.length - 1) {
      v /= 1024;
      i++;
    }
    return `${v.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
  }

  function setOpenPreviewEnabled(enabled) {
    openPreviewBtn.disabled = !enabled;
  }

  function resetUI() {
    promptEl.value = "";
    assetsState = [];
    refreshAssetList();

    current = { html: "", css: "", js: "" };
    selectedTab = "html";
    tabs.forEach((t) => t.classList.toggle("active", t.dataset.tab === "html"));
    codeBlock.textContent = "";

    runIdEl.textContent = "—";
    downloadLink.textContent = "—";
    downloadLink.href = "#";

    siteManifestEl.textContent = "";
    assetsManifestEl.textContent = "";
    finalResponseEl.textContent = "";

    previewFrame.removeAttribute("src");
    currentPreviewUrl = "";
    setOpenPreviewEnabled(false);

    setStatus("");
  }

  function refreshAssetList() {
    assetList.innerHTML = "";
    if (!assetsState.length) return;

    assetsState.forEach((a, idx) => {
      const wrap = document.createElement("div");
      wrap.className = "asset-item";

      const top = document.createElement("div");
      top.className = "asset-top";

      const left = document.createElement("div");
      left.style.minWidth = "0";

      const name = document.createElement("div");
      name.className = "asset-name";
      name.textContent = a.file.name;

      const size = document.createElement("div");
      size.className = "asset-size";
      size.textContent = formatBytes(a.file.size);

      left.appendChild(name);
      left.appendChild(size);

      const remove = document.createElement("button");
      remove.className = "btn btn-secondary btn-small";
      remove.textContent = "Remove";
      remove.addEventListener("click", () => {
        assetsState.splice(idx, 1);
        refreshAssetList();
      });

      top.appendChild(left);
      top.appendChild(remove);

      const desc = document.createElement("input");
      desc.className = "asset-desc";
      desc.type = "text";
      desc.placeholder = "Optional description (e.g., use this as logo / hero image / product image)";
      desc.value = a.desc || "";
      desc.addEventListener("input", () => {
        a.desc = desc.value;
      });

      wrap.appendChild(top);
      wrap.appendChild(desc);

      assetList.appendChild(wrap);
    });
  }

  function addFiles(files) {
    const list = Array.from(files || []);
    if (!list.length) return;

    list.forEach((f) => {
      assetsState.push({ file: f, desc: "" });
    });
    refreshAssetList();
  }

  // Dropzone behaviors
  function openFilePicker() {
    assetInput.click();
  }

  dropzone.addEventListener("click", (e) => {
    // If clicking the button, let that handle it
    if (e.target === browseBtn) return;
    openFilePicker();
  });

  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openFilePicker();
    }
  });

  browseBtn.addEventListener("click", (e) => {
    e.preventDefault();
    openFilePicker();
  });

  assetInput.addEventListener("change", () => {
    addFiles(assetInput.files);
    assetInput.value = "";
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("is-dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("is-dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("is-dragover");
    addFiles(e.dataTransfer.files);
  });

  function setRunUI(payload) {
    runIdEl.textContent = payload.run_id || "—";

    if (payload.download_url) {
      downloadLink.textContent = payload.download_url;
      downloadLink.href = payload.download_url;
    } else {
      downloadLink.textContent = "—";
      downloadLink.href = "#";
    }

    if (payload.preview_url) {
      previewFrame.src = payload.preview_url;
      currentPreviewUrl = payload.preview_url;
      setOpenPreviewEnabled(true);
    } else {
      previewFrame.removeAttribute("src");
      currentPreviewUrl = "";
      setOpenPreviewEnabled(false);
    }

    current.html = payload.html || "";
    current.css = payload.css || "";
    current.js = payload.js || "";

    siteManifestEl.textContent = payload.site_manifest
      ? JSON.stringify(payload.site_manifest, null, 2)
      : "";

    assetsManifestEl.textContent = payload.assets_manifest
      ? JSON.stringify(payload.assets_manifest, null, 2)
      : "";

    finalResponseEl.textContent = payload.final_response || "";

    renderCode();
  }

  function renderCode() {
    const val = current[selectedTab] || "";
    codeBlock.textContent = val;
  }

  tabs.forEach((t) => {
    t.addEventListener("click", () => {
      tabs.forEach((x) => x.classList.remove("active"));
      t.classList.add("active");
      selectedTab = t.dataset.tab;
      renderCode();
    });
  });

  async function runGeneration() {
    const prompt = (promptEl.value || "").trim();
    if (!prompt) {
      setStatus("Prompt is required.", true);
      return;
    }

    setStatus("Generating…");
    runBtn.disabled = true;

    try {
      const fd = new FormData();
      fd.append("prompt", prompt);

      assetsState.forEach((a) => {
        fd.append("assets", a.file);
        fd.append("asset_desc", a.desc || "");
      });

      const res = await fetch("/api/run", { method: "POST", body: fd });
      const data = await res.json();

      if (!data.ok) {
        setStatus(data.error || "Failed.", true);
        return;
      }

      setRunUI(data);
      setStatus("Done ✅");
    } catch (e) {
      setStatus("Error while running. Check console.", true);
      console.error(e);
    } finally {
      runBtn.disabled = false;
    }
  }

  runBtn.addEventListener("click", runGeneration);

  // Clear/New
  clearBtn.addEventListener("click", () => {
    resetUI();
  });

  // Open full preview in new tab
  openPreviewBtn.addEventListener("click", () => {
    if (!currentPreviewUrl) return;
    window.open(currentPreviewUrl, "_blank", "noopener,noreferrer");
  });

  // history modal
  function openHistory() {
    historyModal.classList.remove("hidden");
    historyModal.setAttribute("aria-hidden", "false");
    loadHistory();
  }

  function closeHistoryModal() {
    historyModal.classList.add("hidden");
    historyModal.setAttribute("aria-hidden", "true");
  }

  historyBtn.addEventListener("click", openHistory);
  closeHistory.addEventListener("click", closeHistoryModal);
  historyModal.addEventListener("click", (e) => {
    if (e.target === historyModal) closeHistoryModal();
  });

  async function loadHistory() {
    historyList.innerHTML = "Loading…";
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (!data.ok) {
        historyList.innerHTML = "Failed to load history.";
        return;
      }

      const runs = data.runs || [];
      if (!runs.length) {
        historyList.innerHTML = "No runs yet.";
        return;
      }

      historyList.innerHTML = "";
      runs.forEach((r) => {
        const row = document.createElement("div");
        row.className = "history-item";

        const left = document.createElement("div");
        const id = document.createElement("div");
        id.className = "history-id";
        id.textContent = r.run_id;

        const tm = document.createElement("div");
        tm.className = "history-time";
        tm.textContent = r.mtime_iso || "";

        left.appendChild(id);
        left.appendChild(tm);

        const btn = document.createElement("button");
        btn.className = "btn btn-primary btn-small history-load";
        btn.textContent = "Load";
        btn.addEventListener("click", async () => {
          await loadRun(r.run_id);
          closeHistoryModal();
        });

        row.appendChild(left);
        row.appendChild(btn);
        historyList.appendChild(row);
      });
    } catch (e) {
      console.error(e);
      historyList.innerHTML = "Error loading history.";
    }
  }

  async function loadRun(runId) {
    setStatus(`Loading ${runId}…`);
    try {
      const res = await fetch(`/api/run/${encodeURIComponent(runId)}`);
      const data = await res.json();
      if (!data.ok) {
        setStatus(data.error || "Failed to load run.", true);
        return;
      }

      // Load run into UI
      setRunUI(data);

      // Keep UI clean: assets list remains separate (uploaded assets are not reloaded)
      // But you can clear prompt/assets manually with Clear/New button.

      setStatus("Loaded ✅");
    } catch (e) {
      console.error(e);
      setStatus("Error loading run.", true);
    }
  }

  // init state
  resetUI();
});
