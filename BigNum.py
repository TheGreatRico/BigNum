BASE = 1000
MAX_LEN = 10000000000
EPSILON = 0.003


class BigNum:
    def __init__(self, string):
        if len(string) == 0 or (len(string) == 1 and string[0] == '-'):
            string = '0'
        if string[0] == '-':
            self.sign = '-'
            string = string[1:]
        else:
            self.sign = ''

        # deleting leading zeros
        if len(string) > 1:
            string.lstrip('0')
        self._len = self._determine_length(string)
        self.value = [0] * self._len
        self._create_bignum_from_string(string)

    def _determine_length(self, string):
        length = 0
        try:
            int(string)
        except ValueError:
            print('В вашем числе есть знаки, которые мне непонятны.')
        if (len(string) / len(str(BASE - 1))) % 1 > 0:
            length += 1

        length += round((len(string) / len(str(BASE - 1))) // 1)
        if length > MAX_LEN:
            raise ValueError('Вы задали слишком длинное число. Попробуйте изменить параметры.')
        return length

    def _create_bignum_from_string(self, string):

        try:
            num = int(string)
        except ValueError:
            print('В вашем числе есть знаки, которые мне непонятны.')

        nxt = self._len - 1
        while num > EPSILON:
            self.value[nxt] = num % BASE
            num = num // BASE
            nxt -= 1

    def max(self, other_bignum):
        # comparing signs
        if self.sign != other_bignum.sign:
            if self.sign == '' and other_bignum.sign == '-':
                return self
            elif self.sign == '-' and other_bignum.sign == '':
                return other_bignum

        # comparing length
        if len(self) > len(other_bignum):
            return self
        elif len(self) < len(other_bignum):
            return other_bignum

        # comparing digits of numbers only if both signs and length are equal
        for index in range(len(self)):
            if self.value[index] != other_bignum.value[index]:
                if self.value[index] >= other_bignum.value[index]:
                    return self
                else:
                    return other_bignum
        return self

    def min(self, other_bignum):
        # comparing signs
        if self.sign != other_bignum.sign:
            if self.sign == ' ' and other_bignum.sign == '-':
                return other_bignum
            elif self.sign == '-' and other_bignum.sign == '':
                return self

        # comparing length
        if len(self) > len(other_bignum):
            return other_bignum
        elif len(self) < len(other_bignum):
            return self

        # comparing digits of numbers only if both signs and length are equal
        for index in range(len(self)):
            if self.value[index] != other_bignum.value[index]:
                if self.value[index] >= other_bignum.value[index]:
                    return other_bignum
                else:
                    return self
        return self

    def __add__(self, other_bignum):
        if self == BigNum('0'):
            return other_bignum
        elif other_bignum == BigNum('0'):
            return self

        sign = self.sign
        other_sign = other_bignum.sign
        self_sign = self.sign

        if self.sign == '-' and other_bignum.sign == '-':
            sign = '-'
            self.sign = ''
            other_bignum.sign = ''

        # if -a + b : b - a
        if self.sign == '-' and other_bignum.sign == '':
            return other_bignum - BigNum(self._to_string()[1:])
        # if a + (-b) : a - b
        if self.sign == '' and other_bignum.sign == '-':
            return self - BigNum(other_bignum._to_string()[1:])

        carry = 0
        string = ''
        reversed_self, reversed_other_bignum = self.value[::-1], other_bignum.value[::-1]

        for index in range(len(self.max(other_bignum))):

            if index < len(self) and index < len(other_bignum):
                result = reversed_self[index] + reversed_other_bignum[index] + carry
                if result > (BASE - 1):
                    carry = 1
                    result = str(result)[1:]
                    string = result.zfill(len(str(BASE-1))) + string
                else:
                    carry = 0
                    string = str(result).zfill(len(str(BASE-1))) + string

            elif index < len(other_bignum):
                result = reversed_other_bignum[index] + carry
                if result > (BASE - 1):
                    carry = 1
                    result = str(result)[1:]
                    string = str(result).zfill(len(str(BASE-1))) + string
                else:
                    carry = 0
                    string = str(result).zfill(len(str(BASE-1))) + string

            elif index < len(self):
                result = reversed_self[index] + carry
                if result > (BASE - 1):
                    carry = 1
                    result = str(result)[1:]
                    string = result.zfill(len(str(BASE-1))) + string
                else:
                    carry = 0
                    string = str(result).zfill(len(str(BASE-1))) + string

        string = str(carry) + string
        string = string.lstrip('0')
        string = sign + string
        res = BigNum(string)
        self.sign = self_sign
        other_bignum.sign = other_sign

        return res

    def __sub__(self, other_bignum):
        other_sign = other_bignum.sign
        self_sign = self.sign
        # if -a -b : -(a + b)
        if self.sign == '-' and other_bignum.sign == '':
            return self + BigNum('-' + other_bignum._to_string())
        # if a - (-b)
        if self.sign == '' and other_bignum.sign == '-':
            return self + BigNum(other_bignum._to_string()[1:])

        if self == other_bignum:
            return BigNum('0')

        if other_bignum == self.max(other_bignum):
            smaller_num, bigger_num = self.value[::-1], other_bignum.value[::-1]
            signbit = '-'
        else:
            smaller_num, bigger_num = other_bignum.value[::-1], self.value[::-1]
            signbit = other_bignum.sign

        carry = 0
        string = ''

        for index in range(len(self.max(other_bignum))):
            if index < len(smaller_num):
                result = bigger_num[index] - smaller_num[index] - carry
                if result < 0:
                    result += BASE
                    carry = 1
                else:
                    carry = 0
                result = str(result).zfill(len(str(BASE-1)))
                string = str(result) + string
            else:
                result = bigger_num[index] - carry
                if result < 0:
                    result += BASE
                    carry = 1
                else:
                    carry = 0
                result = str(result).zfill(len(str(BASE-1)))
                string = str(result) + string

        string = string.lstrip('0')
        string = signbit + string

        ret_bignum = BigNum(string)

        self.sign = self_sign
        other_bignum.sign = other_sign
        return ret_bignum

    def __eq__(self, other_bignum):
        if self.sign != other_bignum.sign:
            return False
        if len(self) != len(other_bignum):
            return False
        for index in range(len(self)):
            if self.value[index] != other_bignum.value[index]:
                return False
        return True

    def __truediv__(self, other_bignum):
        other_sign = other_bignum.sign
        self_sign = self.sign
        copy_self = self
        copy_other = other_bignum
        sign = ''
        if self.sign != other_bignum.sign:
            sign = '-'
            copy_self.sign = ''
            copy_other.sign = ''

        tmp = BigNum(copy_self._to_string())
        counter = 0
        while tmp.max(copy_other) == tmp:
            tmp = tmp - copy_other
            counter += 1

        if sign == '-':
            counter = -1 * counter

        self.sign = self_sign
        other_bignum.sign = other_sign
        return counter

    def _digit_shift(self, power):
        value = self.value
        sign = self.sign

        value = value + [0] * power

        s = str()
        for index in range(len(value)):
            s += str(value[index]).zfill(len(str(BASE-1)))
        if len(s) > 1:
            s = s.lstrip('0')

        if sign == '-':
            s = sign + s

        return BigNum(s)

    def _digit_shift_left(self, power):
        if power == 0:
            return self

        value = self.value
        sign = self.sign
        l = len(self)

        value = value[:l-power]

        s = str()
        for index in range(len(value)):
            s += str(value[index]).zfill(len(str(BASE-1)))
        if len(s) > 1:
            s = s.lstrip('0')

        if sign == '-':
            s = sign + s

        return BigNum(s)

    def multiplication_naive(self, other_bignum):
        if self == BigNum('0') or other_bignum == BigNum('0'):
            return BigNum('0')
        if self == BigNum('1'):
            return BigNum(other_bignum._to_string())
        if other_bignum == BigNum('1'):
            return BigNum(self._to_string())

        multiplier = self.min(other_bignum)
        multiplier = str(multiplier.value[0])[::-1]
        number = self.max(other_bignum)
        pwr = 0
        product = list()
        for mult in multiplier:
            mult = int(mult)

            carry = 0
            s = str()
            index = len(number)
            for index in range(len(number), 0, -1):
                result = number.value[index-1] * mult + carry

                if result > (BASE-1):
                    carry = int(str(result)[0])
                    result = str(result)[1:]
                    result = result.zfill(len(str(BASE-1)))
                    s = result + s
                else:
                    carry = 0
                    result = str(result)
                    result = result.zfill(len(str(BASE-1)))
                    s = result + s

            product.append(str(carry) + s + ('0' * pwr))
            pwr += 1

        summ = BigNum('0')
        for item in product:
            summ = summ + BigNum(item)
        return summ

    def __mul__(self, bignum2):
        # Base case
        if len(self) <= 1 or len(bignum2) <= 1:
            return self.multiplication_naive(bignum2)

        # Sign
        sign = ''
        if self.sign != bignum2.sign:
            sign = '-'

        # Making numbers equal length and even
        divider = 0
        if len(self) != len(bignum2) or len(self) % 2 != 0 or len(bignum2) % 2 != 0:
            divider, self, bignum2 = self._self_calc_shift(bignum2)

        # Karatsuba function body
        m = min(len(self), len(bignum2))
        m2 = int(m / 2)

        high1, low1 = self._split_at(m2)
        high2, low2 = bignum2._split_at(m2)

        z0 = low1 * low2
        z2 = high1 * high2
        tmp1 = (low1 + high1)
        tmp2 = (low2 + high2)

        z1 = tmp1 * tmp2

        z1 = z1 - z2
        z1 = z1 - z0

        component1 = z2._digit_shift(m)
        component2 = z1
        component2 = component2._digit_shift(m2)
        result = component1 + component2
        result = result + z0
        result = result._digit_shift_left(divider)

        result.sign = sign
        return result

    def _self_calc_shift(self, bignum2):
        l1 = len(self)
        l2 = len(bignum2)

        if l2 != l1:
            if l2 > l1:
                l1 += (l2 - l1)
            if l1 > l2:
                l2 += (l1 - l2)

        if l1 % 2 != 0:
            l1 += 1
            l2 += 1

        l1 = l1 - len(self)
        l2 = l2 - len(bignum2)
        return_bignum1 = self._digit_shift(l1)
        return_bignum2 = bignum2._digit_shift(l2)
        return l1 + l2, return_bignum1, return_bignum2

    def _calculate_shift(self, bignum1, bignum2):
        l1 = len(bignum1)
        l2 = len(bignum2)

        if l2 != l1:
            if l2 > l1:
                l1 += (l2 - l1)
            if l1 > l2:
                l2 += (l1 - l2)

        if l1 % 2 != 0:
            l1 += 1
            l2 += 1

        l1 = l1 - len(bignum1)
        l2 = l2 - len(bignum2)
        return_bignum1 = bignum1._digit_shift(l1)
        return_bignum2 = bignum2._digit_shift(l2)
        return l1 + l2, return_bignum1, return_bignum2

    def print(self):
        s = str()
        for index in range(len(self)):
            s += ' ' + str(self.value[index]).zfill(4)
        if len(s) > 1:
            s = s.lstrip('0')
        if self.sign == '-':
            s = self.sign + s
        return s

    @staticmethod
    def input(string):
        while True:
            num = input(string)
            num = num.replace(" ", "")

            try:
                int(num)
                break
            except ValueError:
                print('Не понимаю введенного Вами числа, попробуйте еще раз')
                continue

        return BigNum(num)

    def _split_at(self, index):
        high_s, low_s = '', ''
        lst = list()
        for i in range(len(self)):
            lst += [self.value[i]]
        high = lst[:index]
        low = lst[index:]
        for i in range(len(high)):
            high_s += str(high[i]).zfill(len(str(BASE-1)))
        for i in range(len(low)):
            low_s += str(low[i]).zfill(len(str(BASE-1)))
        low_s = low_s.lstrip('0')
        if low_s == '':
            low_s = '0'
        return (BigNum(high_s), BigNum(low_s))

    def _to_string(self):
        s = str()
        for index in range(len(self)):
            s += str(self.value[index]).zfill(len(str(BASE-1)))
        if len(s) > 1:
            s = s.lstrip('0')
        if self.sign == '-':
            s = self.sign + s
        return s

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return self._to_string()

    def __repr__(self):
        return self._to_string()


def main():
    #bignumA = BigNum.input('Введите первое число: ')
    #bignumB = BigNum.input('Введите второе число: ')

    bignumA = BigNum('10000000000')
    bignumB = BigNum('2394782389472')
    print('A =', bignumA)
    print('B =', bignumB)

    print('Проверка базовых операций:')
    print('10 * 1040 =', BigNum('10').multiplication_naive(BigNum('1040')))
    print('20 * 3020 =', BigNum('2').multiplication_naive(BigNum('3020')))
    print('10 000 000 000 * 2 394 782 389 472 =', bignumA * bignumB)

    print('B - A = ', bignumB - bignumA)
    print('A - B = ', bignumA - bignumB)
    print('A + B = ', bignumA + bignumB)
    karatsuba = bignumA * bignumB
    print('A * B = ', karatsuba, 'Количество разрядов:', len(karatsuba._to_string()))
    print('max(A, B) : ', bignumA.max(bignumB))
    print('A / B = ', bignumA / bignumB)



if __name__ == '__main__':
    main()
