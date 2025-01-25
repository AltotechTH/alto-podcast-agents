const express = require('express');
const cors = require('cors');
const fs = require('fs');
const qr = require('qrcode');
const readline = require('readline');

const app = express();
const port = 4000;

// Create readline interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Initialize server with IP input
function startServer(serverIP) {
    app.use(cors());
    app.use(express.json());

    // Store submissions in a JSON file
    const submissionsFile = 'submissions.json';

    // Initialize submissions file if it doesn't exist
    if (!fs.existsSync(submissionsFile)) {
        fs.writeFileSync(submissionsFile, '[]');
    }

    // Create public directory if it doesn't exist
    if (!fs.existsSync('public')) {
        fs.mkdirSync('public');
    }

    // Read the HTML template
    const htmlTemplate = fs.readFileSync('public/form.html', 'utf8');

    // Serve the form with dynamic IP
    app.get('/', (req, res) => {
        const modifiedHtml = htmlTemplate.replace('/submit', `http://${serverIP}:${port}/submit`);
        res.send(modifiedHtml);
    });

    app.use(express.static('public'));

    app.post('/submit', (req, res) => {
        try {
            const submissions = JSON.parse(fs.readFileSync(submissionsFile));
            submissions.push(req.body);
            fs.writeFileSync(submissionsFile, JSON.stringify(submissions, null, 2));
            console.log('New submission received:', req.body);
            res.status(200).json({ message: 'Submission received' });
        } catch (error) {
            console.error('Error saving submission:', error);
            res.status(500).json({ error: 'Error saving submission' });
        }
    });

    const formURL = `http://${serverIP}:${port}`;

    // Generate QR code
    qr.toFile('public/form-qr.png', formURL, {
        color: {
            dark: '#000000',
            light: '#ffffff'
        }
    }, (err) => {
        if (err) console.error('Error generating QR code:', err);
        else console.log('QR code generated successfully');
    });

    app.listen(port, () => {
        console.log(`Server running at ${formURL}`);
        console.log('Scan the QR code to submit questions');
    });
}

// Get available network interfaces
const networkInterfaces = require('os').networkInterfaces();
const addresses = [];

// Collect all IPv4 addresses
Object.keys(networkInterfaces).forEach((interfaceName) => {
    networkInterfaces[interfaceName].forEach((interface) => {
        if (interface.family === 'IPv4' && !interface.internal) {
            addresses.push(interface.address);
        }
    });
});

// Show available IPs and prompt for selection
console.log('\nAvailable IP addresses:');
addresses.forEach((ip, index) => {
    console.log(`${index + 1}. ${ip}`);
});

rl.question('\nEnter the number of the IP to use (or enter a custom IP): ', (answer) => {
    let selectedIP;
    
    // Check if the input is a number corresponding to an available IP
    const index = parseInt(answer) - 1;
    if (!isNaN(index) && index >= 0 && index < addresses.length) {
        selectedIP = addresses[index];
    } else {
        // Use custom IP input
        selectedIP = answer;
    }
    
    console.log(`Using IP address: ${selectedIP}`);
    startServer(selectedIP);
    rl.close();
}); 