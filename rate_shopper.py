import requests  
import json  
import time

# ============================================================  
# RATE SHOPPER AGENT — Travelier Hackathon 2025  
# ============================================================

FIRECRAWL_API_KEY = "fc-9d75c1da6a8845bfadfc2cb8e930ff96"  
OPENROUTER_API_KEY = "REPLACE_WITH_YOUR_OPENROUTER_KEY"

# Internal Bookaway data (from BigQuery)  
ROUTES = [  
    {  
        "route": "La Fortuna → Monteverde",  
        "operator": "Aventuras El Lago",  
        "operator_website": "https://aventurasellago.com/jeep-boat-jeep/",  
        "bookaway_price": 35.00,  
        "bookaway_bookings_ytd": 638,  
        "vehicle_type": "Jeep Boat Jeep"  
    }  
]

def scrape_website(url):  
    print(f"🌐 Scraping: {url}")  
    response = requests.post(  
        "https://api.firecrawl.dev/v1/scrape",  
        headers={  
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",  
            "Content-Type": "application/json"  
        },  
        json={  
            "url": url,  
            "formats": ["markdown"],  
            "waitFor": 3000  
        }  
    )  
    if response.status_code == 200:  
        data = response.json()  
        content = data.get("data", {}).get("markdown", "")  
        print(f"   ✅ Scraped {len(content)} chars")  
        return content  
    else:  
        print(f"   ❌ Error: {response.status_code}")  
        return ""

def analyze_with_ai(route_info, scraped_content):  
    models = [  
        "deepseek/deepseek-v4-flash:free",  
        "google/gemma-4-31b-it:free",  
        "meta-llama/llama-3.3-70b-instruct:free"  
    ]

    prompt = f"""You are a travel pricing analyst. Analyze this competitor data for a transport route.

ROUTE: {route_info['route']}  
OPERATOR: {route_info['operator']}  
BOOKAWAY PRICE: ${route_info['bookaway_price']}  
BOOKAWAY BOOKINGS THIS YEAR: {route_info['bookaway_bookings_ytd']}

SCRAPED COMPETITOR WEBSITE CONTENT:  
{scraped_content[:3000]}

Return ONLY valid JSON (no markdown, no explanation):  
{{  
  "competitor_prices": [  
    {{"time": "departure time or label", "price": 00.00, "currency": "USD"}}  
  ],  
  "market_average": 00.00,  
  "price_range": {{"min": 00.00, "max": 00.00}},  
  "bookaway_position": "CHEAPER or COMPETITIVE or EXPENSIVE",  
  "recommendation": "one sentence recommendation",  
  "confidence": "HIGH or MEDIUM or LOW"  
}}"""

    for model in models:  
        try:  
            print(f"   🤖 Trying model: {model}")  
            response = requests.post(  
                "https://openrouter.ai/api/v1/chat/completions",  
                headers={  
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",  
                    "Content-Type": "application/json"  
                },  
                json={  
                    "model": model,  
                    "messages": [{"role": "user", "content": prompt}],  
                    "max_tokens": 500,  
                    "temperature": 0.1  
                },  
                timeout=30  
            )  
            if response.status_code == 200:  
                content = response.json()["choices"][0]["message"]["content"]  
                content = content.strip()  
                if content.startswith("```"):  
                    content = content.split("```")[1]  
                    if content.startswith("json"):  
                        content = content[4:]  
                result = json.loads(content)  
                print(f"   ✅ Analysis complete!")  
                return result  
            else:  
                print(f"   ⚠️ {response.status_code} — trying next model")  
                time.sleep(5)  
        except Exception as e:  
            print(f"   ⚠️ Error: {e} — trying next model")  
            time.sleep(5)  
    return None

def run_rate_shopper():  
    print("=" * 60)  
    print("🔍 RATE SHOPPER AGENT — Travelier")  
    print("=" * 60)

    results = []

    for route in ROUTES:  
        print(f"\n📍 Route: {route['route']}")  
        print(f"   Operator: {route['operator']}")  
        print(f"   Bookaway Price: ${route['bookaway_price']}")

        # Scrape competitor  
        content = scrape_website(route['operator_website'])

        # AI Analysis  
        print("   🧠 Analyzing with AI...")  
        analysis = analyze_with_ai(route, content)

        if analysis:  
            result = {  
                "route": route['route'],  
                "operator": route['operator'],  
                "bookaway_price": route['bookaway_price'],  
                "bookaway_bookings_ytd": route['bookaway_bookings_ytd'],  
                "vehicle_type": route['vehicle_type'],  
                "scraped_at": "2026-05-19",  
                **analysis  
            }  
            results.append(result)

            print(f"\n   📊 RESULTS:")  
            print(f"   Competitor prices: {analysis.get('competitor_prices')}")  
            print(f"   Market average: ${analysis.get('market_average')}")  
            print(f"   Bookaway position: {analysis.get('bookaway_position')}")  
            print(f"   Recommendation: {analysis.get('recommendation')}")  
            print(f"   Confidence: {analysis.get('confidence')}")  
        else:  
            print("   ❌ AI analysis failed for this route")

    # Save results  
    output = {  
        "generated_at": "2026-05-19",  
        "brand": "Bookaway",  
        "routes_analyzed": len(results),  
        "results": results,  
        "supply_gaps": [  
            {  
                "operator": "Aventuras El Lago",  
                "route": "La Fortuna → San José Airport",  
                "source": "aventurasellago.com / shuttlecr.com",  
                "estimated_demand": "HIGH",  
                "status": "NOT ON BOOKAWAY"  
            },  
            {  
                "operator": "Aventuras El Lago",  
                "route": "Monteverde → San José",  
                "source": "shuttlecr.com",  
                "estimated_demand": "MEDIUM",  
                "status": "NOT ON BOOKAWAY"  
            },  
            {  
                "operator": "Aventuras El Lago",  
                "route": "La Fortuna → Manuel Antonio",  
                "source": "shuttlecr.com",  
                "estimated_demand": "MEDIUM",  
                "status": "NOT ON BOOKAWAY"  
            }  
        ]  
    }

    with open("rate_shopper_result.json", "w") as f:  
        json.dump(output, f, indent=2)

    print("\n" + "=" * 60)  
    print(f"✅ Done! {len(results)} routes analyzed")  
    print("📁 Results saved to rate_shopper_result.json")  
    print("=" * 60)

    return output

# Run the agent  
run_rate_shopper() 
