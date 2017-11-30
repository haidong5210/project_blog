from django.forms import widgets,fields,Form


class Addarticle(Form):
    title = fields.CharField(
        required=True,
        error_messages={"required":'标题不能为空'})
    content = fields.CharField(
        required=True,
        widget=widgets.Textarea(),
        error_messages={"required":'内容不能为空'})

    def clean_content(self):
        content = self.cleaned_data.get('content')
        from bs4 import BeautifulSoup
        legal_tag_dict = {
            'font' : ['color', 'size', 'face', '.background-color'],
            'span' : ['.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.line-height'],
            'div' : ['align', '.border', '.margin', '.padding', '.text-align', '.color','.background-color', '.font-size', '.font-family', '.font-weight', '.background','.font-style', '.text-decoration', '.vertical-align', '.margin-left'],
            'table': ['border', 'cellspacing', 'cellpadding', 'width', 'height', 'align', 'bordercolor','.padding', '.margin', '.border', 'bgcolor', '.text-align', '.color', '.background-color','.font-size', '.font-family', '.font-weight', '.font-style', '.text-decoration', '.background','.width', '.height', '.border-collapse'],
            'td': ['align', 'valign', 'width', 'height', 'colspan', 'rowspan', 'bgcolor','.text-align', '.color', '.background-color', '.font-size', '.font-family', '.font-weight','.font-style', '.text-decoration', '.vertical-align', '.background', '.border'],
            'th': ['align', 'valign', 'width', 'height', 'colspan', 'rowspan', 'bgcolor','.text-align', '.color', '.background-color', '.font-size', '.font-family', '.font-weight','.font-style', '.text-decoration', '.vertical-align', '.background', '.border'],
            'a' : ['href', 'target', 'name'],
            'embed' : ['src', 'width', 'height', 'type', 'loop', 'autostart', 'quality', '.width', '.height', 'align', 'allowscriptaccess'],
            'img' : ['src', 'width', 'height', 'border', 'alt', 'title', 'align', '.width', '.height', '.border'],
            'p' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'ol' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'ul' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'li' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'blockquote' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'h1' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'h2' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'h3' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'h4' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'h5' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'h6' : ['align', '.text-align', '.color', '.background-color', '.font-size', '.font-family', '.background','.font-weight', '.font-style', '.text-decoration', '.vertical-align', '.text-indent', '.margin-left'],
            'pre' : ['class'],
            'hr' : ['class', '.page-break-after'],
            'br' : [],
            'tbody' : [],
            'tr' : [],
            'strong' : [],
            'b' : [],
            'sub' : [],
            'em' : [],
            'i' : [],
            'u' : [],
            'strike' : [],
            's' : [],
            'del' : [],
}
        soup = BeautifulSoup(content, 'html.parser')
        tag_list = soup.find_all()

        for tag in tag_list:
            if tag.name not in legal_tag_dict:
                tag.decompose()
            else:
                l = []
                if tag.attrs:
                    print(123)
                    for attr in tag.attrs:
                        print(attr)
                        if attr not in legal_tag_dict[tag.name]:
                            l.append(attr)
                for i in l:
                    del tag.attrs[i]

        return soup.decode()