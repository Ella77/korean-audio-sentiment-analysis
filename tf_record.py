import tensorflow as tf
import numpy as np
import glob
import os

 # get item 가져올때마다, dataloader
 #
def get_mfcc(filepath):
   return np.load(filepath)
def get_label(filepath):
 label = os.path.basename(filepath) #get file's directory named by its emotion
 return label


def _bytes_features(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _int64_features(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def write_tfrecords(tfrecord_path, sounds, labels, fs=16000):
    with tf.python_io.TFRecordWriter(tfrecord_path) as writer:
        for sound, label in zip(sounds, labels):
      

            example = tf.train.Example(features=tf.train.Features(
                feature={
                    'signal_raw': _bytes_features(sound),
                    'sr': _int64_features(fs),
                    'label': _int64_features(label)
                }))
            writer.write(example.SerializeToString())


def create_tfrecords(wav_path, tfrecord_pathes,
                    , fs=16000,
                     ):
    # tfrecord_pathes = pathes for train, val tfrecords
    train_sounds, train_labels = [], []
    val_sounds, val_labels = [], []

    for wav in glob.glob(dataset):       #walk through dir
   
        
        feature = get_mfcc(wav) 
        label =get_label(wav)
        #random seed and split into train and val data
        train_sounds.append(feature)
        train_labels.append(label)
        val_sounds.append(feature)
        val_labels.append(label)


        print(len(train_sounds), len(train_labels))
        print(len(val_sounds), len(val_labels))

        print('Writing tfrecords...')
        train_tfrecord_path, val_tfrecord_path = tfrecord_pathes

        write_tfrecords(train_tfrecord_path, train_sounds, train_labels, fs=fs)
        write_tfrecords(val_tfrecord_path, val_sounds, val_labels, fs=fs)    
 
# pytorch vesion class BaseDataset(Dataset):
#     def __init__(self, wav_paths, script_paths, bos_id=1307, eos_id=1308):
#         self.wav_paths = wav_paths
#         self.labels
#         self.bos_id, self.eos_id = bos_id, eos_id

#     def __len__(self):
#         return len(self.wav_paths)

#     def count(self):
#         return len(self.wav_paths)

#     def getitem(self, idx):
#         #trim process 가져오기 (datautils에서)
#         feat = get_mfcc(self.wav_paths[idx])
#         label = get_label(self.script_paths[idx])
#         return feat, label

       
if __name__ == "__main__":
    SR = 16000

    data_path = './datasets/'

    wav_path = data_path + '.wav'
    tfrecord_pathes = ['{}wav{}_train.tfrecord'.format(data_path, SR // 1000),
                       '{}wav{}_val.tfrecord'.format(data_path, SRR // 1000)]

    create_tfrecords(wav_path, tfrecord_pathes, fs=SR)       
