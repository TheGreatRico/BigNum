# BigNum
This is a library designed to work with numbers of arbitrary (large) length.

Arbitrary-precision arithmetic is implemented through a single class BigNum, which includes addition and subtraction operations, fast Karatsuba's multiplication with computational complexity $O(n^{log_{2}3}) ≈ O(n^{1.58})$.

For members of the BigNum class, arithmetic is implemented using familiar operators such as '*', '+', and '-'. Representation, length and some other dunder methods are also defined for class members.

The **goal** of the project was to learn how to work in the *object-oriented paradigm*, to learn how to *implement algorithms*, and to create our own *libraries* using Python.
