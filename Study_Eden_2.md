올 것이 왔습니다. **MFCC** 타임입니다..~~슬쩍 읽어보고 포기하고 싶었어요. 사실 아직도 이해가 가지 않..~~

## Mel-frequency cepstral coefficients (MFCCs)

`MFCC`는 동 음성 인식, 화자 인식에서 많이 쓰이고 있는 feature 중 하나입니다. **입력된 신호에서 노이즈 등으로부터 실제 유효한 소리(언어 콘텐츠)의 특징을 추출하는 것입니다.**

MFCC는 6가지 단계로 나눌 수 있습니다.

1. 입력 신호를 작은 프레임으로 나눕니다.
2. 각 프레임에 대하여 Power Spectrum의 Periodogram estimate를 계산합니다. (각 프레임에 대해 FFT를 함)
3. 2번에서 구한 Power Spectrum에 Mel Filterbank를 적용하고, 각 필터에 에너지를 합합니다.
4. 3번에서 구한 모든 Filterbank 에너지의 Log를 취합니다.(1편에서 log-mel 기억나시나요? 그것과 같습니다.)
5. 4번 값에 DCT를 취합니다.
6. DCT를 취한 값에 Coefficients 2~13를 제외한 나머지는 버립니다.

6단계로 잘 나누어 놨지만, 천재가 나누어 놓았음이 틀림없습니다. ~~이 분야는 똑똑한 사람들만 할 수 있는 건가.. 그럼 저는 포기하겠..~~

1번 부터 차례로 한 번 보겠습니다.

#### 1. 입력 신호를 작은 프레임으로 나눕니다.

오디오 신호는 끊임없이 변합니다. 그래서 우리는 짧은 시간의 오디오 신호는 많이 변하지 않을 것이라고 가정할 것입니다. 이게 바로 우리가 입력 신호를 작은 프레임으로 나누는 이유입니다.

보통은 20-40ms 길이의 프레임으로 나눕니다. 이 길이보다 짧다면 신뢰도 높은 주파수 분석 결과를 얻을 수 없을 것이고, 이 길이보다 길다면 신호의 변화가 클 것이라고 생각하기 때문입니다.

#### 2. 각 프레임에 대하여 Power Spectrum의 Periodogram estimate를 계산합니다.

이제는 각 프레임의 파워 스펙트럼을 계산할 것입니다. 이 방법은 사람의 달팽이관이 주파수에 따라 다르게 진동하는 것을 보고 고안되었다고 합니다. ~~생물 싫어하는데 비전도 오디오도 뭘하든 생물이 나오네요.. 전 굳이 고르자면 지구과학 쪽을 좋아합니다.~~

달팽이관이 주파수에 따라 다르게 진동하는 모습은 Periodogram estimate를 이용해서 어떤 주파수가 있는지 알아내는 것과 유사하다고 합니다. 다시 정리하자면 `달팽이관 == Periodogram Estimate`정도가 될 것 같습니다.

1, 2 과정을 정리한다면, 오디오 신호가 짧은 시간동안엔 변하지 않을 것이라고 가정했기 때문에 20~40ms정도 사이즈로 오디오 신호를 자르고, 자른 하나하나를 프레임이라고 부릅니다.

사람의 달팽이관은 주파수에 따라 진동하는데, 이 것을 본따서 우리는 Periodogram Estimate을 이용해서 각 프레임의 파워 스펙트럼을 계산합니다.

#### 3. 2번에서 구한 Power Spectrum에 Mel Filter bank를 적용하고, 각 필터의 에너지를 합합니다.

하지만  Periodogram Spectral Estimation ~~아까는 Periodogram Estimation이라며.. 중간에 Spectral 왜 들어갔는데.. 꼭 이런식이야~~을 해도 여전히 Automatic Speech Recognition(ASR)에 필요하지 않은 정보들을 많이 가지고 있다고 합니다. 처음에 `MFCC`의 역할은 오디오 신호에서 필요한 Speech Feature만을 남기는 거라고 했으니 필요없는 정보들은 다 없애버려야겠죠. 여기서 또 생물 얘기가 나옵니다. ~~달팽이관.. 그만 보고싶다. 달팽이관이 트와이스 같았으면 이러진 않았을텐데~~ 달팽이관은 인접한 주파수의 차이를 잘 구별해내지 못하고, 고주파의 경우에 이런 실수가 더 많아진다고 합니다.

