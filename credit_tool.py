from datetime import datetime

def luhn_check(card_number:str) -> bool:
    digits = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    reverse = digits[::-1]

    for i, d in enumerate(reverse):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    
    return checksum % 10 == 0

def mask_number(num):
    clean = "".join(d for d in num if d.isdigit())
    if len(clean) < 4:
        return "****"
    return "*"*(len(clean)-4) + clean[-4:]

def get_credit_profile():
    print("\n=== CREDIT CARD DETAILS ===")

    while True:
        try:
            n = int(input("How many cards do you have? "))
            if n <= 0:
                print("Enter at least 1.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")
    
    cards = []
    current_year = datetime.now().year

    for i in range(1, n+1):
        print(f"\n--- Card {i} ---")

        issuer = input("Card Issuer (bank/company): ")

        number = input("Card number: ").strip()
        valid = luhn_check(number)


        if not valid:
            print("⚠️ WARNING: CARD NUMBER APPEARS INVALID")
            retry = input("Re-enter once to confirm (y/n): ")

            if retry == "y":
                number = input("Re-enter card number: ").strip()
                valid = luhn_check(number)
        
        if not valid:
            print("⚠️ Card still Invalid")
            print("PLEASE CONTACT YOUR BANK OR ISSUER TO VERIFY THIS CARD.\n")

            cards.append({
                "issuer": issuer,
                "number": number,
                "masked": mask_number(number),
                "valid": False
            })

            continue

        while True:
            try:
                limit = float(input("Credit limit: "))
                balance = float(input("Current Outstanding: "))
                if limit <=0 or balance < 0:
                    print("Invalid Number.")
                    continue
                break
            except ValueError:
                print("Enter a valid number.")
        
        while True:
            try:
                opened = int(input("Year opened: "))
                if opened > current_year or opened < 1950:
                    print("Please Enter a Realistic Year. ")
                    continue
                age = current_year - opened
                break
            except ValueError:
                print("Please Enter a Valid Year. ")
        
        while True:
            try:
                late = int(input("Any late payments on this card: "))
                if late < 0:
                    print("Invalid number.")
                    continue
                break
            except ValueError:
                print("Enter a number")
        
        default_flag = input("Any default on this card? (y:yes / n:no): ").lower()
        has_default = default_flag == "y"

        util = min((balance/limit)*100, 100)

        cards.append({
            "issuer": issuer,
            "masked": mask_number(number),
            "number": number,
            "valid": valid,
            "limit": limit,
            "balance": balance,
            "age": age,
            "late": late,
            "default": has_default,
            "util": util
        })
    return cards

def print_card_summaries(cards):
    print("\n=== CARD SUMMARIES ===")

    valid_count = 0

    for c in cards:
        print(f"\n{c['issuer'].upper()} CARD ({c.get('masked','****')})" )
        print("-" * 40)
        if c ["valid"]:
            print("Card Validity : VALID")
            valid_count += 1
        else:
            print("Card Number : INVALID")
        print(f"Utilization : {c['util']:.1f}%")
        print(f"Age of Card : {c['age']} years")

        if c["default"]:
            health = "POOR"
        elif c["late"] == 0:
            health = "EXCELLENT"
        elif c["late"] <=2:
            health = "GOOD"
        else:
            health = "RISKY"
        
        print(f"Repayment  : {health}")
    
    total = len(cards)
    print("\n=== CARD VALIDITY SUMMARY ===")

    if valid_count == total:
        print(f"All {total} cards are valid")
    else:
        print(f"{valid_count} out of {total} cards are valid")
    
    return valid_count

def combine_cards(cards):
    total_limit = sum(c["limit"] for c in cards)
    total_balance = sum(c["balance"] for c in cards)

    avg_utilt = (total_balance / total_limit) * 100 if total_limit else 0
    oldest_age = max(c["age"] for c in cards)

    total_late = sum(c["late"] for c in cards)
    default_exists = any(c["default"] for c in cards)

    on_time_percent = max(0, 100 - total_late*2)

    return {
        "on_time": on_time_percent,
        "utilization": avg_utilt,
        "history": oldest_age,
        "mix": "2" if len(cards) > 1 else "1",
        "inquiries": 1,
        "default": default_exists
    }

def calculate_credit_score(profile):
    score = 300

    repayment = profile["on_time"]/100
    if profile["default"]:
        repayment*=0.5
    score += repayment * 0.35 * 600

    util_factor = max(0, 1 - profile["utilization"]/100)
    score += util_factor * 0.30 * 600

    history_factor = min(profile["history"]/20, 1)
    score += history_factor * 0.15 * 600

    mix_map = {"1":0.4, "2":0.8, "3":1}
    score += mix_map.get(profile["mix"],0.4) * 0.10 * 600

    score += 0.10 * 600

    return round(min(score,900), 0)

def classify_score(score):
    if score >= 750:
        india = "EXCELLENT"
    elif score >= 650:
        india = "GOOD"
    elif score >= 550:
        india = "FAIR"
    else:
        india = "POOR"
    
    if score >= 800:
        us = "EXCEPTIONAL"
    elif score >= 670:
        us = "GOOD"
    elif score >=580:
        us = "FAIR"
    else:
        us = "POOR"
    
    return india, us

def run_credit_tool():
    print("\n=== CREDIT CARD CHECKER ===")

    cards = get_credit_profile()
    valid_cards = print_card_summaries(cards)

    valid_cards = [c for c in cards if c["valid"]]

    if not valid_cards:
        print("\nX No valid cards available for credit scoring.")
        print("PLEASE CONTACT YOUR RESPECTIVE BANK OR CARD ISSUER.")
        return
    
    profile = combine_cards(valid_cards)
    score = calculate_credit_score(profile)
    india, us = classify_score(score)

    print("\n=== OVERALL CREDIT REPORT ===")
    print(f"Estimated Score: {score}")
    print(f"India Rating   : {india}")
    print(f"US Rating      :{us}")
    print()