from fastapi import HTTPException
from fastapi.logger import logger
from typing import List 
from model.asset_data import Category
from model.snapshot import Snapshot , SnapshotCategory 

from db.mongo_repository import select_user_asset_info

# 查詢資料
async def copy_asset_info(userId :str)  -> bool:

    asset_data :List[Category] = await select_user_asset_info(userId)
    asset_category = asset_data[0]["subCategoryList"]
    liability = asset_data[1]["subCategoryList"]
    other = asset_data[2]["subCategoryList"]

    print(asset_category) 
    print("=========================")
    print(liability)
    print("=========================")
    print(other)

    
    

    

'''
[
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-01",
    "assets": {
      "現金": {
        "items": { "中信": 200000, "玉山": 50000 },
        "total": 250000
      },
      "股票": {
        "items": { "台積電": 500000, "聯發科": 250000, "NVDA": 300000 },
        "total": 1050000
      },
      "加密貨幣": {
        "items": { "BTC": 100000, "ETH": 50000, "SOL": 25000 },
        "total": 175000
      },
      "total": 1475000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 35000 }, "total": 35000 },
      "mortgage": { "items": { "房貸": 3000000 }, "total": 3000000 },
      "total": 3035000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1475000, "liabilities": 3035000, "others": 200000, "netWorth": -1560000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-02",
    "assets": {
      "cash": {
        "items": { "中信": 455000, "玉山": 50000 },
        "total": 505000
      },
      "stock": {
        "items": { "台積電": 510000, "NVDA": 305000 },
        "total": 815000
      },
      "crypto": {
        "items": { "BTC": 102000, "ETH": 51000, "SOL": 26000 },
        "total": 179000
      },
      "total": 1499000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 40000 }, "total": 40000 },
      "mortgage": { "items": { "房貸": 2998000 }, "total": 2998000 },
      "total": 3038000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1499000, "liabilities": 3038000, "others": 200000, "netWorth": -1539000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-03",
    "assets": {
      "cash": {
        "items": { "中信": 420000, "玉山": 50000 },
        "total": 470000
      },
      "stock": {
        "items": { "台積電": 515000, "NVDA": 310000 },
        "total": 825000
      },
      "crypto": {
        "items": { "BTC": 105000, "ETH": 55000, "SOL": 27000, "DOGE": 10000 },
        "total": 197000
      },
      "total": 1492000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 25000 }, "total": 25000 },
      "mortgage": { "items": { "房貸": 2998000 }, "total": 2998000 },
      "total": 3023000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1492000, "liabilities": 3023000, "others": 200000, "netWorth": -1531000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-04",
    "assets": {
      "cash": {
        "items": { "中信": 410000, "玉山": 40000 },
        "total": 450000
      },
      "stock": {
        "items": { "台積電": 480000, "NVDA": 280000 },
        "total": 760000
      },
      "crypto": {
        "items": { "BTC": 85000, "ETH": 40000, "SOL": 18000, "DOGE": 7000 },
        "total": 150000
      },
      "total": 1360000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 28000 }, "total": 28000 },
      "mortgage": { "items": { "房貸": 2996000 }, "total": 2996000 },
      "total": 3024000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1360000, "liabilities": 3024000, "others": 200000, "netWorth": -1664000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-05",
    "assets": {
      "cash": {
        "items": { "中信": 558000, "玉山": 42000 },
        "total": 600000
      },
      "stock": {
        "items": { "台積電": 485000, "NVDA": 285000 },
        "total": 770000
      },
      "crypto": {
        "items": {},
        "total": 0
      },
      "total": 1370000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 15000 }, "total": 15000 },
      "mortgage": { "items": { "房貸": 2996000 }, "total": 2996000 },
      "total": 3011000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1370000, "liabilities": 3011000, "others": 200000, "netWorth": -1641000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-06",
    "assets": {
      "cash": {
        "items": { "中信": 550000, "玉山": 40000 },
        "total": 590000
      },
      "stock": {
        "items": { "台積電": 490000, "NVDA": 290000, "廣達": 100000 },
        "total": 880000
      },
      "crypto": {
        "items": {},
        "total": 0
      },
      "total": 1470000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 18000 }, "total": 18000 },
      "mortgage": { "items": { "房貸": 2994000 }, "total": 2994000 },
      "total": 3012000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1470000, "liabilities": 3012000, "others": 200000, "netWorth": -1542000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-07",
    "assets": {
      "cash": {
        "items": { "中信": 645000, "玉山": 45000 },
        "total": 690000
      },
      "stock": {
        "items": { "台積電": 495000, "NVDA": 295000, "廣達": 105000 },
        "total": 895000
      },
      "crypto": {
        "items": {},
        "total": 0
      },
      "total": 1585000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 20000 }, "total": 20000 },
      "mortgage": { "items": { "房貸": 2994000 }, "total": 2994000 },
      "personalLoan": { "items": { "個人信貸": 100000 }, "total": 100000 },
      "total": 3114000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1585000, "liabilities": 3114000, "others": 200000, "netWorth": -1529000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-08",
    "assets": {
      "cash": {
        "items": { "中信": 580000, "玉山": 40000 },
        "total": 620000
      },
      "stock": {
        "items": { "台積電": 550000, "NVDA": 350000, "廣達": 120000 },
        "total": 1020000
      },
      "crypto": {
        "items": { "BTC": 50000 },
        "total": 50000
      },
      "total": 1690000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 15000 }, "total": 15000 },
      "mortgage": { "items": { "房貸": 2992000 }, "total": 2992000 },
      "personalLoan": { "items": { "個人信貸": 98000 }, "total": 98000 },
      "total": 3105000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1690000, "liabilities": 3105000, "others": 200000, "netWorth": -1415000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-09",
    "assets": {
      "cash": {
        "items": { "中信": 500000, "玉山": 50000 },
        "total": 550000
      },
      "stock": {
        "items": { "台積電": 600000, "NVDA": 400000, "廣達": 150000 },
        "total": 1150000
      },
      "crypto": {
        "items": { "BTC": 80000, "ETH": 40000 },
        "total": 120000
      },
      "total": 1820000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 30000 }, "total": 30000 },
      "mortgage": { "items": { "房貸": 2992000 }, "total": 2992000 },
      "personalLoan": { "items": { "個人信貸": 96000 }, "total": 96000 },
      "total": 3118000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1820000, "liabilities": 3118000, "others": 200000, "netWorth": -1298000
    }
  },
  {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2025-10-10",
    "assets": {
      "cash": {
        "items": { "中信": 380000, "玉山": 40000 },
        "total": 420000
      },
      "stock": {
        "items": { "台積電": 650000, "NVDA": 480000, "廣達": 180000 },
        "total": 1310000
      },
      "crypto": {
        "items": { "BTC": 100000, "ETH": 60000 },
        "total": 160000
      },
      "total": 1890000
    },
    "liabilities": {
      "creditCard": { "items": { "中信卡": 25000 }, "total": 25000 },
      "mortgage": { "items": { "房貸": 2990000 }, "total": 2990000 },
      "personalLoan": { "items": { "個人信貸": 94000 }, "total": 94000 },
      "total": 3109000
    },
    "others": {
      "insurance": { "items": { "壽險": 200000 }, "total": 200000 },
      "total": 200000
    },
    "totals": {
      "assets": 1890000, "liabilities": 3109000, "others": 200000, "netWorth": -1219000
    }
  }
]

'''