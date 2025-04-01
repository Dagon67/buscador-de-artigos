
import { test } from '@playwright/test';
import { expect } from '@playwright/test';

test('GoogleSearchTest_2025-03-30', async ({ page, context }) => {
  
    // Set custom user agent
    await context.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36');

    // Navigate to URL
    await page.goto('https://www.google.com/?hl=pt-BR', { waitUntil: 'networkidle' });

    // Fill input field
    await page.fill('textarea[name='q']', 'r');

    // Fill input field
    await page.fill('textarea[name='q']', 'receita de bolo de chocolate');

    // Take screenshot
    await page.screenshot({ path: 'google_search_results.png.png', { fullPage: true } });

    // Navigate to URL
    await page.goto('https://www.google.com/search?q=receita+de+bolo+de+chocolate&gl=br&hl=pt-BR&pws=0');
});