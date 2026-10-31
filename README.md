# Google Classroom Auto Login Script / Google Classroom 自動登入腳本

This project is for academic and research-oriented automation studies, and for helping staff or administrators handle repetitive classroom onboarding tasks in a controlled environment.

這個專案主要用於學術研究與自動化流程探討，也用於協助同工／管理人員在受控環境中處理重複性的批量加入課程或帳號登入工作。

It is designed to:

- read account and password data from Excel
- open the Google sign-in page automatically
- handle common Google Classroom and Google Workspace login states
- try to join available classroom courses
- log each account's result into a CSV file
- stop safely when Google triggers security checks or verification pages

它的用途包括：

- 從 Excel 讀取帳號與密碼
- 自動開啟 Google 登入頁面
- 處理常見的 Google Classroom / Google Workspace 登入狀態
- 嘗試加入可用的課程
- 將每個帳號的處理結果記錄到 CSV 檔案
- 當 Google 觸發安全檢查或驗證頁面時，安全停止而不是無限重試

> This project is intended for academic research, technical experimentation, and assisting staff with large-scale classroom enrollment support in legitimate operational contexts. This repository does not support or endorse unauthorized, deceptive, or unlawful access.
>
> 本專案僅供學術研究、技術實驗、以及協助同工在合法業務範圍內處理批量加入課程或帳號管理等工作使用，不支援也不鼓勵任何未經授權、欺騙性、或違法的存取行為。

---

## ⚠️ Legal / Ethics Notice / 免責聲明

### Important notice / 重要聲明

This project is not intended for illegal, deceptive, or malicious activity.

- It is designed for academic investigation, controlled testing, and support for legitimate staff workflows.
- It is not a tool for bypassing Google security, violating account policies, or abusing institutional systems.
- If a user chooses to misuse this code for offensive, unauthorized, or unlawful purposes, the author does not accept any responsibility.

本專案不適用於任何非法、欺騙性、或惡意行為。

- 其定位是學術研究、受控測試，以及協助合法業務流程中的批量處理。
- 它不是用來繞過 Google 安全機制、違反帳號政策、或濫用機構系統的工具。
- 若有人將本程式用於違法、不當或不道德目的，作者概不承擔任何責任。

### Explicit disclaimer / 明確免責

The author is not responsible for:

- misuse of this script
- unauthorized access or violations of platform policies
- misuse by institutions, staff, or third parties
- any legal, civil, or disciplinary consequences arising from improper use

作者不承擔以下責任：

- 本腳本被濫用的後果
- 未經授權存取或違反平台政策的後果
- 任何使用者、機構、同工或第三方不當使用所造成的法律、民事、紀律責任
- 因不當使用導致的任何損失、處罰、訴訟或其他後果

> If someone uses this code for unlawful purposes, the author will not be responsible, and no support or warranty is provided for such misuse.
>
> 若有人將本程式用於不法用途，作者一律不負責，也不提供任何支援、保固或協助。

---

## What this script does / 這個腳本做什麼

### 1. Load account file / 載入帳號檔案
The script reads an Excel file and expects at least these columns:

- `account`
- `password`

Example / 範例:

```csv
account,password
student1@example.com,abc123
student2@example.com,pass456
```

### 2. Start browser automation / 啟動瀏覽器自動化
The script launches Chrome via `undetected_chromedriver` and opens the Google login flow.

腳本會透過 `undetected_chromedriver` 啟動 Chrome，並進入 Google 登入流程。

### 3. Login to Google Classroom / 登入 Google Classroom
It tries to:

- enter the email address
- wait for the password box
- enter the password
- click the login buttons
- handle Google account chooser prompts
- handle Google Workspace onboarding or terms pages
- detect whether the session reaches the Classroom homepage

它會嘗試：

- 輸入電子郵件
- 等待密碼欄位
- 輸入密碼
- 點擊登入按鈕
- 處理 Google 帳號選擇頁面
- 處理 Google Workspace 條款與新帳號導引頁
- 判斷是否已成功進入 Classroom 主頁

### 4. Process classroom join flow / 處理加入課程流程
If login succeeds, it checks whether there is a classroom join action and tries to complete it if possible.

若登入成功，腳本會檢查是否有加入課程的操作，並在可能的情況下嘗試完成加入流程。

### 5. Save CSV log results / 儲存 CSV 紀錄
Each account is stored with a result such as:

- `success`
- `already_logged_in`
- `failed`
- `manual_verify`
- `error`
- `test_mode`

每個帳號會記錄狀態，例如：

- `success`
- `already_logged_in`
- `failed`
- `manual_verify`
- `error`
- `test_mode`

---

## Important path settings / 路徑設定

This project originally used hardcoded local paths. Before using it, change the paths in the Python script:

```python
DEFAULT_EXCEL_FILE = r"C:\path\to\your\accounts.xlsx"
DEFAULT_LOG_FILE = r"C:\path\to\your\classroom_login_log.csv"
```

You should replace them with your own local folder paths, for example:

```python
DEFAULT_EXCEL_FILE = r"D:\automation\accounts.xlsx"
DEFAULT_LOG_FILE = r"D:\automation\classroom_login_log.csv"
```

You can also pass paths from the terminal instead of editing the file:

```powershell
python "autoClassRoom.py" --excel "D:\automation\accounts.xlsx" --log "D:\automation\classroom_login_log.csv"
```

這個專案原本使用了硬編碼的本機路徑。在使用前，請先修改 Python 腳本中的路徑：

```python
DEFAULT_EXCEL_FILE = r"C:\path\to\your\accounts.xlsx"
DEFAULT_LOG_FILE = r"C:\path\to\your\classroom_login_log.csv"
```

