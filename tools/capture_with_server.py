import subprocess
import time
import urllib.request
import os
import signal
import traceback

PY = r"C:/Users/Gleybson Dias/OneDrive/Projetos/finance/Scripts/python.exe"
BASE = 'http://127.0.0.1:8001'
OUT = 'screenshots'

p = None
try:
    print('Starting Django server...')
    p = subprocess.Popen([PY, 'manage.py', 'runserver', '127.0.0.1:8001'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to start
    for i in range(30):
        try:
            with urllib.request.urlopen(BASE, timeout=1) as resp:
                print('Server is responding')
                break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError('Server did not start in time')

    # Now run the playwright script
    from tools.capture_screenshots import sync_playwright, capture_sequence

    # Call a function variant (we need to modify capture_screenshots to expose a callable),
    # but for simplicity we'll reimplement the steps here using Playwright directly.
    from playwright.sync_api import sync_playwright
    print('Launching Playwright...')
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(f'{BASE}/login/')
        page.screenshot(path=f'{OUT}/real_login.png', full_page=True)
        page.fill('input[name="username"]','recruiter')
        page.fill('input[name="password"]','recruiterpass')
        page.click('button[type="submit"]')
        page.wait_for_url(f'{BASE}/')
        page.screenshot(path=f'{OUT}/real_dashboard.png', full_page=True)
        page.goto(f'{BASE}/transactions/')
        page.screenshot(path=f'{OUT}/real_transactions_list.png', full_page=True)
        page.goto(f'{BASE}/transactions/new/')
        page.screenshot(path=f'{OUT}/real_transaction_form.png', full_page=True)
        page.goto(f'{BASE}/categories/')
        page.screenshot(path=f'{OUT}/real_categories.png', full_page=True)
        page.goto(f'{BASE}/goals/')
        page.screenshot(path=f'{OUT}/real_goals.png', full_page=True)
        page.goto(f'{BASE}/profile/')
        page.screenshot(path=f'{OUT}/real_profile.png', full_page=True)
        browser.close()

    print('Screenshots saved.')

except Exception:
    print('Error:')
    traceback.print_exc()
finally:
    if p:
        print('Stopping server...')
        p.terminate()
        try:
            p.wait(timeout=5)
        except Exception:
            p.kill()
