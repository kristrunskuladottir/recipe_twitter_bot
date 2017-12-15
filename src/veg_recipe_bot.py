
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, tweepy, unirest, json, random, time

def main():

    # Get twitter authentication keys
    try:
        from secrets import secret_key, consumer_key, access_token, secret_token, recipe_id, recipe_key
    except ImportError as e:
        import logging
        logging.error(e)
        sys.exit(1)

    try:
        recipe = get_recipe(recipe_id, recipe_key)
    except NotImplementedError as e:
        import logging
        logging.error(e)
        sys.exit(1)

    try:
        api = twitter_login(consumer_key, secret_key, access_token, secret_token)
        api.update_status(recipe["name"] + ' ' + recipe["url"])
    except tweepy.TweepError as e:
        import logging
        logging.error(e)

        sys.exit(1)

# authenticate with twitter so we're able to tweet
def twitter_login(consumer_key, secret_key, access_token, secret_token):
    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    auth.set_access_token(access_token, secret_token)

    return tweepy.API(auth)

def get_recipe(recipe_id, recipe_key):
    response = unirest.get("https://api.edamam.com/search?q=&app_id=" + recipe_id + "&app_key=" + recipe_key + "&health=vegetarian")
    bod = json.dumps(response.body)
    bod = json.loads(bod)

    recipe_url = bod[unicode("hits")][0][unicode("recipe")][unicode("url")]
    recipe_label = bod[unicode("hits")][0][unicode("recipe")][unicode("label")]
    return {"url":recipe_url, "name":recipe_label}

if __name__ == '__main__':
    while True:
        main()
