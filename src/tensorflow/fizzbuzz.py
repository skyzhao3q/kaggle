import numpy as np
import tensorflow as tf

def binary_encode(i, num_digits):
    return np.array([i >> d & 1 for d in range(num_digits)])

def pro_data():
    data_set_list = [binary_encode(i, 14) for i in range(101,10001,1)]
    data_set = np.array(data_set_list)
    data_label = []
    for i in range(101, 10001, 1):
        if i%15==0:
            data_label.append([1,0,0,0])
        elif i%5==0:
            data_label.append([0,1,0,0])
        elif i%3==0:
            data_label.append([0,0,1,0])
        else:
            data_label.append([0,0,0,1])
    data_label = np.array(data_label)

    return data_set, data_label

def predict2word(num, prediction):
    return ['fizzbuzz', 'buzz', 'fizz', str(num)][prediction]

def train_model(epoch=10000):
    # dataset
    train_data, train_label = pro_data()
    # input
    X=tf.placeholder('float32', [None, 14])
    # output
    Y=tf.placeholder('float32', [None,4])
    # weights,bias
    weights1 = tf.Variable(tf.random_normal([14, 32]))
    bias1 = tf.Variable(tf.random_normal([32]))
    weights2 = tf.Variable(tf.random_normal([32, 64]))
    bias2 = tf.Variable(tf.random_normal([64]))
    weights3 = tf.Variable(tf.random_normal([64, 4]))
    bias3 = tf.Variable(tf.random_normal([4]))
    # fc1
    fc1 = tf.nn.relu(tf.matmul(X, weights1)+bias1) 
    # fc2
    fc2 = tf.nn.relu(tf.matmul(fc1, weights2)+bias2)
    # out
    out = tf.matmul(fc2, weights3)+bias3
    # cost
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=Y))
    # opt
    train_op = tf.train.GradientDescentOptimizer(0.01).minimize(cost)
    predict_op = tf.argmax(out, 1)
    # session
    sess = tf.Session()
    # initial
    init_op = tf.initialize_all_variables()
    # run
    sess.run(init_op)
    # log
    for i in range(epoch):
        batch_size = 256
        rand_oder = np.random.permutation(range(len(train_data)))
        train_data,train_label = train_data[rand_oder], train_label[rand_oder]
        for j in range(0, len(train_data)-1, batch_size):
            end = j + batch_size
            sess.run(train_op, feed_dict={X:train_data[j:end], Y:train_label[j:end]})
        print(i, np.mean(np.argmax(train_label, axis=1) == sess.run(predict_op, feed_dict={X: train_data, Y: train_label})))
    # test
    numbers = np.arange(1, 101)
    test_data = np.transpose(binary_encode(numbers, 14))
    test_label = sess.run(predict_op, feed_dict={X: test_data})
    output = np.vectorize(predict2word)(numbers, test_label)
    print(output)

if __name__=="__main__":
    train_model()