import argparse
import gc
import os
import random
import time
from datetime import datetime

import pandas as pd
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_EXCEL_FILE = r"C:\path\to\your\accounts.xlsx"
DEFAULT_LOG_FILE = r"C:\path\to\your\classroom_login_log.csv"
REQUIRED_COLUMNS = {"account", "password"}


def load_accounts(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到帳號檔案：{file_path}")

    df = pd.read_excel(file_path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Excel 缺少必要欄位：{sorted(missing)}")
    return df


def open_browser() -> uc.Chrome:
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    # --- 記憶體優化參數 ---
    options.add_argument("--disable-gpu")  # 停用 GPU 硬體加速
    options.add_argument("--no-sandbox")  # 降低系統資源開銷
    options.add_argument("--disable-dev-shm-usage")  # 避免共享記憶體不足
    options.add_argument("--renderer-process-limit=2")  # 限制渲染進程數量
    return uc.Chrome(options=options)


def human_like_pause(min_seconds: float = 0.3, max_seconds: float = 0.8) -> None:
    time.sleep(random.uniform(min_seconds, max_seconds))


def click_by_text(driver, wait: WebDriverWait, texts, timeout: int = 8) -> bool:
    for text in texts:
        xpath = f"//button[contains(., '{text}') or contains(normalize-space(.), '{text}')]"
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            human_like_pause(0.2, 0.5)
            try:
                button.click()
            except Exception:
                driver.execute_script("arguments[0].click();", button)
            return True
        except Exception:
            continue
    return False


def handle_account_chooser(driver) -> None:
    """處理 Google「選擇帳號」列表頁面，自動點擊「使用其他帳戶」"""
    try:
        use_another = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), '使用其他帳戶') or contains(text(), 'Use another account')]")
            )
        )
        use_another.click()
        human_like_pause(0.5, 1.0)
    except TimeoutException:
        pass


def login_classroom(driver, wait: WebDriverWait, account: str, password: str) -> str:
    # 1. 開啟 Google Classroom 登入頁
    driver.get("https://accounts.google.com/AccountChooser?continue=https://classroom.google.com")
    human_like_pause(1.0, 2.0)

    # 檢查是否陷入「選擇帳號」列表
    handle_account_chooser(driver)

    # --- 輸入帳號 ---
    try:
        email_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='email' or @name='identifier' or @id='identifierId']")
            )
        )
        email_input.clear()
        for char in account:
            email_input.send_keys(char)
            human_like_pause(0.03, 0.08)
        human_like_pause(0.4, 0.8)

        if not click_by_text(driver, wait, ["下一步", "Next"], timeout=5):
            email_input.send_keys(Keys.ENTER)

    except TimeoutException:
        if "classroom.google.com" in driver.current_url:
            return "already_logged_in"
        print(f"❌ [{account}] 輸入帳號階段逾時，當前網址：{driver.current_url}")
        return "manual_verify"

    # --- 等待密碼框出現（等待最長 20 秒）---
    try:
        pwd_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='password' or @name='Passwd' or @name='password']")
            )
        )
    except TimeoutException:
        current = driver.current_url.lower()
        print(f"❌ [{account}] 無法進入密碼頁，當前網址：{driver.current_url}")
        if "signin/identifier" in current or "challenge" in current or "checkpoint" in current:
            return "manual_verify"
        return "failed"

    # --- 輸入密碼 ---
    pwd_input.clear()
    for char in password:
        pwd_input.send_keys(char)
        human_like_pause(0.03, 0.08)
    human_like_pause(0.4, 0.8)

    if not click_by_text(driver, wait, ["下一步", "Next"], timeout=5):
        pwd_input.send_keys(Keys.ENTER)

    # --- 處理 Google Workspace / 新帳號條款頁（「我瞭解了」）---
    try:
        welcome_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[contains(., '瞭解') or contains(., '理解') or contains(., '同意') or contains(., 'I understand') or contains(., 'Accept')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", welcome_btn)
        human_like_pause(0.5, 1.0)
        try:
            welcome_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", welcome_btn)
        print("點擊「我瞭解了」通過條款頁面")
        human_like_pause(1.5, 2.5)
    except TimeoutException:
        pass

    # --- 處理 Classroom 帳戶確認彈窗（「繼續」按鈕）---
    try:
        continue_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(., '繼續') or contains(., 'Continue')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        human_like_pause(0.5, 1.0)
        try:
            continue_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", continue_btn)
        print("點擊 Classroom 身份確認「繼續」按鈕")
        human_like_pause(1.5, 2.5)
    except TimeoutException:
        pass

    # --- 處理「選擇你的角色」（我是學生）---
    try:
        student_elem = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[text()='我是學生' or contains(text(), '我是學生') or contains(text(), 'Student') or contains(text(), 'student')]",
                )
            )
        )
        human_like_pause(0.5, 1.0)
        driver.execute_script("arguments[0].click();", student_elem)
        try:
            driver.execute_script("arguments[0].parentElement.click();", student_elem)
        except Exception:
            pass
        print("已成功選擇「我是學生」角色")
        human_like_pause(2.5, 3.5)
    except TimeoutException:
        pass

    # --- 處理「我知道了」引導提示彈窗 ---
    try:
        got_it = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., '我知道了') or contains(., 'Got it')]"))
        )
        got_it.click()
    except TimeoutException:
        pass

    # --- 確認是否成功進入 Classroom 主頁（等待最長 20 秒）---
    try:
        WebDriverWait(driver, 20).until(
            lambda d: "classroom.google.com" in d.current_url and "accounts.google.com" not in d.current_url
        )
        return "success"
    except TimeoutException:
        print(f"❌ [{account}] 進入 Classroom 主頁超時，當前網址：{driver.current_url}")
        if "challenge" in driver.current_url or "rejected" in driver.current_url:
            return "manual_verify"
        return "failed"


