from collections import OrderedDict

from Site.models import Product, Ingredient, Size, ProductTag, Discount


def user_format(data):
    return OrderedDict([
        ("user_id", data.id),
        ("user_name", data.name),
        ("user_phone", data.phone),
    ])


def size_format(data, via_pro=False, via_dis=False):
    dis = Discount.objects.filter(product=data).first()

    l = [
        ("size_id", data.id),
        ("size_content", data.size),
        ("price", data.price),
    ]
    if not via_pro:
        pr = Product.objects.filter(id=data.prod.id).first()
        l.append(("products", 0 if not pr else product_format(pr, via_sizes=True)))

    if not via_dis:
        l.append(('discount', None if not dis else discount_format(dis, via_sizes=True)))

    return OrderedDict(l)


def ing_format(data, via_pro=False):
    l = [
        ("img_id", data.id),
        ("name", data.name),
        ("img", data.img.url),
        ("price", data.price),
    ]
    if not via_pro:
        l.append(("products", [product_format(x, via_ing=True) for x in Product.objects.filter(ctg=data)]))
    return OrderedDict(l)


def product_format(data, via_ctg=False, via_ing=False, via_sizes=False, via_tag=False):
    starter = Size.objects.filter(prod=data).order_by("price").first()
    l = [
        ("product_id", data.id),
        ("name", data.name),
        ("ctg_slug", None if not data.ctg.slug else data.ctg.slug),
        ('starter', 0 if not starter else size_format(starter, via_pro=True)['price']),
        ("short_desc", data.short_desc),
        ("img", '' if not data.img else data.img.url),
        ("status", data.status),
    ]
    if not via_ctg:
        l.append(("ctg_id", None if not data.ctg else ctg_format(data.ctg, via_pro=True)), )
    if not via_ing:
        l.append(("ingredients", [ing_format(x, via_pro=True) for x in Ingredient.objects.filter(prod=data)]))
    if not via_sizes:
        l.append(("sizes", [size_format(x, via_pro=True) for x in Size.objects.filter(prod=data)]))

    # if not via_tag:
    #     tags = [i.tag.tag for i in ProductTag.objects.filter(prod=data)]
    #     l.append(('tag', tags))

    return OrderedDict(l)


def add_basket_format(data):
    prod = size_format(data.product)
    return OrderedDict([
        ('basket_id', data.id),
        ('product', prod),
        ('quantity', data.quantity),
        ('price', data.summa),
    ])


def ctg_format(data, via_pro=False):
    l = [
        ('id', data.id),
        ('content', data.content),
        ('slug', data.slug),
        ('is_main', data.is_main),
    ]
    if not via_pro:
        l.append(("products", [product_format(x, via_ctg=True) for x in Product.objects.filter(ctg=data)]))
    return OrderedDict(l)


def tag_format(data, via_pro=False):
    l = [
        ('id', data.id),
        ('tag', data.tag),
    ]
    if not via_pro:
        l.append(("products", [product_format(x.prod, via_tag=True) for x in ProductTag.objects.filter(tag=data)]))
    return OrderedDict(l)


def discount_format(data, via_sizes=False):
    l = [
        ("procent", data.procent),
        ("discounted_price", data.price),
        ("start_date", data.start_date),
        ("end_date", data.end_date),
    ]
    if not via_sizes:
        l.append(("sizes", size_format(data.product, via_dis=True)))

    return OrderedDict(l)
