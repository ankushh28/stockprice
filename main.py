from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/stock-price/")
def get_stock_price(ticker: str, exchange: str):
    try:
        url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        class1 = 'YMlKec fxKbKc'
        price_element = soup.find(class_=class1)

        if not price_element:
            raise HTTPException(status_code=404, detail="Price not found")

        price = float(price_element.text.strip()[1:].replace(",", ""))
        return {"ticker": ticker, "exchange": exchange, "price": price}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
