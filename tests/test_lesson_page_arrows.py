from pathlib import Path
import unittest


HTML = (Path(__file__).parents[1] / "index.html").read_text(encoding="utf-8")


class LessonPageArrowsTest(unittest.TestCase):
    def test_only_lesson_one_has_symmetric_page_arrows(self):
        lesson = HTML.split("id: 'lesson-01'", 1)[1].split("id: 'lesson-02'", 1)[0]

        self.assertIn("action: 'previous', label: '返回上一页'", lesson)
        self.assertIn("action: 'next', label: '进入下一页'", lesson)
        self.assertIn("x: 1.4, y: 45, w: 4.8, h: 10", lesson)
        self.assertIn("x: 93.8, y: 45, w: 4.8, h: 10", lesson)
        self.assertEqual(HTML.count("kind: 'page-arrow'"), 2)

    def test_bell_and_existing_actions_are_preserved(self):
        lesson = HTML.split("id: 'lesson-01'", 1)[1].split("id: 'lesson-02'", 1)[0]

        self.assertIn("action: 'next', label: '敲响传令钟'", lesson)
        self.assertIn("target.dataset.action === 'home'", HTML)

    def test_page_arrow_visual_and_previous_transition_exist(self):
        self.assertIn(".page-turn-symbol", HTML)
        self.assertIn("function retreat(state)", HTML)
        self.assertIn("target.dataset.action === 'previous'", HTML)


if __name__ == "__main__":
    unittest.main()
