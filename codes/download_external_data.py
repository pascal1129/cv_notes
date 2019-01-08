# ref:	https://www.kaggle.com/c/human-protein-atlas-image-classification/discussion/69984#437386
# ref:  https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000
# update: add continue transferring from breakpoint

# 进程：一个任务就是一个进程(process)，比如一个浏览器进程，一个记事本进程
# 线程：任务内部的多个'子任务'称之为线程(Thread)

import os
import errno
from multiprocessing.pool import Pool
from tqdm import tqdm
import requests
import pandas as pd
from PIL import Image

def download(pid, image_list, base_url, save_dir, image_size=(512, 512)):
    colors = ['red', 'green', 'blue', 'yellow']
    for i in tqdm(image_list, postfix=pid):
        img_id = i.split('_', 1)
        for color in colors:
            img_path = img_id[0] + '/' + img_id[1] + '_' + color + '.jpg'
            img_name = i + '_' + color + '.png'
            img_url = base_url + img_path
            save_path = os.path.join(save_dir, img_name)
            # breakpoint resume
            if not os.path.exists(save_path):
                # Get the raw response from the url
                r = requests.get(img_url, allow_redirects=True, stream=True)
                r.raw.decode_content = True

                # Use PIL to resize the image and to convert it to L
                # (8-bit pixels, black and white)
                im = Image.open(r.raw)
                im = im.resize(image_size, Image.LANCZOS).convert('L')
                im.save(save_path, 'PNG')

if __name__ == '__main__':
    # Parameters
    process_num = 24
    image_size = (512, 512)
    url = 'http://v18.proteinatlas.org/images/'
    csv_path =  "../input/HPAv18RBGY_wodpl.csv"
    save_dir = "./external_data"

    # Create the directory to save the images in case it doesn't exist
    try:
        os.makedirs(save_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    print('Parent process %s.' % os.getpid())
    img_list = pd.read_csv(csv_path)['Id']
    list_len = len(img_list)
    
    p = Pool(process_num)
    for i in range(process_num):
        start = int(i * list_len / process_num)
        end = int((i + 1) * list_len / process_num)
        process_images = img_list[start:end]
        p.apply_async(
            download, args=(str(i), process_images, url, save_dir, image_size)
        )
    print('Waiting for all subprocesses done...')
    p.close()		# 调用close()之后不能继续添加新的Prpcess
    p.join()		# p.join()之前必须等待所有的子进程执行完毕
    print('All subprocesses done.')