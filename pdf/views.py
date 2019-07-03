import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import FormView, View
from xhtml2pdf import pisa

from pdf.forms import MessageForm


class MessageView(View):
    def get(self, request):
        form = MessageForm(data=request.GET)
        return render(request, 'index.html', {
            'form': form
        })

    def post(self, request):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            response = generate_pdf_response(context=form.cleaned_data)
            return response

        return redirect(reverse('pdf:message'))


def font_patch():
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from xhtml2pdf.default import DEFAULT_FONT
    pdfmetrics.registerFont(TTFont('yh', '{}/font/msyh.ttf'.format(
        settings.STATICFILES_DIRS[0])))
    DEFAULT_FONT['helvetica'] = 'yh'


def link_callback(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    # 确保本地文件存在
    if not os.path.isfile(path):
        raise Exception(
            "Media URI must start with "
            f"'{settings.MEDIA_URL}' or '{settings.STATIC_URL}'")

    return path


def generate_pdf_response(context):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = \
        f"attachment; filename='{context['name']}.pdf'"

    html = render_to_string("pdf.html", context=context)
    font_patch()
    status = pisa.CreatePDF(html,
                            dest=response,
                            link_callback=link_callback)

    if status.err:
        return HttpResponse("PDF文件生成失败")
    return response