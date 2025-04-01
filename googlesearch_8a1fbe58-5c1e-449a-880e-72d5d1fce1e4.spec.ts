
import { test } from '@playwright/test';
import { expect } from '@playwright/test';

test('GoogleSearch_2025-03-29', async ({ page, context }) => {
  
    // Navigate to URL
    await page.goto('https://www.google.com');

    // Fill input field
    await page.fill('textarea[name='q']', 'melhor bolo de chocolate');

    // Navigate to URL
    await page.goto('https://duckduckgo.com');

    // Fill input field
    await page.fill('input[name='q']', 'melhor bolo de chocolate receita');

    // Take screenshot
    await page.screenshot({ path: 'duckduckgo_results.png.png', { fullPage: true } });
});