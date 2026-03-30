/**
 * Queens Game — core game logic
 */
(function () {
  "use strict";

  // === Constants ===
  const EMPTY = 0;
  const MARK = 1;
  const QUEEN = 2;
  const STATE_COUNT = 3;
  const QUEEN_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 20h20v2H2zM5 17h14l1.5-9-4.5 3L12 5l-4 6-4.5-3z"/></svg>';

  const REGION_COLORS = {
    light: [
      "#5bb8d9", "#7cc9a0", "#f0a870", "#c88abf", "#e8cc4a",
      "#e88585", "#8aade0", "#b8a07a", "#6ebfbf", "#c88ac8",
    ],
    dark: [
      "#1e7faa", "#2e8f50", "#c08030", "#8f3e8a", "#b09820",
      "#b83a3a", "#3a60c0", "#8a7040", "#2a9595", "#8a3a9a",
    ],
  };

  // === Init: bail early if not on a game page ===
  const boardEl = document.getElementById("game-board");
  if (!boardEl) return;

  const lang = boardEl.dataset.lang || "en";

  // === Parse grid ===
  const rawGrid = boardEl.dataset.grid.trim();
  const rows = rawGrid.split("\n").map((r) => r.trim()).filter((r) => r.length > 0);
  const gridSize = rows.length;
  const grid = rows.map((row) => [...row]);

  document.documentElement.style.setProperty("--grid-size", gridSize);

  const charToRegion = {};
  let regionCount = 0;
  for (const row of grid) {
    for (const ch of row) {
      if (!(ch in charToRegion)) {
        charToRegion[ch] = regionCount++;
      }
    }
  }

  // === State ===
  let cellStates = createEmptyStates();
  let moveHistory = [];
  let moveCount = 0;
  let timerSeconds = 0;
  let timerInterval = null;
  let gameWon = false;

  const settings = {
    hideTimer: localStorage.getItem("qs-hide-timer") === "true",
    hideMoves: localStorage.getItem("qs-hide-moves") === "true",
  };

  function createEmptyStates() {
    return Array.from({ length: gridSize }, () => Array(gridSize).fill(EMPTY));
  }

  function cloneStates() {
    return cellStates.map((row) => [...row]);
  }

  function getQueens() {
    const queens = [];
    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        if (cellStates[r][c] === QUEEN) queens.push({ row: r, col: c });
      }
    }
    return queens;
  }

  // === Timer & Display ===
  const timerEl = document.getElementById("timer");
  const movesEl = document.getElementById("moves");

  function applySettings() {
    timerEl.classList.toggle("hidden", settings.hideTimer);
    movesEl.classList.toggle("hidden", settings.hideMoves);
  }
  applySettings();

  function formatTime(seconds) {
    const m = String(Math.floor(seconds / 60)).padStart(2, "0");
    const s = String(seconds % 60).padStart(2, "0");
    return `${m}:${s}`;
  }

  function formatMoves(n) {
    if (lang === "uk") {
      const mod100 = n % 100;
      if (mod100 >= 11 && mod100 <= 19) return n + " ходів";
      const mod10 = mod100 % 10;
      if (mod10 === 1) return n + " хід";
      if (mod10 >= 2 && mod10 <= 4) return n + " ходи";
      return n + " ходів";
    }
    return n + (n === 1 ? " move" : " moves");
  }

  function updateTimerDisplay() {
    timerEl.textContent = formatTime(timerSeconds);
  }

  function updateMovesDisplay() {
    movesEl.textContent = formatMoves(moveCount);
  }

  function startTimer() {
    if (timerInterval) return;
    timerInterval = setInterval(() => {
      timerSeconds++;
      updateTimerDisplay();
    }, 1000);
  }

  function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
  }

  function resetTimer() {
    stopTimer();
    timerSeconds = 0;
    updateTimerDisplay();
  }

  // === Build Board ===
  boardEl.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`;
  const cells = [];

  for (let r = 0; r < gridSize; r++) {
    cells[r] = [];
    for (let c = 0; c < gridSize; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";

      // Region borders
      if (r === 0 || grid[r - 1][c] !== grid[r][c]) cell.classList.add("border-top");
      if (r === gridSize - 1 || grid[r + 1][c] !== grid[r][c]) cell.classList.add("border-bottom");
      if (c === 0 || grid[r][c - 1] !== grid[r][c]) cell.classList.add("border-left");
      if (c === gridSize - 1 || grid[r][c + 1] !== grid[r][c]) cell.classList.add("border-right");

      cell.addEventListener("pointerup", (e) => {
        e.preventDefault();
        if (e.pointerType === "touch") {
          onCellCycle(r, c);
        } else if (e.button === 0) {
          onCellToggleMark(r, c);
        } else if (e.button === 2) {
          onCellToggleQueen(r, c);
        }
      });
      cell.addEventListener("contextmenu", (e) => e.preventDefault());

      boardEl.appendChild(cell);
      cells[r][c] = cell;
    }
  }

  // === Theme-aware cell colors ===
  function paintCells() {
    const theme = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
    const colors = REGION_COLORS[theme];
    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        const idx = charToRegion[grid[r][c]];
        cells[r][c].style.backgroundColor = colors[idx % colors.length];
      }
    }
  }
  paintCells();

  new MutationObserver(paintCells).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });

  // === Cell Actions ===
  function applyMove(row, col, newState) {
    if (gameWon) return;
    if (!timerInterval) startTimer();
    moveHistory.push(cloneStates());
    moveCount++;
    cellStates[row][col] = newState;
    updateMovesDisplay();
    renderBoard();
    if (newState === QUEEN) checkWin();
  }

  function onCellCycle(row, col) {
    applyMove(row, col, (cellStates[row][col] + 1) % STATE_COUNT);
  }

  function onCellToggleMark(row, col) {
    applyMove(row, col, cellStates[row][col] === MARK ? EMPTY : MARK);
  }

  function onCellToggleQueen(row, col) {
    applyMove(row, col, cellStates[row][col] === QUEEN ? EMPTY : QUEEN);
  }

  // === Rendering ===
  function renderBoard() {
    const queens = getQueens();
    const conflicts = findConflicts(queens);

    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        const cell = cells[r][c];
        cell.classList.remove("has-queen", "has-mark", "cell-error");
        cell.innerHTML = "";

        const state = cellStates[r][c];
        if (state === MARK) {
          cell.classList.add("has-mark");
          const span = document.createElement("span");
          span.className = "mark";
          span.textContent = "\u2715";
          cell.appendChild(span);
        } else if (state === QUEEN) {
          cell.classList.add("has-queen");
          const span = document.createElement("span");
          span.className = "queen";
          span.innerHTML = QUEEN_SVG;
          cell.appendChild(span);
          if (conflicts.has(`${r},${c}`)) {
            cell.classList.add("cell-error");
          }
        }
      }
    }
  }

  // === Game Logic ===
  function findConflicts(queens) {
    const conflicted = new Set();
    for (let i = 0; i < queens.length; i++) {
      for (let j = i + 1; j < queens.length; j++) {
        const a = queens[i];
        const b = queens[j];
        const dr = Math.abs(a.row - b.row);
        const dc = Math.abs(a.col - b.col);

        const isConflict =
          a.row === b.row ||
          a.col === b.col ||
          (dr <= 1 && dc <= 1) ||
          grid[a.row][a.col] === grid[b.row][b.col];

        if (isConflict) {
          conflicted.add(`${a.row},${a.col}`);
          conflicted.add(`${b.row},${b.col}`);
        }
      }
    }
    return conflicted;
  }

  function checkWin() {
    const queens = getQueens();
    if (queens.length !== regionCount) return;
    if (findConflicts(queens).size > 0) return;

    const coveredRegions = new Set(queens.map((q) => grid[q.row][q.col]));
    if (coveredRegions.size !== regionCount) return;

    gameWon = true;
    stopTimer();

    document.getElementById("win-time").textContent = formatTime(timerSeconds);
    document.getElementById("win-overlay").classList.add("active");
  }

  // === Controls ===
  function fullReset() {
    cellStates = createEmptyStates();
    moveHistory = [];
    moveCount = 0;
    gameWon = false;
    resetTimer();
    updateMovesDisplay();
    renderBoard();
    document.getElementById("win-overlay").classList.remove("active");
  }

  document.getElementById("btn-undo").addEventListener("click", () => {
    if (moveHistory.length === 0 || gameWon) return;
    cellStates = moveHistory.pop();
    moveCount = Math.max(0, moveCount - 1);
    updateMovesDisplay();
    renderBoard();
  });

  document.getElementById("btn-restart").addEventListener("click", fullReset);
  document.getElementById("btn-replay").addEventListener("click", fullReset);

  // === Modals ===
  function bindModal(openBtnId, overlayId, closeBtnId) {
    const overlay = document.getElementById(overlayId);
    document.getElementById(openBtnId).addEventListener("click", () => {
      overlay.classList.add("active");
    });
    if (closeBtnId) {
      document.getElementById(closeBtnId).addEventListener("click", () => {
        overlay.classList.remove("active");
      });
    }
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) overlay.classList.remove("active");
    });
  }

  bindModal("btn-how-to-play", "modal-overlay", "btn-close-modal");
  bindModal("btn-settings", "settings-overlay", "btn-close-settings");

  // === Random Level ===
  document.getElementById("btn-random").addEventListener("click", () => {
    try {
      const levelData = JSON.parse(document.getElementById("level-urls").textContent);
      const currentLevel = Number(boardEl.dataset.level);
      const others = levelData.filter((l) => l.level !== currentLevel);
      if (others.length > 0) {
        window.location.href = others[Math.floor(Math.random() * others.length)].url;
      }
    } catch (_) { /* ignore malformed data */ }
  });

  // === Settings ===
  function bindSetting(checkboxId, key) {
    const cb = document.getElementById(checkboxId);
    cb.checked = settings[key];
    cb.addEventListener("change", () => {
      settings[key] = cb.checked;
      localStorage.setItem("qs-" + key.replace(/([A-Z])/g, "-$1").toLowerCase(), settings[key]);
      applySettings();
    });
  }

  bindSetting("setting-hide-timer", "hideTimer");
  bindSetting("setting-hide-moves", "hideMoves");
})();
