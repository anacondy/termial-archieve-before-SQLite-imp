// Terminal simulation script
const output = document.getElementById('output');
const searchModal = document.getElementById('search-modal');
const searchInput = document.getElementById('search-input');
const mobileSearchInput = document.getElementById('mobile-search-input');

let commandHistory = [];
let historyIndex = -1;

// Sample paper database (in a real app, this would come from backend)
const papers = [
    { subject: 'Physics', year: 2024, filename: 'physics_2024.pdf' },
    { subject: 'Mathematics', year: 2024, filename: 'math_2024.pdf' },
    { subject: 'Chemistry', year: 2023, filename: 'chem_2023.pdf' },
    { subject: 'Physics', year: 2023, filename: 'physics_2023.pdf' },
];

// Terminal initialization
function initTerminal() {
    printWelcome();
    showPrompt();
}

function printWelcome() {
    const welcome = `
╔═══════════════════════════════════════════════════════════════╗
║         TERMINAL ARCHIVE - Previous Year Papers              ║
║                                                               ║
║  Type 'help' for available commands                          ║
║  Press Ctrl+K to search database                             ║
╚═══════════════════════════════════════════════════════════════╝

System initialized...
Loading paper archive...
Ready.

`;
    output.textContent = welcome;
}

function showPrompt() {
    const prompt = '\n$ ';
    output.textContent += prompt;
}

function handleCommand(command) {
    command = command.trim().toLowerCase();
    
    if (!command) {
        showPrompt();
        return;
    }
    
    commandHistory.push(command);
    historyIndex = commandHistory.length;
    
    output.textContent += '\n';
    
    switch (command) {
        case 'help':
            output.textContent += `
Available commands:
  help     - Show this help message
  list     - List all available papers
  search   - Search for papers
  upload   - Go to upload page
  clear    - Clear terminal screen
  exit     - Return to main page
`;
            break;
            
        case 'list':
            output.textContent += '\nAvailable Papers:\n';
            papers.forEach((paper, index) => {
                output.textContent += `  ${index + 1}. ${paper.subject} (${paper.year})\n`;
            });
            break;
            
        case 'search':
            openSearchModal();
            return; // Don't show prompt yet
            
        case 'upload':
            window.location.href = '/upload';
            return;
            
        case 'clear':
            output.textContent = '';
            printWelcome();
            showPrompt();
            return;
            
        case 'exit':
            output.textContent += '\nGoodbye!\n';
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
            return;
            
        default:
            output.textContent += `Command not found: ${command}\nType 'help' for available commands.\n`;
    }
    
    showPrompt();
}

// Search modal functions
function openSearchModal() {
    searchModal.classList.remove('hidden');
    searchInput.focus();
}

function closeSearchModal() {
    searchModal.classList.add('hidden');
    searchInput.value = '';
    showPrompt();
}

function performSearch(query) {
    query = query.toLowerCase();
    const results = papers.filter(paper => 
        paper.subject.toLowerCase().includes(query) || 
        paper.year.toString().includes(query)
    );
    
    closeSearchModal();
    
    output.textContent += `\nSearch results for "${query}":\n`;
    if (results.length > 0) {
        results.forEach((paper, index) => {
            output.textContent += `  ${index + 1}. ${paper.subject} (${paper.year})\n`;
        });
    } else {
        output.textContent += '  No papers found.\n';
    }
}

// Event listeners
document.addEventListener('keydown', (e) => {
    // Ctrl+K to open search
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        openSearchModal();
    }
    
    // Esc to close search
    if (e.key === 'Escape') {
        closeSearchModal();
    }
});

if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                performSearch(query);
            }
        }
    });
}

if (mobileSearchInput) {
    mobileSearchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = mobileSearchInput.value.trim();
            if (query) {
                performSearch(query);
                mobileSearchInput.value = '';
            }
        }
    });
}

// Click outside to close modal
if (searchModal) {
    searchModal.addEventListener('click', (e) => {
        if (e.target === searchModal) {
            closeSearchModal();
        }
    });
}

// Simulate terminal input (for demo purposes)
// In a real implementation, you would add an input field
document.addEventListener('keypress', (e) => {
    if (e.target === searchInput || e.target === mobileSearchInput) {
        return;
    }
    
    // Simple command simulation - in real app, use proper input field
    if (e.key === 'Enter') {
        // This is just a placeholder
        // Real implementation would capture typed commands
    }
});

// Initialize terminal on page load
window.addEventListener('DOMContentLoaded', initTerminal);
