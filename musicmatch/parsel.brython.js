__BRYTHON__.use_VFS = true;
var scripts = {"$timestamp": 1621312501666, "parsel.csstranslator": [".py", "try :\n from functools import lru_cache\nexcept ImportError:\n from functools32 import lru_cache\n \nfrom cssselect import GenericTranslator as OriginalGenericTranslator\nfrom cssselect import HTMLTranslator as OriginalHTMLTranslator\nfrom cssselect.xpath import XPathExpr as OriginalXPathExpr\nfrom cssselect.xpath import _unicode_safe_getattr,ExpressionError\nfrom cssselect.parser import FunctionalPseudoElement\n\n\nclass XPathExpr(OriginalXPathExpr):\n\n textnode=False\n attribute=None\n \n @classmethod\n def from_xpath(cls,xpath,textnode=False ,attribute=None ):\n  x=cls(path=xpath.path,element=xpath.element,condition=xpath.condition)\n  x.textnode=textnode\n  x.attribute=attribute\n  return x\n  \n def __str__(self):\n  path=super(XPathExpr,self).__str__()\n  if self.textnode:\n   if path =='*':\n    path='text()'\n   elif path.endswith('::*/*'):\n    path=path[:-3]+'text()'\n   else :\n    path +='/text()'\n    \n  if self.attribute is not None :\n   if path.endswith('::*/*'):\n    path=path[:-2]\n   path +='/@%s'%self.attribute\n   \n  return path\n  \n def join(self,combiner,other):\n  super(XPathExpr,self).join(combiner,other)\n  self.textnode=other.textnode\n  self.attribute=other.attribute\n  return self\n  \n  \nclass TranslatorMixin(object):\n ''\n\n\n \n \n def xpath_element(self,selector):\n  xpath=super(TranslatorMixin,self).xpath_element(selector)\n  return XPathExpr.from_xpath(xpath)\n  \n def xpath_pseudo_element(self,xpath,pseudo_element):\n  ''\n\n  \n  if isinstance(pseudo_element,FunctionalPseudoElement):\n   method='xpath_%s_functional_pseudo_element'%(\n   pseudo_element.name.replace('-','_'))\n   method=_unicode_safe_getattr(self,method,None )\n   if not method:\n    raise ExpressionError(\n    \"The functional pseudo-element ::%s() is unknown\"\n    %pseudo_element.name)\n   xpath=method(xpath,pseudo_element)\n  else :\n   method='xpath_%s_simple_pseudo_element'%(\n   pseudo_element.replace('-','_'))\n   method=_unicode_safe_getattr(self,method,None )\n   if not method:\n    raise ExpressionError(\n    \"The pseudo-element ::%s is unknown\"\n    %pseudo_element)\n   xpath=method(xpath)\n  return xpath\n  \n def xpath_attr_functional_pseudo_element(self,xpath,function):\n  ''\n  \n  if function.argument_types()not in (['STRING'],['IDENT']):\n   raise ExpressionError(\n   \"Expected a single string or ident for ::attr(), got %r\"\n   %function.arguments)\n  return XPathExpr.from_xpath(xpath,\n  attribute=function.arguments[0].value)\n  \n def xpath_text_simple_pseudo_element(self,xpath):\n  ''\n  return XPathExpr.from_xpath(xpath,textnode=True )\n  \n  \nclass GenericTranslator(TranslatorMixin,OriginalGenericTranslator):\n @lru_cache(maxsize=256)\n def css_to_xpath(self,css,prefix='descendant-or-self::'):\n  return super(GenericTranslator,self).css_to_xpath(css,prefix)\n  \n  \nclass HTMLTranslator(TranslatorMixin,OriginalHTMLTranslator):\n @lru_cache(maxsize=256)\n def css_to_xpath(self,css,prefix='descendant-or-self::'):\n  return super(HTMLTranslator,self).css_to_xpath(css,prefix)\n  \n  \n_translator=HTMLTranslator()\n\n\ndef css2xpath(query):\n ''\n return _translator.css_to_xpath(query)\n", ["cssselect", "cssselect.parser", "cssselect.xpath", "functools", "functools32"]], "parsel.selector": [".py", "''\n\n\n\nimport sys\n\nimport six\nfrom lxml import etree,html\n\nfrom .utils import flatten,iflatten,extract_regex,shorten\nfrom .csstranslator import HTMLTranslator,GenericTranslator\n\n\nclass CannotRemoveElementWithoutRoot(Exception):\n pass\n \n \nclass CannotRemoveElementWithoutParent(Exception):\n pass\n \n \nclass SafeXMLParser(etree.XMLParser):\n def __init__(self,*args,**kwargs):\n  kwargs.setdefault('resolve_entities',False )\n  super(SafeXMLParser,self).__init__(*args,**kwargs)\n  \n  \n_ctgroup={\n'html':{'_parser':html.HTMLParser,\n'_csstranslator':HTMLTranslator(),\n'_tostring_method':'html'},\n'xml':{'_parser':SafeXMLParser,\n'_csstranslator':GenericTranslator(),\n'_tostring_method':'xml'},\n}\n\n\ndef _st(st):\n if st is None :\n  return 'html'\n elif st in _ctgroup:\n  return st\n else :\n  raise ValueError('Invalid type: %s'%st)\n  \n  \ndef create_root_node(text,parser_cls,base_url=None ):\n ''\n \n body=text.strip().replace('\\x00','').encode('utf8')or b'<html/>'\n parser=parser_cls(recover=True ,encoding='utf8')\n root=etree.fromstring(body,parser=parser,base_url=base_url)\n if root is None :\n  root=etree.fromstring(b'<html/>',parser=parser,base_url=base_url)\n return root\n \n \nclass SelectorList(list):\n ''\n\n\n \n \n \n def __getslice__(self,i,j):\n  o=super(SelectorList,self).__getslice__(i,j)\n  return self.__class__(o)\n  \n def __getitem__(self,pos):\n  o=super(SelectorList,self).__getitem__(pos)\n  return self.__class__(o)if isinstance(pos,slice)else o\n  \n def __getstate__(self):\n  raise TypeError(\"can't pickle SelectorList objects\")\n  \n def xpath(self,xpath,namespaces=None ,**kwargs):\n  ''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n  \n  return self.__class__(flatten([x.xpath(xpath,namespaces=namespaces,**kwargs)for x in self]))\n  \n def css(self,query):\n  ''\n\n\n\n\n  \n  return self.__class__(flatten([x.css(query)for x in self]))\n  \n def re(self,regex,replace_entities=True ):\n  ''\n\n\n\n\n\n\n\n  \n  return flatten([x.re(regex,replace_entities=replace_entities)for x in self])\n  \n def re_first(self,regex,default=None ,replace_entities=True ):\n  ''\n\n\n\n\n\n\n\n\n\n  \n  for el in iflatten(x.re(regex,replace_entities=replace_entities)for x in self):\n   return el\n  return default\n  \n def getall(self):\n  ''\n\n\n  \n  return [x.get()for x in self]\n extract=getall\n \n def get(self,default=None ):\n  ''\n\n\n  \n  for x in self:\n   return x.get()\n  return default\n extract_first=get\n \n @property\n def attrib(self):\n  ''\n\n  \n  for x in self:\n   return x.attrib\n  return {}\n  \n def remove(self):\n  ''\n\n  \n  for x in self:\n   x.remove()\n   \n   \nclass Selector(object):\n ''\n\n\n\n\n\n\n\n\n\n\n \n \n __slots__=['text','namespaces','type','_expr','root',\n '__weakref__','_parser','_csstranslator','_tostring_method']\n \n _default_type=None\n _default_namespaces={\n \"re\":\"http://exslt.org/regular-expressions\",\n \n \n \n \n \n \n \n \"set\":\"http://exslt.org/sets\"\n }\n _lxml_smart_strings=False\n selectorlist_cls=SelectorList\n \n def __init__(self,text=None ,type=None ,namespaces=None ,root=None ,\n base_url=None ,_expr=None ):\n  self.type=st=_st(type or self._default_type)\n  self._parser=_ctgroup[st]['_parser']\n  self._csstranslator=_ctgroup[st]['_csstranslator']\n  self._tostring_method=_ctgroup[st]['_tostring_method']\n  \n  if text is not None :\n   if not isinstance(text,six.text_type):\n    msg=\"text argument should be of type %s, got %s\"%(\n    six.text_type,text.__class__)\n    raise TypeError(msg)\n   root=self._get_root(text,base_url)\n  elif root is None :\n   raise ValueError(\"Selector needs either text or root argument\")\n   \n  self.namespaces=dict(self._default_namespaces)\n  if namespaces is not None :\n   self.namespaces.update(namespaces)\n  self.root=root\n  self._expr=_expr\n  \n def __getstate__(self):\n  raise TypeError(\"can't pickle Selector objects\")\n  \n def _get_root(self,text,base_url=None ):\n  return create_root_node(text,self._parser,base_url=base_url)\n  \n def xpath(self,query,namespaces=None ,**kwargs):\n  ''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n  \n  try :\n   xpathev=self.root.xpath\n  except AttributeError:\n   return self.selectorlist_cls([])\n   \n  nsp=dict(self.namespaces)\n  if namespaces is not None :\n   nsp.update(namespaces)\n  try :\n   result=xpathev(query,namespaces=nsp,\n   smart_strings=self._lxml_smart_strings,\n   **kwargs)\n  except etree.XPathError as exc:\n   msg=u\"XPath error: %s in %s\"%(exc,query)\n   msg=msg if six.PY3 else msg.encode('unicode_escape')\n   six.reraise(ValueError,ValueError(msg),sys.exc_info()[2])\n   \n  if type(result)is not list:\n   result=[result]\n   \n  result=[self.__class__(root=x,_expr=query,\n  namespaces=self.namespaces,\n  type=self.type)\n  for x in result]\n  return self.selectorlist_cls(result)\n  \n def css(self,query):\n  ''\n\n\n\n\n\n\n\n\n  \n  return self.xpath(self._css2xpath(query))\n  \n def _css2xpath(self,query):\n  return self._csstranslator.css_to_xpath(query)\n  \n def re(self,regex,replace_entities=True ):\n  ''\n\n\n\n\n\n\n\n\n\n\n  \n  return extract_regex(regex,self.get(),replace_entities=replace_entities)\n  \n def re_first(self,regex,default=None ,replace_entities=True ):\n  ''\n\n\n\n\n\n\n\n\n  \n  return next(iflatten(self.re(regex,replace_entities=replace_entities)),default)\n  \n def get(self):\n  ''\n\n\n  \n  try :\n   return etree.tostring(self.root,\n   method=self._tostring_method,\n   encoding='unicode',\n   with_tail=False )\n  except (AttributeError,TypeError):\n   if self.root is True :\n    return u'1'\n   elif self.root is False :\n    return u'0'\n   else :\n    return six.text_type(self.root)\n extract=get\n \n def getall(self):\n  ''\n\n  \n  return [self.get()]\n  \n def register_namespace(self,prefix,uri):\n  ''\n\n\n\n  \n  self.namespaces[prefix]=uri\n  \n def remove_namespaces(self):\n  ''\n\n\n  \n  for el in self.root.iter('*'):\n   if el.tag.startswith('{'):\n    el.tag=el.tag.split('}',1)[1]\n    \n   for an in el.attrib.keys():\n    if an.startswith('{'):\n     el.attrib[an.split('}',1)[1]]=el.attrib.pop(an)\n     \n  etree.cleanup_namespaces(self.root)\n  \n def remove(self):\n  ''\n\n  \n  try :\n   parent=self.root.getparent()\n  except AttributeError:\n  \n   raise CannotRemoveElementWithoutRoot(\n   \"The node you're trying to remove has no root, \"\n   \"are you trying to remove a pseudo-element? \"\n   \"Try to use 'li' as a selector instead of 'li::text' or \"\n   \"'//li' instead of '//li/text()', for example.\"\n   )\n   \n  try :\n   parent.remove(self.root)\n  except AttributeError:\n  \n   raise CannotRemoveElementWithoutParent(\n   \"The node you're trying to remove has no parent, \"\n   \"are you trying to remove a root element?\"\n   )\n   \n @property\n def attrib(self):\n  ''\n  \n  return dict(self.root.attrib)\n  \n def __bool__(self):\n  ''\n\n\n\n  \n  return bool(self.get())\n __nonzero__=__bool__\n \n def __str__(self):\n  data=repr(shorten(self.get(),width=40))\n  return \"<%s xpath=%r data=%s>\"%(type(self).__name__,self._expr,data)\n __repr__=__str__\n", ["lxml", "parsel.csstranslator", "parsel.utils", "six", "sys"]], "parsel.utils": [".py", "import re\nimport six\nfrom w3lib.html import replace_entities as w3lib_replace_entities\n\n\ndef flatten(x):\n ''\n\n\n\n\n\n\n\n\n\n\n\n\n \n return list(iflatten(x))\n \n \ndef iflatten(x):\n ''\n \n for el in x:\n  if _is_listlike(el):\n   for el_ in flatten(el):\n    yield el_\n  else :\n   yield el\n   \n   \ndef _is_listlike(x):\n ''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n \n return hasattr(x,\"__iter__\")and not isinstance(x,(six.text_type,bytes))\n \n \ndef extract_regex(regex,text,replace_entities=True ):\n ''\n\n\n\n \n if isinstance(regex,six.string_types):\n  regex=re.compile(regex,re.UNICODE)\n  \n if 'extract'in regex.groupindex:\n \n  try :\n   extracted=regex.search(text).group('extract')\n  except AttributeError:\n   strings=[]\n  else :\n   strings=[extracted]if extracted is not None else []\n else :\n \n  strings=regex.findall(text)\n  \n strings=flatten(strings)\n if not replace_entities:\n  return strings\n return [w3lib_replace_entities(s,keep=['lt','amp'])for s in strings]\n \n \ndef shorten(text,width,suffix='...'):\n ''\n if len(text)<=width:\n  return text\n if width >len(suffix):\n  return text[:width -len(suffix)]+suffix\n if width >=0:\n  return suffix[len(suffix)-width:]\n raise ValueError('width must be equal or greater than 0')\n", ["re", "six", "w3lib.html"]], "parsel.xpathfuncs": [".py", "import re\nfrom lxml import etree\n\nfrom six import string_types\n\nfrom w3lib.html import HTML5_WHITESPACE\n\nregex='[{}]+'.format(HTML5_WHITESPACE)\nreplace_html5_whitespaces=re.compile(regex).sub\n\n\ndef set_xpathfunc(fname,func):\n ''\n\n\n\n\n\n\n\n\n\n\n\n \n ns_fns=etree.FunctionNamespace(None )\n if func is not None :\n  ns_fns[fname]=func\n else :\n  del ns_fns[fname]\n  \n  \ndef setup():\n set_xpathfunc('has-class',has_class)\n \n \ndef has_class(context,*classes):\n ''\n\n\n\n \n if not context.eval_context.get('args_checked'):\n  if not classes:\n   raise ValueError(\n   'XPath error: has-class must have at least 1 argument')\n  for c in classes:\n   if not isinstance(c,string_types):\n    raise ValueError(\n    'XPath error: has-class arguments must be strings')\n  context.eval_context['args_checked']=True\n  \n node_cls=context.context_node.get('class')\n if node_cls is None :\n  return False\n node_cls=' '+node_cls+' '\n node_cls=replace_html5_whitespaces(' ',node_cls)\n for cls in classes:\n  if ' '+cls+' 'not in node_cls:\n   return False\n return True\n", ["lxml", "re", "six", "w3lib.html"]], "parsel": [".py", "''\n\n\n\n\n__author__='Scrapy project'\n__email__='info@scrapy.org'\n__version__='1.6.0'\n\nfrom parsel.selector import Selector,SelectorList\nfrom parsel.csstranslator import css2xpath\nfrom parsel import xpathfuncs\n\nxpathfuncs.setup()\n", ["parsel", "parsel.csstranslator", "parsel.selector"], 1]}
__BRYTHON__.update_VFS(scripts)