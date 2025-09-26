from playwright.sync_api import Playwright, sync_playwright
import time
import os

WP_URL = "http://wp.development.t4gc.in"
USERNAME = "abhiramnj"
PASSWORD = "Word@t4gc@2026"
PLUGIN_SLUG = "all-in-one-wp-migration"
PLUGIN_NAME = "All-in-One WP Migration"

# --- LOCAL PATH ON EC2 INSTANCE ---
EC2_SAVE_DIR = "/home/ubuntu/backup-receiver/recieved_wp"
LOCAL_DOWNLOAD_PATH = os.path.join(EC2_SAVE_DIR, "latest_wp_backup.wpress")

def install_plugin_via_search(page):
    """Navigates to Add New Plugin page and installs the plugin."""
    print("   -> Plugin not found on installed list. Navigating to Add New.")
    page.goto(f"{WP_URL}/wp-admin/plugin-install.php")
    
    search_term = PLUGIN_NAME
    page.fill("#search-plugins", search_term)
    page.press("#search-plugins", "Enter")
    page.wait_for_load_state("networkidle")
    time.sleep(5) 

    install_selector = page.locator(f'a.install-now[data-slug="{PLUGIN_SLUG}"]')
    
    try:
        install_selector.wait_for(state="visible", timeout=10000)
    except Exception:
        print("FATAL: Install Now button not found after search.")
        return False

    install_selector.click()
    print("   -> Install button clicked. Waiting for activation...")

    activate_selector_post_install = page.get_by_role("button", name="Activate")
    activate_selector_post_install.wait_for(timeout=60000)
    activate_selector_post_install.click()
    print("   -> Plugin installed and activated successfully.")
    return True

def run_migration_workflow(wp_url, admin_user, admin_pass):
    # Ensure the target directory exists on the EC2 instance
    if not os.path.exists(EC2_SAVE_DIR):
        os.makedirs(EC2_SAVE_DIR)
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("--- PHASE 1: LOGIN ---")
        page.goto(f"{wp_url}/wp-admin/")
        page.fill("#user_login", admin_user)
        page.fill("#user_pass", admin_pass)
        page.click("#wp-submit")
        page.wait_for_selector("#wpadminbar")
        print("   -> Login successful.")

        print("--- PHASE 2: CHECK & INSTALL PLUGIN ---")
        
        page.goto(f"{wp_url}/wp-admin/plugins.php")
        time.sleep(3) 

        plugin_row = page.locator(f'tr[data-slug="{PLUGIN_SLUG}"]')
        
        if not plugin_row.is_visible():
            if not install_plugin_via_search(page):
                browser.close()
                return False
        else:
            activate_link = plugin_row.get_by_role("link", name="Activate")
            if activate_link.is_visible():
                activate_link.click()
                print("   -> Plugin was inactive. Activated successfully.")
            else:
                print("   -> Plugin is installed and active. Proceeding to export.")

        print("--- PHASE 3: TRIGGER EXPORT & LOCAL DOWNLOAD ON EC2 ---")
        
        page.goto(f"{wp_url}/wp-admin/admin.php?page=ai1wm_export")
        
        with page.expect_download() as download_info:
            
            print("   -> Clicking 'Export Site To' button...")
            export_button_locator = page.locator('div.ai1wm-button-main:has-text("Export Site To")')
            export_button_locator.click()
            
            print("   -> Clicking 'File' to initiate backup and download...")
            page.locator("#ai1wm-export-file").click()
            
            print("   -> Backup is running. Waiting for completion and download button...")
            
            # --- FINAL FIX: Wait only for the download button's visibility ---
            download_link_locator = page.locator('a.ai1wm-button-download')
            
            download_link_locator.wait_for(state="visible", timeout=300000) 
            print("   -> Download button visible. Proceeding to download.")

            # Use force=True on the click to bypass final stability checks
            download_link_locator.click(force=True) 
        
        download = download_info.value
        final_filename = download.suggested_filename
        final_save_path = os.path.join(EC2_SAVE_DIR, final_filename)

        download.save_as(final_save_path)
        print(f"   ✅ Backup file created and saved to EC2 at: {final_save_path}")
        
        # 4. Dismiss the modal
        page.get_by_role("button", name="CLOSE").click()
        time.sleep(2) 

        print("\n--- WORKFLOW COMPLETE ---")
        print(f"Backup transfer complete. File is located on the EC2 instance at: {final_save_path}")
        browser.close()
        return True

if __name__ == '__main__':
    run_migration_workflow(WP_URL, USERNAME, PASSWORD)
