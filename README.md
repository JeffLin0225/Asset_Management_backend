# Asset Management Backend (資產管理系統後端服務)

基於 **FastAPI**、**Redis (Keyspace Events)** 與 **MongoDB (Motor)** 建構的高效能非同步資產管理與趨勢分析後端。系統針對使用者高頻編輯場景，獨創「**Redis 防抖延遲回寫機制 (Write-Behind Cache Debounce)**」，大幅削峰並保護資料庫 I/O；同時具備定時資產快照與淨值彙整運算功能。

---

## 系統架構

```mermaid
flowchart TB
    %% 樣式定義
    classDef clientStyle fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef gatewayStyle fill:#0f172a,stroke:#818cf8,stroke-width:2px,color:#f8fafc;
    classDef workerStyle fill:#1e1b4b,stroke:#c084fc,stroke-width:2px,color:#f8fafc;
    classDef storageStyle fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc;
    classDef cronStyle fill:#451a03,stroke:#fb923c,stroke-width:2px,color:#f8fafc;
    classDef alertStyle fill:#701a75,stroke:#f472b6,stroke-width:2px,color:#f8fafc;

    %% 觸發層
    subgraph Trigger_Layer ["觸發與調用層 (Trigger & Ingress Layer)"]
        UserClient["前端使用者 / Web Client<br/>[JWT Bearer Token]"]:::clientStyle
        CronTrigger["外部排程器 / Cron Worker<br/>[POST /api/copyAnalyze 附 Secret Token]"]:::cronStyle
    end

    %% FastAPI 服務層
    subgraph API_Layer ["FastAPI 核心服務層 (Port: 8000)"]
        direction TB
        CORS["CORS Middleware<br/>origins: CORS_ORIGINS"]:::gatewayStyle
        AuthService["Auth 認證中介層<br/>JWT HS256 解碼 & 效期驗證"]:::gatewayStyle
        
        subgraph Controllers ["API 控制器 (Routers)"]
            LoginCtrl["login_controller<br/>/api/login"]:::gatewayStyle
            AssetCtrl["asset_controller<br/>/api/getAsset | /api/saveAsset"]:::gatewayStyle
            AnalyzeCtrl["analyze_controller<br/>/api/getAnalyze | /api/copyAnalyze"]:::gatewayStyle
        end

        subgraph Core_Services ["核心業務邏輯 (Services)"]
            LoginService["login_service<br/>bcrypt 密碼校驗 & Token 簽發"]:::gatewayStyle
            AssetService["asset_service<br/>資產查詢與暫存協調"]:::gatewayStyle
            AnalyzeService["analyze_service<br/>Snapshot 快照運算與淨值統計"]:::gatewayStyle
        end
    end

    %% 快取與事件驅動層
    subgraph Cache_Layer ["Redis 快取與事件驅動層 (Pub/Sub & Debounce)"]
        RedisNode[("Redis 服務實例<br/>Port: 6379<br/>notify-keyspace-events=Ex")]:::workerStyle
        TempData[("最新資產資料暫存<br/>key: latest_data:userId<br/>TTL: 30s")]:::workerStyle
        DebounceTimer[("防抖計時器<br/>key: debounce_timer:userId<br/>TTL: 5s")]:::workerStyle
        KeyspacePubSub["Keyspace 事件廣播<br/>__keyevent@*__:expired"]:::alertStyle
        RedisWorker["FastAPI Lifespan 背景監聽程序<br/>redis_subscribe_expired()"]:::workerStyle
    end

    %% 持久化儲存層
    subgraph Storage_Layer ["MongoDB 資料庫持久層 (Motor Async Driver)"]
        direction TB
        MongoClient[("Motor 連線池實例<br/>minPoolSize=5 | maxPoolSize=20<br/>serverSelectionTimeoutMS=5000")]:::storageStyle
        UserCol[("user 集合<br/>使用者帳號與 bcrypt 雜湊密碼")]:::storageStyle
        AssetCol[("asset 集合<br/>使用者當前資產狀態 JSON")]:::storageStyle
        AnalyzeCol[("analyze 集合<br/>每日資產快照 (userId + date 唯一鍵)")]:::storageStyle
    end

    %% 主鏈路 1: 登入驗證
    UserClient -->|"1. 登入請求 (ID + PIN)"| LoginCtrl
    LoginCtrl --> LoginService
    LoginService -->|"1a. 查詢使用者雜湊"| UserCol
    LoginService -.->|"1b. 簽發 JWT Token"| UserClient

    %% 主鏈路 2: 資產防抖寫入
    UserClient -->|"2. 變更資產 (POST /api/saveAsset)"| AssetCtrl
    AssetCtrl -->|"2a. Token 驗證"| AuthService
    AssetCtrl --> AssetService
    AssetService -->|"2b. 寫入最新資產 (TTL 30s)"| TempData
    AssetService -->|"2c. 重置計時器 (TTL 5s)"| DebounceTimer
    AssetCtrl -.->|"2d. 快速回應 200 OK"| UserClient

    %% 背景鏈路: 防抖回寫 (Debounce Write-Behind)
    DebounceTimer -.->|"A. 靜置滿 5 秒自然過期"| KeyspacePubSub
    KeyspacePubSub -->|"B. 發布過期通知"| RedisWorker
    RedisWorker -->|"C. 取出 latest_data"| TempData
    RedisWorker ==>|"D. 批量持久化寫入 (update_one)"| AssetCol

    %% 主鏈路 3: 即時資產與分析查詢
    UserClient -->|"3. 查詢資產 / 分析圖表"| AssetCtrl
    AssetCtrl -->|"3a. 查詢目前資產"| AssetCol
    UserClient -->|"3b. 查詢歷史趨勢"| AnalyzeCtrl
    AnalyzeCtrl -->|"3c. 讀取 Snapshot 清單"| AnalyzeCol

    %% 主鏈路 4: 排程快照產生
    CronTrigger -->|"4. 觸發定時快照 (Token 授權)"| AnalyzeCtrl
    AnalyzeCtrl --> AnalyzeService
    AnalyzeService -->|"4a. 取出全體使用者"| UserCol
    AnalyzeService -->|"4b. 取得當前資產"| AssetCol
    AnalyzeService -->|"4c. 計算淨值 (Assets - Liab - Others)"| AnalyzeService
    AnalyzeService ==>|"4d. Upsert 寫入每日快照"| AnalyzeCol
```

