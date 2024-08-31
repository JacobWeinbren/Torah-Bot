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
    # Get the direct replies to the mention
    replies = client.app.bsky.feed.get_post_thread(
        {"uri": mention.uri, "depth": 1}
    ).thread.replies

    # Check if any of the direct replies are from the bot
    return any(reply.post.author.did == client.me.did for reply in replies)


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

    image_count = len(images)
    image_text = "image" if image_count == 1 else "images"

    client.app.bsky.feed.post.create(
        repo=client.me.did,
        record={
            "text": f"Here {'is' if image_count == 1 else 'are'} the generated {image_text} for {reference}:",
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

    # Set last_checked to 30 minutes ago in UTC
    last_checked = datetime.now(timezone.utc) - timedelta(minutes=30)

    new_mentions = check_mentions(client, last_checked)

    for mention in new_mentions:
        if not has_replied(client, mention):
            images, alt_texts, reference = generate_images(mention.record.text)
            if images and alt_texts and reference:
                post_reply(client, mention, images, alt_texts, reference)
            else:
                print(f"Error processing mention: {mention.record.text}")


if __name__ == "__main__":
    main()
