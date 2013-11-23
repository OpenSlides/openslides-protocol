# -*- coding: utf-8 -*-

from django.test.client import Client

from openslides.agenda.models import Item
from openslides.utils.test import TestCase

from openslides_protocol.models import ItemProtocol


class TestMainMenu(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_main_menu_entry(self):
        response = self.client.get('/projector/dashboard/')
        self.assertContains(response, 'href="/openslides_protocol/"')


class ProtocolPage(TestCase):
    url = '/openslides_protocol/'

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'openslides_protocol/protocol_page.html')


class ItemProtocolView(TestCase):
    url = '/openslides_protocol/'

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_protocol_for_inexisting_item(self):
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, 404)
        response = self.client.post(self.url + '1/', {})
        self.assertEqual(response.status_code, 404)

    def test_get_new_protocol_for_item(self):
        item = Item.objects.create(title='test_title_cu0aix6Ahngach7oYeeb')
        self.assertEqual(item.pk, 1)
        self.assertFalse(ItemProtocol.objects.exists())
        response = self.client.get(self.url + '1/')
        self.assertContains(response, 'Protocol')
        self.assertTemplateUsed(response, 'openslides_protocol/itemprotocol_form.html')
        self.assertTrue(ItemProtocol.objects.exists())

    def test_get_existing_protocol_for_item(self):
        item = Item.objects.create(title='test_title_Mio3mahDiokieNgohtai')
        self.assertEqual(item.pk, 1)
        item_protocol = ItemProtocol.objects.create(item=item, protocol='test_text_naegh1Ai5Pi7yeezuroo')
        self.assertEqual(item_protocol.pk, 1)
        response = self.client.get(self.url + '1/')
        self.assertContains(response, 'test_text_naegh1Ai5Pi7yeezuroo')
        self.assertTemplateUsed(response, 'openslides_protocol/itemprotocol_form.html')

    def test_post_inexisting_protocol(self):
        item = Item.objects.create(title='test_title_boib2eef5oi9Ieg5caic')
        self.assertEqual(item.pk, 1)
        self.assertFalse(ItemProtocol.objects.exists())
        response = self.client.post(self.url + '1/', {'protocol': 'Nohhieraquai0tiephah'})
        self.assertTrue(ItemProtocol.objects.exists())
        self.assertRedirects(response, self.url + '1/')
        self.assertEqual(ItemProtocol.objects.get(item=item).protocol, 'Nohhieraquai0tiephah')
        message = '<strong>Protocol for test_title_boib2eef5oi9Ieg5caic</strong> was successfully modified.'
        self.assertTrue(message in response.cookies['messages'].value)

    def test_post_existing_protocol(self):
        item = Item.objects.create(title='test_title_boib2eef5oi9Ieg5caic')
        self.assertEqual(item.pk, 1)
        item_protocol = ItemProtocol.objects.create(item=item, protocol='test_text_Va3paighoopeilohqu8i')
        self.assertEqual(item_protocol.pk, 1)
        self.assertEqual(ItemProtocol.objects.get(item=item).protocol, 'test_text_Va3paighoopeilohqu8i')
        response = self.client.post(self.url + '1/', {'protocol': 'Ree1eidaPahLeeShu2qu'})
        self.assertTrue(ItemProtocol.objects.exists())
        self.assertRedirects(response, self.url + '1/')
        self.assertEqual(ItemProtocol.objects.get(item=item).protocol, 'Ree1eidaPahLeeShu2qu')
        message = '<strong>Protocol for test_title_boib2eef5oi9Ieg5caic</strong> was successfully modified.'
        self.assertTrue(message in response.cookies['messages'].value)
