# Google Classroom Auto Login Script

A lightweight automation script for Google Classroom account onboarding and batch login checks in controlled, legitimate workflows.

這個專案是一個用於 Google Classroom 批次登入與帳號處理的自動化腳本，適用於受控、合法的教學與行政流程。

## Overview / 總覽

- Reads account and password data from Excel
- Opens Google sign-in flow automatically
- Handles common login and Classroom prompts
- Tries to join available course invitations
- Writes a CSV log for each account result
- Stops safely when Google triggers verification or security checks

- 從 Excel 讀取帳號與密碼
- 自動開啟 Google 登入流程
- 處理常見的登入與 Classroom 提示
- 嘗試加入可用的課程邀請
- 將每個帳號的結果寫入 CSV 日誌
- 當 Google 觸發驗證或安全檢查時安全停止

> This project is intended for research, testing, and authorized staff support workflows only. It does not support unauthorized access or bypassing Google security.
>
> 本專案僅供研究、測試與合法的行政/教學支援流程使用，不支援未授權存取或繞過 Google 安全機制。

---

## Features / 功能

- Excel input with `account` and `password` columns
- Chrome automation via `undetected_chromedriver`
- Google Classroom login flow handling
- Account chooser / terms / role prompt handling
- CSV result tracking with statuses such as `success`, `failed`, `manual_verify`, and `error`

- 支援 `account` 與 `password` 欄位的 Excel 輸入
- 使用 `undetected_chromedriver` 自動化 Chrome
- 處理 Google Classroom 登入流程
- 處理帳戶選擇、條款與角色提示
- 輸出 CSV 結果，包含 `success`、`failed`、`manual_verify`、`error` 等狀態

---

## Requirements / 必要條件

- Python 3.10 to 3.12 recommended
- Google Chrome installed
- Excel file with `account` and `password` columns

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

> `undetected_chromedriver` is not fully compatible with Python 3.14, so Python 3.12 is the safest version for this project.

- Python 3.10 到 3.12（建議）
- 已安裝 Google Chrome
- Excel 檔案需包含 `account` 與 `password` 欄位

---

## Quick start / 快速開始

### Test mode

```bash
python autoClassRoom.py --test-mode --log classroom_login_log.csv
```

### Real run

```bash
python autoClassRoom.py --excel your_accounts.xlsx --log classroom_login_log.csv
```

---

## Excel format / Excel 格式

```csv
account,password
student1@example.com,abc123
student2@example.com,pass456
```

---

## Output / 輸出結果

```csv
account,status,message,time,duration_seconds
student1@example.com,success,登入/課程加入處理完成,2026-10-31 12:00:00,18.54
student2@example.com,manual_verify,Google 觸發驗證/安全檢查/帳密錯誤,2026-10-31 12:01:00,12.20
```

---

## Important note / 重要提醒

This project is intended for lawful, research-oriented, and authorized institutional workflows only. If Google detects suspicious behavior, the script records the result and stops instead of retrying endlessly.

本專案僅適用於合法、研究導向與已授權的機構工作流程。當 Google 偵測到可疑行為時，腳本會記錄結果並停止，而不是無限重試。

---

## License / 授權

This project is provided as-is for educational and research use. If you publish it publicly, add an open-source license such as MIT or Apache 2.0.

本專案以原樣提供，僅供教育與研究用途。若公開發布，請補上 MIT 或 Apache 2.0 等開源授權。
