from django import template
from django.utils.safestring import mark_safe
from web.models import Smartphone, SmartTV

register = template.Library()

TABLE_HEAD = """<table class="table">
    <tbody>"""

TABLE_ITEM = """        <tr>
            <td>{name}</td>
            <td>{value}</td>
        </tr>"""

TABLE_TAIL = """    </tbody>
</table>"""

PRODUCT_SPEC = {
    'notebook': {
        'Diagonal': 'diagonal',
        'Display type': 'display_type',
        'RAM': 'ram',
        'Processor frequency': 'processor_freq',
        'Video card': 'video',
        'Battery life': 'battery',
        'Operating system': 'os'
    },
    'smartphone': {
        'Diagonal': 'diagonal',
        'Display type': 'display_type',
        'Resolution': 'resolution',
        'RAM': 'ram',
        'Maximal SD card volume': 'sd_volume',
        'Battery life': 'battery',
        'Main camera': 'main_cam',
        'Frontal camera': 'frontal_cam'

    },
    'smarttv': {
        'Diagonal': 'diagonal',
        'Resolution': 'resolution',
        'Built-in apps': 'built_in_apps'
    },
    'headphones': {
        'Connection type': 'connection_type',
        'Headphones fastening': 'fastening',
        'Speaker frequency': 'speaker_freq',
        'Battery life': 'battery'
    }
}


@register.filter
def product_specifications(product):
    model_name = product.__class__._meta.model_name

    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC[model_name].pop('Maximal SD card volume', None)
        else:
            PRODUCT_SPEC[model_name]['Maximal SD card volume'] = 'sd_volume'

    if isinstance(product, SmartTV):
        if not product.built_in_apps:
            PRODUCT_SPEC[model_name].pop('Built-in apps', None)
        else:
            PRODUCT_SPEC[model_name]['Built-in apps'] = 'built_in_apps'


    table_content = ''
    
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_ITEM.format(name=name, value=getattr(product, value))

    return mark_safe(TABLE_HEAD + table_content + TABLE_TAIL)