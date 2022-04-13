# HANAMI Modmail Automation Framework v2.0.3 by u/catto_del_fatto et al.
import logging
import os
import praw

_logger = logging.getLogger("hanami")

SUBREDDIT = "r/Superstonk"  # Here's hoping we don't have to change this

# Message stuff, to be decoupled when the glitches affecting this are fixed)
# Using separate flag and keyword lists so it's easier to rework identification when we add TF-IDF

# Added before appends
BASE_REPLY = """
Thanks for reaching out to the mod team of r/Superstonk!
\n
**This message has been auto-generated by the HANAMI modmail automation framework,
written in-house by the r/Superstonk mod team.
As the project is still in its prototype stages, we may encounter some bugs -
if this happens or you need a human response, please let us know by adding the text
<hanami:human> or to your reply.**
\n
"""

DATABASE = [
    {
        "category": "drs",
        "keywords": ["register", "drs"],
        "response": "",
    },
    {
        "category": "ban_appeal",
        "keywords": ["banned", "why", "fuck", "ban", "restore", "banning", "was ban", "appeal", "reinstate",
                     "why was I"],
        "response":         """
        **BAN APPEAL**
        \n
        We've detected that your message is about being banned from participating in the sub, so we've prepared an initial response you may find helpful that addresses many common questions we see below.
        \n
        Our subreddit prides itself on being a safe and civil space for all our members and each rule we put in place and enforce is there for good reason.
        \n
        If you have received a ban (permanent or temporary) please note you can still view and subscribe to r/Superstonk, but you won't be able to post or comment, for how long depends on the ban, but we won't restrict your ability to see the sub's content.
        \n
        The mod team carefully monitors posts and comments to ensure enforcement of the rules, therefore it's not personal, it's just our job.
        \n
        With that said, we do maintain a zero-tolerance policy against harassment, threats, hateful language, or discrimination. If your ban is because of this, it's best to let you know now, it's very unlikely to be overturned.
        \n
        In the words of our community, ape no fight ape.
        \n
        If you still feel the ban wasn't warranted, please read the below before submitting an appeal.
        \n
        If your account is confirmed to be permanently or temporarily banned for a violation of the sub's rules, the ban will not be overturned unless the mod team determines that the rule was inaccurately or unfairly applied.
        \n
        """,
    },
    {
        "category": "post_appeal",
        "keywords": ["delete", "mod", "post", "restore", "reinstate", "comment", "I don't understand why",
                     "my post was removed"],
        "response":         """
        Mods will almost always pin a comment or submit a private message to the OP with the Removal Reason. Please make sure you check for such communication before you send the mods any messages.
        
        It is our goal to create a safe, inclusive, and healthy environment for all. We come across a lot of posts that break the rules of Superstonk – they could promote FUD (Fear, uncertainty or doubt), are spam, contain demonstrably false information, or are otherwise inappropriate for the sub.
        
        Also, most posts have a Quality Vote upvote/downvote system that enables us to get a readout of posts that the average community member feels does not belong. In these cases, we reserve the right to manually remove from view anything that would undermine the integrity of this sub or otherwise doesn’t belong. Often, posts are removed as part of a judgment call based on quality vote feedback, community reports. We get it that it sucks if this has happened to you.
        
        Mods cannot delete posts or comments; we can only remove them, which essentially "hides" them from the subreddit. Sending us a URL to the post or comment helps a lot in solving your problem if you have a specific question.
        
        If you haven’t already, please send us a link to the specific post or comment that was removed with your specific rebuttal, and we will take action towards restoring the post, if it is in the best interest of the community to do so.
        """,
    },
    {
        "category": "report_user",
        "keywords": ["reporting", "shill", "FUD", "review", "should be looked", "user", "found a shill"],
        "response":         """
        **REPORT USER**
        \n
        We've detected that you might be reaching out to the mod team to report a user, post, or comment that appears out of place. Maybe you’ve identified a user with a shilly post history, somebody spamming something unrelated to GME in comments, or generally violating the “ape don’t fight ape” rule.
        \n
        We want this community to be fun and healthy for everyone. Follow the rules and report posts or comments before you message the moderators.
        \n
        In the case of r/Superstonk, it’s true that we see a lot of posts and comments from paid shills and trolls. Reports are the best way to quickly communicate posts or posters that need to be hidden from view. Moderators are actively working around the clock to address reported posts and comments in the order that they are reported.
        \n
        We appreciate the watchful eye of the entire community in helping flag posts that break these rules.
        \n
        A note from us: In regards to Modmail, please know we get a lot of messages, and may elect not to reply to questions that are answered on the wiki and links we have provided.
        \n
        In the meantime, please check out the following for answers to common questions we receive:
        \n
        https://www.reddit.com/r/Superstonk/wiki/index/rules - Superstonk Rules
        \n
        https://www.reddit.com/r/Superstonk/wiki/index/faq - Superstonk FAQ
        \n
        https://www.reddit.com/r/Superstonk/wiki/index - Superstonk Wiki
        \n
        """,
        # human review?
    },
    {
        "category": "satori",
        "keywords": ["satori", "thanks", "approval", "apeprove", "!apeprove!"],
        "response":         """
        \n
        **SATORI**
        \n
        Thanks for reaching out to the moderator team team of r/Superstonk!
        \n
        We've detected that you're likely asking about being approved by another of our friendly bots, Satori.
        \n
        Satori and our team are are constantly working in the background to review users and approve apes as quickly as possible!
        \n
        Despite this, there's a good chance that your account, until Satori can check it over, is still restricted from posting based on our sub's karma restrictions.
        \n
        A little bit about Satori. It is a bot which utilizes advanced technical stuff to differentiate between solid apes in the community, and nefarious actors hoping to undermine the sub.
        \n
        Satori is our communities' response to the shills, trolls, and bots that have been harassing ours, and all the finance subreddits since January.
        \n
        It is a system that can be utilized by bots and mods alike to detect good and bad actors. With this technology, we can utilize sub features in new ways to create a reliable user filter for the sub. Put simply? Ban the bad, approve the good.
        \n
        As we speak, Satori is currently approving users with solid post and comment history and works around the clock.
        \n
        Please therefore do not message us about being approved, as Reddit has limits and Satori can only work as hard as those limits allow.
        \n
        We are currently working as fast as we can. In time, we hope to employ methods that speed this process along, but until then we ask for your continued patience.
        \n
        Please read the Satori announcement post for more info. Please do not spam Modmail about karma or age filters.
        \n
        As a reminder, the easiest way to get a fast track to approval is to type !apeprove! in the comments anywhere on the sub.
        """,

    },
    {
        "category": "karma",
        "keywords": ["lurker", "superstonk", "engage", "post", "posted", "exception", "asking for an exception",
                     "karma", "feed the", "DRS Bot", "not enough", "approval", "to post"],
        "response":         """
        \n
        **KARMA**
        \n
        Thanks for reaching out to the mod team of r/Superstonk!
        \n
        We've detected that you're likely asking about not having enough fake internet points (karma) to post on r/Superstonk.
        \n
        Whilst it might seem unfair to base the ability to post with fake points, they can and do have real meaning to people on Reddit and especially our community - for good reason!
        \n
        We see a lot of posts and comments from paid 'shills', bad actors and trolls. The karma restrictions we have in force help keep our community safe by preventing bad actors, with new accounts, from messing with our sub.
        \n
        Believe us, we understand it can be frustrating to have a comment or post you want to make being blocked by these rules, but we ask for your patience as it helps to preserve the awesome content our community produces.
        \n
        It is important to remember that Awarder Karma doesn't count towards your total Karma.  For a fast track to approval type !apeprove! in any of the comments for a Satori approval.
        \n
        If you are looking for approval specifically to be able to post DRS postings or “feed the bot” you are able to post freely to https://www.reddit.com/r/gmeorphans without any karma restrictions.
        \n
        If that doesn't help, please find below some helpful resources:
        \n
        What is Reddit Karma? -
        \n
        https://www.reddithelp.com/hc/en-us/articles/204511829-What-is-karma-
        \n
        How to get Karma on Reddit - https://zapier.com/blog/how-to-get-karma-on-reddit/
        """,

    },
    {
        "category": "human",
        "keywords": ["<hanami:human>"],
        "response":         """
        
        **HUMAN REVIEW**
        \n
        Review registration received.
        \n
        Your message will be reviewed by a human moderator - note that waiting times may vary significantly.
        """,

    },
    {
        "category": "test",
        "keywords": ["<hanami:test>"],
        "response":         """
        **TEST REPLY**
        \n
        haha bot go brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
        \n
        hanami wörks, now pls moon or i eat you kthxbai
        """
    }
]