---

## 專案結構

```
Asset_Management_backend/
├── api/                             # API 控制層 (路由定義、驗證中介注入與請求轉發)
│   ├── analyze_controller.py        # 資產分析端點：歷史趨勢查詢、手動快照與金鑰保護的批次排程歸檔
│   ├── asset_controller.py          # 個人資產端點：使用者資產讀取 (getAsset) 與防抖暫存 (saveAsset)
│   └── login_controller.py          # 認證端點：驗證使用者 PIN 碼並簽發短期 JWT Access Token
├── cache/                           # 快取與事件工作處理層 (Redis)
│   ├── redis_client.py              # 同步/非同步 Redis 連線客戶端封裝
│   ├── redis_repository.py          # 暫存邏輯：維護 latest_data (30s) 與 debounce_timer (5s)
│   └── redis_worker.py              # 系統生命週期 (Lifespan) 管理、冷啟動未落盤掃描與過期事件回寫監聽
├── db/                              # 資料庫連線與資料存取層 (MongoDB / Motor)
│   ├── __init__.py                  # 套件模組初始化標記
│   ├── mongo_client.py              # Motor 非同步連線池初始化 (配置 minPoolSize=5, maxPoolSize=20)
│   └── mongo_repository.py          # 資料庫 CRUD 封裝 (含連線預熱、資產儲存、分析快照 upsert)
├── dto/                             # 資料傳輸物件層 (Data Transfer Objects)
│   ├── __init__.py                  # 套件模組初始化標記
│   ├── asset_dto.py                 # 資產更新請求 Payload 驗證模型 (AssetRequest)
│   └── login_dto.py                 # 登入請求與回應資料模型 (LoginRequest, LoginResponse)
├── model/                           # 領域模型與資料結構定義 (Pydantic Models)
│   ├── __init__.py                  # 套件模組初始化標記
│   ├── asset_data.py                # 階層化資產結構：Category -> SubCategory -> Card (含金額自動標準化驗證)
│   ├── copy_token.py                # 批次抄寫分析端點授權 Token 驗證模型 (CopyRequest)
│   ├── snapshot.py                  # 資產快照模型 (Snapshot, SnapshotCategory, Totals, SnapshotDTO)
│   └── user_info.py                 # JWT Payload 所載入的使用者基礎識別資訊 (UserInfo)
├── service/                         # 核心業務邏輯層 (Business Logic Layer)
│   ├── __init__.py                  # 套件模組初始化標記
│   ├── analyze_service.py           # 資產轉快照運算邏輯 (彙總項目金額、計算淨值) 與全使用者批次抄寫
│   ├── asset_service.py             # 個人資產查詢與暫存寫入排程協調
│   ├── auth.py                      # FastAPI OAuth2 Bearer Token 依賴注入與 JWT 效期核身
│   └── login_service.py             # 登入 PIN 碼比對 (passlib bcrypt) 與 JWT Token 產生
├── app.py                           # 應用程式入口點 (FastAPI 實例化、CORS 註冊、Lifespan 掛載、路由加載)
├── requirements.txt                 # Python 依賴套件定義檔 (FastAPI, Motor, Redis, Pydantic, Passlib 等)
├── .gitignore                       # Git 忽略配置清單
└── README.md                        # 系統核心架構與開發維運技術文件
```

