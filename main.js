// ── State ─────────────────────────────────────────────────
let mediaRecorder = null;
let audioChunks = [];
let recordingTimer = null;
let recSeconds = 0;
let selectedFile = null;

// ── Emotion Colors ─────────────────────────────────────────
const emotionColors = {
  neutral: '#94a3b8', calm: '#60a5fa', happy: '#fbbf24', sad: '#818cf8',
  angry: '#f87171', fearful: '#a78bfa', disgust: '#34d399', surprised: '#fb923c'
};

// ── DOM Refs ───────────────────────────────────────────────
const uploadZone    = document.getElementById('uploadZone');
const fileInput     = document.getElementById('fileInput');
const fileSelected  = document.getElementById('fileSelected');
const fileName      = document.getElementById('fileName');
const recordBtn     = document.getElementById('recordBtn');
const recordingState = document.getElementById('recordingState');
const loadingState  = document.getElementById('loadingState');
const resultState   = document.getElementById('resultState');
const analyzeBtn    = document.getElementById('analyzeBtn');
const clearBtn      = document.getElementById('clearBtn');
const stopBtn       = document.getElementById('stopBtn');
const recTimer      = document.getElementById('recTimer');

// ── Drag & Drop ────────────────────────────────────────────
uploadZone.addEventListener('dragover', e => {
  e.preventDefault();
  uploadZone.classList.add('drag-over');
});
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault();
  uploadZone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('audio/')) selectFile(file);
});

// ── File Input ─────────────────────────────────────────────
fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) selectFile(fileInput.files[0]);
});

function selectFile(file) {
  selectedFile = file;
  fileName.textContent = file.name;
  uploadZone.classList.add('hidden');
  fileSelected.classList.remove('hidden');
}

// ── Clear ──────────────────────────────────────────────────
clearBtn.addEventListener('click', resetDemo);

function resetDemo() {
  selectedFile = null;
  fileInput.value = '';
  uploadZone.classList.remove('hidden');
  fileSelected.classList.add('hidden');
  recordingState.classList.add('hidden');
  loadingState.classList.add('hidden');
  resultState.classList.add('hidden');
}

// ── Analyze ────────────────────────────────────────────────
analyzeBtn.addEventListener('click', () => {
  if (selectedFile) analyzeFile(selectedFile);
});

async function analyzeFile(file) {
  fileSelected.classList.add('hidden');
  loadingState.classList.remove('hidden');

  const formData = new FormData();
  formData.append('audio', file);

  try {
    const res = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();

    loadingState.classList.add('hidden');

    if (data.error) {
      alert('Error: ' + data.error);
      resetDemo();
      return;
    }

    showResult(data);
  } catch (err) {
    loadingState.classList.add('hidden');
    alert('Failed to connect to server. Make sure Flask is running.');
    resetDemo();
  }
}

function showResult(data) {
  document.getElementById('resultEmoji').textContent = data.emoji;
  document.getElementById('resultLabel').textContent = data.emotion;
  document.getElementById('resultLabel').style.color = data.color;
  document.getElementById('resultConf').textContent = data.confidence + '%';

  const container = document.getElementById('barsContainer');
  container.innerHTML = '';

  // Sort by score descending
  const sorted = Object.entries(data.scores).sort((a, b) => b[1] - a[1]);

  sorted.forEach(([emotion, pct]) => {
    const color = emotionColors[emotion] || '#94a3b8';
    const row = document.createElement('div');
    row.className = 'bar-row';
    row.innerHTML = `
      <div class="bar-label">${emotion}</div>
      <div class="bar-track">
        <div class="bar-fill" style="width: 0%; background: ${color}"></div>
      </div>
      <div class="bar-pct">${pct}%</div>
    `;
    container.appendChild(row);

    // Animate bar after paint
    requestAnimationFrame(() => {
      setTimeout(() => {
        row.querySelector('.bar-fill').style.width = pct + '%';
      }, 50);
    });
  });

  resultState.classList.remove('hidden');
  resultState.style.animation = 'fadeIn 0.4s ease';
}

// ── Microphone Recording ───────────────────────────────────
recordBtn.addEventListener('click', async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = () => {
      stream.getTracks().forEach(t => t.stop());
      clearInterval(recordingTimer);
      const blob = new Blob(audioChunks, { type: 'audio/wav' });
      const file = new File([blob], 'recorded_audio.wav', { type: 'audio/wav' });

      uploadZone.classList.add('hidden');
      recordingState.classList.add('hidden');

      selectedFile = file;
      fileName.textContent = 'recorded_audio.wav';
      fileSelected.classList.remove('hidden');
    };

    mediaRecorder.start();
    recSeconds = 0;
    recTimer.textContent = '0s';
    recordingTimer = setInterval(() => {
      recSeconds++;
      recTimer.textContent = recSeconds + 's';
      if (recSeconds >= 30) stopRecording(); // auto stop at 30s
    }, 1000);

    uploadZone.classList.add('hidden');
    recordingState.classList.remove('hidden');
  } catch (err) {
    alert('Microphone access denied or not available.');
  }
});

stopBtn.addEventListener('click', stopRecording);

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
}

// ── Smooth scroll for nav links ────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
