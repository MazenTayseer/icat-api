from unittest.mock import Mock, patch

import factory

from apps.dal.models import Module


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Module

    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=200)
    text = factory.Faker('text', max_nb_chars=300)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        with patch('apps.dal.models.module.ChromaClient') as mock_chroma_class:
            mock_chroma_instance = Mock()
            mock_chroma_class.return_value = mock_chroma_instance
            return super()._create(model_class, *args, **kwargs)
