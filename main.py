import random
class LongInt:
    BASE = 1000000000

    def __init__(self, value=0):
        self._digits = []
        self._is_negative = False

        if isinstance(value, str):
            self._init_from_string(value)
        elif isinstance(value, int):
            self._init_from_integer(value)
        else:
            raise TypeError("Unsupported type for initializing LongInt")

    def _init_from_string(self, value_str):
        if len(value_str) == 0:
            self._is_negative = False
        else:
            if value_str[0] == '-':
                value_str = value_str[1:]
                self._is_negative = True
            else:
                self._is_negative = False

            for i in range(len(value_str), 0, -9):
                if i < 9:
                    self._digits.append(int(value_str[0:i]))
                else:
                    self._digits.append(int(value_str[i - 9:i]))

            self._remove_leading_zeros()

    def _init_from_integer(self, value_int):
        if value_int < 0:
            self._is_negative = True
            value_int = abs(value_int)

        while value_int != 0:
            self._digits.append(value_int % self.BASE)
            value_int //= self.BASE

    def _remove_leading_zeros(self):
        while len(self._digits) > 1 and self._digits[-1] == 0:
            self._digits.pop()
        if len(self._digits) == 1 and self._digits[0] == 0:
            self._is_negative = False

    def __str__(self):
        result = ""
        if self._is_negative:
            result += "-"
        if self._digits:
            result += str(self._digits[-1])
            for i in range(len(self._digits) - 2, -1, -1):
                result += str(self._digits[i]).zfill(9)
        else:
            result += "0"
        return result

    def __neg__(self):
        result = LongInt()
        result._digits = self._digits[:]
        result._is_negative = not self._is_negative
        return result

    def __pos__(self):
        result = LongInt()
        result._digits = self._digits[:]
        result._is_negative = self._is_negative
        return result

    def __eq__(self, other):
        if self._is_negative != other._is_negative:
            return False
        if not self._digits:
            return not other._digits or (len(other._digits) == 1 and other._digits[0] == 0)
        if not other._digits:
            return len(self._digits) == 1 and self._digits[0] == 0
        if len(self._digits) != len(other._digits):
            return False
        for i in range(len(self._digits)):
            if self._digits[i] != other._digits[i]:
                return False
        return True

    def __lt__(self, other):
        if self == other:
            return False
        if self._is_negative:
            if other._is_negative:
                return -other < -self
            else:
                return True
        elif other._is_negative:
            return False
        else:
            if len(self._digits) != len(other._digits):
                return len(self._digits) < len(other._digits)
            else:
                for i in range(len(self._digits) - 1, -1, -1):
                    if self._digits[i] != other._digits[i]:
                        return self._digits[i] < other._digits[i]
                return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __add__(self, other):
        if self._is_negative:
            if other._is_negative:
                return -(-self + (-other))
            else:
                return other - (-self)
        elif other._is_negative:
            return self - (-other)
        carry = 0
        result_digits = []
        for i in range(max(len(self._digits), len(other._digits))):
            sum_ = (self._digits[i] if i < len(self._digits) else 0) + (
                other._digits[i] if i < len(other._digits) else 0) + carry
            carry = sum_ // self.BASE
            result_digits.append(sum_ % self.BASE)
        if carry:
            result_digits.append(carry)
        result = LongInt()
        result._digits = result_digits
        return result

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        if other._is_negative:
            return self + (-other)
        elif self._is_negative:
            return -(-self + other)
        elif self < other:
            return -(other - self)
        result_digits = []
        borrow = 0
        for i in range(len(self._digits)):
            diff = self._digits[i] - (other._digits[i] if i < len(other._digits) else 0) - borrow
            if diff < 0:
                diff += self.BASE
                borrow = 1
            else:
                borrow = 0
            result_digits.append(diff)
        result = LongInt()
        result._digits = result_digits
        result._remove_leading_zeros()
        return result

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        result_digits = [0] * (len(self._digits) + len(other._digits))
        for i in range(len(self._digits)):
            carry = 0
            for j in range(len(other._digits)):
                temp = self._digits[i] * other._digits[j] + result_digits[i + j] + carry
                result_digits[i + j] = temp % self.BASE
                carry = temp // self.BASE
            result_digits[i + len(other._digits)] = carry
        result = LongInt()
        result._digits = result_digits
        result._is_negative = self._is_negative != other._is_negative
        result._remove_leading_zeros()
        return result

    def __imul__(self, other):
        return self * other

    def __truediv__(self, other):
        if other == LongInt("0"):
            raise ZeroDivisionError("division by zero")
        divisor = other if other._is_negative == False else -other
        dividend = self if self._is_negative == False else -self
        quotient = LongInt()
        remainder = LongInt()
        for i in range(len(dividend._digits) - 1, -1, -1):
            remainder *= LongInt.BASE
            remainder += LongInt(dividend._digits[i])
            quotient_digit = 0
            while remainder >= divisor:
                remainder -= divisor
                quotient_digit += 1
            quotient._digits.insert(0, quotient_digit)
        quotient._remove_leading_zeros()
        quotient._is_negative = self._is_negative != other._is_negative
        return quotient

    def __itruediv__(self, other):
        return self / other

    def __abs__(self):
        result = LongInt()
        result._digits = self._digits.copy()
        result._is_negative = False
        if self._is_negative:
            result._is_negative = False
        return result

    def __int__(self):
        if not self._digits:
            return 0
        value = self._digits[-1]
        if len(self._digits) > 1:
            for digit in reversed(self._digits[:-1]):
                value = value * 10 ** 9 + digit
        return value

    def __floordiv__(self, other):
        if other == LongInt(0):
            raise ZeroDivisionError("division by zero")
        result = LongInt()
        dividend = abs(self)
        divisor = abs(other)
        quotient = dividend // divisor
        result._digits = quotient._digits
        result._is_negative = self._is_negative != other._is_negative
        return result

    def __mod__(self, other):
        return self - (self // other) * other

    def __imod__(self, other):
        return self % other

    def odd(self):
        if not self._digits:
            return False
        return self._digits[0] & 1

    def even(self):
        return not self.odd()

    def pow(self, n):
        if n == LongInt("0"):
            return LongInt("1")
        result = LongInt("1")
        base = self
        while n > LongInt("0"):
            if n.odd():
                result *= base
            base *= base
            n //= LongInt("2")
        return result

def test_long_int():
    def generate_random_number(min_val, max_val):
        return random.randint(min_val, max_val)

    def test_long_int():
        random.seed()  # Инициализация генератора случайных чисел

        for _ in range(1000000):
            aa = generate_random_number(-45000, 45000)
            bb = generate_random_number(-45000, 45000)
            cc = aa * bb
            dd = cc // bb

            a = LongInt(aa)
            b = LongInt(bb)
            c = a * b
            c2 = LongInt(aa * bb)

            d = c // b

            if d != a:
                print("UNCORRECT d != a")

            if dd != aa:
                print("UNCORRECT dd != aa")

            if d != dd:
                print("UNCORRECT d != dd")

    if __name__ == "__main__":
        test_long_int()


