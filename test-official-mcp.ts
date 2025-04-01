import axios from 'axios';

const BASE_URL = 'http://localhost:7000'; // Official MCP server runs on port 7000

async function testOfficialMCPServer() {
    try {
        // Initialize browser session
        console.log('Initializing browser session...');
        const session = await axios.post(`${BASE_URL}/session/new`, {
            capabilities: {
                browserName: 'chromium',
                headless: false
            }
        });
        const sessionId = session.data.sessionId;
        console.log('Session created:', sessionId);

        // Navigate to Google
        console.log('Navigating to Google...');
        await axios.post(`${BASE_URL}/session/${sessionId}/url`, {
            url: 'https://www.google.com'
        });

        // Wait for search input
        console.log('Waiting for search input...');
        await axios.post(`${BASE_URL}/session/${sessionId}/element`, {
            selector: 'textarea[name="q"]',
            state: 'visible'
        });

        // Type into search field
        console.log('Typing search query...');
        await axios.post(`${BASE_URL}/session/${sessionId}/element/fill`, {
            selector: 'textarea[name="q"]',
            value: 'Playwright automation testing'
        });

        // Take screenshot
        console.log('Taking screenshot...');
        const screenshot = await axios.post(`${BASE_URL}/session/${sessionId}/screenshot`, {
            path: 'google-mcp-official.png'
        });
        console.log('Screenshot saved');

        // Click search button
        console.log('Clicking search button...');
        await axios.post(`${BASE_URL}/session/${sessionId}/element/click`, {
            selector: 'input[name="btnK"]'
        });

        // Wait for results
        console.log('Waiting for results...');
        await axios.post(`${BASE_URL}/session/${sessionId}/element`, {
            selector: '#search',
            state: 'visible'
        });

        // Get page title
        console.log('Getting page title...');
        const title = await axios.post(`${BASE_URL}/session/${sessionId}/evaluate`, {
            expression: 'document.title'
        });
        console.log('Page title:', title.data);

        // Close session
        console.log('Closing session...');
        await axios.delete(`${BASE_URL}/session/${sessionId}`);
        console.log('Session closed');

        console.log('Test completed successfully!');
    } catch (error) {
        console.error('Error during test:', error.message);
        if (error.response) {
            console.error('Error response:', error.response.data);
        }
    }
}

// Run the test
console.log('Starting Official Playwright MCP Server test...');
testOfficialMCPServer(); 