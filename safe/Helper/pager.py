#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/7 上午10:22
# @Author  : Yu BenLiu
# @Site    : QVQ
# @File    : pager.py.py
# @Software: PyCharm

class Pagination(object):
    def __init__(self, totalCount, currentPage, name, perPageItemNum=20, maxPageNum=7):
        # 数据总个数
        self.total_count = totalCount
        # 当前页
        try:
            v = int(currentPage)
            if v <= 0:
                v = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        # 每页显示的行数
        self.per_page_item_num = perPageItemNum
        # 最多显示页面
        self.max_page_num = maxPageNum
        self.name=name

    def start(self):
        return (self.current_page - 1) * self.per_page_item_num

    def end(self):
        return self.current_page * self.per_page_item_num

    @property
    def num_pages(self):
        """
        总页数
        :return:
        """
        # 666
        # 10
        a, b = divmod(self.total_count, self.per_page_item_num)
        if b == 0:
            return a
        return a + 1

    def pager_num_range(self):
        # self.num_pages()
        # self.num_pages
        # 当前页
        # self.current_page
        # 最多显示的页码数量 11
        # self.per_pager_num
        # 总页数
        # self.num_pages
        if self.num_pages < self.max_page_num:
            return range(1, self.num_pages + 1)
        # 总页数特别多 5
        part = int(self.max_page_num / 2)
        if self.current_page <= part:
            return range(1, self.max_page_num + 1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages - self.max_page_num + 1, self.num_pages + 1)
        return range(self.current_page - part, self.current_page + part + 1)

    def page_str(self):
        page_list = []

        first = '<li class="page-item  pagination-first"><a class="page-link" href="%s?p=1"></a></li>' %(self.name)
        page_list.append(first)

        if self.current_page == 1:
            prev = '<li class="page-item  pagination-prev"><a class="page-link" href="#"></a></li>'
        else:
            prev = '<li class="page-item pagination-prev"><a class="page-link" href="/%s?p=%s"></a></li>' % (self.name,self.current_page - 1,)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = '<li  class="page-item active"><a class="page-link"  href="/%s?p=%s">%s</a></li>' % (self.name,i, i)
            else:
                temp = '<li class="page-item"><a class="page-link"  href="/%s?p=%s">%s</a></li>' % (self.name,i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = '<li class="page-item active pagination-next"><a  a class="page-link" href="#"></a></li>'
        else:
            nex = '<li class="page-item pagination-next" ><a  class="page-link" href="/%s?p=%s"></a></li>' % (self.name,self.current_page + 1,)
        page_list.append(nex)

        last = '<li class="page-item pagination-last"><a class="page-link" href="/%s?p=%s">尾页</a></li>' % (self.name,self.num_pages,)
        page_list.append(last)

        return ''.join(page_list)