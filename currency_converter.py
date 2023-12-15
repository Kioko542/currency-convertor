from forex_python.converter import CurrencyRates
from sqlalchemy.orm import sessionmaker
from database import add_exchange_rate, convert_currency, initialize_database, view_all_exchange_rates, update_exchange_rate

def print_menu():
    print("\nCurrency Converter:")
    print("1. Add Exchange Rate")
    print("2. Convert Currency")
    print("3. View All Exchange Rates")
    print("4. Update Exchange Rate")
    print("5. Quit")

def main():
    engine = initialize_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print_menu()

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            base_currency = input("Enter the base currency code: ")
            target_currency = input("Enter the target currency code: ")
            rate = float(input("Enter the exchange rate: "))

            add_exchange_rate(session, base_currency, target_currency, rate)
            print(f"Exchange rate added: {base_currency} to {target_currency} = {rate}")

        elif choice == '2':
            amount = float(input("Enter the amount to convert: "))
            base_currency = input("Enter the base currency code: ")
            target_currency = input("Enter the target currency code: ")

            converted_amount, new_currency = convert_currency(session, amount, base_currency, target_currency)
            if converted_amount is not None:
                print(f"{amount} {base_currency} is equal to {converted_amount:.2f} {new_currency}")

        elif choice == '3':
            view_all_exchange_rates(session)

        elif choice == '4':
            base_currency = input("Enter the base currency code: ")
            target_currency = input("Enter the target currency code: ")
            new_rate = float(input("Enter the new exchange rate: "))

            update_exchange_rate(session, base_currency, target_currency, new_rate)

        elif choice == '5':
            print("Exiting the currency converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
