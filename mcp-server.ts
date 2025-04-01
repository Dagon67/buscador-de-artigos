import express from 'express';
import { chromium, firefox, webkit, Browser, Page, BrowserContext } from 'playwright';
import cors from 'cors';

class PlaywrightMCPServer {
    private app = express();
    private browser: Browser | null = null;
    private context: BrowserContext | null = null;
    private page: Page | null = null;
    private port = 3000;

    constructor() {
        this.setupServer();
    }

    private setupServer() {
        this.app.use(express.json());
        this.app.use(cors());

        // Initialize browser with specific engine
        this.app.post('/init', async (req, res) => {
            try {
                const { browser = 'chromium', headless = false } = req.body;
                const engines = { chromium, firefox, webkit };
                
                if (!engines[browser]) {
                    throw new Error(`Invalid browser engine: ${browser}. Use chromium, firefox, or webkit.`);
                }

                this.browser = await engines[browser].launch({ headless });
                this.context = await this.browser.newContext();
                this.page = await this.context.newPage();
                
                res.json({ 
                    status: 'success', 
                    message: `Browser initialized: ${browser}`,
                    data: { browser, headless }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Navigate to URL
        this.app.post('/navigate', async (req, res) => {
            try {
                const { url, waitUntil = 'load' } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                const response = await this.page.goto(url, { waitUntil });
                const status = response?.status();
                
                res.json({ 
                    status: 'success', 
                    message: 'Navigation complete',
                    data: { url, status }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Click element
        this.app.post('/click', async (req, res) => {
            try {
                const { selector, options = {} } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                await this.page.click(selector, options);
                res.json({ 
                    status: 'success', 
                    message: 'Click performed',
                    data: { selector }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Fill form field
        this.app.post('/fill', async (req, res) => {
            try {
                const { selector, value, options = {} } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                await this.page.fill(selector, value, options);
                res.json({ 
                    status: 'success', 
                    message: 'Field filled',
                    data: { selector, value }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Get element text
        this.app.post('/getText', async (req, res) => {
            try {
                const { selector } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                const text = await this.page.textContent(selector);
                res.json({ 
                    status: 'success', 
                    data: { selector, text }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Take screenshot
        this.app.post('/screenshot', async (req, res) => {
            try {
                const { path, options = {} } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                const buffer = await this.page.screenshot({ path, ...options });
                res.json({ 
                    status: 'success', 
                    message: 'Screenshot taken',
                    data: { path }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Check if element exists
        this.app.post('/exists', async (req, res) => {
            try {
                const { selector } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                const element = await this.page.$(selector);
                res.json({ 
                    status: 'success', 
                    data: { selector, exists: element !== null }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Execute JavaScript in page context
        this.app.post('/evaluate', async (req, res) => {
            try {
                const { script, args = [] } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                const result = await this.page.evaluate(script, ...args);
                res.json({ 
                    status: 'success', 
                    data: { result }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Wait for selector
        this.app.post('/waitForSelector', async (req, res) => {
            try {
                const { selector, options = {} } = req.body;
                if (!this.page) throw new Error('Browser not initialized');
                
                await this.page.waitForSelector(selector, options);
                res.json({ 
                    status: 'success', 
                    message: 'Element found',
                    data: { selector }
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Close browser
        this.app.post('/close', async (req, res) => {
            try {
                if (this.context) {
                    await this.context.close();
                    this.context = null;
                }
                if (this.browser) {
                    await this.browser.close();
                    this.browser = null;
                }
                this.page = null;
                
                res.json({ 
                    status: 'success', 
                    message: 'Browser closed'
                });
            } catch (error) {
                res.status(500).json({ status: 'error', message: error.message });
            }
        });

        // Get server status
        this.app.get('/status', (req, res) => {
            res.json({
                status: 'running',
                browserActive: this.browser !== null,
                contextActive: this.context !== null,
                pageActive: this.page !== null
            });
        });
    }

    public start() {
        this.app.listen(this.port, () => {
            console.log(`Playwright MCP Server running on http://localhost:${this.port}`);
            console.log('Available endpoints:');
            console.log('  POST /init - Initialize browser');
            console.log('  POST /navigate - Navigate to URL');
            console.log('  POST /click - Click element');
            console.log('  POST /fill - Fill form field');
            console.log('  POST /getText - Get element text');
            console.log('  POST /screenshot - Take screenshot');
            console.log('  POST /exists - Check if element exists');
            console.log('  POST /evaluate - Execute JavaScript');
            console.log('  POST /waitForSelector - Wait for element');
            console.log('  POST /close - Close browser');
            console.log('  GET /status - Get server status');
        });
    }
}

// Start server
const server = new PlaywrightMCPServer();
server.start(); 