import { test, expect } from '@playwright/test';

test.describe('Browser Automation Tests', () => {
  test('Google search test', async ({ page }) => {
    // Navigate to Google
    await page.goto('https://www.google.com');
    
    // Verify title
    await expect(page).toHaveTitle(/Google/);
    
    // Type in search
    await page.waitForSelector('textarea[name="q"]');
    await page.fill('textarea[name="q"]', 'Playwright testing');
    await page.keyboard.press('Enter');
    
    // Wait for results and verify
    await page.waitForSelector('#search');
    const results = await page.$$('#search .g');
    expect(results.length).toBeGreaterThan(0);
    
    // Take screenshot of results
    await page.screenshot({ path: 'screenshots/google-search-results.png' });
  });

  test('GitHub navigation test', async ({ page }) => {
    // Navigate to GitHub
    await page.goto('https://github.com');
    
    // Click sign in button if present
    const signInButton = page.getByRole('link', { name: 'Sign in' });
    if (await signInButton.isVisible()) {
      await signInButton.click();
    }
    
    // Verify navigation
    await expect(page).toHaveURL(/.*github.com.*/);
    
    // Take screenshot
    await page.screenshot({ path: 'screenshots/github-page.png' });
  });

  test('network monitoring', async ({ page }) => {
    // Listen to all network requests
    const requests: string[] = [];
    const responses: { url: string, status: number }[] = [];
    
    page.on('request', request => {
      requests.push(request.url());
    });
    
    page.on('response', response => {
      responses.push({
        url: response.url(),
        status: response.status()
      });
    });
    
    // Visit a website with multiple resources
    await page.goto('https://www.wikipedia.org');
    
    // Log network activity
    console.log('Requests made:', requests.length);
    console.log('Responses received:', responses.length);
    console.log('Response statuses:', responses.map(r => r.status));
  });

  test('form automation', async ({ page }) => {
    // Navigate to a form page (using GitHub signup as an example)
    await page.goto('https://github.com/signup');
    
    // Fill in form fields
    await page.waitForSelector('#email');
    await page.fill('#email', 'test@example.com');
    
    // Take screenshot
    await page.screenshot({ path: 'screenshots/form-filled.png' });
  });

  test('multiple tabs handling', async ({ context }) => {
    // Create first tab with GitHub
    const page1 = await context.newPage();
    await page1.goto('https://github.com');
    
    // Create second tab with Google
    const page2 = await context.newPage();
    await page2.goto('https://www.google.com');
    
    // Switch between tabs and verify content
    await page1.bringToFront();
    await expect(page1).toHaveURL(/.*github.com.*/);
    
    await page2.bringToFront();
    await expect(page2).toHaveURL(/.*google.com.*/);
    
    // Take screenshots of both tabs
    await page1.bringToFront();
    await page1.screenshot({ path: 'screenshots/tab1.png' });
    
    await page2.bringToFront();
    await page2.screenshot({ path: 'screenshots/tab2.png' });
  });

  test('responsive testing', async ({ page }) => {
    // Navigate to a responsive website
    await page.goto('https://www.wikipedia.org');
    
    // Test different viewport sizes
    const viewports = [
      { width: 1920, height: 1080, name: 'desktop' },
      { width: 1024, height: 768, name: 'tablet' },
      { width: 375, height: 667, name: 'mobile' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(1000); // Wait for layout to adjust
      await page.screenshot({
        path: `screenshots/responsive-${viewport.name}.png`,
        fullPage: true
      });
    }
  });

  test('keyboard and mouse interactions', async ({ page }) => {
    // Navigate to Google
    await page.goto('https://www.google.com');
    
    // Type with keyboard
    await page.waitForSelector('textarea[name="q"]');
    await page.click('textarea[name="q"]');
    await page.keyboard.type('Playwright automation', { delay: 100 }); // Slow typing
    
    // Use keyboard shortcuts
    await page.keyboard.press('Control+A');
    await page.keyboard.press('Control+C');
    await page.keyboard.press('Control+V');
    
    // Mouse movements
    await page.mouse.move(100, 100);
    await page.mouse.down();
    await page.mouse.move(200, 200);
    await page.mouse.up();
    
    // Take screenshot
    await page.screenshot({ path: 'screenshots/keyboard-mouse.png' });
  });
}); 