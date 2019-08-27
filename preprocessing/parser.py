import json
import pprint
'''
json파일에서 감정 관련 데이터 추출 -> path|label이 담긴 metadata.txt로 저장 
'''

def parser(file_path):
	with open(file_path) as f:
		raw_data = json.load(f)
	
	info = {}
	info['clip_id'] = raw_data['clip_id']
	info['nr_frame'] = raw_data['nr_frame']
	info['situation'] = raw_data['situation']
	
	temp = set()
	
	data = raw_data['data']
	
	for i in data:
		info[i] = {}
		for j in data[i].keys(): # j can be '1' or '2'
			if 'sound' in data[i][j]:
				info[i]['sound'] = data[i][j]['sound']
			if 'emotion' in data[i][j]:
				info[i]['sound'] = data[i][j]['emotion']
			if 'text' in data[i][j]:
				if 'person_id' in data[i][j]:
                                	info[i]['person_id'] = data[i][j]['person_id']
				#print(data[i][j]['text'])
				info[i]['script'] = data[i][j]['text']['script']
				info[i]['morpheme'] = data[i][j]['text']['morpheme']
	#pprint.pprint(info)
	return info

#parser('clip_226.json')
