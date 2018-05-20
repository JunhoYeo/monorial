#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1. neural network (초기 가중치는 랜덤으로 적절히 조절)
import sys
import collections
import numpy as np

# def sigmoid(x): # sigmoid(시그모이드) 함수 : 은닉층에서 사용하는 활성화 함수
#     return 1 / (1 + np.exp(-x))

def softmax(a): # softmax(소프트맥스) 함수 : 출력층에서 사용하는 활성화 함수
    c = np.max(a)
    exp_a = np.exp(a - c)
    return exp_a / np.sum(exp_a)

def cross_entropy_error(y, t): # 교차 엔트로피 오차 함수 : 손실 함수로 사용
    # 배치 데이터 처리를 하게 될 수도 있으므로 모두를 처리할 수 있도록 구현된 코드를 사용
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t.astype('int64')])) / batch_size
    '''
    >>> t = [0, 0, 1]
    >>> y = [0.5, 0.5]
    >>> cross_entropy_error(np.array(y), np.array(t))
    2.0794415416798357
    '''
    # 위와 같이 테스트한 결과 정상적으로 작동함

class Relu:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0
        return out

    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout
        return dx

class Affine:
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.x = None
        self.original_x_shape = None
        # 가중치와 편향 매개변수의 미분
        self.dW = None
        self.db = None

    def forward(self, x):
        # 텐서 대응
        self.original_x_shape = x.shape
        x = x.reshape(x.shape[0], -1)
        self.x = x
        out = np.dot(self.x, self.W) + self.b
        return out

    def backward(self, dout):
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)
        dx = dx.reshape(*self.original_x_shape)  # 입력 데이터 모양 변경(텐서 대응)
        return dx

class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None # 손실함수
        self.y = None    # softmax의 출력
        self.t = None    # 정답 레이블(원-핫 인코딩 형태)
        
    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size: # 정답 레이블이 원-핫 인코딩 형태일 때
            dx = (self.y - self.t) / batch_size
        else:
            dx = self.y.copy()
            dx[np.arange(batch_size), self.t] -= 1
            dx = dx / batch_size
        return dx

class Network:
    # input_size : 입력층의 뉴런 수 (제 1층)
    # hidden_size : 은닉층의 뉴런 수
        # hidden_size[0] : 첫 번째 은닉층의 뉴런 수 (제 2층)
        # hidden_size[1] : 두 번째 은닉층의 뉴런 수 (제 3층)
        # hidden_size[2] : 두 번째 은닉층의 뉴런 수 (제 4층)
    # output_size : 출력층의 뉴런 수
    def __init__(self, input_size, hidden_size, output_size):
        weight_init_std = 0.01
        self.params = {}
        self.params['w1'] = weight_init_std * np.random.randn(input_size, hidden_size[0])
        self.params['b1'] = np.zeros(hidden_size[0])
        self.params['w2'] = weight_init_std * np.random.randn(hidden_size[0], hidden_size[1])
        self.params['b2'] = np.zeros(hidden_size[1])
        self.params['w3'] = weight_init_std * np.random.randn(hidden_size[1], hidden_size[2])
        self.params['b3'] = np.zeros(hidden_size[2])
        self.params['w4'] = weight_init_std * np.random.randn(hidden_size[2], output_size)
        self.params['b4'] = np.zeros(output_size)
        # 계층 생성
        self.layers = collections.OrderedDict()
        self.layers['Affine1'] = Affine(self.params['w1'], self.params['b1'])
        self.layers['Relu1'] = Relu()
        self.layers['Affine2'] = Affine(self.params['w2'], self.params['b2'])
        self.layers['Relu2'] = Relu()
        self.layers['Affine3'] = Affine(self.params['w3'], self.params['b3'])
        self.layers['Relu3'] = Relu()
        self.layers['Affine4'] = Affine(self.params['w4'], self.params['b4'])
        self.lastLayer = SoftmaxWithLoss()
    
    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)
        return x

    def loss(self, x, t):
        y = self.predict(x)
        return self.lastLayer.forward(y, t)

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        if t.ndim != 1 : 
            t = np.argmax(t, axis=1)
        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy

    def gradient(self, x, t):
        # forward
        self.loss(x, t)
        # backward
        dout = 1
        dout = self.lastLayer.backward(dout)
        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)
        # 결과 저장
        grads = {}
        grads['w1'], grads['b1'] = self.layers['Affine1'].dW, self.layers['Affine1'].db
        grads['w2'], grads['b2'] = self.layers['Affine2'].dW, self.layers['Affine2'].db
        grads['w3'], grads['b3'] = self.layers['Affine3'].dW, self.layers['Affine3'].db
        grads['w4'], grads['b4'] = self.layers['Affine4'].dW, self.layers['Affine4'].db
        return grads

# if __name__ == '__main__':
#     net = Network(26, [50, 200, 800], 676)
#     print('w1 shape : ' + str(net.params['w1'].shape))
#     print('L b1 shape : ' + str(net.params['b1'].shape))
#     print('w2 shape : ' + str(net.params['w2'].shape))
#     print('L b2 shape : ' + str(net.params['b2'].shape))
#     print('w3 shape : ' + str(net.params['w3'].shape))
#     print('L b3 shape : ' + str(net.params['b3'].shape))
#     print('w4 shape : ' + str(net.params['w4'].shape))
#     print('L b4 shape : ' + str(net.params['b4'].shape))
