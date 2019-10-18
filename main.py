# Given a 7-segment LED digit with one defect segment that is always OFF
# - which numbers 0..9 will become ambiguous for any 1 given faulty segment?
# - given alternative renderings, like 6 and 9 resembling b and q, and/or 7 with extra vertical segment,
#   which set is the most resilient against a broken segment?

# Some ASCII art to show the bit number in the digits encodings:
#
#   6666
#  11  55
#  11  55
#   0000
#  22  44
#  22  44
#   3333

# The standard set, where 6 and 9 have the top and bottom segment respectively, and 7 is like a 1 with a top segment
digits = [
    0b1111110, #0
    0b0110000, #1
    0b1101101, #2
    0b1111001, #3
    0b0110011, #4
    0b1011011, #5
    0b1011111, #6
    0b1110000, #7
    0b1111111, #8
    0b1111011, #9
]

# Extra vertical segment for 7 (bit 1)
digits7 = digits.copy()
digits7[7] = 0b1110010

# Remove the top segment from the 6 and the bottom segment from the 9 (like b and q)
digits69 = digits.copy()
digits69[6] = 0b0011111
digits69[9] = 0b1110011

# Combine the variations of 6, 7 and 9
digits679 = digits69.copy()
digits679[7] = digits7[7]


# Run the check for the given digit set
def led(digitSet):
    mask = 0b1000000
    ok = 0
    ambi = 0
    while mask > 0:
        clash = []
        for i in range(0, 10):
            a = digitSet[i] & ~mask
            for j in range(i + 1, 10):
                b = digitSet[j] & ~mask
                if a == b:
                    clash.append((i, j))
                    break
        draw(mask, plus=True)
        mask = mask >> 1
        if len(clash) > 0:
            print("Ambiguous:", clash)
            ambi += len(clash)
        else:
            print("Identifiable")
            ok += 1
    print(f"{ok} OK, {7-ok} not, {ambi} ambiguous pairs.")
    print("-" * 50)
    print()
        
def drawH(d, mask, plus=False):
    if plus:
        print("+--+" if d & mask else "+  +")
    else:
        print(" -- " if d & mask else "")


def drawV(d, mask1, mask2):
    print(f"{'|' if d & mask1 else ' '}  {'|' if d & mask2 else ' '}")

def draw(d, plus=False):
    print()
    drawH(d, 0b1000000, plus)
    drawV(d, 0b0000010, 0b0100000)
    drawH(d, 0b0000001, plus)
    drawV(d, 0b0000100, 0b0010000)
    drawH(d, 0b0001000, plus)

def drawSet(digitSet):
    for d in digitSet:
        draw(d)
        

if __name__ == "__main__":
    #drawSet(digits679)  # uncomment/change to draw a the number of a set
    print("Standard segments")
    led(digits)
    print("7 with extra segment")
    led(digits7)
    print('6 and 9 without horizontal')
    led(digits69)
    print("6 and 9 w/o horizontal, 7 with extra segment")
    led(digits679)

# Conclusion: digits679 is the best, with 5 OK, 2 ambiguous, and 3 clashing pairs. 
# This result is the same for digits69, but there is a difference in on of the pairs:
# (1,7) for digits69 vs. (7,9) for digits679. The latter has a smaller diff between the clashing
# numbers, therefore less severe.
# Surprisingly, the standard has the worst score, with 2 OK, 5 ambiguous, 7 ambiguous pairs.
# Finally, some variations were tried with either 6 or 9 changed, but yielded no better results.