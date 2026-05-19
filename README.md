# 🔍 Rate Shopper Agent — Travelier Hackathon 2026

An AI-powered Supply Intelligence Agent that monitors competitor prices and identifies supply gaps for Travelier's OTA brands.

## 🚀 What it does

1. **Price Intelligence** — Scrapes competitor operator websites in real-time and compares against Bookaway prices  
2. **Supply Gap Discovery** — Identifies routes that operators sell directly but Bookaway doesn't have listed

## 🛠 Tech Stack

- **Firecrawl** — Web scraping (operator direct sites)  
- **OpenRouter + LLaMA 3.3 70B** — AI price analysis  
- **BigQuery** — Internal booking & supply data  
- **Lovable** — React dashboard UI

## 📊 Live Demo

🔗 [Rate Shopper Dashboard](YOUR_LOVABLE_URL_HERE)

## 🔬 Real Data Example

**Route: La Fortuna → Monteverde (Jeep Boat Jeep)**  
- Bookaway price: $35  
- Competitor (Aventuras El Lago): $33 (8AM) / $40 (2PM)  
- Position: ✅ COMPETITIVE

**Supply Gap Found:**  
- La Fortuna → Airport ($45) — NOT ON BOOKAWAY  
- Monteverde → San José ($25) — NOT ON BOOKAWAY

## 💡 Business Impact

- Reduce manual price monitoring from hours to seconds  
- Identify onboarding opportunities automatically  
- Powered by real Travelier BigQuery data

## 🏃 How to Run

```bash  
pip install requests  
python rate_shopper.py 
