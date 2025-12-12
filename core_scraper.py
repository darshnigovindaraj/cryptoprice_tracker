from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
try:
    from email_alert import send_email
except:
    print("⚠️ email_alert.py not found - emails disabled")
    def send_email(subject, body): pass
import time
import warnings
warnings.filterwarnings("ignore")

def scrape_crypto():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://coinmarketcap.com/")
        
        wait = WebDriverWait(driver, 20)
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        rows = table.find_elements(By.TAG_NAME, "tr")[:10]

        coins, prices, changes, market_caps = [], [], [], []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 6:
                coins.append(cols[2].text.strip())
                prices.append(cols[3].text.strip())
                changes.append(cols[4].text.strip())
                market_caps.append(cols[6].text.strip())

        driver.quit()

        def clean_price(p): 
            try: return float(p.replace("$","").replace(",",""))
            except: return 0.0
        def clean_change(c): 
            try: return float(c.replace("%",""))
            except: return 0.0
        def clean_market(m): 
            try: return float(m.replace("$","").replace(",",""))
            except: return 0.0

        df = pd.DataFrame({
            "Coin": coins,
            "Price": [clean_price(p) for p in prices],
            "24h Change": [clean_change(c) for c in changes],
            "Market Cap": [clean_market(m) for m in market_caps],
            "Time": datetime.now()
        })

        file_name = datetime.now().strftime("crypto_%Y-%m-%d_%H%M.csv")
        df.to_csv(file_name, index=False)
        print(f"✅ Saved: {file_name}")

        # Chart 
        plt.figure(figsize=(12,6))
        top_idx = df["24h Change"].idxmax()
        colors = ["black" if i == top_idx else "violet" for i in range(len(df))]
        sns.barplot(data=df, x="Coin", y="24h Change", hue="Coin", palette=colors, legend=False)
        plt.title("Top 10 Crypto 24h Changes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("crypto_chart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("📈 Chart saved!")

        big_gainers = df[df["24h Change"] > 5]
        if not big_gainers.empty:
            print(f"🚀 {len(big_gainers)} big gainers!")
            for _, row in big_gainers.iterrows():
                try:
                    send_email(f"🚀 {row['Coin']} +{row['24h Change']:.1f}%!", f"{row['Coin']}: ${row['Price']:,.2f}")
                except: pass
        else:
            print("📊 No big gainers")

        return df

    except Exception as e:
        print(f"❌ Error: {e}")
        if driver: driver.quit()
        return pd.DataFrame()

if __name__ == "__main__":
    while True:
        print("🚀 Starting...")
        scrape_crypto()
        print("⏱️  1 hour break...\n")
        time.sleep(3600)
