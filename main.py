from Nat import Nat

if __name__ == '__main__':
    print(Nat(r'Z plus Z is Z'))
    print(Nat(r'Z plus S(S(Z)) is S(S(Z))'))
    print(Nat(r'S(S(Z)) plus Z is S(S(Z))'))
    print(Nat(r'S(Z) plus S(S(S(Z))) is S(S(S(S(Z))))'))
    print(Nat(r'Z times S(S(Z)) is Z'))
    print(Nat(r'S(S(Z)) times Z is Z'))
    print(Nat(r'S(S(Z)) times S(Z) is S(S(Z))'))
    print(Nat(r'S(S(Z)) times S(S(Z)) is S(S(S(S(Z))))'))