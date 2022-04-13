import unittest
from hanami import find_msg_flags, generate_reply


class HanamiTest(unittest.TestCase):

    def test_should_identify_karma_and_post_appeal_flags(self):
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
            with self.subTest():
                flags = find_msg_flags(message)
                self.assertEqual(flags, {'karma', 'post_appeal'})

    def test_should_identify_concatenate_correct_message(self):
        expected = """
Thanks for reaching out to the mod team of r/Superstonk!


**This message has been auto-generated by the HANAMI modmail automation framework,
written in-house by the r/Superstonk mod team.
As the project is still in its prototype stages, we may encounter some bugs -
if this happens or you need a human response, please let us know by adding the text
<hanami:human> or to your reply.**



        

        **KARMA**
        

        Thanks for reaching out to the mod team of r/Superstonk!
        

        We've detected that you're likely asking about not having enough fake internet points (karma) to post on r/Superstonk.
        

        Whilst it might seem unfair to base the ability to post with fake points, they can and do have real meaning to people on Reddit and especially our community - for good reason!
        

        We see a lot of posts and comments from paid 'shills', bad actors and trolls. The karma restrictions we have in force help keep our community safe by preventing bad actors, with new accounts, from messing with our sub.
        

        Believe us, we understand it can be frustrating to have a comment or post you want to make being blocked by these rules, but we ask for your patience as it helps to preserve the awesome content our community produces.
        

        It is important to remember that Awarder Karma doesn't count towards your total Karma.  For a fast track to approval type !apeprove! in any of the comments for a Satori approval.
        

        If you are looking for approval specifically to be able to post DRS postings or “feed the bot” you are able to post freely to https://www.reddit.com/r/gmeorphans without any karma restrictions.
        

        If that doesn't help, please find below some helpful resources:
        

        What is Reddit Karma? -
        

        https://www.reddithelp.com/hc/en-us/articles/204511829-What-is-karma-
        

        How to get Karma on Reddit - https://zapier.com/blog/how-to-get-karma-on-reddit/
        
        Mods will almost always pin a comment or submit a private message to the OP with the Removal Reason. Please make sure you check for such communication before you send the mods any messages.
        
        It is our goal to create a safe, inclusive, and healthy environment for all. We come across a lot of posts that break the rules of Superstonk – they could promote FUD (Fear, uncertainty or doubt), are spam, contain demonstrably false information, or are otherwise inappropriate for the sub.
        
        Also, most posts have a Quality Vote upvote/downvote system that enables us to get a readout of posts that the average community member feels does not belong. In these cases, we reserve the right to manually remove from view anything that would undermine the integrity of this sub or otherwise doesn’t belong. Often, posts are removed as part of a judgment call based on quality vote feedback, community reports. We get it that it sucks if this has happened to you.
        
        Mods cannot delete posts or comments; we can only remove them, which essentially "hides" them from the subreddit. Sending us a URL to the post or comment helps a lot in solving your problem if you have a specific question.
        
        If you haven’t already, please send us a link to the specific post or comment that was removed with your specific rebuttal, and we will take action towards restoring the post, if it is in the best interest of the community to do so.
        


A note from us: In regards to Modmail, please know we get a lot of messages, and may elect not to reply to questions that are answered on the wiki and links we have provided.


In the meantime, please check out the following for answers to common questions we receive:


https://www.reddit.com/r/Superstonk/wiki/index/rules - Superstonk Rules


https://www.reddit.com/r/Superstonk/wiki/index/faq - Superstonk FAQ


https://www.reddit.com/r/Superstonk/wiki/index - Superstonk Wiki
"""
        actual = generate_reply(['karma', 'post_appeal'])
        self.maxDiff = None
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()
