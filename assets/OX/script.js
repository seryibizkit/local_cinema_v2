let currentPlayer = 'X';
const grid = document.getElementById('grid');
const winningCombinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // Горизонтальные
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // Вертикальные
    [0, 4, 8], [2, 4, 6]            // Диагонали
];
let gameActive = true;

function createBoard() {
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.setAttribute('data-index', i);
        cell.addEventListener('click', onClick);
        grid.appendChild(cell);
        currentPlayer = 'X';
    }
}

function onClick(event) {
    const cell = event.target;
    const index = cell.getAttribute('data-index');

    if (cell.textContent === '' && gameActive) {
        cell.textContent = currentPlayer;
        checkWinner();
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    }
}

function checkWinner() {
    for (const combination of winningCombinations) {
        const [a, b, c] = combination;
        const cells = document.querySelectorAll('.cell');

        if (cells[a].textContent && 
            cells[a].textContent === cells[b].textContent && 
            cells[a].textContent === cells[c].textContent) {
            
            highlightWinner(cells[a], cells[b], cells[c]);
	         // alert(`${cells[a].textContent} выиграл!`);
            gameActive = false;
            return;
        }
    }
}

function highlightWinner(cell1, cell2, cell3) {
    cell1.classList.add('winner');
    cell2.classList.add('winner');
    cell3.classList.add('winner');
}

function resetGame() {
    grid.innerHTML = '';
    createBoard();
    gameActive = true;
}

createBoard();