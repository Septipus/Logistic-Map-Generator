# Logistic Map Generator
### Logistic Map Generator class - output mapped to arbitrary fractal depth

The logistic Map recursively maps an input value in the interval [0, 1.0] onto the sam einterval according to teh function:
</br><img src='http://mathurl.com/render.cgi?%5Ctextmode%20%5Cdisplaystyle%20x_%7Bn+1%7D%3Drx_%7Bn%7D%5Cleft%281-x_%7Bn%7D%5Cright%29%5Cnocache'>

The map is known to transition from periodic behaviour into a chaotic one by varying the value of **r** of the function displayed, independent of the input value of **x**. That is quite cool with very interesting implications.
For reference, [see here](https://en.wikipedia.org/wiki/Logistic_map)

This class is a simple implementation of the Logistic Map with 2 possible options for the output:
1. Decimal
2. Recursed Alpha

Applying the next() operator on the class will yield: (previous value, current value) i.e. (x @ t-1, x @ t = 0)
* If 'decimal' is chosen as return type, decimal values will be returned. A sample of the sequential application of next() in this case would be:

      (0.5096589132008696, 0.7997014572664898)
      (0.7997014572664898, 0.5125729168394957)
      (0.5125729168394957, 0.7994941496388708)
      (0.7994941496388708, 0.5129704138626869)
      (0.5129704138626869, 0.7994616587655381)

* If 'alpha' is chosen as return type, a label for each of the return values will be generated and returned. The labels generated will correspond to the recursive breakdown of the interval [0, 1.0] through a supplied input alphabet. A sample output for the following init params {alphabet='ABCD', depth=6} is:

      ('BCCBCB', 'DABCCA')
      ('DABCCA', 'CADCCC')
      ('CADCCC', 'DACCAB')
      ('DACCAB', 'CACAAC')
      ('CACAAC', 'DACDDD')
      
### TODO:
* Provide visual explanation of the label creation process
* Provide worked out examples of the expression of a decimal value into a label
