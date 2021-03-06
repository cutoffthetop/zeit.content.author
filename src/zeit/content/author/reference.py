import copy
import grokcore.component as grok
import lxml.objectify
import zeit.cms.content.interfaces
import zeit.content.author.interfaces
import zope.security.proxy


@grok.adapter(zeit.content.author.interfaces.IAuthor, name='author')
@grok.implementer(zeit.cms.content.interfaces.IXMLReference)
def XMLReference(context):
    node = lxml.objectify.E.author(href=context.uniqueId)
    updater = zeit.cms.content.interfaces.IXMLReferenceUpdater(context)
    updater.update(node)
    return node


class XMLReferenceUpdater(zeit.cms.content.xmlsupport.XMLReferenceUpdater):

    target_iface = zeit.content.author.interfaces.IAuthor

    def update_with_context(self, node, context):
        node.display_name = context.display_name


class AuthorshipXMLReferenceUpdater(
        zeit.cms.content.xmlsupport.XMLReferenceUpdater):

    target_iface = zeit.cms.content.interfaces.ICommonMetadata

    def update_with_context(self, node, context):
        for author in node.findall('author'):
            node.remove(author)
        for reference in context.authorships:
            node.append(copy.copy(zope.security.proxy.getObject(
                reference.xml)))
        # BBB The ``author`` attribute is deprecated in favor of the <author>
        # tags, but XSLT and mobile still use it.
        try:
            legacy_author = unicode(';'.join(
                [x.target.display_name for x in context.authorships]))
            node.attrib.pop('author', None)
            if context.authorships:
                node.set('author', legacy_author)
        except:
            # We've sometimes seen data errors with Friedbert where authors
            # don't have a type (and thus no ``display_name``), see VIV-629.
            if not self.suppress_errors:
                raise


class Reference(zeit.cms.content.reference.Reference):

    grok.implements(zeit.content.author.interfaces.IAuthorReference)
    grok.provides(zeit.content.author.interfaces.IAuthorReference)
    grok.name('author')

    location = zeit.cms.content.property.ObjectPathProperty('.location')


@grok.adapter(zeit.content.author.interfaces.IAuthor, name='authorbio')
@grok.implementer(zeit.cms.content.interfaces.IXMLReference)
def XMLBioReference(context):
    node = lxml.objectify.E.author(href=context.uniqueId)
    updater = zeit.cms.content.interfaces.IXMLReferenceUpdater(context)
    updater.update(node)
    return node


class BioReference(zeit.cms.content.reference.Reference):

    grok.implements(zeit.content.author.interfaces.IAuthorBioReference)
    grok.provides(zeit.content.author.interfaces.IAuthorBioReference)
    grok.name('authorbio')

    biography = zeit.cms.content.property.ObjectPathProperty('.biography')
