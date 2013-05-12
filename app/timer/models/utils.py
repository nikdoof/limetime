import django
from django.db.models.query import QuerySet
from django.db.models.fields.related import OneToOneField
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.db.models.constants import LOOKUP_SEP
except ImportError: # Django < 1.5
    from django.db.models.sql.constants import LOOKUP_SEP


class InheritanceQuerySet(QuerySet):
    def select_subclasses(self, *subclasses):
        if not subclasses:
            # only recurse one level on Django < 1.6 to avoid triggering
            # https://code.djangoproject.com/ticket/16572
            levels = None
            if django.VERSION < (1, 6, 0):
                levels = 1
            subclasses = self._get_subclasses_recurse(self.model, levels=levels)
            # workaround https://code.djangoproject.com/ticket/16855
        field_dict = self.query.select_related
        new_qs = self.select_related(*subclasses)
        if isinstance(new_qs.query.select_related, dict) and isinstance(field_dict, dict):
            new_qs.query.select_related.update(field_dict)
        new_qs.subclasses = subclasses
        return new_qs


    def _clone(self, klass=None, setup=False, **kwargs):
        for name in ['subclasses', '_annotated']:
            if hasattr(self, name):
                kwargs[name] = getattr(self, name)
        return super(InheritanceQuerySet, self)._clone(klass, setup, **kwargs)


    def annotate(self, *args, **kwargs):
        qset = super(InheritanceQuerySet, self).annotate(*args, **kwargs)
        qset._annotated = [a.default_alias for a in args] + list(kwargs.keys())
        return qset


    def iterator(self):
        iter = super(InheritanceQuerySet, self).iterator()
        if getattr(self, 'subclasses', False):
            for obj in iter:
                sub_obj = None
                for s in self.subclasses:
                    sub_obj = self._get_sub_obj_recurse(obj, s)
                    if sub_obj:
                        break
                if not sub_obj:
                    sub_obj = obj

                if getattr(self, '_annotated', False):
                    for k in self._annotated:
                        setattr(sub_obj, k, getattr(obj, k))

                yield sub_obj
        else:
            for obj in iter:
                yield obj


    def _get_subclasses_recurse(self, model, levels=None):
        rels = [rel for rel in model._meta.get_all_related_objects()
                if isinstance(rel.field, OneToOneField)
            and issubclass(rel.field.model, model)]
        subclasses = []
        if levels:
            levels -= 1
        for rel in rels:
            if levels or levels is None:
                for subclass in self._get_subclasses_recurse(
                        rel.field.model, levels=levels):
                    subclasses.append(rel.var_name + LOOKUP_SEP + subclass)
            subclasses.append(rel.var_name)
        return subclasses


    def _get_sub_obj_recurse(self, obj, s):
        rel, _, s = s.partition(LOOKUP_SEP)
        try:
            node = getattr(obj, rel)
        except ObjectDoesNotExist:
            return None
        if s:
            child = self._get_sub_obj_recurse(node, s)
            return child or node
        else:
            return node