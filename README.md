# Logistic Map Generator
### Logistic Map Generator class - output mapped to arbitrary fractal depth

The logistic Map recursively maps an input value in the interval [0, 1.0] onto the same interval according to the function:
</br><img src='http://mathurl.com/render.cgi?%5Ctextmode%20%5Cdisplaystyle%20x_%7Bn+1%7D%3Drx_%7Bn%7D%5Cleft%281-x_%7Bn%7D%5Cright%29%5Cnocache'>

The map is known to transition from periodic behaviour into a chaotic one by varying the value of **r** of the function displayed, independent of the input value of **x**. That is quite cool with very interesting implications.
For reference, [see here](https://en.wikipedia.org/wiki/Logistic_map) and [here](http://mathworld.wolfram.com/LogisticMap.html)

This class is a simple implementation of the Logistic Map with 2 possible options for the output:
1. Decimal *
2. Alpha *
3. Ternary (for ternary plot output)

the following is an output of the ternary plot clearly showing the periodic-chaotic interplay of the Logistic Map function as r is incremented between [3.0, 4.0)

<p align="center">
  <img src="https://github.com/SubstanceIsFormAndContent/Logistic-Map-Generator/blob/master/visualisations/Ternary%20Plot%20%5Bt%3D0%2C%20t%3D%2B1%2C%20t%3D%2B2%5D%20of%20Logistic%20Map.gif" width="500"/>
</p>

Applying the next() operator on the class will yield: (previous value, current value) i.e. (x @ t = 0, x @ t = +1, ... x @ t = + ret_history). Note the the importance of the plotted point @ [1/3, 13, 1/3] which represents the map's fixed point(s) at x = [0, 1-1/r]

What is even cooler is the indirect expression of [Feigenbaum's Constant](http://mathworld.wolfram.com/FeigenbaumConstant.html) in the periods displayed and how fast they double and become fully chaotic (expecially in periods 2 -> 4 -> 8 -> 16 -> ... CHAOS! -> ... ).

What I find most interesting is the length of the curve that is drawn in the ternay plot and  how it increases in length as a function of r. It is important to note here that the values being plotted are not the output of the logistic map, rather the normalized weight of the last 3 values in time. This implies that as the curve shown in the ternary plot approaches either one of the sides or verticies of the triangle, that the respective time value is eiter much larger or much lower compared to the other two.  

This implies a very interesting characteristic that I plan to investigate further; that there exists a cyclic nature to the chaotic behaviour of the map based on how close the ternary plot is to the sides and veritices of the plot as well as the centroid (fixed point(s)).

### Notes:
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
