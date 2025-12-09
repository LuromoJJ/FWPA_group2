const calendarContainer = document.getElementById('calendar-container');
const medicineSchedule = JSON.parse(calendarContainer.dataset.schedule);

const calendarGrid = document.getElementById('calendar-grid');
const monthDisplay = document.getElementById('calendar-month');

let currentDate = new Date();

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    monthDisplay.textContent = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });

    calendarGrid.innerHTML = '';

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty cells before first day
    for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.classList.add('calendar-cell', 'empty');
        calendarGrid.appendChild(emptyCell);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const cell = document.createElement('div');
        cell.classList.add('calendar-cell');
        cell.textContent = day;

        // Add medicines scheduled for this day
        const dayMeds = medicineSchedule.filter(med => {
            const medDate = new Date(med.schedule_time);
            return medDate.getDate() === day && medDate.getMonth() === month && medDate.getFullYear() === year;
        });

        if (dayMeds.length > 0) {
            const list = document.createElement('ul');
            dayMeds.forEach(m => {
                const li = document.createElement('li');
                li.textContent = `${m.medication} @ ${new Date(m.schedule_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;
                list.appendChild(li);
            });
            cell.appendChild(list);
        }

        calendarGrid.appendChild(cell);
    }
}

document.querySelector('.calendar-prev').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

document.querySelector('.calendar-next').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Initialize calendar
renderCalendar();