---

## 核心機制解析

### 1. Redis Keyspace 防抖延遲回寫 (Write-Behind Cache Debounce)
- **問題背景**：前端在拖曳、微調資產數字或頻繁編輯多個項目時，若每次 HTTP 請求皆直接寫入 MongoDB，將造成大量 I/O 爭搶與資料庫寫入放大。
- **解法設計**：
  1. 前端送出 `POST /api/saveAsset` 時，後端將資料寫入 Redis `latest_data:{userId}` (TTL 30s)，並建立/刷新 `debounce_timer:{userId}` (TTL 5s)。
  2. 使用者在 5 秒內的後續編輯會持續刷新 `debounce_timer`，後端即刻回應成功。
  3. 使用者靜置滿 5 秒後，Redis 自動觸發過期事件 `__keyevent@*__:expired`。
  4. 背景程序 `redis_subscribe_expired` 捕捉事件，取出 `latest_data:{userId}` 並非同步持久化至 MongoDB `asset` 集合。
  5. **冷啟動補償機制**：服務在重新啟動時（FastAPI lifespan），會自動執行 `scan_iter("latest_data:*")` 掃描所有因重開機可能遺留的暫存資料，立即補償存入 MongoDB，保證資料不流失。

### 2. 資產結構轉換與歷史快照 (Asset Snapshot & Net Worth Calculation)
- **階層模型**：資產資料以 `Category` (資產、負債、其他) 包含多個 `SubCategory` (如現金、股票、房貸)，各子類別下掛多個 `Card` 項目。
- **快照演算法**：
  $$\text{NetWorth (淨資產)} = \text{Total Assets} - \text{Total Liabilities} - \text{Total Others}$$
- **定時/批次抄寫**：透過 `POST /api/copyAnalyze`（需帶 Secret Key 授權），系統可每日自動將全站使用者的資產狀態轉換為規格化快照 (`Snapshot`)，Upsert 存入 `analyze` 集合，供前端繪製資產隨時間變化的折線與圓餅分析圖。

---

## 環境變數設定

請在專案根目錄建立 `.env` 檔案，填入以下參數：

| 變數名稱 | 必填 | 說明 | 範例值 |
| :--- | :---: | :--- | :--- |
| `CORS_ORIGINS` | 是 | 允許跨域請求的來源 (逗號分隔) | `http://localhost:3000,http://localhost:5173` |
| `REDIS_URL` | 是 | Redis 連線字串 | `redis://localhost:6379/0` |
| `MONGO_URL` | 是 | MongoDB 連線字串 | `mongodb://localhost:27017` |
| `ASSET_DB` | 是 | 系統使用的 MongoDB 資料庫名稱 | `asset_management` |
| `SECRET_KEY` | 是 | JWT 簽發與解碼用密鑰 | `your-secure-jwt-secret` |
| `ALGORITHM` | 是 | JWT 簽署演算法 | `HS256` |
| `EXPIRE_MINUTES`| 是 | JWT Token 有效期限 (分鐘) | `60` |
| `COPY_SECRET_KEY`| 是 | 批次抄寫快照端點的授權 Token | `your-cron-batch-token` |

---

## 本機啟動與開發

### 1. 建立並啟用虛擬環境
```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# 或 .\venv\Scripts\activate  # Windows
```

### 2. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 3. 啟動本機開發伺服器
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
- API 文件 (Swagger UI)：`http://localhost:8000/docs`
- 替代文件 (ReDoc)：`http://localhost:8000/redoc`

---

## API 規格摘要

所有受保護 API 皆須在 HTTP Header 中帶上 `Authorization: Bearer <access_token>`。

| 方法 | 路徑 | 授權 | 說明 |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/login` | 否 | 使用者登入驗證（傳入 `ID` 與 `pin`），取得 JWT Token |
| `GET` | `/api/getAsset?userId={id}` | 是 | 取得指定使用者的當前資產清單 |
| `POST` | `/api/saveAsset` | 是 | 暫存使用者資產，觸發 5 秒防抖延遲持久化 |
| `GET` | `/api/getAnalyze?userId={id}` | 是 | 取得指定使用者的歷史資產快照與淨值數據 |
| `GET` | `/api/manualcopyAnalyze?userId={id}` | 否 | 手動為指定使用者產生一筆當日的資產快照 |
| `POST` | `/api/copyAnalyze` | 否* | 批次執行全使用者快照產出（*須在 Body 傳入合法的 `token`） |
