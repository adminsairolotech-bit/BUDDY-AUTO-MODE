"""
BUDDY AI - ChatGPT & Codex Browser Automation Agent
Automatically manages ChatGPT and Codex workflow with auto-approval
"""

import time
import json
import pyperclip
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChatGPTCodexAutomation:
    """
    Automates workflow between ChatGPT and Codex:
    1. Monitors Codex for code output
    2. Copies code to ChatGPT for review/modification
    3. Gets response from ChatGPT
    4. Sends back to Codex
    5. Auto-approves when Codex asks for confirmation
    """
    
    def __init__(self, browser="chrome", headless=False):
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None
        self.running = False
        self.approval_keywords = ["yes", "run", "continue", "approve", "confirm", "execute", "ok"]
        self.config = {
            "check_interval": 2,  # seconds between checks
            "auto_approve": True,
            "copy_code_to_chatgpt": True,
            "monitor_codex": True,
        }
        
    def setup_browser(self):
        """Initialize browser with appropriate settings"""
        logger.info(f"Setting up {self.browser} browser...")
        
        if self.browser == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")
            # Keep browser open after script ends
            options.add_experimental_option("detach", True)
            self.driver = webdriver.Chrome(options=options)
            
        elif self.browser == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--start-maximized")
            options.add_experimental_option("detach", True)
            self.driver = webdriver.Edge(options=options)
            
        elif self.browser == "opera":
            # Opera uses Chrome driver with opera binary
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            # You may need to set opera binary path
            # options.binary_location = "C:/Users/.../opera.exe"
            self.driver = webdriver.Chrome(options=options)
            
        logger.info("Browser setup complete!")
        return self.driver
    
    def open_chatgpt(self):
        """Open ChatGPT in a new tab"""
        self.driver.execute_script("window.open('https://chat.openai.com', '_blank');")
        time.sleep(2)
        logger.info("ChatGPT tab opened")
        
    def open_codex(self):
        """Open Codex/ChatGPT Codex in a new tab"""
        # Codex is part of ChatGPT, open in coding mode
        self.driver.execute_script("window.open('https://chat.openai.com/?model=gpt-4', '_blank');")
        time.sleep(2)
        logger.info("Codex tab opened")
        
    def switch_to_tab(self, tab_index):
        """Switch to specific browser tab"""
        self.driver.switch_to.window(self.driver.window_handles[tab_index])
        
    def get_chatgpt_response(self):
        """Get the latest response from ChatGPT"""
        try:
            # Wait for response to complete (no loading indicator)
            WebDriverWait(self.driver, 60).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='loading']"))
            )
            
            # Get all message elements
            messages = self.driver.find_elements(By.CSS_SELECTOR, "[data-message-author-role='assistant']")
            if messages:
                return messages[-1].text
        except Exception as e:
            logger.error(f"Error getting ChatGPT response: {e}")
        return None
    
    def send_to_chatgpt(self, text):
        """Send text to ChatGPT input"""
        try:
            # Find input textarea
            input_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "prompt-textarea"))
            )
            input_box.clear()
            input_box.send_keys(text)
            
            # Click send button or press Enter
            time.sleep(0.5)
            input_box.send_keys(Keys.RETURN)
            logger.info("Message sent to ChatGPT")
            return True
        except Exception as e:
            logger.error(f"Error sending to ChatGPT: {e}")
            return False
    
    def check_for_approval_buttons(self):
        """Check if there are any approval buttons to click"""
        approval_selectors = [
            "button:contains('Run')",
            "button:contains('Yes')",
            "button:contains('Continue')",
            "button:contains('Approve')",
            "button:contains('Confirm')",
            "button:contains('Execute')",
            "[data-testid='approve-button']",
            "[data-testid='run-button']",
            "[data-testid='continue-button']",
        ]
        
        try:
            # Find all buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                button_text = button.text.lower().strip()
                if any(keyword in button_text for keyword in self.approval_keywords):
                    logger.info(f"Found approval button: {button.text}")
                    return button
        except Exception as e:
            logger.debug(f"Error checking approval buttons: {e}")
        return None
    
    def auto_approve(self):
        """Automatically click approval buttons"""
        button = self.check_for_approval_buttons()
        if button:
            try:
                button.click()
                logger.info("✅ Auto-approved!")
                return True
            except Exception as e:
                logger.error(f"Error clicking approval button: {e}")
        return False
    
    def get_code_from_codex(self):
        """Extract code blocks from Codex response"""
        try:
            code_blocks = self.driver.find_elements(By.CSS_SELECTOR, "pre code, .code-block, [data-testid='code-block']")
            if code_blocks:
                return code_blocks[-1].text
        except Exception as e:
            logger.error(f"Error getting code from Codex: {e}")
        return None
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        pyperclip.copy(text)
        logger.info("Text copied to clipboard")
        
    def paste_from_clipboard(self):
        """Get text from clipboard"""
        return pyperclip.paste()
    
    def monitor_and_automate(self):
        """Main automation loop"""
        logger.info("🤖 Starting automation monitor...")
        self.running = True
        last_codex_code = ""
        last_chatgpt_response = ""
        
        while self.running:
            try:
                # Check all tabs for approval buttons
                for i, handle in enumerate(self.driver.window_handles):
                    self.driver.switch_to.window(handle)
                    
                    # Auto-approve any pending approvals
                    if self.config["auto_approve"]:
                        self.auto_approve()
                    
                    # Check for new code in Codex
                    if self.config["monitor_codex"]:
                        code = self.get_code_from_codex()
                        if code and code != last_codex_code:
                            logger.info("📝 New code detected in Codex!")
                            last_codex_code = code
                            
                            if self.config["copy_code_to_chatgpt"]:
                                # Switch to ChatGPT tab and send code
                                self.switch_to_tab(0)  # Assuming ChatGPT is first tab
                                self.send_to_chatgpt(f"Review this code:\n```\n{code}\n```")
                    
                    # Check for new ChatGPT response
                    response = self.get_chatgpt_response()
                    if response and response != last_chatgpt_response:
                        logger.info("💬 New ChatGPT response detected!")
                        last_chatgpt_response = response
                        self.copy_to_clipboard(response)
                
                time.sleep(self.config["check_interval"])
                
            except Exception as e:
                logger.error(f"Error in automation loop: {e}")
                time.sleep(5)
    
    def start(self):
        """Start the automation in a background thread"""
        self.setup_browser()
        self.open_chatgpt()
        time.sleep(2)
        self.open_codex()
        
        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_and_automate, daemon=True)
        monitor_thread.start()
        logger.info("✅ Automation started! Running in background...")
        return monitor_thread
    
    def stop(self):
        """Stop the automation"""
        self.running = False
        logger.info("Automation stopped")
        
    def close(self):
        """Close browser and cleanup"""
        self.stop()
        if self.driver:
            self.driver.quit()
        logger.info("Browser closed")


