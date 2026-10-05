import unittest

from thread_splitter import render_thread, split_thread


class TestSplit(unittest.TestCase):
    def test_short_text_single_post(self):
        posts = split_thread("这是一段很短的话。", max_len=300)
        self.assertEqual(len(posts), 1)
        self.assertIn("(1/1)", posts[0])

    def test_numbering(self):
        text = "第一段讲背景。\n\n第二段讲做法。\n\n第三段讲结果。"
        posts = split_thread(text, max_len=40)
        self.assertGreaterEqual(len(posts), 2)
        for i, p in enumerate(posts, 1):
            self.assertIn(f"({i}/{len(posts)})", p)

    def test_hook_present_on_first_post(self):
        text = "第一段讲背景。\n\n第二段讲做法。"
        posts = split_thread(text, max_len=40, hook="全文分 {total} 条 👇")
        self.assertIn("👇", posts[0])

    def test_no_hook(self):
        text = "第一段。第二段。"
        posts = split_thread(text, max_len=40, hook="")
        self.assertNotIn("帖子串", posts[0])

    def test_oversized_paragraph_hard_split(self):
        long_para = "。".join(f"句子{i}" for i in range(50)) + "。"
        posts = split_thread(long_para, max_len=60)
        self.assertGreater(len(posts), 1)
        for p in posts:
            body = p.rsplit(" (", 1)[0]
            self.assertLessEqual(len(body), 60 + 20)

    def test_empty_text(self):
        self.assertEqual(split_thread("   "), [])

    def test_render(self):
        posts = split_thread("一二三。", max_len=300)
        rendered = render_thread(posts)
        self.assertIn("👇", rendered)


if __name__ == "__main__":
    unittest.main()
