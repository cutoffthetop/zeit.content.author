import pkg_resources
import zeit.cms.testing
import zeit.workflow.testing
import zope.testing.doctest

product_config = """
<product-config zeit.content.author>
  author-folder /foo/bar/authors
  biography-questions file://{fixtures}/tests/biography-questions.xml
</product-config>
""".format(fixtures=pkg_resources.resource_filename(__name__, '.'))

ZCML_LAYER = zeit.cms.testing.ZCMLLayer(
    'ftesting.zcml',
    product_config=zeit.cms.testing.cms_product_config +
    zeit.workflow.testing.product_config +
    product_config)


def FunctionalDocFileSuite(*args, **kw):
    kw.setdefault('layer', ZCML_LAYER)
    kw['package'] = zope.testing.doctest._normalize_module(kw.get('package'))
    return zeit.cms.testing.FunctionalDocFileSuite(*args, **kw)