이 스케일을 통합하면 우리의 특징이 사람들이 듣는 것과 더 밀접하게 일치하게되기 때문에, periodogram 뭉치를 모아서 더합니다. 다양한 주파수의 영역에 얼마나 에너지가 있는지 아이디어를 얻기 위해서는 Mel Filter라는 것을 사용합니다.

달팽이관이 완벽한 알고리즘을 가지고 있었으면 편했을텐데, 그렇지 않기 때문에 Mel Scale을 해야하고, 그것을 위해서 Mel Filterbank를 적용합니다.

</br>

![figure1](http://dl.dropbox.com/s/sa7ys5pt4vv740d/mel_scale.png)

*figure1 : Mel Scale*

</br>

Mel Scale, Mel filterbank 뭐가 뭔지 너무 헷갈리는데, 정리를 한다면 Mel Scale을 하기위해서 Mel filterbank라는 filter를 거치게 하는 것 같습니다. ~~맞으려나..~~

#### 4. 3번에서 구한 모든 Filter bank 에너지의 Log를 취합니다.

log를 취하는 것은 사람이 실제로 듣는 것과 비슷하게 만들어주기 때문이라고 합니다. 일반적으로 감지된 소리의 볼륨을 2배로 얻기 위해 우리는 소리에 들어있는 에너지의 8배를 필요로 합니다. log를 이용한 이런 압축 기능은 우리의 feature를 사람이 실제 듣는것에 가깝게 매치시킵니다.
왜 세제곱근이 아닌 로그일까요? 로그는 cepstral mean subtraction이라는 채널 노멀라이제이션 기술을 쓸 수 있게 해주기 때문이라고 합니다. ~~이해하는데 한나절이라 토할 것 같아요..~~

#### 5. 4번 값에 DCT를 취합니다.
튜토리얼에선 DCT를 취한다고 써있지만, 저는 DCT가 뭔지도 몰라서 찾아보니 DCT는 *이산 코사인 변환(Discrete Cosine Transform)*, *Dreams Come True*, *듀얼 클러치 변속기(Dual Clutch Transmission)* 등의 뜻이 있네요. 눈치로 튜토리얼을 읽은지 몇 년째이므로 이산 코사인 변환이 바로 여기서 말하는 DCT일 것이라 생각됩니다.
이 DCT를 왜 해야하냐면, Filterbank는 겹치는 구간이 있어서 Filterbank 에너지들 사이에 상관관계가 존재하므로 이것을 분리해주어야하기 때문이라고 합니다.

#### 6. DCT를 취한 값에 Coefficients 2~13를 제외한 나머지는 버립니다.
하지만 여기서 26개 DCT Coefficient 중에서 12만 남겨야 합니다. DCT Coefficient가 많으면, Filterbank 에너지의 빠른 변화를 나타내게 되고, 이것이 음성인식의 성능을 낮추게 되기 때문이라고 합니다.

</br>

자.. 이게 바로 **MFCC** 입니다. 어떠셨나요?
전 아직도 정확하게 모르겠네요ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ반복에서 읽으면 읽을 수록 이해가 가긴하지만 에너지 소모가 너무 큽니다..
**MFCC** 에 대해 공부하면서 느낀 것은, **MFCC** 의 흐름은 의 귀를 따라하기 위해 노력했기 때문에 공부하면서 '아 왜 이걸 이렇게 했지?' 라는 생각이 들 때는 사람의 달팽이관의 어느 부분을 따라하려고 노력했는지 다시 생각해보면서 읽으면 버블티의 펄 사이즈 만큼 더 이해가 잘 되네요..
이걸 코드로 짜야한다니 거지같죠? 하지만 걱정마세요. 그럴 필요가 없습니다. 이미 유명한 audio data processing library가 존재하거든요.

</br>

* 참고자료

> [Mel Frequency Cepstral Coefficient (MFCC) tutorial](http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/)
>
> [Mel Frequency Cepstral Coefficient (MFCC) 란 무엇인가? - 음성 인식 알고리즘](http://blog.naver.com/PostView.nhn?blogId=mylogic&logNo=220988857132&redirect=Dlog&widgetTypeCall=true)
>
> [Mel filter in MFCC - is it necessary?](https://dsp.stackexchange.com/questions/19574/mel-filter-in-mfcc-is-it-necessary)
