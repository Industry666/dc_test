import argparse
import os
from multiprocessing.pool import ThreadPool

import pandas as pd
import requests

parser = argparse.ArgumentParser(description='Enter directory name.')
parser.add_argument('name_of_directory', type=str, help='Directory path.')
dir_name = parser.parse_args()

_req = requests.post('https://back.missmarple.ai/api/data-for-ai?shop_name=mvideo.ru').json()


def make_brand_file():
    request_data = _req
    brand_list = [request_data['data'][brand]['brand'] for brand in range(len(request_data['data']))]
    lower_case_brands = {str(brand).lower() for brand in brand_list}

    products_data = pd.DataFrame({'brands': list(lower_case_brands)})

    print('Saving file "brands.xlsx"...')

    products_data.to_excel(os.path.join(dir_name.name_of_directory, 'brands.xlsx'))


def make_product_file():
    request_data = _req
    name_list = [request_data['data'][product_name]['name'] for product_name in range(len(request_data['data']))]
    article_list = [request_data['data'][product_article]['article']
                    for product_article in range(len(request_data['data']))]

    images_list_dict = make_product_list_dict()

    reformed_dict = dict()

    for key, value in images_list_dict.items():
        for edit_list in value:
            if str(edit_list).endswith(('.jpg', '.png', '.jpeg')) is True:
                reformed_dict.setdefault(key, list()).append(edit_list)

    products_data = pd.DataFrame({'id': reformed_dict.keys(),
                                  'name': name_list,
                                  'article': article_list,
                                  'images': reformed_dict.values()
                                  })

    print('Saving file "products.xlsx"...')

    products_data.to_excel(os.path.join(dir_name.name_of_directory, 'products.xlsx'))


def make_product_list_dict():
    request_data = _req
    product_list = [request_data['data'][product_number] for product_number in range(len(request_data['data']))]

    images_list = list()

    for product in product_list:
        image_counter_id = 1
        for images in product['images']:
            images_list.append([product['id'], str(product['id']) + '_' + str(image_counter_id) + str(
                images['file_path'][-4:])])
            image_counter_id += 1

    images_list_dict = dict()

    for key, value in images_list:
        images_list_dict.setdefault(key, list()).append(value)

    return images_list_dict


def save_product_images():
    request_data = _req
    product_list = [request_data['data'][product_number] for product_number in range(len(request_data['data']))]

    images_list_links = list()
    for product in product_list:
        for images in product['images']:
            images_list_links.append(images['file_path'])

    list_of_name = make_product_list_dict()

    full_list_of_names = list()

    for list_of_names in list_of_name.values():
        for names in list_of_names:
            full_list_of_names.append(names)

    result_list = list()

    for links, name in zip(images_list_links, full_list_of_names):
        if str(links).endswith(('.jpg', '.png', '.jpeg')) and str(name).endswith(('.jpg', '.png', '.jpeg')) is True:
            result_list.append({'url': links, 'file_name': name})

    def download_img(img_data):
        img_content = requests.get(img_data['url']).content

        try:
            os.mkdir('images')
            print('Saving files in "images" directory:')
        except FileExistsError:
            pass

        with open(os.path.join('images', img_data['file_name']), 'wb') as handler:
            handler.write(img_content)

        return img_data['file_name']

    def run_downloader(images_url: list):
        results = ThreadPool().imap_unordered(download_img, images_url)
        for img in results:
            print(f'Now saving {img} file')

    run_downloader(result_list)

    print('Files "brands.xlsx" and "products.xlsx" are created.\n'
          'All images were saved in "images" directory.')


def main(directory_name):
    if not os.path.isdir(directory_name.name_of_directory):
        os.mkdir(directory_name.name_of_directory)
        make_brand_file()
        make_product_file()
        os.chdir(directory_name.name_of_directory)
        save_product_images()
    else:
        print("Directory already exist.")


if __name__ == '__main__':
    main(dir_name)
