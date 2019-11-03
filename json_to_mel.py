import json
import pprint
import pandas as pd
import io
import yaml
import pylab
import numpy as np
import os
import glob


def parser(file_path):
    with io.open(file_path, encoding='utf-8') as f:
        #io.open(f, encoding='utf-8-sig')
        #raw_data = yaml.safe_load(f)
        raw_data = json.load(f, encoding ='utf-8')
        #raw_data = json.load(f, object_hook=_decode_dict)
    return raw_data

def jsonread(raw_data):

    data = raw_data['data']

    sound_flag = False
    text_flag = False

    columns = ['clip_id', 'nr_frame', 'script', 'script_start', 'script_end', 'sound_emotion', 'sound_arousal', 'sound_valence']
    df = pd.DataFrame(columns=columns)
    info = {}


    for i in data:
        info[i] = {}
        info[i]['clip_id'] = raw_data['clip_id']
        info[i]['nr_frame'] = raw_data['nr_frame']
        info[i]['situation'] = raw_data['situation']

        for j in data[i].keys(): # j can be '1' or '2'
            if 'emotion' in data[i][j]:
                emotion = data[i][j]['emotion']
                #             print(emotion)
                if 'sound' in emotion:
                    info[i]['sound_arousal'] = emotion['sound']['arousal']
                    info[i]['sound_emotion'] = emotion['sound']['emotion']
                    info[i]['sound_valence'] = emotion['sound']['valence']
            #                 sound_flag = True
            if 'text' in data[i][j]:
                info[i]['script'] = data[i][j]['text']['script']
                info[i]['script_start'] = data[i][j]['text']['script_start']
                info[i]['script_end'] = data[i][j]['text']['script_end']

    for i in info.keys():
        #     print(info[i])
        try:
            info[i]['frame'] = i
        #         print(type(info[i]['frame']))
        except:
            print(type(i))
        df = df.append(info[i], ignore_index=True)

    df = df[df['sound_emotion'].notnull()]
    npy_save = np.array(df)
    return npy_save

def split_by_emo(data_path, json_name, clean_data):

    real_file_name = json_name[:-5]  #327.json -> 327 #NEEDS change based on datasets
    audio_path = real_file_name+ '.mp4'
    y, sr = librosa.load(audio_path)

    import pandas as pd
    frame_info_s =[]
    frame_info_e =[]
    bef_e = ''
    label = []
    check = 0
    # frame_info : all_real_fr_num (#총개수)
    # y : y.shape
    #print(len(y))
    #print(all_real_fr_num)
    all_real_fr_num = clean_data.shape[0]
    fract = len(y)/all_real_fr_num # 프레임수(이미지)에 대한 y 의 비율
    print(fract)
    for i in range(0, clean_data.shape[0]):
        now_e = clean_data[i][5]
        if(bef_e!=now_e): #앞과 다를때
            if(check==1):
                frame_info_e.append(round((float(clean_data[i][8])- float(start_fr_num) -1)*fract)) #번째 frame-> y 비율곱로 저장
                check = 0
            if(pd.notnull(now_e)): #nan 이 아니면서
                print(now_e)
                label.append(now_e)
                #print(i)
                frame_info_s.append(round((float(clean_data[i][8])- float(start_fr_num) -1)*fract)) #번째 frame-> y 비율곱로 저장
                bef_e = now_e
                check = 1
                #print((float(clean_data[i][8])- float(start_fr_num) -1))
    if(check==1):
        frame_info_e.append(len(y))
    print(frame_info_s) #변화되기 직전 순간이 저장됨
    print(len(frame_info_s))
    print(len(frame_info_e))
    #print(clean_data[180])
    #print(clean_data[181])


    k= 0
    new_arr = []
    all_arr = []
    for i in range(len(y)):
        if(i>=frame_info_s[k]):
            new_arr.append(y[i])
            if(i==frame_info_e[k]):
                all_arr.append(new_arr)
                print(len(new_arr))
                new_arr = []
                if(k<(len(frame_info_e)-1)):
                    k = k+1
    all_arr = np.asarray(all_arr)
    print(all_arr.shape)
    S = []
    image = []
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    for i in range(len(all_arr)):
        emo = label[i]
        S = librosa.feature.melspectrogram(np.asarray(all_arr[i]), sr=sr, n_mels=128)
        print(S.shape)


        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        log_S = librosa.power_to_db(S, ref=np.max)
        save_path = os.path.join(data_path,label[i],real_file_name+'_'+frame_info_s[i]+ '_' + frame_info_e[i] + '_'+'feature') #save to datasets/hap/clip226_334_235345_feature
        np.save(log_S,save_path)






if __name__ == "__main__":

    data_path = './datasets/'
    labels = ['hap', 'sur','fear','neu'] #NEEDS to add more label like
    # anger, 1=disgust&contempt, 2=afraid, 3=happiness, 4=sadness, 5=surprise, 6=neutral

    if os.path.exists(os.path.join(data_path,labels)) == False:
        os.makedirs(os.path.join(data_path,labels))



    json_pattern = os.path.join(data_path,'*.json' )
    for json_name in glob.glob(json_pattern):
        clean_data = jsonread(parser(json_name))
        split_by_emo(data_path,json_name, clean_data)