# To be added after appends
POSTSCRIPT = """
\n
A note from us: In regards to Modmail, please know we get a lot of messages, and may elect not to reply to questions that are answered on the wiki and links we have provided.
\n
In the meantime, please check out the following for answers to common questions we receive:
\n
https://www.reddit.com/r/Superstonk/wiki/index/rules - Superstonk Rules
\n
https://www.reddit.com/r/Superstonk/wiki/index/faq - Superstonk FAQ
\n
https://www.reddit.com/r/Superstonk/wiki/index - Superstonk Wiki
"""


class Hanami:
    def __init__(self, database, reddit=None):
        self.database = database
        self.reddit = reddit

    def authenticate(self):
        return praw.Reddit(username=os.environ["reddit_username"],
                           password=os.environ["reddit_password"],
                           client_id=os.environ["reddit_client_id"],
                           client_secret=os.environ["reddit_client_secret"],
                           user_agent="desktop:superstonk.hanami:v2.0.1 (by r/superstonk mods)")

    def find_msg_flags(self, msg_text):
        msg_text = msg_text.lower()
        msg_flags = set()  # DO NOT use a list, lest we have a re-run of the duplicate bug
        for entry in self.database:
            for kw in entry['keywords']:
                if kw.lower() in msg_text:
                    msg_flags.add(entry['category'])

        # If no appropriate categories are found, use human review
        if len(msg_flags) == 0:
            msg_flags.add("human")
        return msg_flags

    def generate_reply(self, msg_flags):
        reply = BASE_REPLY

        if len(msg_flags) > 0:
            for flag in msg_flags:
                for entry in self.database:
                    if flag == entry['category']:
                        reply += str(entry['response'])
            reply += POSTSCRIPT
        return reply

    def print_modmail(self):
        subreddit = self.reddit.subreddit(SUBREDDIT)
        convos = subreddit.modmail.conversations(state="new")

        for c in convos:
            for msg in c.messages:
                msg_text = msg.body_markdown  # ApeSpeak NLP parser from SATORI to be added once adjustments are made
                msg_flags = self.find_msg_flags(msg_text)
                reply = self.generate_reply(msg_flags)

                _logger.debug(f"""user: {msg.author}  
                message: {msg.body_markdown}
                --- 
                flags: {msg_flags}
                --- """)

                # print(reply)
                # c.reply(reply, author_hidden=True)
                #
                # if "human" in msg_flags:
                #     print("Human review, not archiving")
                # else:
                #     print("Archiving")
                #     c.archive()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    print("Authenticating...")
    reddit = praw.Reddit(username=os.environ["reddit_username"],
                           password=os.environ["reddit_password"],
                           client_id=os.environ["reddit_client_id"],
                           client_secret=os.environ["reddit_client_secret"],
                           user_agent="desktop:superstonk.hanami:v2.0.1 (by r/superstonk mods)")

    print("Authentication successful.")
    print(f'Current user is {reddit.user.me()}')

    Hanami(DATABASE, reddit).print_modmail()