請替換成你自己的本機資料夾路徑，例如：

```python
DEFAULT_EXCEL_FILE = r"D:\automation\accounts.xlsx"
DEFAULT_LOG_FILE = r"D:\automation\classroom_login_log.csv"
```

也可以直接從命令列傳入路徑，不必修改程式碼：

```powershell
python "autoClassRoom.py" --excel "D:\automation\accounts.xlsx" --log "D:\automation\classroom_login_log.csv"
```

---

## Requirements / 必要條件

Create a virtual environment and install the required packages:

```powershell
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

You also need:

- Python 3.10 to 3.12 recommended
- Google Chrome installed
- a valid Excel file with account/password data

> Note: `undetected_chromedriver` currently has compatibility issues with Python 3.14, so Python 3.12 is the safest option for this project.

你還需要：

- Python 3.10 到 3.12（建議）
- 已安裝 Google Chrome
- 含有帳號 / 密碼的有效 Excel 檔案

> 備註：`undetected_chromedriver` 目前與 Python 3.14 之間有相容性問題，因此本專案建議使用 Python 3.12。

---

## How to run / 如何執行

### 1. Test mode / 測試模式
This mode checks whether the script runs without trying to log in to Google.

```powershell
python "autoClassRoom.py" --test-mode --log "D:\automation\classroom_login_log.csv"
```

此模式只檢查腳本是否能正常執行，不會真的登入 Google。

### 2. Real execution / 真實執行
Run the script with your Excel file and log file:

```powershell
python "autoClassRoom.py" --excel "D:\automation\accounts.xlsx" --log "D:\automation\classroom_login_log.csv"
```

使用你的 Excel 帳號檔與輸出 log 檔執行腳本：

```powershell
python "autoClassRoom.py" --excel "D:\automation\accounts.xlsx" --log "D:\automation\classroom_login_log.csv"
```

### 3. Use default script paths / 使用預設路徑
If you already edited the script with your file paths, you can simply run:

```powershell
python "autoClassRoom.py"
```

如果你已經在腳本中設定好自己的路徑，可以直接執行：

```powershell
python "autoClassRoom.py"
```

---

## Example folder layout / 範例資料夾結構

```text
googleClassroom/
├── autoClassRoom.py
├── README.md
├── accounts.xlsx
└── classroom_login_log.csv
```

---

## Known limitations / 已知限制

Google may trigger:

- account verification pages
- reCAPTCHA or human verification screens
- terms / welcome pages
- security checks
- account chooser or role selection flows

When those appear, the script marks the result as `manual_verify` or `failed` instead of retrying endlessly.

This is intentional because real Google login flows can block automated tools when security detection is triggered.

Google 可能會觸發：

- 帳號驗證頁面
- reCAPTCHA 或人工驗證畫面
- 條款 / 新帳號導引頁
- 安全檢查
- 帳號選擇或角色選擇流程

當這些情況出現時，腳本會將結果標記為 `manual_verify` 或 `failed`，而不是無限重試。

這是故意設計的，因為 Google 在實際登入流程中，遇到安全檢測時可能會阻止自動化工具。

---

## Logging behavior / 紀錄方式

The script records a CSV log with information like:

```csv
account,status,message,time,duration_seconds
student1@example.com,success,登入/課程加入處理完成,2026-10-31 12:00:00,18.54
student2@example.com,manual_verify,Google 觸發驗證/安全檢查/帳密錯誤,2026-10-31 12:01:00,12.20
```

腳本會輸出 CSV 記錄檔，例如：

```csv
account,status,message,time,duration_seconds
student1@example.com,success,登入/課程加入處理完成,2026-10-31 12:00:00,18.54
student2@example.com,manual_verify,Google 觸發驗證/安全檢查/帳密錯誤,2026-10-31 12:01:00,12.20
```

---

## Purpose and responsibility / 用途與責任

This code is intended for:

- academic research
- controlled testing
- legitimate institutional support workflows
- helping staff with repetitive batch enrollment tasks under authorized conditions

It is not intended for:

- unauthorized account access
- bypassing security checks
- exploiting Google or school systems
- illegal, deceptive, or malicious use

The author does not accept responsibility for misuse of this project.

此程式的用途包括：

- 學術研究
- 受控測試
- 合法機構內部支援工作
- 在授權條件下協助同工處理批量加入課程等重複性任務

以下用途不在本專案範圍：

- 未授權存取帳號
- 繞過安全檢查
- 濫用 Google 或學校系統
- 任何非法、欺騙性、或惡意用途

作者對本專案的濫用不承擔任何責任。

---

## Disclaimer / 免責聲明

This project is provided as-is for educational and research purposes. It is meant to assist certain staff workflows in a lawful and accountable manner. Any use beyond that scope, including unauthorized access or unlawful activity, is strictly outside the intent of this project.

The author does not provide guarantees, warranties, or support for misuse.

If someone uses this code for unlawful purposes, the author will not be responsible under any circumstances.

本專案以「現狀」提供，僅供教育與研究使用。其目的是在合法且可被問責的前提下，協助部分同工處理批量流程。任何超出此範圍的用途，包括未授權存取或違法行為，均不屬於本專案的意圖。

作者不提供任何保證、擔保或對濫用情況的支援。

若有人將本程式用於不法用途，作者在任何情況下均不負責。

---

## License / 授權

This project is provided as-is for educational purposes. If you plan to publish it publicly, add an open-source license such as MIT or Apache 2.0.

本專案以原樣提供，僅供教育與研究用途。如果你計劃公開發布，請補上開源授權，例如 MIT 或 Apache 2.0。