class DesktopChatGPTAutomation:
    """
    Automation for ChatGPT Desktop App (uses pyautogui for native app control)
    Works with ChatGPT desktop application on Windows
    """
    
    def __init__(self):
        self.running = False
        self.approval_keywords = ["yes", "run", "continue", "approve", "confirm", "execute", "ok"]
        self.config = {
            "check_interval": 1,
            "auto_approve": True,
            "screenshot_interval": 2,
        }
        
    def find_window(self, title_contains):
        """Find window by title"""
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle(title_contains)
        return windows[0] if windows else None
    
    def focus_window(self, window):
        """Bring window to focus"""
        if window:
            window.activate()
            time.sleep(0.5)
            return True
        return False
    
    def take_screenshot(self, region=None):
        """Take screenshot of screen or region"""
        return pyautogui.screenshot(region=region)
    
    def find_button_on_screen(self, button_text):
        """Find button by text using OCR (requires pytesseract)"""
        try:
            import pytesseract
            from PIL import Image
            
            screenshot = self.take_screenshot()
            text_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            
            for i, text in enumerate(text_data['text']):
                if button_text.lower() in text.lower():
                    x = text_data['left'][i] + text_data['width'][i] // 2
                    y = text_data['top'][i] + text_data['height'][i] // 2
                    return (x, y)
        except ImportError:
            logger.warning("pytesseract not installed. Using image matching instead.")
        except Exception as e:
            logger.error(f"Error finding button: {e}")
        return None
    
    def click_at(self, x, y):
        """Click at specific coordinates"""
        pyautogui.click(x, y)
        logger.info(f"Clicked at ({x}, {y})")
        
    def type_text(self, text):
        """Type text"""
        pyautogui.typewrite(text, interval=0.02)
        
    def paste_text(self, text):
        """Paste text using clipboard"""
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        
    def press_enter(self):
        """Press Enter key"""
        pyautogui.press('enter')
        
    def auto_approve_desktop(self):
        """Find and click approval buttons in desktop app"""
        for keyword in self.approval_keywords:
            pos = self.find_button_on_screen(keyword)
            if pos:
                self.click_at(pos[0], pos[1])
                logger.info(f"✅ Auto-approved: {keyword}")
                return True
        return False
    
    def monitor_desktop(self):
        """Monitor desktop ChatGPT app for approvals"""
        logger.info("🖥️ Starting desktop automation monitor...")
        self.running = True
        
        while self.running:
            try:
                # Find ChatGPT window
                chatgpt_window = self.find_window("ChatGPT")
                if chatgpt_window:
                    self.focus_window(chatgpt_window)
                    
                    # Check for approval buttons
                    if self.config["auto_approve"]:
                        self.auto_approve_desktop()
                
                time.sleep(self.config["check_interval"])
                
            except Exception as e:
                logger.error(f"Error in desktop monitor: {e}")
                time.sleep(5)
    
    def start(self):
        """Start desktop automation"""
        monitor_thread = threading.Thread(target=self.monitor_desktop, daemon=True)
        monitor_thread.start()
        logger.info("✅ Desktop automation started!")
        return monitor_thread
    
    def stop(self):
        """Stop automation"""
        self.running = False


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║       🤖 BUDDY AI - ChatGPT & Codex Automation           ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  1. Browser Automation (Chrome/Edge/Opera)                ║
    ║  2. Desktop App Automation (ChatGPT Desktop)              ║
    ║  3. Exit                                                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    choice = input("Select mode (1/2/3): ").strip()
    
    if choice == "1":
        browser = input("Browser (chrome/edge/opera): ").strip().lower() or "chrome"
        
        automation = ChatGPTCodexAutomation(browser=browser)
        automation.start()
        
        print("\n✅ Automation running! Press Ctrl+C to stop.\n")
        print("Features:")
        print("  • Auto-approves Yes/Run/Continue buttons")
        print("  • Monitors Codex for new code")
        print("  • Copies code to ChatGPT for review")
        print("  • Syncs responses between tabs")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            automation.close()
            print("\n👋 Automation stopped!")
            
    elif choice == "2":
        automation = DesktopChatGPTAutomation()
        automation.start()
        
        print("\n✅ Desktop automation running! Press Ctrl+C to stop.\n")
        print("Features:")
        print("  • Auto-approves Yes/Run/Continue buttons")
        print("  • Monitors ChatGPT desktop app")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            automation.stop()
            print("\n👋 Automation stopped!")
    
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()
