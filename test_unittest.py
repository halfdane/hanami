import unittest
from hanami import Hanami


class HanamiUnitTest(unittest.TestCase):

    def test_should_identify_multiple_flags(self):
        testee = Hanami([{
            "category": "karma",
            "keywords": ["first word for karma", "secondKarmaWord"],
            "response": "",
        }, {
            "category": "post_appeal",
            "keywords": ["appealing", "something else to appeal"],
            "response": "",
        }])

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
                flags = testee.find_msg_flags(message)
                self.assertEqual(flags, {'karma', 'post_appeal'})

    def test_should_fall_back_to_human_if_nothing_fits(self):
        testee = Hanami([{
            "category": "karma",
            "keywords": ["first word for karma", "secondKarmaWord"],
            "response": "",
        }, {
            "category": "post_appeal",
            "keywords": ["appealing", "somthing else to appeal"],
            "response": "",
        }])

        input_strings = [
            "first word for something",
            "secondKarmaLetter",
            "sim",
            "secondKarmaAppeal",
        ]
        for message in input_strings:
            with self.subTest():
                flags = testee.find_msg_flags(message)
                self.assertEqual(flags, {"human"})


if __name__ == '__main__':
    unittest.main()
