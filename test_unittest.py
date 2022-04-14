import unittest
from hanami import Hanami


class HanamiUnitTest(unittest.TestCase):


    def mock_wiki_response(self):
        return {
            'base': {
                'introduction': 'some introduction ',
                'postscript': ' a goodbye message'
            },
            'types': {
                'karma': {
                    'keywords': ["first word for karma", "secondKarmaWord"],
                    'response': "",
                },
                'post_appeal': {
                    'keywords': ["appealing", "something else to appeal"],
                    'response': "",
                },
            }}

    def test_should_identify_multiple_flags(self):
        testee = Hanami()

        input_strings = [
            """ appealing
                             https://www.reddit.com/r/secondKarmaWord/comments/rbdce/ewfnei/
                             """,
            "https://www.reddit.com/r/secondKarmaWord/comments/rbdce/ewfnei/appealing",
            "first word for karma something else to appeal",
            "secondKarmaWordappealing",
        ]
        for message in input_strings:
            with self.subTest(msg=message):
                flags = testee.find_msg_flags(self.mock_wiki_response(), message)
                self.assertEqual(flags, {'karma', 'post_appeal'})

    def test_should_fall_back_to_human_if_nothing_fits(self):
        testee = Hanami()

        input_strings = [
            "first word for something",
            "secondKarmaLetter",
            "sim",
            "secondKarmaAppeal",
        ]
        for message in input_strings:
            with self.subTest():
                flags = testee.find_msg_flags(self.mock_wiki_response(), message)
                self.assertEqual(flags, {"human"})


if __name__ == '__main__':
    unittest.main()
