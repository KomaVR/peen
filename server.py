import express from 'express';
import net from 'net';

const app = express();

app.use(express.json());

let servers = [];

app.post('/attack', (req, res) => {
    const ip = req.body.ip;
    const port = parseInt(req.body.port);

    try {
        // Try to parse the input as an IPv4 or IPv6 address
        const ipaddress = require('ipaddress');
        ipaddress.ip_address(ip);
    } catch (e) {
        console.log("Invalid IP address. Please enter a valid IPv4 or IPv6 address.");
        res.status(400).send({ error: 'Invalid IP address' });
        return;
    }

    // Validate the input to ensure it's a valid port number
    if (isNaN(port) || !Number.isInteger(port) || !port >= 0 && port <= 65535) {
        console.log("Invalid port number. Please enter a valid port number between 0 and 65535.");
        res.status(400).send({ error: 'Invalid port number' });
        return;
    }

    // Log the target IP address and port number
    console.log(`Target IP: ${ip}, Target Port: ${port}`);

    // Perform application layer attacks on the target IP address and port number
    perform_application_layer_attacks(ip, port).then(() => {
        res.status(200).send({ message: 'Attack completed successfully' });
    }).catch((e) => {
        console.log(`Error performing attack: ${e}`);
        res.status(500).send({ error: 'Error performing attack' });
    });
});

app.get('/servers', (req, res) => {
    // Send the list of servers to the client
    res.send(servers);
});

const perform_application_layer_attacks = async (ip, port) => {
    return new Promise((resolve, reject) => {
        const sock = net.createConnection(port, ip);

        sock.on('connect', () => {
            console.log(`Connected to ${ip}:${port}`);
            // Simulate a simple application layer attack by sending a GET request
            sock.write("GET / HTTP/1.0\r\nHost: invalid-host\r\nConnection: close\r\n\r\n");
            resolve();
        });

        sock.on('error', (e) => {
            console.log(`Error connecting to ${ip}:${port}: ${e}`);
            reject(e);
        });
    });
};

app.listen(3000, () => {
    console.log('Server listening on port 3000');
});
