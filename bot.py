import os
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse
from atproto import Client, models
from main import main as generate_images


def check_mentions(client, last_checked):
    mentions = client.app.bsky.notification.list_notifications({"limit": 50})
    return [
        notif
        for notif in mentions.notifications
        if notif.reason == "mention" and isoparse(notif.indexed_at) > last_checked
    ]


def has_replied(client, mention):
    replies = client.app.bsky.feed.get_post_thread(
        {"uri": mention.uri, "depth": 1}
    ).thread.replies
    return any(reply.post.author.did == client.me.did for reply in replies)


def post_reply(client, mention, images, alt_texts, reference):
    total_alt_text_length = sum(len(alt_text) for alt_text in alt_texts)

    if total_alt_text_length > 4000:
        client.app.bsky.feed.post.create(
            repo=client.me.did,
            record={
                "text": f"I'm sorry, but the request for {reference} is too long. Please try a shorter passage.",
                "reply": {
                    "parent": {"uri": mention.uri, "cid": mention.cid},
                    "root": {"uri": mention.uri, "cid": mention.cid},
                },
                "createdAt": datetime.now(timezone.utc).isoformat(),
            },
        )
        return

    embed = models.AppBskyEmbedImages.Main(
        images=[
            models.AppBskyEmbedImages.Image(
                alt=alt_text,
                image=client.com.atproto.repo.upload_blob(
                    open(image_path, "rb").read()
                ).blob,
            )
            for image_path, alt_text in zip(images, alt_texts)
        ]
    )

    image_count = len(images)
    client.app.bsky.feed.post.create(
        repo=client.me.did,
        record={
            "text": f"Here {'is' if image_count == 1 else 'are'} the generated image{'s' if image_count > 1 else ''} for {reference}:",
            "reply": {
                "parent": {"uri": mention.uri, "cid": mention.cid},
                "root": {"uri": mention.uri, "cid": mention.cid},
            },
            "embed": embed,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        },
    )


def check_my_tweets(client, last_checked):
    my_tweets = client.app.bsky.feed.get_author_feed(
        {"actor": client.me.did, "limit": 50}
    )

    return [
        tweet
        for tweet in my_tweets.feed
        if isoparse(tweet.post.record.created_at) > last_checked
    ]


def is_blacklisted(client, mention, my_tweets):
    for tweet in my_tweets:
        if tweet.post.uri == mention.uri or (
            tweet.post.record.reply
            and tweet.post.record.reply.parent.uri == mention.uri
        ):
            return True
    return False


def main():
    client = Client()
    client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_PASSWORD"])

    last_checked = datetime.now(timezone.utc) - timedelta(minutes=30)
    new_mentions = check_mentions(client, last_checked)
    my_tweets = check_my_tweets(client, last_checked)

    for mention in new_mentions:
        if not has_replied(client, mention) and not is_blacklisted(
            client, mention, my_tweets
        ):
            try:
                images, alt_texts, result = generate_images(mention.record.text)
                if images and alt_texts:
                    post_reply(client, mention, images, alt_texts, result)
                else:
                    client.app.bsky.feed.post.create(
                        repo=client.me.did,
                        record={
                            "text": f"I'm sorry, but there was an issue processing your request: {result}",
                            "reply": {
                                "parent": {"uri": mention.uri, "cid": mention.cid},
                                "root": {"uri": mention.uri, "cid": mention.cid},
                            },
                            "createdAt": datetime.now(timezone.utc).isoformat(),
                        },
                    )
            except Exception as e:
                print(f"Error processing mention: {mention.record.text}")
                print(f"Error details: {str(e)}")
                client.app.bsky.feed.post.create(
                    repo=client.me.did,
                    record={
                        "text": "I'm sorry, but an unexpected error occurred while processing your request. Please try again later.",
                        "reply": {
                            "parent": {"uri": mention.uri, "cid": mention.cid},
                            "root": {"uri": mention.uri, "cid": mention.cid},
                        },
                        "createdAt": datetime.now(timezone.utc).isoformat(),
                    },
                )


if __name__ == "__main__":
    main()
