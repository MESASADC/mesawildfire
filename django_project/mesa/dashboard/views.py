from django.shortcuts import render_to_response

def dashboard(request):
    return render_to_response('dashboard.html')

def wmst(request):
    return render_to_response('wmst.html')

