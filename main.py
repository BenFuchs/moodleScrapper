from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    
    try:
        page.goto("https://nidp.tau.ac.il/nidp/saml2/sso?id=10&sid=0&option=credential&sid=0", timeout=60000)

        page.fill('input#Ecom_User_ID', 'netarosh')  # Fills in username
        page.fill('input#Ecom_User_Pid', '323817932')  # Fills in ID 
        page.fill('input#Ecom_Password', 'Lols31415!')  # Fills in password 
        page.get_by_role('button').click()  # Tries to log in 

        # Wait for navigation after login
        page.wait_for_load_state('networkidle', timeout=120000)  # Wait until there are no more network connections for at least 500 ms

        # Wait for the specific div to be visible and then click it
        page.wait_for_selector('div:has-text("Moodle - מודל")', timeout=60000)
        # Click the div to open a new tab
        page.click('span:has-text("Moodle - מודל")')

        # Wait for the new page/tab to open
        with page.expect_popup() as popup_info:
            page.click('div:has-text("Moodle - מודל")')  # Click to open the new tab
        new_page = popup_info.value  # Get the new page object

        # Wait for the new page to load
        new_page.wait_for_load_state('networkidle', timeout=120000)

        # You can now perform actions on the new page
        print("New page URL:", new_page.url)
        scrap_page = 'https://moodle.tau.ac.il/course/view.php?id=509142401' #goes directly to the page
        new_page.goto(scrap_page)
        # new_page.wait_for_selector('h6:has-text("0509142401 - אלגברה ליניארית לתלמידי הנדסת תעשייה וניהול")', timeout=60000)
        # new_page.click('h6:has-text("0509142401 - אלגברה ליניארית לתלמידי הנדסת תעשייה וניהול")')
        # page.wait_for_load_state('networkidle', timeout=120000)  # Wait until there are no more network connections for at least 500 ms

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
