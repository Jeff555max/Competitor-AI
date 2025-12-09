// Frontend logic for Competitor Monitor
const apiBase = '';

// === Анализ текста ===
document.getElementById('text-form').onsubmit = async function(e) {
    e.preventDefault();
    const text = document.getElementById('text-input').value;
    const res = await fetch(apiBase + '/analyze_text', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
    });
    const data = await res.json();
    const result = document.getElementById('text-result');
    if (data.success && data.analysis) {
        result.innerHTML = renderTextAnalysis(data.analysis);
    } else {
        result.innerHTML = `<div class="result-block">Ошибка: ${data.error}</div>`;
    }
};

function renderTextAnalysis(a) {
    return `<div class="result-block"><b>Сильные стороны:</b> <ul>${a.strengths.map(x=>`<li>${x}</li>`).join('')}</ul></div>
    <div class="result-block"><b>Слабые стороны:</b> <ul>${a.weaknesses.map(x=>`<li>${x}</li>`).join('')}</ul></div>
    <div class="result-block"><b>Уникальные предложения:</b> <ul>${a.unique_offers.map(x=>`<li>${x}</li>`).join('')}</ul></div>
    <div class="result-block"><b>Рекомендации:</b> <ul>${a.recommendations.map(x=>`<li>${x}</li>`).join('')}</ul></div>
    <div class="result-block"><b>Резюме:</b> ${a.summary}</div>`;
}

// === Анализ изображения ===
document.getElementById('image-form').onsubmit = async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('image-input');
    if (!fileInput.files.length) return;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    const res = await fetch(apiBase + '/analyze_image', {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    const result = document.getElementById('image-result');
    if (data.success && data.analysis) {
        result.innerHTML = renderImageAnalysis(data.analysis);
    } else {
        result.innerHTML = `<div class="result-block">Ошибка: ${data.error}</div>`;
    }
};

function renderImageAnalysis(a) {
    return `<div class="result-block"><b>Описание:</b> ${a.description}</div>
    <div class="result-block"><b>Инсайты:</b> <ul>${a.insights.map(x=>`<li>${x}</li>`).join('')}</ul></div>
    <div class="result-block"><b>Оценка стиля:</b> ${a.visual_style_score}/10</div>
    <div class="result-block"><b>Рекомендации:</b> <ul>${a.recommendations.map(x=>`<li>${x}</li>`).join('')}</ul></div>`;
}

// === Парсинг сайта ===
document.getElementById('parse-form').onsubmit = async function(e) {
    e.preventDefault();
    const url = document.getElementById('url-input').value;
    const res = await fetch(apiBase + '/parse_demo', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url})
    });
    const data = await res.json();
    const result = document.getElementById('parse-result');
    if (data.success && data.analysis) {
        result.innerHTML = renderTextAnalysis(data.analysis);
    } else {
        result.innerHTML = `<div class="result-block">Ошибка: ${data.error}</div>`;
    }
};

// === История ===
async function loadHistory() {
    const res = await fetch(apiBase + '/history');
    const data = await res.json();
    const list = document.getElementById('history-list');
    if (data.items && data.items.length) {
        list.innerHTML = data.items.map(item => `
            <div class="result-block">
                <b>${item.request_type}</b> — ${item.request_summary}<br>
                <small>${item.timestamp}</small><br>
                <i>${item.response_summary}</i>
            </div>
        `).join('');
    } else {
        list.innerHTML = '<div class="result-block">История пуста</div>';
    }
}
document.getElementById('refresh-history').onclick = loadHistory;
document.getElementById('clear-history').onclick = async function() {
    await fetch(apiBase + '/history', {method: 'DELETE'});
    loadHistory();
};
loadHistory();
