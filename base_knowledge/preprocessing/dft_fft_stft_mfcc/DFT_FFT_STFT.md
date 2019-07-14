* `Audio Recognition`이란?
* `Audio Recognition`이 쓰이는 곳
* `Audio Recognition`을 위한 전처리 기법

위 세가지를 이야기 해보겠습니다. *이 글을 쓰는 저 역시 공부하는 입장이므로 틀린 부분은 지적해주세요.*

전처리 기법은 구글이 Github에 push한 [**Web based audio recognition(Google)**](https://github.com/google/web-audio-recognition)에서 이야기하는 전처리 기법들을 중심으로 이야기할 것입니다. ~~웹 버전의 PoseNet도 그렇고 구글은 예쁜 짓을 잘하네요.~~ 해당 문서외에 참고 자료들은 [**이곳**](#참고자료)을 참고해주세요.

## `Audio Recognition`이란?

Google에 'What is Audio?'라고 검색하면 여러개의 사이트에서 Audio의 정의하길 Audio란  Hertz로 측정되며, 인간의 귀가 들을 수 있는 범위 내에 있는 어떤 소리나 소음을 나타내는데 사용하는 것이라고 합니다. 쉽게 말하면 인간이 들을 수 있는 소리를 recognize하는 것이라고 할 수 있겠네요.

## `Audio Recognition`이 쓰이는 곳

가장 먼저 생각 나는 것은 제가 좋아했던 Shazam이라는 서비스입니다. 노래 이름을 찾아달라고 하고, 노래를 들려주면 노래 이름을 찾아주는 서비스인데 이 역시 audio recognition의 예입니다.
Amazon echo, GiGA Genie와 같은 스마트 스피커에도 audio recognition이 유저가 말하는 명령을 알아듣는데 쓰입니다. STT(Speech To Text)에도 audio recognition이 쓰입니다.

## `Audio Recognition`을 위한 전처리 기법

제가 참고하는 있는 블로그에서는 **어떤 남자가 'left'라고 말을 하는 데이터** 를 사용해서 **log-mel spectrogram** 까지의 전처리 기법의 순서를 보여줍니다.
하지만 그냥 그 데이터를 쓰면 재미없고, 저는 재미없는 건 싫어합니다. 그래서 ~~월드 베스트 아이돌~~ Twice의 Cheer Up이라는 노래 가사 중 사나🐹 의 파트인 `샤샤샤`를 데이터로 써보겠습니다. ~~모르시는 분이 없을 거라 믿어 의심치 않습니다.~~(MR제거가 아닌 음원에서 따온 데이터입니다.)

</br>

mp3 파일이었던 데이터를 파형 형태로 시간 도메인(time domain)으로 나타낸다면 아래 figure1과 같이 나옵니다.

![figure1](http://dl.dropbox.com/s/wo5e38f9d0mk8fp/time_domain.png)
*figure1 : 샤샤샤 time domain*

</br>

이제 우리는 시간 도메인(time domain)으로 나타냈던 `샤샤샤`를 주파수 도메인(frequency domain)으로 나타낼 것입니다.
이 과정을 위해서 우리는 푸리에 변환(Fourier Transform)이라는 방법을 사용합니다. 아래에서 잠시 Fourier Transform에 대해 이야기해보겠습니다.~~이제부터는 이해하기 위해 많은 에너지가 필요합니다. 하아..~~

*  Fourier Transform

`푸리에 변환`은 시간(time) **도메인의 신호를 주파수(frequency) 도메인으로 변환해주는 방법입니다.** 이게 무슨 뜻이냐면 임의의 입력 신호를 다양한 주파수를 갖는 주기함수들의 합으로 분해하여 표현해준다는 것입니다. 주파수 도메인의 신호는 저장을 위한 컴퓨팅 공간을 훨씬 적게 필요로 합니다.
아래의 figure3의 빨강색으로 나타낸 신호가 어떤 임의의 신호라고 할 때, 이 신호를 푸리에 변환해서 여러가지 파랑색 주기함수들로 나타낼 수 있습니다.

![figure2](http://dl.dropbox.com/s/2fakw82xv3jgnt6/fft.png)

*figure2 : 푸리에 변환, (출처: 위키피디아)*

</br>

 푸리에 변환에는 **DFT** , **FFT** , **STFT** 가 있습니다.

1. DFT(Discrete Fourier Transform)
: **DFT** 는 유한한 신호 시퀀스의 이산(Discrete) 신호의 푸리에 변환을 구하기 위한 방법입니다.
컴퓨터로 푸리에 변환을 할 때 생기는 문제점인 1) 신호의 길이가 유한하지 않다는 것 2) 컴퓨터는 Discrete 한 정보만을 계산할 수 있다는 문제점을 해결한 방법입니다.
**DFT** 는 신호를 유한하게 만들기 위해 신호를 N개로 자르고, 주파수를 sampling해서 연속한 주파수를 discrete하게 바꿔줍니다.

2. FFT(Fast Fourier Transform)
: 연산 처리가 빠를 것 같다는 것은 이름에서부터 느낄 수 있습니다. DFT의 연산시간이 길어져 고안된 방법입니다. 입력된 신호 중 필요한 신호만을 골라내서 빠른 시간안에 변환을 하는 것입니다.

3. STFT(Shor-Time Fourier Transform)
: 푸리에 변환은 해당 신호를 주파수 영역으로 봤을 때, 어떤 주파수의 성분을 얼만큼 가지고 있는지 가시적으로 잘 표현해줍니다. 하지만 시간의 흐름에 따라 주파수가 변했을 때, 어느 시간 때에 어떻게 변하는지 알 수 없다고 합니다. 이 단점을 보완한 푸리에 변환이 STFT입니다.

 ~~각 방법마다 수식이 있지만 전 수식은 꺼내고 싶지가 않네요..~~방금 배운 3가지의 방법 중 제일 먼저 **Fast Fourier Transform (FFT)** 를 해볼 것입니다.

</br>

![figure3](http://dl.dropbox.com/s/ng0na2pl4wfzdfs/frequency_domain.png?dl=0)

*figure3 : 샤샤샤 frequency domain*

</br>

짜잔! figure3을 보세요! 시간 도메인(time domain)이었던 figure1의 `샤샤샤`가 주파수 도메인(frequency domain)으로 바뀌었습니다. 매력적이진 않지만 도메인이 바뀌었다는건 한 눈에 확인할 수 있습니다.
이 데이터를 Neural Nets에 사용해도 상관은 없습니다. 하지만 조금 더 개선할 수 있습니다. ~~제가 한 말이 아니라 참고있는 블로그 주인이 그렇다고 하네요.~~ 사람은 높은 주파수보다 낮은 주파수에서 작은 피치(음 높낮이 변화)를 잘 알아차립니다.
**Mel scale** 은 순수한 톤의 피치를 실제 측정된 주파수와 연관시켜줍니다. 주파수에서 Mel로 변환하려면 우리는 **triangular filterbank** 를 생성해야 합니다.
</br>

![figure4](http://dl.dropbox.com/s/cqfzj077b6urh42/mel_filterbank.png)

*figure4 : 샤샤샤 Mel filterbank*

</br>

figure4에서 보이는 화려한 삼각형들은 소리의 주파수 표현에 적용할 수 있는 윈도우입니다. 앞에서 생성한 FFT 에너지에 각 윈도우를 적용하면 **Mel Spectrum** 을 얻을 수 있습니다. 우리의 경우엔 39개의 값을 얻었고 아래의 figure5에서 확인 할 수 있습니다.

</br>

![figure5](http://dl.dropbox.com/s/y6lb1048ctyi2wo/mel_coeff.png)

*figure5 : 샤샤샤 Mel Coefficients*

</br>

이것을 스펙트로그램(Spectrogram)으로 나타낸다면, 우리는 fiure6에서 보이는 것 처럼 우리가 목표로 했던 **log-mel spectrogram** 을 얻을 수 있습니다.
~~음 사나🐹 샤샤샤를 데이터로 쓰면 공부가 즐거울 줄 알았는데, 계속 알아보기 어려운 스펙트로그램만 보니까 안즐겁네요.~~

</br>

![figure6](http://dl.dropbox.com/s/zc750q9dqtb0iev/mel_energy.png)

*figure6 : 샤샤샤 Mel energy spectrogram*

</br>
이렇게 **log-mel spectrogram** 을 얻었는데, 아무것도 모르는 오린이(오디오+어린이)로서 "그래서 이걸 뭐.. 어쩌라고"

![어쩌라고](https://media.giphy.com/media/h8gegRhdFrKURb2v4q/giphy.gif)

싶었는데 지금까지 설명했던 이 과정이 많이 쓰이고 있는 전처리 기법 중 **MFCC** 의 과정 중 하나였습니다.
**MFCC** 가 무엇인지는 모르겠지만, 일단 figure7과 같이 샤샤샤의 MFCC Spectrogram은 얻었습니다.

</br>

![figure7](http://dl.dropbox.com/s/ikbnvqn0r7j4ptf/mfcc_spectrogram.png)

*figure7 : `샤샤샤` MFCC spectrogram*

</br>

이번 편에서는 전처리 기법에 **푸리에 변환(DFT, FFT, STFT)** 이 있었고, 이 과정은 **MFCC** 를 위한 순서였다는 것 정도만 알고 가보겠습니다.
그럼 다음 시간엔 MFCC가 무엇인지 알아보러 가보겠습니다. ~~살짝 읽어봤는데 진짜 이해가 안되네요. 공부 1회차만에 위기가 왔습니다.~~

</br>


## 참고자료
> [Ok Google: How to do Speech Recognition?](https://towardsdatascience.com/ok-google-how-to-do-speech-recognition-f77b5d7cbe0b)
>
> [Fourier Transform(푸리에 변환)의 이해와 활용](https://darkpgmr.tistory.com/171)
>
> [Getting Started with Audio Data Analysis using Deep Learning (with case study)](https://www.analyticsvidhya.com/blog/2017/08/audio-voice-processing-deep-learning/)
>
> [STFT (Shor-Time Fourier Transform) 의 기본](https://jbear.tistory.com/entry/STFT-Short-Time-Furier-Transform-%EC%9D%98-%EA%B8%B0%EB%B3%B8)
