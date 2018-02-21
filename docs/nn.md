# neuron network

## activate functions
[RELU 激活函数及其他相关的函数](http://blog.csdn.net/u013146742/article/details/51986575)

## ReLu

f(x) = max(0, x)

当 x < 0 f(x) = 0
当 x > 0 f(x) = x

如果你使用 ReLU，那么一定要小心设置 learning rate，而且要注意不要让你的网络出现很多 “dead” 神经元，如果这个问题不好解决，那么可以试试 Leaky ReLU、PReLU 或者 Maxout.

友情提醒：最好不要用 sigmoid，你可以试试 tanh，不过可以预期它的效果会比不上 ReLU 和 Maxout.

还有，通常来说，很少会把各种激活函数串起来在一个网络中使用的。