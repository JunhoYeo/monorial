#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1. neural network (초기 가중치는 랜덤으로 적절히 조절)
from net import *
from game import *

if __name__ == '__main__':
    net = Network(26, [50, 100], 26)
    # x = np.array([1.0, 0.5])
    # y = network.predict(x)
    # print(y)
    print('w1 shape : ' + str(net.params['w1'].shape))
    print('L b1 shape : ' + str(net.params['b1'].shape))
    print('w2 shape : ' + str(net.params['w2'].shape))
    print('L b2 shape : ' + str(net.params['b2'].shape))
    print('w3 shape : ' + str(net.params['w3'].shape))
    print('L b3 shape : ' + str(net.params['b3'].shape))

	# 현재 게임판의 타일 상태를 입력으로 받음
	# 배열의 인덱스 : 흰 타일(0~11 + 조커) + 검은 타일(0~11 + 조커) => 26개 원소(인덱스 0~25)
	# 0 : 흰 타일 0
	# 1 : 흰 타일 1
	# 2 : 흰 타일 2
	# 3 : 흰 타일 3
	# 4 : 흰 타일 4
	# 5 : 흰 타일 5
	# 6 : 흰 타일 6
	# 7 : 흰 타일 7
	# 8 : 흰 타일 8
	# 9 : 흰 타일 9
	# 10 : 흰 타일 10
	# 11 : 흰 타일 11
	# 12 : 흰 조커
	# 13 : 검은 타일 0
	# 14 : 검은 타일 1
	# 15 : 검은 타일 2
	# 16 : 검은 타일 3
	# 17 : 검은 타일 4
	# 18 : 검은 타일 5
	# 19 : 검은 타일 6
	# 20 : 검은 타일 7
	# 21 : 검은 타일 8
	# 22 : 검은 타일 9
	# 23 : 검은 타일 10
	# 24 : 검은 타일 11
	# 25 : 검은 조커
    # x = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]])
    # print(x)
    # y = net.predict(x)
    # print(y)
	
    # x_train = (학습) 입력 데이터
    # t_train = (학습) 정답 

    # iters_num = 10000  # 반복 횟수를 적절히 설정한다.
    # train_size = x_train.shape[0]
    # batch_size = 100   # 미니배치 크기
    # learning_rate = 0.1

    # train_loss_list = []
    # train_acc_list = []
    # # test_acc_list = []

    # # 1에폭당 반복 수
    # iter_per_epoch = max(train_size / batch_size, 1)

    # for i in range(iters_num):
    #     # 미니배치 획득
    #     # batch_mask = np.random.choice(train_size, batch_size)
    #     # x_batch = x_train[batch_mask]
    #     # t_batch = t_train[batch_mask]

    #     # 기울기 계산
    #     #grad = network.numerical_gradient(x_batch, t_batch)
    #     grad = network.gradient(x_batch, t_batch)

    #     # 매개변수 갱신
    #     for key in ('W1', 'b1', 'W2', 'b2'):
    #         network.params[key] -= learning_rate * grad[key]

    #     # 학습 경과 기록
    #     loss = network.loss(x_batch, t_batch)
    #     train_loss_list.append(loss)

    #     # 1에폭당 정확도 계산
    #     if i % iter_per_epoch == 0:
    #         train_acc = network.accuracy(x_train, t_train)
    #         test_acc = network.accuracy(x_test, t_test)
    #         train_acc_list.append(train_acc)
    #         test_acc_list.append(test_acc)
    #         print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

	# # 그래프 그리기
    # markers = {'train': 'o', 'test': 's'}
    # x = np.arange(len(train_acc_list))
    # plt.plot(x, train_acc_list, label='train acc')
    # plt.plot(x, test_acc_list, label='test acc', linestyle='--')
    # plt.xlabel("epochs")
    # plt.ylabel("accuracy")
    # plt.ylim(0, 1.0)
    # plt.legend(loc='lower right')
    # plt.show()

# 2. input data, get output

# 3. output과 answer(상대의 타일)를 비교, get loss

# 4. 기울기 구해 갱신

# 5. 1~4를 자동화시켜서 서로 플레이하며 배우는 방식으로 자동화

# 6. profit!!! (과연 여기까지 올 수 있을까)

# 7. 만약 되면 GUI(웹서버 열던가)
