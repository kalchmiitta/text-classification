import requests
import time
import click




def getjson(url, data=None):
    response = requests.get(url, params=data)
    print(response.url)
    response = response.json()
    return response


def get_all_posts(access_token, owner_id, count=100, offset=0):
    cnt_zaprosov=0;
    while True:
        time.sleep(0.4)
        all_posts = []
        wall = getjson('https://api.vk.com/method/wall.get', {
            'owner_id': owner_id,
            'count': count,
            'access_token': access_token,
            'offset': offset,
            'v': '5.84'
        })

        cnt_zaprosov+=1
        print(cnt_zaprosov)

        count_posts = count
        posts = wall['response']['items']

        all_posts.extend(posts)
        print(len(all_posts))

        if (len(all_posts) >= count_posts):
            break
        else:
            offset += 100
    return all_posts, count_posts


def make_posts(all_posts):
    filtered_data = []
    for post in all_posts:
        if len(post['text']) != 0:
            filtered_data.append(post['text'])
    return filtered_data


def make_file(finish_posts, file):
    f = open('C:\Contest/' + file + '.txt', 'a', encoding='utf-8')
    for post in finish_posts:
        f.write('{%' + '\n')
        f.write(post + '\n')
        f.write('%}' + '\n')
    f.close()


@click.command()
@click.option('--file_info', prompt=True)
@click.option('--result_file', prompt=True)
@click.option('--tokens_file', prompt=True)
def my_main(file_info, result_file,tokens_file):
    f = open(file_info, 'r', encoding='utf-8')
    f_tokens=open(file_info, 'r', encoding='utf-8')
    tokens=[]
    for line in f_tokens:
        tokens.append(line[6:-1])
    for lines in f:  # в каждой строчке содержится id cnt
        inf = lines.split(' ', maxsplit=1)
        owner_id, count = inf[0], int(inf[1])
        access_token = '3de87ee63de87ee63de87ee62a3d802a1133de83de87ee661a7502113d5979aacadbad4' # ИСПРАВЬ ПОТОМ!!!!
        all_posts, count_posts = get_all_posts(access_token, owner_id, count)
        finish_posts = make_posts(all_posts)
        make_file(finish_posts, result_file)
    f.close()


if __name__ == '__main__':
    my_main()
 
