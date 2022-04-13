import unittest
from hanami import find_msg_flags


class HanamiTest(unittest.TestCase):

    def test_should_identify_karma_and_post_appeal_flags(self):
        karma_post_appeal = ["https://www.reddit.com/r/Superstonk/comments/u2b3ei/wtf_tda_spinoff_need/"
            """ https://www.reddit.com/r/Superstonk/comments/u2b3ei/wtf_tda_spinoff_need/

            Please validate this email or debunk it
            """,
            """  Hi Mods - I wrote a song for the community. It's mid-90's punk rock. My goal is to hit 1000 plays so I can continue to write more songs about the community. I'm calling it the $hitpost Ep. My first single is GME Apes. Have a listen.

            https://open.spotify.com/track/7LQluIvkiANRt4pWkRTllV?si=15b51d5fb2ce44b8

            Let me know what you think.

            m@ $CEO/Founder Corp Rock™️
            """,
            """   Greetings,  I  meant to award No_Pie_2019 for his ummmm yea post but inadvertently awarded the automod.  Lmayo

            Thank you
            """]
        for message in karma_post_appeal:
            with self.subTest():
                flags = find_msg_flags(message)
                self.assertEqual(flags, {'karma', 'post_appeal'})


if __name__ == '__main__':
    unittest.main()
