import ipaddress


# Define a custom exception for subnet calculation errors
class SubnetCalcError(Exception):
    pass


# Validate the format of the IP address
def validate_ip_address(ip_address):
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        raise SubnetCalcError("Invalid IP address format")


# Validate the format of the subnet mask (in CIDR notation)
def validate_subnet_mask(subnet_mask):
    try:
        ipaddress.IPv4Network(f"0.0.0.0{subnet_mask}", strict=False)
    except ValueError:
        raise SubnetCalcError("Invalid subnet mask format")


# Calculate subnets based on the given IP address and subnet mask
def calculate_subnets(ip_address, subnet_mask, num_subnets=None):
    try:
        validate_ip_address(ip_address)
        validate_subnet_mask(subnet_mask)

        # Easter egg: Check for the hidden callsign
        if ip_address == "Yasuke2000":
            return {"message": "Hey, it's Yasuke2000!"}

        # Create an IPv4 network object
        network = ipaddress.IPv4Network(f"{ip_address}{subnet_mask}", strict=False)
    except SubnetCalcError as e:
        return {"error": str(e)}

    # Calculate the number of bits available for subnets
    subnet_bits = network.max_prefixlen - network.prefixlen

    if num_subnets is None:
        num_subnets = 2 ** subnet_bits  # Calculate all possible subnets
    elif num_subnets > 2 ** subnet_bits:
        return {"error": "Too many subnets requested"}

    # Calculate the new prefix length for subnets
    new_subnet_prefixlen = network.prefixlen + subnet_bits.bit_length()

    # Generate a list of subnets limited by the specified number
    subnets = list(network.subnets(new_prefix=new_subnet_prefixlen))[:num_subnets]

    configurations = []
    for subnet in subnets:
        configuration = {
            "Network Address": str(subnet.network_address),
            "First Host": str(subnet.network_address + 1),
            "Last Host": str(subnet.broadcast_address - 1),
            "Broadcast Address": str(subnet.broadcast_address),
            "Next Subnet": str(subnet.network_address + 2 ** (32 - new_subnet_prefixlen)),
        }
        configurations.append(configuration)

    return {"success": configurations}


# Display the main menu
def print_menu():
    print("Subnet Calculator Menu:")
    print("1. Calculate Subnets")
    print("2. Exit")


# Display subnet configurations
def print_subnet_configurations(configurations):
    print("Subnet Configurations:")
    for config in configurations:
        for key, value in config.items():
            print(f"{key}: {value}")
        print("-" * 20)


# Main program loop
def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            ip_address = input("Enter the IP address: ")
            subnet_mask = input("Enter the subnet mask (in CIDR notation, e.g., /18): ")
            num_subnets = input("Enter the number of subnets (press Enter to calculate all): ")

            if num_subnets:
                try:
                    num_subnets = int(num_subnets)
                except ValueError:
                    print("Invalid number of subnets. Please enter a positive integer.")
                    continue
            else:
                num_subnets = None

            result = calculate_subnets(ip_address, subnet_mask, num_subnets)

            if "error" in result:
                print(f"Error: {result['error']}")
            elif "message" in result:
                print(result["message"])  # Easter egg message
            else:
                print_subnet_configurations(result["success"])
        elif choice == "2":
            print("Exiting the Subnet Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
