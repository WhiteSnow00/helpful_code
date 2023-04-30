def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def main():
    n = int(input("Enter the number of coin denominations: "))
    coins = list(map(int, input("Enter the coin denominations separated by spaces: ").split()))
    amount = int(input("Enter the target amount: "))
    
    min_coins = coin_change(coins, amount)
    
    if min_coins == -1:
        print("There is no solution to change the target amount with the given coins.")
    else:
        print(f"The minimum number of coins required: {min_coins}")

if __name__ == "__main__":
    main()
