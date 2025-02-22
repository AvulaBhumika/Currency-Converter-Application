import gradio as gr
import requests

API_KEY = "API-KEY"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

def get_exchange_rate(from_currency, to_currency): 
    try:
        response = requests.get(BASE_URL + from_currency)
        data = response.json() 

        if "conversion_rates" not in data or to_currency not in data["conversion_rates"]:
            return None, "Error: Unable to fetch exchange rate. Please try again later."

        return data["conversion_rates"][to_currency], None
    except Exception as e:
        return None, f"Error: {str(e)}"

def convert_currency(amount, from_currency, to_currency):
    try:
        if not isinstance(amount, (int, float)) or amount <= 0:
            return "Error: Please enter a valid positive number."
        
        rate, error = get_exchange_rate(from_currency, to_currency)
        if error:
            return error

        converted_amount = amount * rate
        return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} (Rate: {rate})"

    except Exception as e:
        return f"Error: {str(e)}"

available_currencies = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CHF", "CNY", "SGD"]

app = gr.Interface(
    fn=convert_currency,
    inputs=[
        gr.Number(label="Amount"),
        gr.Dropdown(available_currencies, label="From Currency"),
        gr.Dropdown(available_currencies, label="To Currency"),
    ],
    outputs=gr.Textbox(label="Converted Amount"),
    title="AVB Currency Converter",
    description="Convert between multiple currencies with real-time exchange rates.",
)

app.launch(share=True)
