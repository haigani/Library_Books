from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class BookAPITestCase(APITestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {'username': 'Hossein', 'password': 'rR@13606794'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book(self):
        self.client.post(reverse('register'), {'username': 'Hossein', 'password': 'rR@13606794'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'Hossein', 'password': 'rR@13606794'})
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(reverse('book-list-create'), {
            'title': 'Book1',
            'author': 'Author1',
            'publication_date': '2023-01-01',
            'isbn_number': '1234567890123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_books(self):
        # Register and log in the user
        self.client.post(reverse('register'), {'username': 'Hossein', 'password': 'rR@13606794'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'Hossein', 'password': 'rR@13606794'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create a book
        self.client.post(reverse('book-list-create'), {
            'title': 'Test Book',
            'author': 'Author Name',
            'publication_date': '2023-01-01',
            'isbn_number': '1234567890123'
        })

        # Fetch the books
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one book is returned
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_update_book(self):
        # Register and log in the user
        self.client.post(reverse('register'), {'username': 'Hossein', 'password': 'rR@13606794'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'Hossein', 'password': 'rR@13606794'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create a book
        response = self.client.post(reverse('book-list-create'), {
            'title': 'Old Book',
            'author': 'Old Author',
            'publication_date': '2023-01-01',
            'isbn_number': '1234567890123'
        })
        book_id = response.data['id']

        # Update the book
        response = self.client.put(reverse('book-detail', args=[book_id]), {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_date': '2024-01-01',
            'isbn_number': '1234567890124'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the book was updated
        updated_response = self.client.get(reverse('book-detail', args=[book_id]))
        self.assertEqual(updated_response.data['title'], 'Updated Book')

    def test_delete_book(self):
        # Register and log in the user
        self.client.post(reverse('register'), {'username': 'Hossein', 'password': 'rR@13606794'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'Hossein', 'password': 'rR@13606794'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create a book
        response = self.client.post(reverse('book-list-create'), {
            'title': 'Book to Delete',
            'author': 'Author',
            'publication_date': '2023-01-01',
            'isbn_number': '1234567890123'
        })
        book_id = response.data['id']

        # Delete the book
        response = self.client.delete(reverse('book-detail', args=[book_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the book was deleted
        response = self.client.get(reverse('book-detail', args=[book_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_books(self):
        # Register and log in the user
        self.client.post(reverse('register'), {'username': 'Hossein', 'password': 'rR@13606794'})
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'Hossein', 'password': 'rR@13606794'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create books
        self.client.post(reverse('book-list-create'), {
            'title': 'Django Basics',
            'author': 'Author One',
            'publication_date': '2022-01-01',
            'isbn_number': '1234567890123'
        })
        self.client.post(reverse('book-list-create'), {
            'title': 'Advanced Django',
            'author': 'Author Two',
            'publication_date': '2023-01-01',
            'isbn_number': '1234567890124'
        })

        # Search by title
        response = self.client.get(reverse('book-list-create') + '?title=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both books should match

        # Search by author
        response = self.client.get(reverse('book-list-create') + '?author=Author One')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book should match
