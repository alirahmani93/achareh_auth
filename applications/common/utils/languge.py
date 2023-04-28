from django.conf import settings


def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)

    parts = path.split('/')

    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
    return '/'.join(parts)


def get_admin_url(model, pk=None):
    from django.urls import reverse
    info = (model._meta.app_label, model._meta.model_name)
    return reverse('admin:%s_%s_change' % info, args=(pk,)) if pk else reverse('admin:%s_%s_changelist' % info, )


def get_model_fullname(self):
    return '%s_%s' % (self.opts.app_label, self.model._meta.model_name)
