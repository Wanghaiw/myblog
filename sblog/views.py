# !/use/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.template import Template, Context,RequestContext
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime
from django.shortcuts import render_to_response,render
from sblog.models import Blog,Tag,Author

from  sblog.forms import BlogForm,TagForm


#首页
def blog_list(request):
    tags = Tag.objects.all()
    blogs = Blog.objects.all()
    return render(request,"blog_list.html",locals())


def blog_show(request, id=''):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    return render(request,"blog_show.html", locals())

def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render(request,"blog_list.html",locals())


def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            for taglist in tagname.split():
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            author = Author.objects.get(id=1)
            content = cd['content']
            blog = Blog(caption=title, author=author, content=content)
            blog.save()
            for taglist in tagname.split():
                blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                blog.save()
            id = Blog.objects.order_by('-publish_time')[0].id
            return HttpResponseRedirect('/sblog/blog/%s' % id)
    else:
        form = BlogForm()
        tag = TagForm(initial={'tag_name': 'notags'})

    return render(request,'blog_add.html',locals())

def blog_update(request, id=""):
    id = id
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            blog = Blog.objects.get(id=id)
            if blog:
                blog.caption = title
                blog.content = content
                blog.save()
                for taglist in tagnamelist:
                    blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    blog.save()
                tags = blog.tags.all()
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = blog.tags.get(tag_name=tagname)
                        blog.tags.remove(notag)
            else:
                blog = Blog(caption=blog.caption, content=blog.content)
                blog.save()
            return HttpResponseRedirect('/sblog/blog/%s' % id)
    else:
        try:
            blog = Blog.objects.get(id=id)
        except Exception:
            raise Http404
        form = BlogForm(initial={'caption': blog.caption, 'content': blog.content}, auto_id=False)
        tags = blog.tags.all()
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        else:
            tag = TagForm()
    return render(request,'blog_add.html',locals())

def blog_del(request, id=""):
    try:
        blog = Blog.objects.get(id=id)
    except Exception:
        raise Http404
    if blog:
        blog.delete()
        return HttpResponseRedirect("/sblog/bloglist/")
    blogs = Blog.objects.all()
    return render(request,"blog_list.html",locals())