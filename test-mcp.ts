import axios from 'axios';

const BASE_URL = 'http://localhost:3000';

async function testMCPServer() {
    try {
        // Test server status before starting
        console.log('Checking server status...');
        const initialStatus = await axios.get(`${BASE_URL}/status`);
        console.log('Initial status:', initialStatus.data);

        // Initialize browser with Firefox
        console.log('Initializing Firefox browser...');
        await axios.post(`${BASE_URL}/init`, {
            browser: 'firefox',
            headless: false
        });

        // Check server status after browser init
        const statusAfterInit = await axios.get(`${BASE_URL}/status`);
        console.log('Status after init:', statusAfterInit.data);

        // Navigate to Google
        console.log('Navigating to Google...');
        const navResponse = await axios.post(`${BASE_URL}/navigate`, {
            url: 'https://www.google.com',
            waitUntil: 'networkidle'
        });
        console.log('Navigation response:', navResponse.data);

        // Wait for search input
        console.log('Waiting for search input...');
        await axios.post(`${BASE_URL}/waitForSelector`, {
            selector: 'textarea[name="q"]',
            options: { state: 'visible' }
        });

        // Fill search field
        console.log('Filling search field...');
        await axios.post(`${BASE_URL}/fill`, {
            selector: 'textarea[name="q"]',
            value: 'Playwright automation testing'
        });

        // Take screenshot before search
        console.log('Taking screenshot before search...');
        await axios.post(`${BASE_URL}/screenshot`, {
            path: 'google-before-search.png',
            options: { fullPage: true }
        });

        // Check if search button exists
        console.log('Checking search button...');
        const buttonExists = await axios.post(`${BASE_URL}/exists`, {
            selector: 'input[name="btnK"]'
        });
        console.log('Search button exists:', buttonExists.data);

        // Execute JavaScript to get page title
        console.log('Getting page title via JavaScript...');
        const evalResult = await axios.post(`${BASE_URL}/evaluate`, {
            script: 'document.title'
        });
        console.log('Page title:', evalResult.data);

        // Click search button
        console.log('Clicking search button...');
        await axios.post(`${BASE_URL}/click`, {
            selector: 'input[name="btnK"]',
            options: { force: true }
        });

        // Wait for search results
        console.log('Waiting for search results...');
        await axios.post(`${BASE_URL}/waitForSelector`, {
            selector: '#search'
        });

        // Get search results text
        console.log('Getting search results text...');
        const searchResults = await axios.post(`${BASE_URL}/getText`, {
            selector: '#search'
        });
        console.log('Search results:', searchResults.data);

        // Take screenshot after search
        console.log('Taking screenshot after search...');
        await axios.post(`${BASE_URL}/screenshot`, {
            path: 'google-after-search.png',
            options: { fullPage: true }
        });

        // Close browser
        console.log('Closing browser...');
        await axios.post(`${BASE_URL}/close`);

        // Verify final status
        const finalStatus = await axios.get(`${BASE_URL}/status`);
        console.log('Final status:', finalStatus.data);

        console.log('Test completed successfully!');
    } catch (error) {
        console.error('Error during test:', error.message);
        if (error.response) {
            console.error('Error response:', error.response.data);
        }
    }
}

// Run the test
console.log('Starting Playwright MCP Server test...');
testMCPServer(); 