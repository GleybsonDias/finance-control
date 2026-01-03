import traceback
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8001'
OUT = 'screenshots'

print('Starting Playwright script...')
try:
    with sync_playwright() as p:
        print('Launching browser...')
        browser = p.chromium.launch()
        page = browser.new_page()

        print('Opening login page...')
        page.goto(f'{BASE}/login/')
        page.screenshot(path=f'{OUT}/real_login.png', full_page=True)

        print('Logging in...')
        page.fill('input[name="username"]', 'recruiter')
        page.fill('input[name="password"]', 'recruiterpass')
        page.click('button[type="submit"]')
        page.wait_for_url(f'{BASE}/')

        print('Capturing dashboard...')
        page.screenshot(path=f'{OUT}/real_dashboard.png', full_page=True)

        print('Capturing transactions list...')
        page.goto(f'{BASE}/transactions/')
        page.screenshot(path=f'{OUT}/real_transactions_list.png', full_page=True)

        print('Capturing transaction form...')
        page.goto(f'{BASE}/transactions/new/')
        page.screenshot(path=f'{OUT}/real_transaction_form.png', full_page=True)

        print('Capturing categories...')
        page.goto(f'{BASE}/categories/')
        page.screenshot(path=f'{OUT}/real_categories.png', full_page=True)

        print('Capturing goals...')
        page.goto(f'{BASE}/goals/')
        page.screenshot(path=f'{OUT}/real_goals.png', full_page=True)

        print('Capturing profile...')
        page.goto(f'{BASE}/profile/')
        page.screenshot(path=f'{OUT}/real_profile.png', full_page=True)

        browser.close()

    print('Screenshots saved in screenshots/')
except Exception:
    print('Error during screenshot capture:')
    traceback.print_exc()
