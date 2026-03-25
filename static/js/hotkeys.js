/* 
 * hotkeys.js - Global keyboard navigation for the POS system using Mousetrap 
 * Requires: Mousetrap.js, SweetAlert2
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // Help dialog mapping F1
    Mousetrap.bind('f1', (e) => {
        e.preventDefault();
        Swal.fire({
            title: 'Keyboard Shortcuts',
            html: `
                <div style="text-align: left;">
                    <p><b>Global</b></p>
                    <ul>
                        <li><kbd>F1</kbd> - Show this help</li>
                        <li><kbd>Shift + D</kbd> - Dashboard</li>
                        <li><kbd>Shift + S</kbd> - New Sale</li>
                        <li><kbd>Shift + P</kbd> - Products</li>
                    </ul>
                    <hr/>
                    <p><b>POS / New Sale Screen</b></p>
                    <ul>
                        <li><kbd>F2</kbd> - Focus Product Search</li>
                        <li><kbd>F4</kbd> - Focus overall Discount</li>
                        <li><kbd>F8</kbd> - Complete Sale</li>
                        <li><kbd>Escape</kbd> - Clear / Cancel action</li>
                    </ul>
                </div>
            `,
            icon: 'info',
            confirmButtonText: 'Got it!'
        });
    });

    // Global navigation
    Mousetrap.bind('shift+d', (e) => {
        window.location.href = '/dashboard/';
    });

    Mousetrap.bind('shift+s', (e) => {
        window.location.href = '/sales/new/';
    });

    Mousetrap.bind('shift+p', (e) => {
        window.location.href = '/products/';
    });

    // We allow inputs to trigger Mousetrap by using mousetrap-global or binding directly on inputs
    // For Mousetrap standard, inputs don't trigger unless we use the 'global' plugin or handle it.
    // Mousetrap ignores inputs by default. To allow shortcuts like F2, F4 inside inputs, we must override:
    Mousetrap.prototype.stopCallback = function(e, element, combo) {
        // if the element has the class "mousetrap" then no need to stop
        if ((' ' + element.className + ' ').indexOf(' mousetrap ') > -1) {
            return false;
        }
        
        // F-keys should always work, even inside inputs
        if (combo.startsWith('f')) {
            return false;
        }

        // stop for input, select, and textarea
        return element.tagName == 'INPUT' || element.tagName == 'SELECT' || element.tagName == 'TEXTAREA' || (element.contentEditable && element.contentEditable == 'true');
    };

    console.log("Global hotkeys loaded. Press F1 for help.");
});
