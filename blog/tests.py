from django.test import TestCase
from django.urls import reverse
from .models import BlogPost, Comment

class BlogPostTestCase(TestCase):
    def test_blog_post_creation(self):
        post = BlogPost.objects.create(title="Test Post", content="This is a test post.")
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is a test post.")


    def test_blog_post_edit(self):
        post = BlogPost.objects.create(title="Original Title", content="Original content.")
        post.title = "Updated Title"
        post.content = "Updated content."
        post.save()
        self.assertEqual(post.title, "Updated Title")
        self.assertEqual(post.content, "Updated content.")

    
    def test_blog_post_deletion(self):
        post = BlogPost.objects.create(title="Test Post", content="Test content.")
        post_id = post.id
        post.delete()
        self.assertFalse(BlogPost.objects.filter(id=post_id).exists())

class CommentTestCase(TestCase):
    def test_comment_addition(self):
        post = BlogPost.objects.create(title="Test Post", content="Test content.")
        comment = Comment.objects.create(post=post, author="Test Author", text="Test comment.")
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.text, "Test comment")   

    def test_comment_edit(self):
        post = BlogPost.objects.create(title="Test Post", content="Test content.")
        comment = Comment.objects.create(post=post, author="Test Author", text="Original comment.")
        comment.text = "Updated comment."
        comment.save()
        self.assertEqual(comment.text, "Updated comment.")


    def test_comment_deletion(self):
        post = BlogPost.objects.create(title="Test Post", content="Test content.")
        comment = Comment.objects.create(post=post, author="Test Author", text="Test comment.")
        comment_id = comment.id
        comment.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())


class BlogPostViewTestCase(TestCase):
    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_view(self):
        post = BlogPost.objects.create(title="Test Post", content="Test content.")
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, "Test content")


    def test_post_detail_view(self):
        post = BlogPost.objects.create(title="Test Post", content="Test content.")
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, "Test content")

    def test_redirect_after_post_creation(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Redirect Test',
            'content': 'Test content for redirection.'
        })
        self.assertEqual(response.status_code, 302)  # HTTP 302 for redirection
        self.assertTrue(BlogPost.objects.filter(title="Redirect Test").exists())