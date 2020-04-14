class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None: # если у тега есть классы
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items(): # не понятно
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if len(self.children) > 0: # если у тега есть потомки
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else: # если у тега нет потомков
            if self.is_single: #и он одиночный
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else: # тэг парный
                return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)


class HTML:
    def __init__(self, output):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args): 
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "</html>"
        return html


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args): # зачем здесь аргументы
        pass

    def __str__(self):
        html = "<%s>" % self.tag
        for child in self.children:
            html += "\n"+str(child)
        html += "\n</%s>\n" % self.tag
        return html



def main():
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main()





















    