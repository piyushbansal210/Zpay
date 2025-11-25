from django.shortcuts import render
def render_partial(request, full_template, partial_template, ctx=None):
    ctx = ctx or {}
    if request.headers.get('HX-Request') == 'true':
        return render(request, partial_template, ctx)
    return render(request, full_template, ctx)