document.addEventListener('DOMContentLoaded', function () {
    // ---------- SIDEBAR ----------
    const sidebar = document.getElementById('sidebar');
    const burgerBtn = document.getElementById('burgerBtn');
    let expanded = false;

    if (burgerBtn) {
        burgerBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            expanded = !expanded;
            sidebar.classList.toggle('expanded', expanded);
        });
    }

    document.addEventListener('click', function (e) {
        if (expanded && !sidebar.contains(e.target) && e.target !== burgerBtn) {
            expanded = false;
            sidebar.classList.remove('expanded');
        }
    });

    // ---------- CASH FLOW SUBMENU ----------
    const cashflowMenu = document.getElementById('cashflowMenu');
    const cashflowSubmenu = document.getElementById('cashflowSubmenu');
    if (cashflowMenu && cashflowSubmenu) {
        cashflowMenu.addEventListener('click', function (e) {
            if (!expanded) {
                expanded = true;
                sidebar.classList.add('expanded');
            }
            cashflowMenu.classList.toggle('open');
            cashflowSubmenu.classList.toggle('open');
        });
    }

    // ---------- AFGHAN CALENDAR ----------
    function getShamsiDate(gDate) {
        const g = new Date(gDate);
        const nowruz = new Date(g.getFullYear(), 2, 21);
        let shYear, days;
        if (g >= nowruz) {
            shYear = g.getFullYear() - 621;
            days = Math.floor((g - nowruz) / (1000 * 60 * 60 * 24)) + 1;
        } else {
            shYear = g.getFullYear() - 622;
            const prevNowruz = new Date(g.getFullYear() - 1, 2, 21);
            days = Math.floor((g - prevNowruz) / (1000 * 60 * 60 * 24)) + 1;
        }
        const monthLengths = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29];
        const monthNames = ['حمل', 'ثور', 'جوزا', 'سرطان', 'اسد', 'سنبله',
                            'میزان', 'عقرب', 'قوس', 'جدی', 'دلو', 'حوت'];
        const dayNames = ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه'];
        let rem = days, mIdx = 0;
        for (let i = 0; i < monthLengths.length; i++) {
            if (rem <= monthLengths[i]) { mIdx = i; break; }
            rem -= monthLengths[i];
        }
        const dow = g.getDay();
        return {
            formatted: `${dayNames[dow]}، ${rem} ${monthNames[mIdx]} ${shYear}`,
            formattedShort: `${shYear}/${String(mIdx + 1).padStart(2, '0')}/${String(rem).padStart(2, '0')}`
        };
    }

    function updateDate() {
        const now = new Date();
        const shamsi = getShamsiDate(now);
        const shamsiDateEl = document.getElementById('shamsiDate');
        const gregorianDateEl = document.getElementById('gregorianDate');
        if (shamsiDateEl) shamsiDateEl.textContent = shamsi.formatted;
        if (gregorianDateEl) gregorianDateEl.textContent = now.toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric'
        });
    }
    updateDate();

    // ---------- DASHBOARD CHART (global) ----------
    window.buildChart = function (data) {
        const container = document.getElementById('barChart');
        if (!container) return;
        if (!data || !data.labels || data.labels.length === 0) {
            container.innerHTML = '<p style="text-align:center; padding:20px; color:#6c6c6a;">No transaction data for the last 6 months.</p>';
            return;
        }
        const labels = data.labels;
        const incomes = data.income;
        const expenses = data.expense;
        const maxVal = Math.max(...incomes, ...expenses, 1);

        let html = '';
        for (let i = 0; i < labels.length; i++) {
            const inHeight = (incomes[i] / maxVal) * 140;
            const outHeight = (expenses[i] / maxVal) * 140;
            html += `
            <div class="bar-col">
                <div class="bar-amount">${(incomes[i] / 1000000).toFixed(1)}M</div>
                <div class="bar inflow" style="height:${Math.max(inHeight, 4)}px;" title="IN: AFN ${incomes[i].toLocaleString()}"></div>
                <div class="bar outflow" style="height:${Math.max(outHeight, 4)}px;" title="OUT: AFN ${expenses[i].toLocaleString()}"></div>
                <div class="bar-label">${labels[i]}</div>
            </div>`;
        }
        container.innerHTML = html;
    };

    // ---------- AUTO-BUILD CHART IF DATA EXISTS ----------
    if (window.dashboardChartData) {
        window.buildChart(window.dashboardChartData);
    }
    // Make tables horizontally scrollable by dragging (mobile)
document.querySelectorAll('.panel').forEach(panel => {
    let isDown = false, startX, scrollLeft;
    panel.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - panel.offsetLeft;
        scrollLeft = panel.scrollLeft;
        panel.style.cursor = 'grabbing';
    });
    panel.addEventListener('mouseleave', () => { isDown = false; panel.style.cursor = ''; });
    panel.addEventListener('mouseup', () => { isDown = false; panel.style.cursor = ''; });
    panel.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - panel.offsetLeft;
        const walk = (x - startX) * 1.5;
        panel.scrollLeft = scrollLeft - walk;
    });
});
});