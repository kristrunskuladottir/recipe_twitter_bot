
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, tweepy, unirest

def main():

    # Get twitter authentication keys
    try:
        from secrets import secret_key, consumer_key, access_token, secret_token, api_key
    except ImportError as e:
        import logging
        logging.error(e)
        sys.exit(1)

    try:
        recipe = get_recipe(api_key)
    except:
        import logging
        logging.error('there was an error while fetching a recipe')
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

def get_recipe(api_key):
    response = unirest.get(
        "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1&tags=vegetarian",
        headers={
            "X-Mashape-Key": api_key,
            "Accept": "application/json"
       })

    recipe = {}
    recipe["url"] = response.body["recipes"][0]["sourceUrl"]
    recipe["name"] = response.body["recipes"][0]["title"]

    return recipe

if __name__ == '__main__':
    main()

