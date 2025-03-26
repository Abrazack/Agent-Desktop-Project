require('dotenv').config(); // Load environment variables
const fetch = globalThis.fetch;

const express = require('express');

const app = express();  // ✅ Initialize Express
const PORT = 3000;
const API_KEY = process.env.OPENROUTER_API_KEY; // Load API Key from .env

app.use(express.json()); // ✅ Middleware to parse JSON requests

// ✅ POST Route for Chat API
app.post('/api/chat', async (req, res) => {
    try {
        console.log("Received message:", req.body.message);

        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${API_KEY}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "deepseek/deepseek-chat-v3-0324:free",
                messages: [{ role: "user", content: req.body.message }]
            })
        });

        const responseBody = await response.text(); // Read response as text
        console.log("API Response:", responseBody);

        if (!response.ok) {
            throw new Error(`API request failed with status: ${response.status} - ${responseBody}`);
        }

        res.json(JSON.parse(responseBody));

    } catch (error) {
        console.error("API Request Failed:", error);
        res.status(500).json({ error: "Internal Server Error", details: error.message });
    }
});

// ✅ Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
