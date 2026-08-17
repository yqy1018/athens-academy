from pathlib import Path
import unittest


HTML = (Path(__file__).parents[1] / "index.html").read_text(encoding="utf-8")


class LessonPageArrowsTest(unittest.TestCase):
    def screen_block(self, screen_id, next_screen_id):
        return HTML.split(f"id: '{screen_id}'", 1)[1].split(
            f"id: '{next_screen_id}'", 1
        )[0]

    def test_every_lesson_state_has_the_same_symmetric_page_arrows(self):
        screen_pairs = (
            ('lesson-01', 'lesson-02'),
            ('lesson-02', 'lesson-03'),
            ('lesson-03', 'lesson-04'),
            ('lesson-04', 'question-before'),
            ('question-before', 'question-after'),
            ('question-after', 'summary'),
        )

        for screen_id, next_screen_id in screen_pairs:
            with self.subTest(screen=screen_id):
                screen = self.screen_block(screen_id, next_screen_id)
                self.assertIn("label: '返回上一页', kind: 'page-arrow', direction: 'left'", screen)
                self.assertIn("x: 1.4, y: 45, w: 4.8, h: 10", screen)
                self.assertIn("kind: 'page-arrow', direction: 'right'", screen)
                self.assertIn("x: 93.8, y: 45, w: 4.8, h: 10", screen)
                self.assertEqual(screen.count("kind: 'page-arrow'"), 2)

        self.assertEqual(HTML.count("kind: 'page-arrow'"), 12)

    def test_page_arrows_navigate_between_logical_pages(self):
        expected_targets = {
            'lesson-02': ('lesson-01', 'lesson-03', 'lesson-03'),
            'lesson-03': ('lesson-02', 'lesson-04', 'lesson-04'),
            'lesson-04': ('lesson-03', 'question-before', 'question-before'),
            'question-before': ('lesson-04', 'summary', 'question-after'),
            'question-after': ('lesson-04', 'summary', 'summary'),
        }

        for screen_id, (previous_target, next_target, next_screen_id) in expected_targets.items():
            with self.subTest(screen=screen_id):
                screen = self.screen_block(screen_id, next_screen_id)
                self.assertIn(f"action: 'go-to', target: '{previous_target}'", screen)
                self.assertIn(f"action: 'go-to', target: '{next_target}'", screen)

        lesson_one = self.screen_block('lesson-01', 'lesson-02')
        self.assertIn("action: 'previous', label: '返回上一页'", lesson_one)
        self.assertIn("action: 'next', label: '进入下一页'", lesson_one)

    def test_existing_teaching_actions_are_preserved(self):
        expected_actions = {
            ('lesson-01', 'lesson-02'): ("敲响传令钟",),
            ('lesson-02', 'lesson-03'): ("点亮 It",),
            ('lesson-03', 'lesson-04'): ("开始匹配",),
            ('lesson-04', 'question-before'): ("启动 Transformer",),
            ('question-before', 'question-after'): ("选择 A", "选择 B", "选择 C"),
            ('question-after', 'summary'): ("完成本卷",),
        }

        for (screen_id, next_screen_id), labels in expected_actions.items():
            with self.subTest(screen=screen_id):
                screen = self.screen_block(screen_id, next_screen_id)
                for label in labels:
                    self.assertIn(f"action: 'next', label: '{label}'", screen)

        self.assertIn("target.dataset.action === 'home'", HTML)

    def test_page_arrow_visual_and_direct_transition_exist(self):
        self.assertIn(".page-turn-symbol", HTML)
        self.assertIn("function goToScreen(screenId)", HTML)
        self.assertIn("target.dataset.action === 'go-to'", HTML)
        self.assertIn("target.dataset.target", HTML)


if __name__ == "__main__":
    unittest.main()
