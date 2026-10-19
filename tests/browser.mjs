import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
const port = 18768,
  base = `http://127.0.0.1:${port}`;
const server = spawn(
  process.env.PYTHON || 'python3',
  ['-m', 'invoice_contract', 'serve', String(port)],
  { stdio: ['ignore', 'pipe', 'inherit'] },
);
let browser;
try {
  for (let i = 0; i < 100; i++) {
    try {
      if ((await fetch(base)).ok) break;
    } catch {}
    if (server.exitCode !== null) throw Error('server exited');
    if (i === 99) throw Error('server timeout');
    await new Promise((r) => setTimeout(r, 100));
  }
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1300, height: 1000 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const lang of ['fr', 'en', 'es']) {
    await page.goto(`${base}/?lang=${lang}`);
    await page.waitForFunction(() => document.getElementById('available').textContent === '1');
    assert.equal(await page.locator('html').getAttribute('lang'), lang);
    assert.equal(await page.locator('.finding').count(), 2);
    await page.locator('#prepare').click();
    await page.waitForSelector('.proposal-status');
    assert.match(await page.locator('#proposal').textContent(), /12.50/);
    assert.equal(await page.locator('.change').count(), 2);
    const event = page.waitForEvent('download');
    await page.locator('#download').click();
    assert.equal((await event).suggestedFilename(), 'invoice-acceptance-proposal.json');
    await page.locator('#missing').check();
    await page.locator('#audit').click();
    await page.waitForFunction(() => document.getElementById('available').textContent !== '1');
    assert.match(
      await page.locator('#available').textContent(),
      { fr: /inconnue/, en: /unknown/, es: /desconocida/ }[lang],
    );
    await page.locator('#prepare').click();
    await page.waitForSelector('.proposal-status');
    assert.equal(await page.locator('.change').count(), 0);
    await page.locator('#basis').selectOption('ordered');
    await page.locator('#audit').click();
    await page.waitForFunction(() => document.getElementById('available').textContent === '8');
    await page.locator('#prepare').click();
    await page.waitForSelector('.proposal-status');
    assert.match(await page.locator('#proposal').textContent(), /50.00/);
  }
  await page.goto(`${base}/?lang=fr`);
  await page.waitForFunction(() => document.getElementById('available').textContent === '1');
  await page.locator('#prepare').click();
  await page.waitForSelector('.proposal-status');
  await mkdir('.local', { recursive: true });
  await page.screenshot({ path: '.local/preview-fr.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  assert.deepEqual(errors, []);
  console.log(
    'FR/EN/ES: exact reconciliation, draft, unknown evidence, ordered basis, export and mobile verified.',
  );
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}
