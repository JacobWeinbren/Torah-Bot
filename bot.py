import os
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse
from atproto import Client, models
from main import main as generate_images


def check_mentions(client, last_checked):
    # Fetch mentions since last check
    mentions = client.app.bsky.notification.list_notifications({"limit": 50})

    new_mentions = [
        notif
        for notif in mentions.notifications
        if notif.reason == "mention" and isoparse(notif.indexed_at) > last_checked
    ]

    return new_mentions


def has_replied(client, mention):
    # Check if we've already replied to this mention
    replies = client.app.bsky.feed.get_post_thread({"uri": mention.uri}).thread.replies
    if replies:
        for reply in replies:
            if reply.post.author.did == client.me.did:
                return True
    return False


def post_reply(client, mention, images, alt_texts, reference):
    # Post a reply with images
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

    client.app.bsky.feed.post.create(
        repo=client.me.did,
        record={
            "text": f"Here are the generated images for {reference}:",
            "reply": {
                "parent": {"uri": mention.uri, "cid": mention.cid},
                "root": {"uri": mention.uri, "cid": mention.cid},
            },
            "embed": embed,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        },
    )


def main():
    client = Client()
    client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_PASSWORD"])

    # Set last_checked to 15 minutes ago in UTC
    last_checked = datetime.now(timezone.utc) - timedelta(minutes=15)

    new_mentions = check_mentions(client, last_checked)

    for mention in new_mentions:
        if not has_replied(client, mention):
            images, alt_texts, reference = generate_images(mention.record.text)
            post_reply(client, mention, images, alt_texts, reference)


if __name__ == "__main__":
    main()
