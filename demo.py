#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import pickle
import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob
image_files = glob('./test_images/*.*')


if __name__ == '__main__':
    result_dir = './test_result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)

    for image_file in sorted(image_files):
        image = np.array(Image.open(image_file).convert('RGB'))
        t = time.time()
        tmp_res, result, image_framed = ocr.model(image)
        print(tmp_res)
        
        output_file = os.path.join(result_dir, image_file.split('/')[-1])
        Image.fromarray(image_framed).save(output_file)
        print(output_file)
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        print("\nRecognition Result:\n")
	#print("---type--", result)
	#print("---filenamne is ----", image_file.split('/')[-1])
	with open(output_file + ".pkl", "wb") as fp:
		pickle.dump(result, fp, protocol=pickle.HIGHEST_PROTOCOL)
        for key in result:
            print(str(result[key][1]))
        tmp_file = output_file + '.txt'
        with open(tmp_file, "w") as f:
            for line in tmp_res:
                if not any(line):
                    continue 
                else:
                    for i in range(len(line)-1):
                        f.write(str(line[i]))
                        f.write(' ')
                    f.write(str(line[-1]))
                    f.write('\n')
