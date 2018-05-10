# Monorial
Monorial(모노리얼) is an AI for the [Coda](https://en.wikipedia.org/wiki/Coda_(board_game))  game.

Coda is usually known as Da Vinci Code(다빈치 코드).

## Gameplay of Coda

- https://en.wikipedia.org/wiki/Coda_(board_game)
- https://namu.wiki/w/%EB%8B%A4%EB%B9%88%EC%B9%98%20%EC%BD%94%EB%93%9C(%EB%B3%B4%EB%93%9C%20%EA%B2%8C%EC%9E%84)

## Implementation

### Basic concept of idea
Machine Learning needs...

- data
- output
- target function
- algorithm to minimize loss

On our application...

- data : AI가 알고 있는, 현재 게임판의 타일 상태
- output : 상대의 타일 하나를 reasoning한 결과
- target function : 현제 게임판의 타일 상태를 입력으로 하고, 상대의 타일 하나를 예측해서 가져온다.
- algorithm to minimize loss : 상대의 타일 하나를 맞추는 데 성공했는가?

장기적으로 게임을 바라보고 bluffing 등의 전략을 하는 경우도 있지만 이는 생각하지 않는다.

### Things to consider

- 조커가 들어온 경우 이를 어디에 place할지도 AI가 직접 정해야 함
- 어떤 타일을 reasoning하는 것이 가장 유리할지 선택해야 함

### End-to-end machine learning
조커 place 문제만 나중에 살펴보고, 일단 기본적으로 end-to-end machine learning(사람의 개입 없이 출력을 얻음)으로 하고 프로그램 두 대를 서로 dual시키며 플레이하는 방식으로 이들을 학습시킬 데이터를 얻기로 함 

따라서 개발 순서는...

1. neural network (초기 가중치는 랜덤으로 적절히 조절)
2. input data, get output
3. output과 answer(상대의 타일)를 비교, get loss
4. 기울기 구해 갱신
5. 1~4를 자동화시켜서 서로 플레이하며 배우는 방식으로 자동화
6. profit!!! (과연 여기까지 올 수 있을까)
7. 만약 되면 GUI(웹서버 열던가)

몰라... 일단 다 야매로 시작하는 거야!

# 인공신경망 만들기

## 딥러닝 특)
무식한 본인 기준이다.

1. 개요 부분만 보면 뭔 내용일지 알 것 같은데 정작 몇 페이지 더 가면 생전 듣도 보다 못한 수식이며 기호가 등장
2. 이렇게 활용해야 할지 감이 안 잡힘

## 야매로 AI 코딩하기
```Python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```
일단 무작정 `app.py` 파일을 만들었다.
```Python
# 1. neural network (초기 가중치는 랜덤으로 적절히 조절)
# 2. input data, get output
# 3. output과 answer(상대의 타일)를 비교, get loss
# 4. 기울기 구해 갱신
# 5. 1~4를 자동화시켜서 서로 플레이하며 배우는 방식으로 자동화
# 6. profit!!! (과연 여기까지 올 수 있을까)
# 7. 만약 되면 GUI(웹서버 열던가)
```
위에서 생각했던 개발 순서를 주석으로 달아두었다.

가만히 생각해보니 1번 단계부터 구현하기 매우 어렵네...

<밑바닥부터 시작하는 딥러닝>의 예제 코드를 이용하려 했건만 그것도 쉽지 않다.

그냥 꼼수부릴 생각은 버리고 처음부터 읽으면서 직접 짜야겠다.

## 신경망 각 층의 배열 형상

### 1차 구상

![picture 1](images/pic_1.png)

입력은 모든 타일 `(0~11 + 조커)*(흑&백)=13*2=26`, 26개 원소로 구성된 현재 타일 상태이고,

출력 역시 원소 26개로 구성된 1차원 배열이다.

일단은 위 그림과 같이 3층으로 구성된 신경망부터 만들어보자.

입력과 출력의 각 원소는 상태에 따라 아래 세 값 중 하나를 가진다.

- `0(상태를 알 수 없음)`
- `1(AI가 가진 타일)`
- `2(상대방이 가진 타일)`

#### 구현

```Python
>>> net = Network(26, [50, 100], 26)
>>> net.params['w1'].shape
(26, 50)
>>> net.params['w2'].shape
(50, 100)
>>> net.params['w3'].shape
(100, 26)
```
형상 구현 성공! 이렇게 하면 대충 될 것 가따.

```
w1 shape : (26, 50)
L b1 shape : (50,)
w2 shape : (50, 100)
L b2 shape : (100,)
w3 shape : (100, 26)
L b3 shape : (26,)
```
편향까지 보면 요렇게 나온다.

#### 헉

```Python
>>> from app import *
>>> x = np.random.rand(1, 26)
>>> t = np.random.rand(1, 26)
>>> net = Network(26, [50, 100], 26)
>>> grads = net.numerical_gradient(x, t)
(에러 발생)
PS C:\Users\JunhoYeo\Documents\GitHub\monorial>
```

헉!! 기울기 산출에 책에 나온 수치 미분 함수를 썼더니 `Python의 작동이 중지되었습니다`라면서 terminated되었다ㅠㅠ

결국 오차역전파법을 써야 하나 보다...

https://stackoverflow.com/questions/36061994/sklearn-cross-validation-raises-indexerror-arrays-used-as-indices-must-be-of-in

구현 중에 `-np.sum(np.log(y[np.arange(batch_size), t])) / batch_size`에서 `IndexError: arrays used as indices must be of integer (or boolean) type`라며 에러가 나길래 위 글 참고, 

`.astype('int64')`를 붙여서 `-np.sum(np.log(y[np.arange(batch_size), t.astype('int64')])) / batch_size` 이렇게 수정했더니 정상적으로 작동했다.

책 예제코드 써서 일단 3층짜리 신경망에 적용해뒀다.

일단 커밋하고 나머지는 학교 컴실에서 해야지

## 응 아니였다(2차 구상)
그런데 조금만 생각해 보니까 위와 같이 형상을 두면 안 된다는 것이 나왔다.

먼저 입력을 생각해보자.

입력에 전혀 '상대방 타일을 배치한 순서'라는 변수가 들어 있지 않다.

상대방의 타일이 `0 1 ? 11`일 때랑 `0 1 11 ?`일 때의 결과는 차원이 다르다.

그런데 플레이어의 타일 수 자체가 유동적이니까 형상 생각하기가 어렵다.

즉, 형상은 그대로 두고 배열을 이루는 원소의 값을 바꾸는 수밖에 없다.

- `0(상태를 알 수 없음)`
- `1(AI가 가진 타일)`
- `2 이상(상대방이 가진 타일)`

즉 위와 같이 상대방이 가진 타일의 경우 2 '이상'으로 두는 것으로 하고

해당 원소의 값을 2 + (패 인덱스)로 두는 방법이 가장 나은 것 같다.

과연 이걸로 될지 의심스럽지만 뭐 애초에 재미로 하는 거니까...

예를 들어서 상대방이 다음과 같이 0, 1, 2, 3 타일을 가지고 있다고 하면

```
 ___   ___   ___   ___
| 0 | | 1 | | 2 | | 3 |
|___| |___| |___| |___| 
```

`[0] = 2 + 0 = 2`

`[1] = 2 + 1 = 3`

`[2] = 2 + 2 = 4`

`[3] = 2 + 3 = 5`

`상대방의 타일 = 번호 + 상대 패 인덱스`라는 식이므로 위와 같이 된다. 

또 앞서 출력 역시 현재 게임판 상태로 뒀는데, 이렇게 하면 그걸로 뭘 알아낼 수가 없다.

어떤 처리를 하는 것(상대방의 어떤 타일을 어떤 값으로 찍는 것)이 좋을지의 확률을 알아내는 거니까...

즉 상대방 패 수를 N이라고 하면 상대방의 패 1~N에 대해 0~25번 타일일 각각의 확률을 구해야 한다.

근데 아까도 언급했듯이 사용자의 패 수 자체가 유동적인 개념이다.

어? 어쩌지? 하면서 막 생각했는데 그냥 26으로 두는 게 가장 나을 것 같다.

MAX 26의 각각의 타일 자리마다 들어갈 수 있는 26개의 타일에 대한 각각의 확률을 구해야 하므로

`26*26=676`, 세상에... 출력은 사이즈 676짜리 1차원 배열이 되어야 한다.

일단 그렇게 해 두고, 가장 확률이 높은 타일 자리/타일이 unavailable하다면 내림차순으로 하나씩 탐색하면서 결과가 존재하는(적어도 '찍을 수'는 있는) 값을 선택하면 되는 것이다.

그런데 그렇게 하면 은닉층의 뉴런 수가 좀 안 맞는 것 같아서 걍 4층짜리 신경망을 들고 왔다. ^^7

### 아마 결론

![](images/pic_2.png)

즉 이렇게 형상을 설계하는 것이 가능할 것이다.

~~그럼 구현하러 가 볼까?~~ 

```Python
PS C:\Users\JunhoYeo\Documents\GitHub\monorial> python .\net.py
w1 shape : (26, 50)
L b1 shape : (50,)
w2 shape : (50, 200)
L b2 shape : (200,)
w3 shape : (200, 800)
L b3 shape : (800,)
w4 shape : (800, 676)
L b4 shape : (676,)
```

학습 및 추론 테스트는 나중에 하고 다음 부분부터 진행해 보자.

## 신경망의 각 층
```Python
self.layers['Affine1'] = Affine(self.params['w1'], self.params['b1'])
self.layers['Relu1'] = Relu()
```
0층과 1층 사이의 가중치, 활성화 함수로 Relu() 사용
```Python
self.layers['Affine2'] = Affine(self.params['w2'], self.params['b2'])
self.layers['Relu2'] = Relu()
```
1층과 2층 사이의 가중치, 활성화 함수로 Relu() 사용
```Python
self.layers['Affine3'] = Affine(self.params['w3'], self.params['b3'])
self.layers['Relu3'] = Relu()
```
3층과 4층 사이의 가중치, 활성화 함수로 Relu() 사용
```Python
self.layers['Affine4'] = Affine(self.params['w4'], self.params['b4'])
self.lastLayer = SoftmaxWithLoss()
```
4층과 출력층 사이의 가중치, 활성화 함수로 소프트맥스 함수 사용

# 모노리얼 vs 모노리얼
다빈치코드 플레이 데이터가 없으니까 모노리얼 vs 모노리얼 대전을 통해 데이터를 얻으며 학습해야 함

기획 및 메모는 Trello를 사용해서 해버림

## Reference
- https://namu.wiki/w/%EA%B8%B0%EA%B3%84%ED%95%99%EC%8A%B5
- http://sanghyukchun.github.io/76
- https://github.com/WegraLee/deep-learning-from-scratch
