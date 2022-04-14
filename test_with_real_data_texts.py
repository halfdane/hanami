import unittest

from hanami import Hanami


class HanamiTest(unittest.TestCase):

    def mock_wiki_response(self):
        return {
            'base': {
                'introduction': 'some introduction ',
                'postscript': ' a goodbye message'
            },
            'types': {
                'karma': {
                    'keywords': ['superstonk', 'post'],
                    'response': 'the karma response'
                },
                'post_appeal': {
                    'keywords': ['mod', 'comment'],
                    'response': 'the post_appeal response'
                },
            }}

    def test_should_identify_karma_and_post_appeal_flags(self):
        testee = Hanami()

        karma_post_appeal = [
                             """ https://www.reddit.com/r/Superstonk/comments/u2b3ei/wtf_tda_spinoff_need/
                 
                             Please validate this email or debunk it
                             """,

                             """Hi Mods - I wrote a song for the community. It's mid-90's punk rock. My goal is to 
                             hit 1000 plays so I can continue to write more songs about the community. I'm calling it 
                             the $hitpost Ep. My first single is GME Apes. Have a listen. 
                 
                             https://open.spotify.com/track/7LQluIvkiANRt4pWkRTllV?si=15b51d5fb2ce44b8
                 
                             Let me know what you think.
                 
                             m@ $CEO/Founder Corp Rock™️ """,

                             """Greetings,  I  meant to award No_Pie_2019 for his ummmm yea post but inadvertently 
                             awarded the automod.  Lmayo 
                 
                             Thank you""",

                             """I finally got around to updating my last lots of CS shares. It got removed after I 
                             tagged a mod I think? A bot asked me to provide more proof. I’m real smooth brained with 
                             this stuff and the only reason it took me so long to update the bot is because I work 
                             full time and have 4 kids, I don’t exactly have much time to post for the bot. Anyways, 
                             I was super excited because I’d moved my biggest position out of eToro, and I’ve had the 
                             hugest battle with eToro including getting the AFCA to help me battle them to either 
                             transfer or provide proof of share registration. Long story short I just am really 
                             excited to finally get out of eToro once and for all. And! Because of the dip I managed 
                             to score an extra 8 shares by the time CS landed my shares. Anyways. Please put my post 
                             back up."""]
        for message in karma_post_appeal:
            with self.subTest(msg=message):
                flags = testee.find_msg_flags(self.mock_wiki_response(), message)
                self.assertEqual(flags, {'karma', 'post_appeal'})

    def test_should_identify_concatenate_correct_message(self):
        testee = Hanami(database=self.mock_wiki_response())

        expected = "some introduction the karma response the post_appeal response a goodbye message"
        actual = testee.generate_reply(self.mock_wiki_response(), ['karma', 'post_appeal'])
        self.maxDiff = None
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()
