"""
Translate each schema file in Source directory to multiple formats in Out directory
"""
import os
import shutil
import jadn
from typing import NoReturn


def translate(filename: str, odir: str) -> NoReturn:
    fn, ext = os.path.splitext(filename)
    try:
        loader = {
            '.jadn': jadn.load,
            '.jidl': jadn.convert.jidl_load,
            '.html': jadn.convert.html_load
        }[ext]
    except KeyError:
        print(f'Unsupported schema format: {filename}')
        return

    print(f'{filename:}:')
    schema = loader(os.path.join('Source', filename))
    print('\n'.join([f'{k:>15}: {v}' for k, v in jadn.analyze(jadn.check(schema)).items()]))

    jadn.convert.dot_dump(schema, os.path.join(odir, fn + '.dot'), style={'links': True})
    cols = {'desc': 48, 'page': 120}    # specify comment position and page width to truncate
    jadn.convert.jidl_dump(schema, os.path.join(odir, fn + '.jidl'), style=cols)
    jadn.convert.html_dump(schema, os.path.join(odir, fn + '.html'))
    jadn.convert.table_dump(schema, os.path.join(odir, fn + '.md'))
    jadn.translate.json_schema_dump(schema, os.path.join(odir, fn + '.json'))
    jadn.dump(schema, os.path.join(odir, fn + '.jadn'))
    jadn.dump(jadn.transform.simplify(jadn.transform.strip_comments(schema)),
              os.path.join(odir, fn + '_core.jadn'))


if __name__ == '__main__':
    print(f'Installed JADN version: {jadn.__version__}\n')
    output_dir = 'Out'
    css_dir = os.path.join(output_dir, 'css')
    os.makedirs(css_dir, exist_ok=True)
    shutil.copy(os.path.join(jadn.data_dir(), 'dtheme.css'), css_dir)
    for f in os.listdir('Source'):
        translate(f, output_dir)
