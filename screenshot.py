"""
screenshot.py — Auto-capture 2 screenshot deliverable menggunakan Selenium.
Jalankan saat app Streamlit masih running (streamlit run app.py).

Output:
  screenshots/screenshot_1_full_map.png  — Tampilan penuh dengan legenda
  screenshots/screenshot_2_popup.png     — Tampilan pop-up yang sedang diklik
"""

import os
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Installing selenium...")
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC


SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
APP_URL = "http://localhost:8501"


def setup_driver():
    """Setup Chrome WebDriver."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--force-device-scale-factor=1")
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver


def wait_for_streamlit(driver, timeout=30):
    """Tunggu Streamlit app fully loaded."""
    print("  Waiting for Streamlit to load...")
    driver.get(APP_URL)
    
    # Wait for Streamlit to finish loading (the running indicator disappears)
    time.sleep(5)
    
    # Wait for iframe (Folium map is rendered inside an iframe by streamlit-folium)
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        print("  ✅ Map iframe found")
    except Exception:
        print("  ⚠️ Map iframe not found, continuing anyway...")
    
    # Extra wait for map tiles to load
    time.sleep(8)
    print("  ✅ Page loaded")


def screenshot_full_map(driver):
    """Screenshot 1: Tampilan penuh dengan legenda."""
    print("\n📸 Taking Screenshot 1: Full map with legend...")
    
    filepath = os.path.join(SCREENSHOT_DIR, "screenshot_1_full_map.png")
    driver.save_screenshot(filepath)
    print(f"  ✅ Saved: {filepath}")
    return filepath


def screenshot_popup(driver):
    """Screenshot 2: Klik marker dan capture pop-up."""
    print("\n📸 Taking Screenshot 2: Pop-up clicked...")
    
    try:
        # Find the Folium map iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            # Switch to the map iframe
            driver.switch_to.frame(iframes[0])
            print("  Switched to map iframe")
            
            # Try to find and click a circle marker (SVG circle elements in Leaflet)
            time.sleep(2)
            
            # Leaflet renders CircleMarkers as SVG <circle> or <path> elements
            circles = driver.find_elements(By.CSS_SELECTOR, "circle, path.leaflet-interactive")
            
            if circles:
                # Click the first visible marker
                for circle in circles:
                    try:
                        if circle.is_displayed():
                            ActionChains(driver).move_to_element(circle).click().perform()
                            print(f"  ✅ Clicked marker")
                            time.sleep(2)  # Wait for popup to render
                            break
                    except Exception:
                        continue
            else:
                # Fallback: click on the map center area where markers likely are
                print("  ⚠️ No SVG markers found, clicking map center...")
                map_el = driver.find_element(By.CLASS_NAME, "leaflet-container")
                ActionChains(driver).move_to_element(map_el).click().perform()
                time.sleep(2)
            
            # Switch back to main content for screenshot
            driver.switch_to.default_content()
        
    except Exception as e:
        print(f"  ⚠️ Could not click marker: {e}")
        driver.switch_to.default_content()
    
    filepath = os.path.join(SCREENSHOT_DIR, "screenshot_2_popup.png")
    driver.save_screenshot(filepath)
    print(f"  ✅ Saved: {filepath}")
    return filepath


def main():
    print("=" * 60)
    print("  SCREENSHOT TOOL — Auto-capture 2 deliverable screenshots")
    print("=" * 60)
    
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    driver = setup_driver()
    
    try:
        wait_for_streamlit(driver)
        
        # Screenshot 1: Full map
        path1 = screenshot_full_map(driver)
        
        # Screenshot 2: Click popup
        path2 = screenshot_popup(driver)
        
        print("\n" + "=" * 60)
        print("  ✅ SELESAI! 2 screenshot tersimpan di folder: screenshots/")
        print(f"  1. {path1}")
        print(f"  2. {path2}")
        print("=" * 60)
        
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
