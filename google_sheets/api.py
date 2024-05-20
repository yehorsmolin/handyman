from google.oauth2.service_account import Credentials
import os.path

import gspread
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCredentials

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Handyman.settings')

# django.setup()

from inventory.models import Product


CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")


def get_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=scopes)

    client = gspread.authorize(credentials)

    return client


def get_user_client(user):
    token = user.socialaccount_set.get(provider="google").socialtoken_set.get().token
    refresh_token = user.socialaccount_set.get(provider="google").socialtoken_set.get().token_secret

    credentials = UserCredentials(
        token=token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(credentials)

    return client


def write_to_sheet(sheet_name, range_name, data, user=None):
    client = get_user_client(user) if user else get_client()

    spreasheet = client.open("Handyman")

    sheet = spreasheet.worksheet(sheet_name)

    sheet.update(range_name, data)


def read_from_sheet(range_name):
    client = get_client()

    spreasheet = client.open("Handyman")

    sheet = spreasheet.sheet1

    values = sheet.get(range_name)

    return values


def write_available_stock_to_sheet(sheet_name, range_name, user=None):
    client = get_user_client(user) if user else get_client()

    spreadsheet = client.open("Handyman")
    sheet = spreadsheet.worksheet(sheet_name)

    # Retrieve all products that are not sold (status id is not 6)
    available_products = Product.objects.exclude(status_id=6)

    # Extract data for each available product
    data = []
    for product in available_products:
        # Exclude fields that are not required
        product_data = {
            "title": product.title,
            "price": str(product.price),
            "storage": str(product.storage),
            "grade": str(product.grade),
            "color": str(product.color),
            "imei": product.imei
        }
        data.append(product_data)

    # Write data to Google Sheets
    for i, product_data in enumerate(data):
        row = i + 2  # Adjust row number to account for headers
        for j, field_value in enumerate(product_data.values()):
            column = j + 1
            sheet.update_cell(row, column, field_value)

if __name__ == "__main__":
    write_available_stock_to_sheet('Sheet1','A1')