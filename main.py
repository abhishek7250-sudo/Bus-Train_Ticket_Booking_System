# Bus/Train Ticket Booking System
# Console-Based Application in Python 3

TOTAL_SEATS = 10
FARE = 500
REFUND_PERCENTAGE = 0.80  # 80% refund = Rs. 400

# Data structures as per synopsis
seats = [True] * (TOTAL_SEATS + 1)  # Index 1 to 10: True means free, False means booked
bookings = {}  # {seat_number: "Passenger Name"}


def validate_seat(seat_str):
    """Checks that the seat is an integer from 1 to 10."""
    try:
        seat = int(seat_str)
        if 1 <= seat <= TOTAL_SEATS:
            return seat
        else:
            print(f"Invalid seat. Choose a seat from 1 to {TOTAL_SEATS}.")
            return None
    except ValueError:
        print(f"Invalid seat. Choose a seat from 1 to {TOTAL_SEATS}.")
        return None


def validate_name(name):
    """Checks that the passenger name is not empty and contains valid characters."""
    clean_name = name.strip()
    if clean_name and all(c.isalpha() or c.isspace() for c in clean_name):
        return clean_name
    print("Please enter a valid passenger name (letters only).")
    return None


def view_seats():
    """Displays the available seats and the number of seats left."""
    available = [str(i) for i in range(1, TOTAL_SEATS + 1) if seats[i]]
    seats_left = len(available)

    print("\n--- Available Seats ---")
    if seats_left == 0:
        print("No seats available. Bus is full.")
    else:
        print(f"Available seats: {', '.join(available)}")
    print(f"Seats left: {seats_left}")


def book_seat():
    """Books a free seat for a passenger, charges Rs.500 and shows remaining seats."""
    available_count = sum(1 for i in range(1, TOTAL_SEATS + 1) if seats[i])
    if available_count == 0:
        print("Bus is now full. No further bookings allowed.")
        return

    seat_input = input(f"Enter seat number (1 to {TOTAL_SEATS}): ")
    seat = validate_seat(seat_input)
    if seat is None:
        return

    if not seats[seat]:
        print(f"Seat {seat} is already booked.")
        return

    name_input = input("Enter passenger name: ")
    name = validate_name(name_input)
    if name is None:
        return

    # Confirm booking
    seats[seat] = False
    bookings[seat] = name
    seats_left = sum(1 for i in range(1, TOTAL_SEATS + 1) if seats[i])

    print(f"Seat {seat} booked for {name}. Fare: {FARE}. Seats left: {seats_left}", end="")
    if seats_left == 0:
        print(". Bus is now full.")
    else:
        print()


def view_bookings():
    """Lists all current bookings with seat numbers and passenger names."""
    print("\n--- Current Bookings ---")
    if not bookings:
        print("No bookings found.")
        return

    for seat in sorted(bookings.keys()):
        print(f"Seat {seat}: {bookings[seat]}")


def cancel_booking():
    """Cancels a booking, frees the seat and calculates 80% refund."""
    seat_input = input("Enter seat number to cancel: ")
    seat = validate_seat(seat_input)
    if seat is None:
        return

    if seats[seat] or seat not in bookings:
        print(f"Seat {seat} is not currently booked.")
        return

    # Process cancellation
    refund_amount = int(FARE * REFUND_PERCENTAGE)
    del bookings[seat]
    seats[seat] = True

    available = [str(i) for i in range(1, TOTAL_SEATS + 1) if seats[i]]
    print(f"Booking for seat {seat} cancelled. Refund: {refund_amount}. Available: {', '.join(available)}")


def main():
    """Main menu loop."""
    while True:
        print("\n==============================")
        print(" BUS TICKET BOOKING SYSTEM")
        print("==============================")
        print("1. View seats")
        print("2. Book")
        print("3. Bookings")
        print("4. Cancel")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            view_seats()
        elif choice == "2":
            book_seat()
        elif choice == "3":
            view_bookings()
        elif choice == "4":
            cancel_booking()
        elif choice == "5":
            print("Thank you for using the Ticket Booking System!")
            break
        else:
            print("Invalid choice. Please select an option between 1 and 5.")


if __name__ == "__main__":
    main()