class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwards):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        
       
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, val in kwards.items():
            self.attributes[attr] = val

    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass

    def __str__(self):
        attrs = []  
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s \n" % self.text
            for child in self.children:
                internal += str(child) + "\n"
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )
    # Метод вызывается, когда мы пишем +=
    def __iadd__(self,other):
        # Добавляем тег other в список внутренних элементов  тега 
        self.children.append(other)
        # Возращаем self
        return self
        
class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        print(str(self))

    # Метод вызывается, когда мы пишем +=
    def __iadd__(self,other):
        # Добавляем тег other в список внутренних элементов  тега 
        self.children.append(other)
        # Возращаем self
        return self
    
    def __str__(self):
        opening = "<html>"
        internal = "\n"
        for child in self.children:
            internal += str(child) + "\n"
        ending = "</html>"
        return opening + internal + ending

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    # Метод вызывается, когда мы пишем +=
    def __iadd__(self,other):
        # Добавляем тег other в список внутренних элементов  тега 
        self.children.append(other)
        # Возращаем self
        return self
   
    def __str__(self):
        opening = "<{tag}>".format(tag=self.tag)
        internal = "\n"
        for child in self.children:
            # Тут добавим перенос строки
            internal += str(child) + "\n"
        ending = "</%s>" % self.tag
        return opening + internal + ending

if __name__ == "__main__":
    with HTML(output=None) as doc:
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