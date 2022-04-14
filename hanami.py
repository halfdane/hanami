import asyncio
import logging
import os
import re
from pprint import pprint

from asyncprawcore.exceptions import NotFound

import asyncpraw
import yaml

_logger = logging.getLogger("hanami")

DATABASE = [

    {
        "category": "human",
        "keywords": ["<hanami:human>"],
        "response": """
        
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
        "response": """
        **TEST REPLY**
        \n
        haha bot go brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
        \n
        hanami wörks, now pls moon or i eat you kthxbai
        """
    }
]


class Hanami:
    command_extract = re.compile(r"<hanami:([^>]*)>")
    hanami_configs = re.compile(r'hanami_config/(.+)')

    def __init__(self,
                 subreddit=None,
                 testsubreddit=None):
        self.subreddit = subreddit
        self.testsubreddit = testsubreddit
        self.moderators = []
        self.test_database = None
        self.database = None

    async def setup(self):
        if self.subreddit:
            self.moderators = [moderator for moderator in await self.subreddit.moderator()]
            self.database = await self.fetch_config_from_wiki(self.subreddit)

        if self.testsubreddit:
            self.test_database = await self.fetch_config_from_wiki(self.testsubreddit)

    async def synchronize_test_wiki_to_superstonk(self):
        base_config_wiki_page = await self.testsubreddit.wiki.get_page('hanami_config')
        await base_config_wiki_page.load()
        await self._edit_or_create_wiki(base_config_wiki_page)

        async for wikipage in self.testsubreddit.wiki:
            hanami_config = self.hanami_configs.match(wikipage.name)
            if hanami_config:
                await self._edit_or_create_wiki(wikipage)

    async def _edit_or_create_wiki(self, wikipage):
        _logger.info(f"synching {wikipage.name}")
        await wikipage.load()
        try:
            existing_page = await self.subreddit.wiki.get_page(wikipage.name)
            await existing_page.edit(content=wikipage.content_md, reason="Synchronizaton from test")
        except NotFound:
            new_page = await self.subreddit.wiki.create(wikipage.name, wikipage.content_md, "Initial creation")
            await new_page.mod.update(listed=True, permlevel=2)

    async def fetch_config_from_wiki(self, subreddit):
        """
        :return: {'base': {'introduction': 'some introduction', 'postscript': 'a goodbye message'},
         'types': {'request_type': {'keywords': ['list', 'of keywords that trigger the response'],
                                  'response': 'the response for this kind of request'}}}
        """
        database = dict()

        base_config_wiki_page = await subreddit.wiki.get_page('hanami_config')
        await base_config_wiki_page.load()
        base_config = yaml.safe_load(base_config_wiki_page.content_md)
        database['base'] = base_config

        database['types'] = dict()
        async for wikipage in subreddit.wiki:
            await wikipage.load()
            hanami_config = self.hanami_configs.match(wikipage.name)
            if hanami_config:
                _logger.info(f"Reading {subreddit} {wikipage.name}")
                wiki_config = yaml.safe_load(wikipage.content_md)
                database['types'][hanami_config.group(1)] = wiki_config
            else:
                _logger.info(f"Ignoring {subreddit} {wikipage.name}")

        _logger.info(f"Finished reading hanami config for {subreddit}")
        return database

    def find_msg_flags(self, database, msg_text):
        msg_text = msg_text.lower()
        unique_msg_flags = \
            set([k for k, v in database['types'].items() for kw in v['keywords']
                 if kw.lower() in msg_text])

        # If no appropriate categories are found, use human review
        if len(unique_msg_flags) == 0:
            unique_msg_flags.add("human")
        return unique_msg_flags

    def generate_reply(self, database, msg_flags):
        reply = database['base']['introduction']

        category_texts = [v['response'] for flag in msg_flags for k, v in database['types'].items()
                          if flag == k]
        reply += " ".join(category_texts)

        reply += database['base']['postscript']
        return reply

    async def print_modmail(self):
        _logger.info(f"reading regular modmail")
        async for c in self.subreddit.mod.stream.modmail_conversations(state="new"):
            await c.load()
            for msg in c.messages:

                msg_text = msg.body_markdown  # ApeSpeak NLP parser from SATORI to be added once adjustments are made
                # if (command := self.command_extract.match(msg_text)) and (msg.author in self.moderators):
                #     _logger.info(f"identified command: {command.group(1)}")
                #     func = getattr(self, command.group(1))
                #     try:
                #         reply = func()
                #         c.reply(str(reply), author_hidden=True)
                #         # c.archive()
                #     except Exception as e:
                #         _logger.exception("oops, something went wrong during the command execution")
                # else:
                msg_flags = self.find_msg_flags(self.test_database, msg_text)
                reply = self.generate_reply(self.test_database, msg_flags)
                _logger.info(f"""user: {msg.author}
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


async def main():
    logging.basicConfig(level=logging.INFO)

    print("Authenticating...")
    asyncreddit = asyncpraw.Reddit(username=os.environ["reddit_username"],
                                   password=os.environ["reddit_password"],
                                   client_id=os.environ["reddit_client_id"],
                                   client_secret=os.environ["reddit_client_secret"],
                                   user_agent="desktop:superstonk.hanami:v2.0.1 (by r/superstonk mods)")

    async with asyncreddit as reddit:
        print("Authentication successful.")
        print(f'Current user is {await reddit.user.me()}')

        hanami = Hanami(subreddit=await reddit.subreddit('Superstonk'),
                        testsubreddit=await reddit.subreddit('testsubsuperstonk'))
        await hanami.setup()
        await hanami.print_modmail()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
