from playwright.sync_api import Playwright, sync_playwright
import time
import os
import re

# --- CONFIGURATION ---
WP_URL = ""
USERNAME = ""
PASSWORD = ""
PLUGIN_SLUG = "all-in-one-wp-migration"
PLUGIN_NAME = "All-in-One WP Migration"

# --- BASE SAVE DIR ON EC2 INSTANCE ---
BASE_EC2_DIR = "/home/ubuntu/backup-receiver/recieved_wp"

# --- UTILITY FUNCTIONS ---

def get_safe_site_name(url):
    """Generates a filesystem-safe folder name from the URL."""
    name = re.sub(r'https?://', '', url).strip('/')
    name = re.sub(r':\d+', '', name)
    return re.sub(r'[^\w\s-]', '_', name).strip().lower()

def install_plugin_via_search(page):
    """Navigates to Add New Plugin page and installs the plugin."""
    print("   -> Plugin not found on installed list. Navigating to Add New.")
    page.goto(f"{WP_URL}/wp-admin/plugin-install.php", wait_until="domcontentloaded")
    
    page.fill("#search-plugins", PLUGIN_NAME)
    page.press("#search-plugins", "Enter")
    
    page.wait_for_selector(f'a.install-now[data-slug="{PLUGIN_SLUG}"]', timeout=15000)
    install_selector = page.locator(f'a.install-now[data-slug="{PLUGIN_SLUG}"]')
    
    install_selector.click()
    print("   -> Install clicked. Waiting for activation...")

    activate_selector_post_install = page.get_by_role("button", name="Activate")
    activate_selector_post_install.wait_for(timeout=60000)
    activate_selector_post_install.click()
    print("   -> Plugin installed and activated successfully.")
    return True

def ensure_plugin_active(page):
    """Ensures the plugin is installed and active, handles all states safely."""
    plugin_row = page.locator(f'tr[data-slug="{PLUGIN_SLUG}"]')
    plugin_row.wait_for(timeout=30000)

    deactivate_link = plugin_row.locator("a:has-text('Deactivate')")
    if deactivate_link.is_visible():
        print("   -> Plugin is already ACTIVE. Proceeding to export.")
        return True

    activate_link = plugin_row.locator("a:has-text('Activate')")
    if activate_link.is_visible():
        print("   -> Plugin is inactive. Activating now...")
        activate_link.click()
        for attempt in range(3):
            try:
                deactivate_link.wait_for(state="visible", timeout=10000)
                print("   -> Plugin activated successfully.")
                return True
            except:
                print(f"   -> Waiting for plugin activation... attempt {attempt+1}")
                time.sleep(2)
        raise Exception("Plugin activation failed after retries.")

    print("   -> Plugin not installed. Installing...")
    install_plugin_via_search(page)
    return True

# --- MAIN WORKFLOW ---

def run_migration_workflow(wp_url, admin_user, admin_pass):
    # 1. Derive and Prepare Site Folder
    wp_site_folder = get_safe_site_name(wp_url)
    site_save_dir = os.path.join(BASE_EC2_DIR, wp_site_folder)
    if not os.path.exists(site_save_dir):
        os.makedirs(site_save_dir)
        print(f"   -> Created site backup directory: {site_save_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            # --- PHASE 1: LOGIN ---
            print("--- PHASE 1: LOGIN ---")
            page.goto(f"{wp_url}/wp-admin/", timeout=60000)
            page.fill("#user_login", admin_user)
            page.fill("#user_pass", admin_pass)
            page.click("#wp-submit")
            page.wait_for_selector("#wpadminbar", timeout=60000)
            print("   -> Login successful.")

            # --- PHASE 2: CHECK & INSTALL PLUGIN ---
            print("--- PHASE 2: CHECK & INSTALL PLUGIN ---")
            page.goto(f"{wp_url}/wp-admin/plugins.php")
            page.wait_for_load_state('networkidle', timeout=30000)
            ensure_plugin_active(page)

            # --- PHASE 3: TRIGGER EXPORT & DOWNLOAD ---
            print("--- PHASE 3: TRIGGER EXPORT & LOCAL DOWNLOAD ON EC2 ---")
            page.goto(f"{wp_url}/wp-admin/admin.php?page=ai1wm_export")
            
            # Wait until 'Export Site To' button is ready
            export_button_locator = page.locator('div.ai1wm-button-main')
            export_button_locator.wait_for(state="visible", timeout=60000)

            for attempt in range(3):
                try:
                    print(f"   -> Clicking 'Export Site To' button (Attempt {attempt+1}/3)...")
                    export_button_locator.click(force=True, timeout=10000)
                    break
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Failed to click 'Export Site To' button after 3 attempts. Last error: {e}")
                    time.sleep(5)

            print("   -> Clicking 'File' to initiate backup...")
            page.locator("#ai1wm-export-file").click()

            # Wait for download button to appear
            print("   -> Waiting for backup to complete and download button to appear...")
            with page.expect_download(timeout=300000) as download_info:
                download_link_locator = page.locator('a.ai1wm-button-download')
                download_link_locator.wait_for(state="visible", timeout=300000)
                download_link_locator.click(force=True)

            download = download_info.value
            final_filename = download.suggested_filename
            final_save_path = os.path.join(site_save_dir, final_filename)
            download.save_as(final_save_path)
            print(f"   ✅ Backup file saved to EC2 at: {final_save_path}")

            page.get_by_role("button", name="CLOSE").click()
            print("\n--- WORKFLOW COMPLETE ---")
            print(f"File is located in site-specific folder: {site_save_dir}")
            return True

        except Exception as e:
            print(f"\n❌ FATAL WORKFLOW ERROR: {e}")
            return False

        finally:
            browser.close()

if __name__ == '__main__':
    if run_migration_workflow(WP_URL, USERNAME, PASSWORD):
        print("MIGRATION TOOL: SUCCESS. Check backup files.")
    else:
        print("MIGRATION TOOL: FAILURE. Review logs for error details.")
