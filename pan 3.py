"""Bus/Train Ticket Booking System (PS 41) - console application in Python 3."""

TOTAL_SEATS = 10
FARE = 500
REFUND_PERCENT = 80

# seats[0] is seat 1 ... seats[9] is seat 10. True = free, False = booked
seats = [True] * TOTAL_SEATS
# passenger details: {seat_number: passenger_name}
bookings = {}


def seats_left():
    return seats.count(True)


def available_seats():
    return [str(i + 1) for i in range(TOTAL_SEATS) if seats[i]]


def validate_seat(value):
    """Return seat number (int) if valid, otherwise None."""
    try:
        seat = int(str(value).strip())
    except ValueError:
        return None
    if 1 <= seat <= TOTAL_SEATS:
        return seat
    return None


def validate_name(name):
    """Name must not be empty and must contain only letters and spaces."""
    name = name.strip()
    if name and all(ch.isalpha() or ch == " " for ch in name):
        return name
    return None


def view_seats():
    if bookings:
        for seat in sorted(bookings):
            print(f"Booked: {seat} ({bookings[seat]})")
    if seats_left() == 0:
        print("Available: None (Bus is full)")
    else:
        print("Available: " + ", ".join(available_seats()))


def book_seat(seat_input, name_input):
    seat = validate_seat(seat_input)
    if seat is None:
        print(f"Invalid seat. Choose a seat from 1 to {TOTAL_SEATS}.")
        return
    if not seats[seat - 1]:
        print(f"Seat {seat} is already booked.")
        return
    name = validate_name(name_input)
    if name is None:
        print("Invalid name. Enter letters only.")
        return
    seats[seat - 1] = False
    bookings[seat] = name
    print(f"Seat {seat} booked for {name}. Fare: {FARE}")
    print(f"Seats left: {seats_left()}")
    if seats_left() == 0:
        print("Bus is now full.")


def view_bookings():
    if not bookings:
        print("No bookings yet.")
        return
    for seat in sorted(bookings):
        print(f"Seat {seat}: {bookings[seat]}")


def cancel_booking(seat_input):
    seat = validate_seat(seat_input)
    if seat is None:
        print(f"Invalid seat. Choose a seat from 1 to {TOTAL_SEATS}.")
        return
    if seats[seat - 1]:
        print(f"Seat {seat} is not booked.")
        return
    del bookings[seat]
    seats[seat - 1] = True
    refund = FARE * REFUND_PERCENT // 100
    print(f"Booking for seat {seat} cancelled. Refund: {refund}")
    print(f"Seats left: {seats_left()}")


def show_menu():
    print("\n--- Bus Ticket Booking System ---")
    print("1. View seats")
    print("2. Book")
    print("3. Bookings")
    print("4. Cancel")
    print("5. Exit")


import io
from contextlib import redirect_stdout


def reset():
    """Make all seats free again (each test case starts with all seats free)."""
    global seats, bookings
    seats = [True] * TOTAL_SEATS
    bookings = {}


def run(func, *args):
    """Run a function, show its output on screen and also return it as text."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    output = buffer.getvalue()
    for line in output.splitlines():
        print("   " + line)
    return output


def silent(func, *args):
    """Run a function without showing its output (used for test setup)."""
    with redirect_stdout(io.StringIO()):
        func(*args)


def check(output, expected_lines):
    ok = all(line in output.splitlines() for line in expected_lines)
    print("   -> " + ("PASS" if ok else "FAIL"))
    return ok


def run_test_cases():
    results = []
    print("=" * 60)
    print("RUNNING ALL TEST CASES")
    print("=" * 60)

    # Test Case 1: Normal Input
    print("\nTest Case 1: Normal Input")
    reset()
    print("  Input: Book seat 3 for Aman")
    out = run(book_seat, "3", "Aman")
    results.append(check(out, ["Seat 3 booked for Aman. Fare: 500", "Seats left: 9"]))

    # Test Case 2: Boundary / Minimum Input
    print("\nTest Case 2: Boundary / Minimum Input")
    reset()
    for s in range(1, 10):
        silent(book_seat, str(s), "Passenger")
    print("  Input: Seats 1 to 9 already booked, book seat 10 for Riya")
    out = run(book_seat, "10", "Riya")
    results.append(check(out, ["Seat 10 booked for Riya. Fare: 500",
                               "Seats left: 0", "Bus is now full."]))

    # Test Case 3: Invalid Input
    print("\nTest Case 3: Invalid Input")
    reset()
    silent(book_seat, "3", "Aman")
    print("  Input: Seat 3 is booked by Aman")
    print("  (a) Book seat 3")
    out_a = run(book_seat, "3", "Aman")
    print("  (b) Book seat 11")
    out_b = run(book_seat, "11", "Aman")
    results.append(check(out_a + out_b, ["Seat 3 is already booked.",
                                         "Invalid seat. Choose a seat from 1 to 10."]))

    # Test Case 4: Different Valid Scenario
    print("\nTest Case 4: Different Valid Scenario")
    reset()
    silent(book_seat, "3", "Aman")
    silent(book_seat, "5", "Riya")
    print("  Input: Booked seat 3 (Aman), seat 5 (Riya)")
    print("  (a) Option 4 (Cancel): seat 3")
    out_a = run(cancel_booking, "3")
    print("  (b) Option 1 (View seats)")
    out_b = run(view_seats)
    results.append(check(out_a + out_b, ["Booking for seat 3 cancelled. Refund: 400",
                                         "Booked: 5 (Riya)",
                                         "Available: 1, 2, 3, 4, 6, 7, 8, 9, 10"]))

    print("\n" + "=" * 60)
    print(f"RESULT: {sum(results)} / {len(results)} TEST CASES PASSED")
    print("=" * 60)


def main():
    run_test_cases()
    reset()
    answer = input("\nOpen the interactive booking menu? (y/n): ").strip().lower()
    if answer != "y":
        print("Thank you!")
        return
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_seats()
        elif choice == "2":
            seat = input("Seat number: ")
            name = input("Passenger name: ")
            book_seat(seat, name)
        elif choice == "3":
            view_bookings()
        elif choice == "4":
            seat = input("Seat number: ")
            cancel_booking(seat)
        elif choice == "5":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Enter 1 to 5.")


if __name__ == "__main__":
    main()