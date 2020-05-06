import argparse
from tkinter import *
from InstagramAPI import InstagramAPI
from random import choice
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    def profile_page_recent_posts_time(self, profile):
        profile_url = 'https://www.instagram.com/{}/'.format(profile)
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                "edges"]
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
            time_difference = datetime.now() - datetime.fromtimestamp(int(results[0]['taken_at_timestamp']))
            #print('{:<25s} posted {:>12s} ago'.format(profile, str(time_difference)))

            if time_difference.days>150:
                #print('{:<25s}'.format(profile, str(time_difference)))
                return '@ {:<25s}\n'.format(profile, str(time_difference))
        except:
            return ""

        return ""

def pasif_bul(f):
    obj = InstagramScraper()

    # Reads file instead of copy and paste method below
    username_list = [line.rstrip() for line in open('usernames.txt')]

    for x in username_list:
        zaman = obj.profile_page_recent_posts_time(x)

        if zaman!="":
            f.write(zaman)


def GetAllFollowing(bot, user_id):
    following = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = bot.getUserFollowings(user_id, maxid=next_max_id)
        following.extend(bot.LastJson.get('users', []))
        next_max_id = bot.LastJson.get('next_max_id', '')
    following = set([_['pk'] for _ in following])
    return following


def GetAllFollowers(bot, user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = bot.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(bot.LastJson.get('users', []))
        next_max_id = bot.LastJson.get('next_max_id', '')
    followers = set([_['pk'] for _ in followers])
    return followers


if __name__ == '__main__':

    # parse cmd line args
    parser = argparse.ArgumentParser(description='Unfollow instagram users that don\'t follow you back!.')
    parser.add_argument('username', help='your instagram username')
    parser.add_argument('password', help='your instagram password')

    parser.add_argument('-n', '--num_unfollows', type=int, default=50,
                        help='Max number of users to unfollow in session')
    parser.add_argument('-d', '--max_delay', type=int, default=5,
                        help='Max seconds to wait between unfollow calls')

    args = parser.parse_args()

    # get credentials, authenticate
    ig = InstagramAPI(args.username, args.password)

    # success is just a bool
    success = ig.login()
    if not success:
        print('INSTAGRAM LOGIN FAILED!')
        sys.exit()

    # fetch your own primary key
    ig.getSelfUsernameInfo()
    self_id = ig.LastJson['user']['pk']

    # loop through json for followers/following
    followers = GetAllFollowers(ig, self_id)
    following = GetAllFollowing(ig, self_id)


    f = open("usernames.txt", "w+")
    for _ in ig.LastJson['users']:
        f.write(_['username']+'\n')

    f.close()

    print("Your following list has been saved to usernames.txt\n")

    f = open("analysis.txt", "w+")
    f.write('Following {} users\n'.format(len(following)))
    f.write('Followers {} users\n'.format(len(followers)))
    # they don't reciprocate
    unreciprocated = following - followers
    # i don't reciprocate
    free_followers = followers - following

    f.write('\nYou have {} followers that you dont follow back\n'.format(len(free_followers)))
    f.writelines('You have {} unfollowers\n'.format(len(unreciprocated)))

    f.write('\nUnfollower List\n')
    for _ in list(unreciprocated)[:min(len(unreciprocated), args.num_unfollows)]:
        ig.getUsernameInfo(str(_))
        #print('  @ {}'.format(ig.LastJson['user']['username']))
        f.write('  @ {}\n'.format(ig.LastJson['user']['username']))

    print("Your inactive users will be found within 5-10 mins...\n")

    f.write('\nInactive User List\n')
    pasif_bul(f)
    f.close()

    print("Your inactive following users has been saved to analysis.txt\n")

    f = open("analysis.txt", "r")

    if f.mode == 'r':
        contents = f.read()
        print(contents)
    f.close()

    p = Tk()
    p.geometry("300x700")
    p.title("Form")
    s1Lbl = Label(p, text=contents)
    s1Lbl.grid(row=1, column=0)
    p.mainloop()