def handle_join_course(driver, wait: WebDriverWait) -> bool:
    """處理課程卡片加入與確認彈窗"""
    try:
        join_buttons = WebDriverWait(driver, 12).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[contains(., '加入') or contains(., 'Join')]")
            )
        )
        if join_buttons:
            driver.execute_script("arguments[0].scrollIntoView(true);", join_buttons[0])
            human_like_pause(0.5, 1.0)
            try:
                join_buttons[0].click()
            except Exception:
                driver.execute_script("arguments[0].click();", join_buttons[0])
            print("已點擊課程卡片「加入」按鈕")
            human_like_pause(1.5, 2.5)

            # 處理二次確認彈窗（「確定要加入」）
            try:
                try:
                    checkbox = WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "//div[@role='dialog']//input[@type='checkbox'] | //div[@role='dialog']//*[contains(text(), '日後收到邀請')]",
                            )
                        )
                    )
                    checkbox.click()
                except TimeoutException:
                    pass

                confirm_button = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@role='dialog']//button[contains(., '加入') or contains(., 'Join')]")
                    )
                )
                try:
                    confirm_button.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", confirm_button)
                print("已點擊對話框「確定要加入」按鈕")
            except TimeoutException:
                pass

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//*[contains(text(), '訊息串') or contains(text(), '課堂作業') or contains(text(), 'Stream')]",
                        )
                    )
                )
                print("已成功加入並進入課程頁面！")
            except TimeoutException:
                pass

            human_like_pause(2.0, 3.0)
            return True
    except TimeoutException:
        print("未發現需要加入的課程卡片（可能已加入過或無新邀請）")
    return False


def logout_account(driver) -> None:
    try:
        driver.get("https://accounts.google.com/Logout")
        time.sleep(2)
    except Exception as e:
        print(f"登出頁面開啟失敗：{e}")
    finally:
        try:
            driver.delete_all_cookies()
        except Exception:
            pass


def process_account(account: str, password: str, test_mode: bool = False) -> dict:
    started_at = datetime.now()
    start_time = time.time()
    driver = None

    try:
        if test_mode:
            return {
                "account": account,
                "status": "test_mode",
                "message": "測試模式",
                "time": started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": round(time.time() - start_time, 2),
            }

        driver = open_browser()
        wait = WebDriverWait(driver, 20)

        status = login_classroom(driver, wait, account, password)
        if status in {"success", "already_logged_in"}:
            handle_join_course(driver, wait)
            message = "登入/課程加入處理完成"
        elif status == "failed":
            message = "登入超時或未成功進入 Classroom"
        elif status == "manual_verify":
            message = "Google 觸發驗證/安全檢查/帳密錯誤"
        else:
            message = "登入狀態未知"

        logout_account(driver)
        return {
            "account": account,
            "status": status,
            "message": message,
            "time": started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": round(time.time() - start_time, 2),
        }

    except Exception as e:
        return {
            "account": account,
            "status": "error",
            "message": str(e),
            "time": started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": round(time.time() - start_time, 2),
        }
    finally:
        # 關閉瀏覽器並強制進行垃圾回收
        if driver is not None:
            try:
                driver.quit()
            except WebDriverException:
                pass
        gc.collect()


def save_log(records: list, log_file: str) -> None:
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
    df = pd.DataFrame(records)
    df.to_csv(log_file, index=False, encoding="utf-8-sig")
    print(f"\n已寫入紀錄檔：{log_file}")


def run_real_batch(excel_file: str, log_file: str) -> None:
    df = load_accounts(excel_file)
    records = []

    for index, row in df.iterrows():
        account = str(row["account"]).strip()
        password = str(row["password"]).strip()
        print("\n==========================================")
        print(f"正在處理第 {index + 1}/{len(df)} 個帳戶：{account}")
        print("==========================================")

        # 執行首次嘗試
        res = process_account(account, password, test_mode=False)

        # 失敗時自動重試一次
        if res["status"] in {"failed", "error"}:
            print(f"⚠️ 帳號 {account} 處理失敗/超時，正在進行自動重試 (第 2 次嘗試)...")
            time.sleep(3)
            res = process_account(account, password, test_mode=False)

        records.append(res)

        # 每處理 20 個帳號，強制清理背景未正常關閉的死掉進程
        if (index + 1) % 20 == 0:
            print("🧹 正在進行記憶體深層清理...")
            os.system('taskkill /f /im chromedriver.exe /fi "status eq NOT RESPONDING" 2>nul')
            gc.collect()
            time.sleep(3)

        cool_down = random.uniform(4.0, 7.0)
        print(f"冷卻中，等待 {round(cool_down, 1)} 秒後處理下一個帳號...")
        time.sleep(cool_down)

    save_log(records, log_file)
    print("\n所有帳號自動化處理完成！")


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Classroom 自動登入與加入課程")
    parser.add_argument("--excel", default=DEFAULT_EXCEL_FILE, help="帳號 Excel 路徑")
    parser.add_argument("--log", default=DEFAULT_LOG_FILE, help="輸出紀錄 CSV 路徑")
    parser.add_argument("--test-mode", action="store_true", help="測試模式")
    args = parser.parse_args()

    if args.test_mode:
        print("[測試模式] 僅檢查程式流程，不會實際登入 Google Classroom")
        save_log(
            [{
                "account": "test_account@example.com",
                "status": "test_mode",
                "message": "測試模式執行完成",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": 0.0,
            }],
            args.log,
        )
        return

    run_real_batch(args.excel, args.log)


if __name__ == "__main__":
    main()