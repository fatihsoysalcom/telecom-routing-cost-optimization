import random

# Simulate different telecom carriers and their interconnect agreements
# Costs are per "data unit" (e.g., per minute of call, per MB of data).
# These small per-unit costs represent the 'easy tokens' from the article's metaphor.
CARRIER_RATES = {
    "ATT": {"Frontier": 0.05, "Verizon": 0.03, "T-Mobile": 0.04, "DiscountCarrier": 0.01},
    "Frontier": {"ATT": 0.06, "Verizon": 0.02, "T-Mobile": 0.035, "DiscountCarrier": 0.015},
    "Verizon": {"ATT": 0.03, "Frontier": 0.025, "T-Mobile": 0.03, "DiscountCarrier": 0.012},
    "T-Mobile": {"ATT": 0.045, "Frontier": 0.03, "Verizon": 0.028, "DiscountCarrier": 0.013},
    # A hypothetical "Discount Carrier" often used for least-cost routing
    # It offers lower rates for transit, making it attractive for 'redirecting' traffic.
    "DiscountCarrier": {"ATT": 0.01, "Frontier": 0.015, "Verizon": 0.012, "T-Mobile": 0.013}
}

def calculate_route_cost(originating_carrier: str, destination_carrier: str,
                         intermediate_carrier: str = None, data_units: int = 100000) -> float:
    """
    Calculates the total cost for routing data units from origin to destination.
    Can route directly or via an intermediate carrier.
    """
    total_cost = 0.0
    path_description = f"Route: {originating_carrier}"

    if intermediate_carrier:
        # Route via an intermediate carrier
        # Cost from origin to intermediate
        cost_to_intermediate = CARRIER_RATES.get(originating_carrier, {}).get(intermediate_carrier)
        if cost_to_intermediate is None:
            print(f"Error: No direct rate from {originating_carrier} to {intermediate_carrier}")
            return float('inf') # Indicate an invalid path

        total_cost += cost_to_intermediate * data_units
        path_description += f" -> {intermediate_carrier} (Cost: ${cost_to_intermediate:.4f}/unit)"

        # Cost from intermediate to destination
        cost_to_destination = CARRIER_RATES.get(intermediate_carrier, {}).get(destination_carrier)
        if cost_to_destination is None:
            print(f"Error: No direct rate from {intermediate_carrier} to {destination_carrier}")
            return float('inf') # Indicate an invalid path

        total_cost += cost_to_destination * data_units
        path_description += f" -> {destination_carrier} (Cost: ${cost_to_destination:.4f}/unit)"
        # The 'redirection' of 'easy tokens' is demonstrated here: by choosing a specific
        # intermediate, we exploit small per-unit cost differences that accumulate
        # over a large volume of data units, leading to significant overall savings.
    else:
        # Route directly
        cost_direct = CARRIER_RATES.get(originating_carrier, {}).get(destination_carrier)
        if cost_direct is None:
            print(f"Error: No direct rate from {originating_carrier} to {destination_carrier}")
            return float('inf') # Indicate an invalid path

        total_cost += cost_direct * data_units
        path_description += f" -> {destination_carrier} (Cost: ${cost_direct:.4f}/unit)"

    print(f"{path_description}")
    print(f"  Total Cost for {data_units} units: ${total_cost:.2f}\n")
    return total_cost

def main():
    origin = "ATT"
    destination = "Frontier"
    data_volume = 500000 # Simulate a large volume of data units (e.g., call minutes, data packets)

    print(f"Simulating routing {data_volume} data units from {origin} to {destination}\n")

    # Scenario 1: Direct Routing (often the default or most straightforward)
    print("--- Scenario 1: Direct Routing (Default) ---")
    cost_direct = calculate_route_cost(origin, destination, data_units=data_volume)

    # Scenario 2: Routing via a standard intermediary (e.g., Verizon)
    print("--- Scenario 2: Routing via Verizon (Alternative Intermediary) ---")
    cost_via_verizon = calculate_route_cost(origin, destination, intermediate_carrier="Verizon", data_units=data_volume)

    # Scenario 3: Routing via a "Discount Carrier" (illustrating 'redirecting easy tokens')
    # This simulates finding a less obvious but cheaper path to reduce overall billing.
    print("--- Scenario 3: Routing via DiscountCarrier (Optimized 'Easy Token' Redirection) ---")
    cost_via_discount = calculate_route_cost(origin, destination, intermediate_carrier="DiscountCarrier", data_units=data_volume)

    print("\n--- Summary of Routing Costs ---")
    print(f"Direct Route ({origin} -> {destination}): ${cost_direct:.2f}")
    print(f"Route via Verizon ({origin} -> Verizon -> {destination}): ${cost_via_verizon:.2f}")
    print(f"Route via DiscountCarrier ({origin} -> DiscountCarrier -> {destination}): ${cost_via_discount:.2f}")

    if cost_direct > cost_via_discount:
        savings = cost_direct - cost_via_discount
        print(f"\nSignificant savings achieved by 'redirecting easy tokens' via DiscountCarrier!")
        print(f"Savings compared to direct route: ${savings:.2f}")
    elif cost_via_verizon > cost_via_discount:
        savings = cost_via_verizon - cost_via_discount
        print(f"\nSavings achieved by 'redirecting easy tokens' via DiscountCarrier compared to Verizon route!")
        print(f"Savings: ${savings:.2f}")
    else:
        print("\nNo significant savings found with the alternative routes in this simulation.")

if __name__ == "__main__":
    main()
