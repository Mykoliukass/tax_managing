from mongo_db_functions import MongoCRUD
import os
import time
from typing import List, Union
import click

# Create an income tax calculator:
# - Generate at least 500 documents , with fields: name, surname, date of birth , age (determined from date of birth), anual salary before tax (EUR, round to 2 numbers after comma)
# - Create a CLI application that would let us get first 10 people from database within the age bracket [min_age, max_age]
# - Those people name surname and age should be shown as an option to choose.
# - When one of ten options is chosen, there should be calculated tax return (it should be created a document as a tax card, values taken from database). Lets say GPM tax is 20% and HealtTax is 15% from 90% of the income left after GPM deduction.
# - The final values should be show and wrriten to database (like a generated data and taxes paid, take home pay etc.) and portrayed in a web page (use flask and docker, show the url were to click )


mongodb_host = "localhost"
mongodb_port = 27017
database_name = "taxes"
collection_name = "people"

db = MongoCRUD(mongodb_host, mongodb_port, database_name, collection_name)


def calculate_tax_return(income):
    gpm_tax_rate = 0.20
    health_tax_rate = 0.15
    left_after_gpm = income * 0.9
    health_tax_amount = left_after_gpm * health_tax_rate
    tax_paid = income * gpm_tax_rate + health_tax_amount
    take_home_pay = income - tax_paid
    return {"tax_paid": round(tax_paid, 2), "take_home_pay": round(take_home_pay, 2)}


def main_menu() -> None:
    while True:
        # os.system("cls")
        print("\n------------------\n|--TAX MANAGER--|\n------------------")
        min_age = click.prompt("Please provide minimum age", default=1, type=int)
        max_age = click.prompt("Please provide maximum age", default=100, type=int)
        try:
            documents = MongoCRUD.get_data_between_ages(
                db.collection, "age", min_age, max_age
            )
        except Exception as e:
            print("Encountered an error: " + str(e))
            continue

        for idx, document in enumerate(documents, 1):
            print(
                f"{idx}. {document.get('name')} {document.get('surname')}, age {document.get('age')}"
            )

        while True:
            try:
                choice = int(input("Select a person (1-10): "))
                if 1 <= choice <= 10:
                    selected_person = documents[choice - 1]
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        tax_card = calculate_tax_return(selected_person["anual_salary_before_tax"])
        print("Tax Information:")
        print(f"Tax Paid: {tax_card['tax_paid']} EUR")
        print(f"Take Home Pay: {tax_card['take_home_pay']} EUR")
        time.sleep(2)


main_menu()
