import os
import unittest
from planner import load_platforms, load_posts, load_engagement, compile_performance_report_data

class TestPlanner(unittest.TestCase):
    def test_load_platforms(self):
        platforms = load_platforms()
        self.assertTrue(len(platforms) > 0)
        self.assertEqual(platforms[0]["name"], "Instagram")
        
    def test_load_posts(self):
        posts = load_posts()
        self.assertTrue(len(posts) > 0)
        self.assertEqual(posts[0]["post_id"], "POST001")
        
    def test_load_engagement(self):
        eng = load_engagement()
        self.assertTrue(len(eng) > 0)
        
    def test_report(self):
        report = compile_performance_report_data()
        self.assertIsNotNone(report)
        self.assertIn("posts_per_platform", report)
        # Seed posts has: 2 on Instagram (POST001, POST004), 1 on TikTok (POST002), 1 on X (POST003)
        self.assertEqual(report["posts_per_platform"]["Instagram"], 2)
        self.assertEqual(report["posts_per_platform"]["TikTok"], 1)
        self.assertEqual(report["posts_per_platform"]["X"], 1)
        # Seed engagement has: 
        # POST002 (TikTok): 1200 likes + 85 comments + 45 shares + 15000 views = 16330 interaction points
        # POST003 (X): 150 likes + 12 comments + 8 shares + 850 views = 1020 interaction points
        # POST002 should be the best-performing post
        self.assertEqual(report["best_post"]["post_id"], "POST002")
        self.assertEqual(report["best_post"]["total_engagement"], 16330)

if __name__ == "__main__":
    unittest.main()
