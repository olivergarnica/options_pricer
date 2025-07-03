from black_scholes import BlackScholes


# read evaluate process loop
def repl():
    while True:
        try:
            user_input = input("Enter 'exit' to quit or ENTER to continue: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            # Evaluate the input

            # K
            user_input = input("Enter your K (strike price): ")
            K = float(user_input)

            # S
            user_input = input("Enter your S (current stock price): ")
            S = float(user_input)

            # T
            user_input = input("Enter your T (time to expiration in years): ")
            T = float(user_input)

            # r
            user_input = input("Enter your r (risk-free interest rate as a decimal): ")
            r = float(user_input)

            # sigma
            user_input = input("Enter your sigma (volatility as a decimal): ")
            sigma = float(user_input)

            user_input = input("Enter 'call' for call option or 'put' for put option: ").strip().lower()
            if user_input == 'call':
                result = BlackScholes.call_price(S, K, T, r, sigma)
            elif user_input == 'put':
                result = BlackScholes.put_price(S, K, T, r, sigma)
            else:
                print("Invalid option type. Please enter 'call' or 'put'.")
                continue

            
            print(result)

        except Exception as e:
            print(f"Error: {e}")

repl()