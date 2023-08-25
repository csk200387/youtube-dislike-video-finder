import os
import json
from module.auth import get_authenticated_service
from googleapiclient.errors import HttpError




def get_video_list():
    if os.path.exists('response.json'):
        os.remove('response.json')
    
    try:
        service = get_authenticated_service('youtube', 'v3')

        request = service.videos().list(
            part='snippet,contentDetails,statistics',
            myRating='dislike',
            maxResults=50,
            pageToken=None
        )

        response = request.execute()
        
        print(response)
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=4, ensure_ascii=False)

    except HttpError as err:
        print(err)


def write_report_page():
    response = None
    with open('response.json', 'r', encoding='utf-8') as f:
        response = json.load(f)
    

    with open('report.html', 'w', encoding='utf-8') as f:
        items = response['items']
        for i in range(len(items)):
            video_id = items[i]['id']
            video_title = items[i]['snippet']['title']
            video_thumbnail = items[i]['snippet']['thumbnails']['medium']['url']
            video_link = f'https://youtu.be/{video_id}'

            f.write(f'''
            <div class="video">
                <a href="{video_link}" target="_blank">
                    <img src="{video_thumbnail}" alt="{video_title}">
                    <p>{video_title}</p>
                </a>
            </div>
            ''')

def main():

    get_video_list()
    write_report_page()


if __name__ == '__main__':
    main()