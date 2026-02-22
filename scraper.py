import json
import time
from playwright.sync_api import sync_playwright

def scrape_zoe():
    with sync_playwright() as p:
        # Запускаем браузер
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        try:
            # Переходим на страницу
            page.goto("https://www.zoe.com.ua/outage/", wait_until="networkidle", timeout=60000)
            
            # Ждем появления таблицы или графиков (селекторы нужно будет уточнить)
            # Для примера берем текст всех таблиц
            data = []
            tables = page.query_all("table")
            
            for i, table in enumerate(tables):
                rows = table.query_all("tr")
                table_data = []
                for row in rows:
                    cells = row.query_all("td, th")
                    table_data.append([c.inner_text().strip() for c in cells])
                data.append({f"table_{i}": table_data})

            # Сохраняем в JSON
            result = {
                "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "success",
                "data": data
            }
        except Exception as e:
            result = {"status": "error", "message": str(e)}
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        browser.close()

if __name__ == "__main__":
    scrape_zoe()
